//
//  gxpLoverModel.h
//
//  Created by JSON2Mantle on 11/30/16.
//  Copyright (c) 2016 gao. All rights reserved.
//

#import <Mantle.h>


/**
 *  The gxpLoverModel class represents a Mantle model.
 */
@interface gxpLoverModel : MTLModel <MTLJSONSerializing>

@property (nonatomic, copy) NSString *relationship;
@property (nonatomic, copy) NSString *loverName;

@end
