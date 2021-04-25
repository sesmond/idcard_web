#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : 基础请求报文
@File    :   base_request_vo.py    
@Author  : vincent
@Time    : 2020/6/8 4:47 下午
@Version : 1.0 
'''


class ImageBaseRequest:
    """
    图片请求的共用请求报文
    """
    # 请求id
    sid = ""
    # 要识别的图片（base64格式）
    img = ""
    # 识别的图片地址 和 img二选一
    img_url = ""
    # 是否返回debug图片
    do_verbose = False
