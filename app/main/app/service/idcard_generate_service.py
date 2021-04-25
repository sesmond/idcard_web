# coding:utf-8
import os
from multiprocessing import Process

import PIL.Image as PImage
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw

from app.main.app.service import config_util
from app.main.app.utils import image_util, config, text_util, vo_utils
from app.main.app.vo.response.base_response import BaseResponse

"""

“姓名”、“性别”、“民族”、“出生年月日”、“住址”、“公民身份号码”为6号黑体字，用蓝色油墨印刷;
登记项目中的姓名项用5号黑体字印刷;其他项目则用小5号黑体字印刷;

身份证上自己的姓名的字体是什么字体？

出生年月日 方正黑体简体
字符大小：姓名＋号码（11点）其他（9点）
字符间距（AV）：号码（50）
字符行距：住址（12点）

身份证号码字体 OCR-B 10 BT 文字 华文细黑

其右侧为证件名称“中华人民共和国居民身份证”，分上下两排排列，
其中上排的“中华人民共和国”为4号宋体字，
下排的“居民身份证”为2号宋体字;
“签发机关”、“有效期限”为6号加粗黑体字;
签发机关登记项采用，“xx市公安局”;
有效期限采用“xxxx.xx-xxxx.xx.xx”格式，使用5号黑体字印刷

### 生成需求：

- 各种信息自动生成，地址变长
- 对生成图，做各类仿射和透射
- 对生成图，做各类模糊和噪音、光照处理
- 选择多张背景进行贴片
- 生成仿射后的EAST训练数据
"""
base_dir = "./resource"


def changeBackground(img, img_back, zoom_size, center):
    # 缩放
    img = cv2.resize(img, zoom_size)
    rows, cols, channels = img.shape

    # 转换hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 获取mask
    # lower_blue = np.array([78, 43, 46])
    # upper_blue = np.array([110, 255, 255])
    diff = [5, 30, 30]
    gb = hsv[0, 0]
    lower_blue = np.array(gb - diff)
    upper_blue = np.array(gb + diff)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    # 腐蚀膨胀
    erode = cv2.erode(mask, None, iterations=1)
    dilate = cv2.dilate(erode, None, iterations=1)

    # 粘贴
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 0:  # 0代表黑色的点
                img_back[center[0] + i, center[1] + j] = img[i, j]  # 此处替换颜色，为BGR通道

    return img_back


def paste(avatar, bg, zoom_size, center):
    avatar = cv2.resize(avatar, zoom_size)
    rows, cols, channels = avatar.shape
    for i in range(rows):
        for j in range(cols):
            bg[center[0] + i, center[1] + j] = avatar[i, j]
    return bg


class IdCardGenerator(object):
    def __init__(self):
        # 加载空模板
        im = PImage.open(os.path.join(base_dir, 'empty.png'))
        self.empty_img = im

        self.name_font = ImageFont.truetype(os.path.join(base_dir, 'font/hei.ttf'), 72)
        self.other_font = ImageFont.truetype(os.path.join(base_dir, 'font/hei.ttf'), 60)
        self.bdate_font = ImageFont.truetype(os.path.join(base_dir, 'font/fzhei.ttf'), 60)
        self.id_font = ImageFont.truetype(os.path.join(base_dir, 'font/ocrb10bt.ttf'), 72, index=0)  # TODO 字体大小

    def generate(self, id_card):
        addr = id_card.addr
        draw = ImageDraw.Draw(self.empty_img)
        # TODO 计算坐标 根据字体大小计算  四点坐标 八项元素
        front_boxes = []  # 文字框 [[x1,y1,x2,y2,x3,y3],[]]
        # TODO 看需要标注的坐标有哪些
        draw.text((630, 690), id_card.name, fill=(0, 0, 0), font=self.name_font)
        box_name = text_util.calculate_text_box(630, 690, id_card.name, self.name_font)
        draw.text((630, 840), id_card.sex, fill=(0, 0, 0), font=self.other_font)
        box_sex = text_util.calculate_text_box(630, 840, id_card.sex, self.other_font)
        draw.text((1030, 840), id_card.nation, fill=(0, 0, 0), font=self.other_font)
        box_nation = text_util.calculate_text_box(1030, 840, id_card.nation, self.other_font)
        draw.text((630, 980), id_card.year, fill=(0, 0, 0), font=self.bdate_font)
        draw.text((950, 980), id_card.month, fill=(0, 0, 0), font=self.bdate_font)
        draw.text((1150, 980), id_card.day, fill=(0, 0, 0), font=self.bdate_font)

        # 生日年月日画在同一个框里
        # box_year = text_util.calculate_text_box(1030,840,id_card.year,bdate_font)
        birth_box = text_util.generate_box_by_two(630, 980, 1288, 1035)
        front_boxes.append(birth_box)
        # TODO 字符间距
        draw.text((950, 1475), id_card.idNo, fill=(0, 0, 0), font=self.id_font)
        box_id_no = text_util.calculate_text_box(950, 1475, id_card.idNo, self.id_font)
        front_boxes.append(box_id_no)

        name_label = text_util.generate_box_by_two(432, 710, 587, 764)
        front_boxes.append(name_label)
        sex_label = text_util.generate_box_by_two(432, 845, 587, 900)
        front_boxes.append(sex_label)
        nation_label = text_util.generate_box_by_two(847, 845, 1004, 900)
        front_boxes.append(nation_label)
        birth_label = text_util.generate_box_by_two(432, 982, 587, 1035)
        front_boxes.append(birth_label)
        addr_label = text_util.generate_box_by_two(432, 1116, 587, 1173)
        front_boxes.append(addr_label)
        id_code_label = text_util.generate_box_by_two(432, 1482, 791, 1537)
        front_boxes.append(id_code_label)

        front_boxes.append(box_name)
        front_boxes.append(box_sex)
        front_boxes.append(box_nation)

        # 地址换行处理 TODO 画框
        start = 0
        loc = 1120
        while start + 11 < len(addr):
            draw.text((630, loc), addr[start:start + 11], fill=(0, 0, 0), font=self.other_font)
            temp_box = text_util.calculate_text_box(630, loc, addr[start:start + 11], self.other_font)
            front_boxes.append(temp_box)
            start += 11
            loc += 100
        # TODO 画图并返回box 代码可以合并
        draw.text((630, loc), addr[start:], fill=(0, 0, 0), font=self.other_font)
        addr_box = text_util.calculate_text_box(630, loc, addr[start:], self.other_font)
        front_boxes.append(addr_box)

        # 背面
        back_boxes = []
        draw.text((1050, 2750), id_card.org, fill=(0, 0, 0), font=self.other_font)
        box_org = text_util.calculate_text_box(1050, 2750, id_card.org, self.other_font)
        draw.text((1050, 2895), id_card.validPeriod, fill=(0, 0, 0), font=self.other_font)
        box_period = text_util.calculate_text_box(1050, 2895, id_card.validPeriod, self.other_font)
        back_boxes.append(box_org)
        back_boxes.append(box_period)
        org_lable = text_util.generate_box_by_two(725, 2751, 987, 2815)
        period_lable = text_util.generate_box_by_two(725, 2897, 987, 2960)
        back_boxes.append(org_lable)
        back_boxes.append(period_lable)

        # 头像处理
        avatar = id_card.avatar
        avatar = cv2.cvtColor(np.asarray(avatar), cv2.COLOR_RGBA2BGRA)
        im = cv2.cvtColor(np.asarray(self.empty_img), cv2.COLOR_RGBA2BGRA)
        avatar = cv2.cvtColor(avatar, cv2.COLOR_RGBA2BGRA)
        im = changeBackground(avatar, im, (500, 670), (690, 1500))

        im = PImage.fromarray(cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA))

        # 抠出身份证正反面图片
        front_box = [284, 489, 2170, 1670]
        # TODO 去黑边
        front = im.crop(front_box)
        front = image_util.remove_black_edge(front)
        back_box = [283, 1903, 2168, 3093]
        back = im.crop(back_box)
        back = image_util.remove_black_edge(back)
        return front, back

    def paste_background(self, front, back, bg_front, bg_back):
        # TODO 前后抠图，先抠图后贴字还是先贴字后抠图
        # # 正面处理 image_name + "_front"
        # new_img, img_boxes = process_id_image(bg_front, front, front_box, front_boxes)
        # # 反面处理 image_name + "_back"
        # new_img, img_boxes = process_id_image(bg_back, back, back_box, back_boxes)
        pass


def generator(id_card, image_name, bg_front, bg_back):
    pass


def process_id_image(bg_img, img, img_boxes):
    # 大图坐标切为小图坐标
    w, h = img.size()
    img_boxes = text_util.move_box_coordinate(w, h, img_boxes)

    img_size = img.size
    img = img.resize((img_size[0] // config.SCALE_RATE, img_size[1] // config.SCALE_RATE))
    # TODO 缩小之后坐标转换
    img_boxes = text_util.calculate_scale_box(img_boxes, config.SCALE_RATE)
    # TODO box 转换 转换为身份证小图的坐标
    # 旋转贴背景

    new_img, img_boxes = image_util.random_process_paste(img, bg_img, img_boxes)

    return new_img, img_boxes

    # img_region = front_new.crop((0, 0, front.size[0], front.size[1]))
    # save_image_and_label(front_boxes, image_name)
    if not os.path.exists(path): os.makedirs(path)
    # 生成的图片存放目录
    data_images_dir = os.path.join(path, "images")
    # 生成的图片对应的标签的存放目录，这个是小框的标签
    data_labels_dir = os.path.join(path, "labels")
    if not os.path.exists(data_images_dir):
        os.makedirs(data_images_dir)
    if not os.path.exists(data_labels_dir):
        os.makedirs(data_labels_dir)
    # TODO 是否要生成大框坐标 方便UNET使用
    # image_path = os.path.join(data_images_dir, image_name + ".png")
    #
    # new_img.save(image_path)
    # print("生成样本：", image_path)
    # label_path = os.path.join(data_labels_dir, image_name + ".txt")
    # print("生成标签：", label_path)

    # 标签名字
    # with open(label_path, "w") as label_file:
    #     for label in img_boxes:
    #         # TODO 坐标怎么拼接
    #         xy_info = ",".join([str(pos) for pos in label])
    #         label_file.write(xy_info)
    #         label_file.write("\n")


def generate_batch(path, work_no, task_num, icon_list, bg_list):
    for i in range(0, task_num):
        print("生成第", work_no, "批，第", i, "张身份证")
        card = config_util.generateIdCard()
        card.print()
        card.avatar = image_util.get_random_icon(icon_list)
        bg_1, w1, h1 = image_util.create_backgroud_image(bg_list)
        bg_2, w2, h2 = image_util.create_backgroud_image(bg_list)
        img_name = str(work_no) + '_id_' + str(i).zfill(5)
        generator(card, img_name, bg_1, bg_2)
        # except Exception as e:
        #     print("样本生成发生错误，忽略此错误，继续....",str(e))


def generate_idcard():
    config_util.initArea()

    card = config_util.generateIdCard()
    card.print()
    icon_list = image_util.get_all_icons()
    card.avatar = image_util.get_random_icon(icon_list)
    gen = IdCardGenerator()
    front, back = gen.generate(card)
    images = []
    front = cv2.cvtColor(np.asarray(front), cv2.COLOR_RGBA2BGRA)
    back = cv2.cvtColor(np.asarray(back), cv2.COLOR_RGBA2BGRA)
    images.append(front)
    images.append(back)
    labels = ["正面", "反面"]
    show_info = vo_utils.generate_debug_two(None, images, labels)
    resp = BaseResponse()
    resp.show_info = show_info
    # 生成身份证图片，根据一些信息因素
    return resp


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--type")
    parser.add_argument("--dir")
    parser.add_argument("--num")
    parser.add_argument("--worker")
    args = parser.parse_args()
    print(args)
    num = int(args.num)

    worker = int(args.worker)
    task_num = num // worker  # 每个进程应该处理的个数

    save_path = args.dir + "/" + args.type
    # 初始化参数
    utils.initArea()

    icon_list = image_util.get_all_icons()
    bg_list = image_util.get_all_bg_images()
    print("save_path:", save_path)
    for i in range(worker):
        p = Process(target=generate_batch, args=(save_path, i, task_num, icon_list, bg_list))
        p.start()
        # generate_batch(save_path,i,task_num, icon_list,bg_list)
    print("生成成功")


if __name__ == '__main__':
    xxx = generate_idcard()
