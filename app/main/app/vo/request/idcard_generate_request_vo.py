#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Title   : 身份证生成器
@File    :   idcard_generate_request_vo.py    
@Author  : vincent
@Time    : 2021/4/23 下午5:37
@Version : 1.0 
"""
from app.main.app.vo.request.base_request_vo import ImageBaseRequest


class IdcardGenerateRequest(ImageBaseRequest):
    name = ""
    sex = ""
    nation = ""
    year = ""
    month = ""
    day = ""
    addr = ""
    idNo = ""
    org = ""
    validPeriod = ""
