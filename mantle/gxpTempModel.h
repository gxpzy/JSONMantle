//
//  gxpTempModel.h
//
//  Created by JSON2Mantle on 11/30/16.
//  Copyright (c) 2016 gao. All rights reserved.
//

#import <Mantle.h>
#import "gxpLoverModel.h"

/**
 *  The gxpTempModel class represents a Mantle model.
 */
@interface gxpTempModel : MTLModel <MTLJSONSerializing>

@property (nonatomic, copy) NSString *title;
@property (nonatomic, copy) NSString *name;
@property (nonatomic, strong) NSArray *lover;

@end
