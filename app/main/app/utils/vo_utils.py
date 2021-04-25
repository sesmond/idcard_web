#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : VO 转换工具类
@File    :   vo_utils.py    
@Author  : vin
@Time    : 2020/6/1 3:35 下午
@Version : 1.0 
'''
import numpy as np

from app.main.app.utils import image_utils
from app.main.app.vo.response.base_response import PositionEntity, WordEntity, DebugEntity, DebugTitleEntity, \
    DebugRowEntity


def boxes2vo(boxes):
    """
    ndarray 类型的 转换成vo类型
    :param boxes:
    :return:
    """
    result_box = []
    for box in boxes:
        result_box.append(box2pos(box))
    return result_box


def box2pos(box):
    """
    box 转换成PositionEntity 类型的list
    :param box:
    :return:
    """
    # print(type(box),box)
    box = np.array(box)
    # temp_box = box
    temp_box = np.reshape(box, (-1, 2))
    # print(type(temp_box),temp_box)
    box_pos = []
    for pts in temp_box:
        box_pos.append(PositionEntity(int(pts[0]), int(pts[1])))
    return box_pos


def convert_word_entity(boxes, text_arr, prob_arr=None):
    """
        构造word entity报文
    @param boxes: 文本框坐标（n,2）
    @param text_arr: 文本列表
    @param prob_arr: 文本置信度
    @return:
    """
    text = ""
    wordsInfo = []

    # 处理未分行的内容
    for i, box in enumerate(boxes):
        # logger.debug('文字:%s',text_arr[i])
        pos = []
        box = np.array(box)
        box = box.reshape(-1, 2)
        for pts in box:
            # logger.info("pts:%r",pts)
            pos.append(PositionEntity(int(pts[0]), int(pts[1])))
        word = WordEntity(text_arr[i], pos)
        if prob_arr:
            probs = prob_arr[i]
            prob = [float(_p) for _p in probs]
            word.prob = prob
        wordsInfo.append(word)
        text += text_arr[i] + " "
    return wordsInfo, text


def ndarray2list(boxes):
    if isinstance(boxes, list):
        boxes = np.array(boxes)
        return boxes.tolist()
    else:
        return boxes.tolist()


def generate_debug_two(show_img, small_images, text_arr):
    show_info = DebugEntity()
    if show_img is not None:
        show_info.type = "img"
        show_info.content = image_utils.nparray2base64(show_img)
    title_list = []
    title_list.append(DebugTitleEntity('img', 'img', '识别小图', 80))
    title_list.append(DebugTitleEntity('text', 'text', '识别结果', 20))
    show_info.title_list = title_list
    for img, txt in zip(small_images, text_arr):
        row = DebugRowEntity()
        row.add_cell("img", image_utils.nparray2base64(img))
        row.add_cell("text", txt)
        show_info.add_row(row)
    return show_info
