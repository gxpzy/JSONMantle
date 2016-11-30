import re
import os


class Render(object):
    def __init__(self, properties_h, properties_m, output_dir='output'):
        base_path = os.path.dirname(__file__)
        file_h = os.path.abspath(os.path.join(base_path, 'model.h'))
        file_m = os.path.abspath(os.path.join(base_path, 'model.m'))
        self.properties = {
            'h': properties_h,
            'm': properties_m,
        }
        self.templates = {
            'h': open(file_h).read(),
            'm': open(file_m).read(),
        }
        self.output_dir = output_dir

    def render_objc(self):
        for model in ('h', 'm'):
            for class_name, prop in self.properties[model].items():
                # output .h .m
                filename = '{}.{}'.format(class_name, model)
                output_file = os.path.join(self.output_dir, filename)
                # use template model by default
                output_doc = self.templates[model]

                for name, value in prop.items():
                    # replace author properties and so on
                    placeholder = '{{%s}}' % (name,)
                    output_doc = output_doc.replace(placeholder, value)

                output_doc = re.sub(r'{{.*?}}', '',output_doc)
                with open(output_file, 'w') as output:
                    output.write(output_doc)