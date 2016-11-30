import re
import argparse
import os
import json
import time
import objc_template as objc_tpl
from render import Render


class JSONMantle(object):
    def __init__(self):
        self.class_prefix = ''
        self.class_suffix = 'Model'
        self.reserved_words = ('class', 'id', 'super', 'description')
        self.properties = {}
        self.meta_data = {
            'year': time.strftime('%Y', time.gmtime()),
            'created_at': time.strftime('%m/%d/%y', time.gmtime()),
            'author': 'gxp',
        }

    def make_class_name(self, name):
        if not name.startswith(self.class_prefix) or not name.endswith(self.class_suffix):
            return self.class_prefix + name[0].upper() + name[1:] + self.class_suffix
        else:
            return name

    def convert_name_style(self, name):
        if name in self.reserved_words:
            new_name = 'model{}{}'.format(name[0].upper, name[1:])
            return new_name
        candidates = re.findall(r'(_\w)', name)
        if not candidates:
            return name
        new_name = re.sub(r'_(\w)', lambda x: x.group(1).upper(), name)
        return new_name

    def extract_properties(self, dict_data, class_name):
        """
        extract properties from a dictionary.
        :param dict_data: dictionary
        :param class_name: class name of dictionary
        :return: json containes all properties
        """
        # items: current properties
        items = []
        # results:key = class_name,value = items
        results = {}
        # sub_model: sub model to be merged
        sub_model = {}
        class_name = self.make_class_name(class_name)

        for original_name, value in dict_data.items():
            new_name = self.convert_name_style(original_name)
            # if it is a dictionary,it should be a model
            if isinstance(value, dict):
                new_class_name = self.make_class_name(new_name)
                sub_model = self.extract_properties(value, new_name)
                results.update(sub_model)
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'strong',
                    'class_name': new_class_name,
                    'transform': {
                        'type': 'Dictionary',
                        'class': new_class_name,
                    },
                }
            elif isinstance(value, list):
                new_class_name = self.make_class_name(new_name)
                if len(value) == 0:
                    print('WARING: "{}" is not generated'.format(new_class_name))
                    continue
                if isinstance(value[0], dict):
                    sub_model = self.extract_properties(value[0], new_class_name)
                    results.update(sub_model)
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'strong',
                    'class_name': 'NSArray',
                    'transform': {
                        'type': 'Array',
                        'class': new_class_name,
                    },
                }
            elif isinstance(value, str):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'copy',
                    'class_name': 'NSString',
                    'transform': None,
                }
            elif isinstance(value, int):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'assign',
                    'class_name': 'NSInteger',
                    'transform': None,
                }
            elif isinstance(value, bool):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'assign',
                    'class_name': 'BOOL',
                    'transform': None,
                }
            elif isinstance(value, float):
                item = {
                    'name': new_name,
                    'original_name': original_name,
                    'storage': 'assign',
                    'class_name': 'CGfloat',
                    'transform': None,
                }
            else:
                raise ValueError(value)
            items.append(item)
        results[class_name] = items
        results.update(sub_model)
        return results

    def generate_properties(self, dict_data, class_name):
        if isinstance(dict_data, list):
            class_name = input('"{}" is an array, give the items a name: ')
            dict_data = dict_data[0]
        self.properties = self.extract_properties(dict_data, class_name)
        # print('properties: \n', self.properties)

    def get_template_data(self):
        render_h = {}
        render_m = {}

        for model_name, properties in self.properties.items():
            # header: properties
            joined_properties = '\n'.join(map(objc_tpl.property_tpl, properties))

            # header: extra headers
            joined_headers = '\n'.join(filter(lambda x: x, map(objc_tpl.header_tpl, properties)))

            # implementation: aliases
            joined_aliases = '\n   '.join(filter(lambda x: x,map(objc_tpl.alias_tpl, properties)))

            # implementation: transformers
            joined_transformers = '\n'.join(
                filter(lambda x: x, map(objc_tpl.transformer_tpl, properties))
            )

            render_h[model_name] = {
                'file_name': model_name,
                'properties': joined_properties,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
                'headers': joined_headers,
            }

            render_m[model_name] = {
                'file_name': model_name,
                'property_alias': joined_aliases,
                'created_at': self.meta_data['created_at'],
                'author': self.meta_data['author'],
                'year': self.meta_data['year'],
                'transformers': joined_transformers,
            }
        return render_h, render_m


def init_args():
    parser = argparse.ArgumentParser(
        description='Generate Mantle models by a given JSON file.'
    )
    parser.add_argument('json_file',
                        help='the JSON file to be parsed')
    parser.add_argument('output_dir',
                        help='output directory for generated Objective-C files')
    parser.add_argument('--prefix',
                        help='class prefix of Objective-C files')
    parser.add_argument('--author',
                        help='author info')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        try:
            os.mkdir(args.output_dir)
        except IOError:
            print('Error: could not create directory {}'.format(
                args.output_dir
            ))
            exit()

    return args


def main():
    args = init_args()

    try:
        dict_data = json.loads(open(args.json_file).read())
    except IOError:
        print('Error: no such file {}'.format(args.json_file))
        exit()

    mantle = JSONMantle()
    mantle.class_prefix = args.prefix if args.prefix else ''
    if args.author:
        mantle.meta_data['author'] = args.author

    # Get the file base name
    file_basename = os.path.basename(args.json_file)

    # Eliminating filename extension
    class_name = file_basename.split('.')[0]

    mantle.generate_properties(dict_data, class_name)

    render_h, render_m = mantle.get_template_data()
    render = Render(render_h, render_m, args.output_dir)
    render.render_objc()
if __name__ == '__main__':
    main()