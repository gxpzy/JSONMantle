//
//  gxpTempModel.m
//
//  Created by JSON2Mantle on 11/30/16.
//  Copyright (c) 2016 gao. All rights reserved.
//

#import <Mantle.h>
#import "gxpTempModel.h"

@implementation gxpTempModel

/**
 * The dictionary returned by this method specifies
 * how your model object's properties map to the keys
 * in the JSON representation.
 * 
 * @see https://github.com/Mantle/Mantle#jsonkeypathsbypropertykey
 * @return NSDictionary
 */
+ (NSDictionary *)JSONKeyPathsByPropertyKey
{
    // modelProperty : json_field_name
    return @{
            
            };
}


/**
 * Converts 'lover' property from 'gxpLoverModel' class.
 *
 * @return NSValueTransformer
 */
+ (NSValueTransformer *)loverJSONTransformer
{
    return [NSValueTransformer mtl_JSONArrayTransformerWithModelClass:gxpLoverModel.class];
}

@end
