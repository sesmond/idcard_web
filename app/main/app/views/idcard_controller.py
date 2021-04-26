#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : 测试案例控制器
@File    :   case_controller.py
@Author  : vincent
@Time    : 2020/8/31 2:59 下午
@Version : 1.0 
'''
import logging
import time

from flask import jsonify, request

from app.main.app.entity.idcard import IdCard
from app.main.app.service import idcard_generate_service
from app.main.app.utils import json_utils, image_utils
from app.main.app.views import idcard_app
from app.main.app.vo.request.base_request_vo import ImageBaseRequest
from app.main.app.vo.request.idcard_generate_request_vo import IdcardGenerateRequest
from app.main.app.vo.response.base_response import BaseResponse

logger = logging.getLogger(__name__)
"""
功能列表：
1. 用例执行历史列表：query.ajax
2. 用例执行
3. 用例详情

"""


@idcard_app.route('/generate/random.ajax', methods=["POST"])
def generate_random():
    try:
        criteria = ImageBaseRequest()
        start = time.time()
        json_utils.json_deserialize(request.get_data(), criteria, ignore_null=True)
        response = idcard_generate_service.generate_idcard_random()
        return jsonify(json_utils.obj2json(response))
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error("处理图片过程中出现问题：%r", e)
        return jsonify(BaseResponse("9999", str(e)).__dict__)


@idcard_app.route('/generate.ajax', methods=["POST"])
def generate():
    try:
        criteria = IdcardGenerateRequest()
        start = time.time()
        json_utils.json_deserialize(request.get_data(), criteria, ignore_null=True)

        img = image_utils.base64_2_image(criteria.img)
        card = IdCard()
        card.name = criteria.name
        card.sex = criteria.sex
        card.nation = criteria.nation
        card.year = criteria.year
        card.month = criteria.month
        card.day = criteria.day
        card.addr = criteria.addr
        card.idNo = criteria.idNo
        card.org = criteria.org
        card.validPeriod = criteria.validPeriod
        card.avatar = img
        response = idcard_generate_service.generate_idcard(card)
        return jsonify(json_utils.obj2json(response))
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.exception("处理图片过程中出现问题：%r", e)
        return jsonify(BaseResponse("9999", str(e)).__dict__)
