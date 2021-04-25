# encoding:utf-8
# !/usr/bin/python3

import os
import cv2
import numpy as np
import random
import math
import json
from PIL import Image, ImageDraw
import image_rotate
from multiprocessing import Process, Pool
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

'''
    随机抽取一张汽车背景图片，随机选择一张生成的车牌，将生成的车牌贴在汽车背景图片上，增加干扰线、干扰点、随机旋转和切边等，增加生成车牌的真实性
'''

# 颜色的算法是，产生一个基准，然后RGB上下浮动FONT_COLOR_NOISE
MAX_FONT_COLOR = 100    # 最大的可能颜色
FONT_COLOR_NOISE = 10   # 最大的可能颜色
INTERFER_LINE_NUM = 8      # 最多干扰线
INTERFER_LINE_WIGHT = 2
INTERFER_POINT_NUM = 15     # 最多干扰点
ROTATE_ANGLE = 20      # 最大旋转角度
# 仿射的倾斜的错位长度  |/_/, 这个是上边或者下边右移的长度
AFFINE_OFFSET = 50

POSSIBILITY_RESIZE = 0.3    # 图像压缩的比例
POSSIBILITY_ROTATE = 0.7    # 图像旋转的比例
POSSIBILITY_INTEFER = 0.6   # 需要被干扰的图片比例，包括干扰线和点
POSSIBILITY_NOISE = 0.7  # 加干扰项概率
POSSIBILITY_PERSPECTIVE = 0.3  # 随机透射概率
POSSIBILITY_AFFINE = 0.4  # 随机仿射概率


def show(img, title='无标题'):
    """
    本地测试时展示图片
    :param img:
    :param name:
    :return:
    """
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font = FontProperties(fname='/Users/yanmeima/workspace/ocr/crnn/data/data_generator/fonts/simhei.ttf')
    plt.title(title, fontsize='large', fontweight='bold', FontProperties=font)
    plt.imshow(img)
    plt.show()


def get_random_icon(icon_list):
    '''
    随机获取一张图片
    :return:
    '''
    img = random.choice(icon_list)
    return img.copy()

# 随机接受概率
def _random_accept(accept_possibility):
    return np.random.choice([True,False], p=[accept_possibility,1 - accept_possibility])

# 产生随机点
def _get_random_point(x_scope,y_scope):
    x1 = random.randint(0,x_scope)
    y1 = random.randint(0,y_scope)
    return x1, y1

# 产生随机颜色
def _get_random_color():
    base_color = random.randint(0, MAX_FONT_COLOR)
    noise_r = random.randint(0, FONT_COLOR_NOISE)
    noise_g = random.randint(0, FONT_COLOR_NOISE)
    noise_b = random.randint(0, FONT_COLOR_NOISE)

    noise = np.array([noise_r,noise_g,noise_b])
    font_color = (np.array(base_color) + noise).tolist()

    return tuple(font_color)

# # 画干扰点
def randome_intefer_point(img, possible, num):
    if not _random_accept(possible): return

    w, h = img.size
    draw = ImageDraw.Draw(img)

    point_num = random.randint(0, num)
    for i in range(point_num):
        x, y = _get_random_point(w, h)
        draw.point([x, y], _get_random_color())
    del draw

# 画干扰线
def randome_intefer_line(img,possible,line_num,weight):
    if not _random_accept(possible): return

    w,h = img.size
    draw = ImageDraw.Draw(img)
    line_num = random.randint(0, line_num)

    for i in range(line_num):
        x1, y1 = _get_random_point(w,h)
        x2, y2 = _get_random_point(w,h)
        _weight = random.randint(0, weight)
        draw.line([x1,y1,x2,y2],_get_random_color(),_weight)

    del draw

def sp_noise(image, prob=0.1):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image / 255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out * 255)

    return out

def random_add_noise(img):
    '''
    随机添加噪声，光照、模糊
    :param img:
    :return:
    '''
    if not _random_accept(POSSIBILITY_NOISE):
        return img

    # TODO 光线
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)
    # 噪声
    if _random_accept(POSSIBILITY_NOISE):
        img = gasuss_noise(img)
    if _random_accept(POSSIBILITY_NOISE):
        img = sp_noise(img)
    # 高斯模糊----（图片太模糊，暂时关掉了）
    # if _random_accept(POSSIBILITY_NOISE):
    #     img = cv2.GaussianBlur(img, (15, 15), 0)

    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    randome_intefer_line(img, POSSIBILITY_INTEFER, INTERFER_LINE_NUM, INTERFER_LINE_WIGHT)
    randome_intefer_point(img, POSSIBILITY_INTEFER, INTERFER_POINT_NUM)

    return img


# 随机仿射一下，也就是歪倒一下
# 不能随便搞，我现在是让图按照平行方向歪一下，高度不变，高度啊，大小啊，靠别的控制，否则，太乱了
def random_affine(img, boxes):
    # TODO 仿射怎么搞
    HEIGHT_PIX = 10
    WIDTH_PIX = 50

    # 太短的不考虑了做变换了
    # print(img.size)
    original_width = img.size[0]
    original_height = img.size[1]
    points = [(0, 0), (original_width, 0), (original_width, original_height), (0, original_height)]

    if original_width < WIDTH_PIX: return img, points
    #print("!!!!!!!!!!")
    if not _random_accept(POSSIBILITY_AFFINE):
        return img, boxes

    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)

    is_top_fix = random.choice([True, False])

    bottom_offset = random.randint(0, AFFINE_OFFSET)  # bottom_offset 是 上边或者下边 要位移的长度

    height = img.shape[0]

    # 这里，我们设置投影变换的3个点的原则是，使用    左上(0,0)     右上(WIDTH_PIX,0)    左下(0,HEIGHT_PIX)
    # 所以，他的投影变化，要和整个的四边形做根据三角形相似做换算
    # .
    # |\
    # | \
    # |__\  <------投影变化点,  做三角形相似计算，offset_ten_pixs / bottom_offset =  HEIGHT_PIX / height
    # |   \                   所以： offset_ten_pixs = (bottom_offset * HEIGHT_PIX) / height
    # |____\ <-----bottom_offset
    offset_ten_pixs = int(HEIGHT_PIX * bottom_offset / height)  # 对应10个像素的高度，应该调整的横向offset像素
    width = int(original_width + bottom_offset)  # 宽度加上去了

    pts1 = np.float32([[0, 0], [WIDTH_PIX, 0], [0, HEIGHT_PIX]])  # 这就写死了，当做映射的3个点：左上角，左下角，右上角

    # \---------\
    # \         \
    #  \_________\
    logger.info("is_top_fix:%s", is_top_fix)
    if is_top_fix:  # 上边固定，意味着下边往右
        # print("上边左移") 高度固定
        pts2 = np.float32([[0, 0], [WIDTH_PIX, 0], [offset_ten_pixs, HEIGHT_PIX]])  # 看，只调整左下角
        M = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M, (width, height))
        # cv2.invertAffineTransform()
        # TODO 新坐标 大框还要吗？ 不要了 ，只要小框就可以 原来的坐标可能已经没有了，
        pts = np.array([[0, 0]], dtype="float32")
        pts = np.array([pts])
        pts1 = cv2.warpAffine(pts, M, (width, height))
        #print("仿射后坐标：", pts1)

        points = [(0, 0),
                  (original_width, 0),
                  (width, original_height),
                  (bottom_offset, original_height)]
    #  /---------/
    # /         /
    # /_________/
    else:  # 下边固定，意味着上边往右
        # 得先把图往右错位，然后
        # 先右移
        # print("上边右移")
        H = np.float32([[1, 0, bottom_offset], [0, 1, 0]])  #
        img = cv2.warpAffine(img, H, (width, height))
        # 然后固定上部，移动左下角
        pts2 = np.float32([[0, 0], [WIDTH_PIX, 0], [-offset_ten_pixs, HEIGHT_PIX]])  # 看，只调整左下角
        M = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M, (width, height))

        points = [(bottom_offset, 0),
                  (original_width + bottom_offset, 0),
                  (width, original_height),
                  (0, original_height)]

    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
    #show(img)
    return img, boxes


def random_perspective(img, boxes):
    '''
    随机透射
    :param img:
    :param boxes:
    :return:
    '''
    if not _random_accept(POSSIBILITY_PERSPECTIVE):
        return img, boxes
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGBA2BGRA)

    # #透射
    # TODO 随机生成坐标 计算输出坐标
    # 输入、输出图像上相应的四个点
    h, w = img.shape[:2]
    # 四点透视
    pts1 = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]])
    # TODO 任意固定两个点
    # TODO 往哪儿透射，设定一个幅度 可以各边各20% 的幅度吧
    percent = 0.2
    w_percent = w * percent
    h_percent = h * percent

    # TODO 四点分别几个点位置偏可以 有概率的选择，否则维持原点

    x1 = np.random.randint(0, w_percent)
    y1 = np.random.randint(0, h_percent)
    x2 = np.random.randint(0, w_percent)
    y2 = h - np.random.randint(1, h_percent)
    x3 = w - np.random.randint(1, w_percent)
    y3 = h - np.random.randint(1, h_percent)
    x4 = w - np.random.randint(1, w_percent)
    y4 = np.random.randint(0, h_percent)

    pts2 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

    dst = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGRA2RGBA))
    new_boxes = None
    if boxes is not None and len(boxes) > 0:
        new_boxes = []
        for box in boxes:
            temp = np.array(box, dtype="float32")
            temp = np.array([temp])
            box_new = cv2.perspectiveTransform(temp, M)
            box_new = box_new.astype(np.int)
            box_list = box_new.tolist()
            new_boxes.append(box_list[0])

    return dst, new_boxes


def image_resize(image, points):
    if not _random_accept(POSSIBILITY_RESIZE): return image, points

    w, h = image.size
    image = image.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
    new_points = []
    for point in points:
        x = point[0] / 2
        y = point[1] / 2
        new_points.append([x, y])

    return image, new_points


# def rotate(image, angle, scale=1.0):
#     #angle = random.randrange(MIN_ROTATE_ANGLE,MAX_ROTATE_ANGLE)
#     (h, w) = image.shape[:2]  # 2
#     # if center is None: #3
#     center = (w // 2, h // 2)  # 4
#     M = cv2.getRotationMatrix2D(center, angle, scale)  # 5
#
#     # 防止旋转图像丢失
#     sin = math.fabs(math.sin(math.radians(angle)))
#     cos = math.fabs(math.cos(math.radians(angle)))
#     h_new = int(w * sin + h * cos)
#     w_new = int(h * sin + w * cos)
#     M[0, 2] += (w_new - w) / 2
#     M[1, 2] += (h_new - h) / 2
#     # 旋转后边角填充
#     # rotated = cv2.warpAffine(image, M, (w_new, h_new), borderMode=cv2.BORDER_REPLICATE)
#     # 白背景填充
#     rotated = cv2.warpAffine(image, M, (w_new, h_new), borderValue=(254, 254, 254))
#     return rotated


def rotate_bound(image, background_image, w, h):
    '''
    随机旋转，贴背景
    '''
    if not _random_accept(POSSIBILITY_ROTATE):
        background_image.paste(image, (0, 0))
        angle = 0
    else:
        image_con = image.convert("RGBA")
        p = Image.new('RGBA', (w, h))
        p.paste(image_con, (0, 0))
        angle = random.randrange(-ROTATE_ANGLE, ROTATE_ANGLE)
        image_r = p.rotate(angle)

        r, g, b, a = image_r.split()
        w1, h1 = image_r.size
        background_image = background_image.resize((int(w1), int(h1)), Image.ANTIALIAS)
        background_image.paste(image_r, (0, 0), mask=a)

    return background_image, angle


def img_label_rotate(img, background_image, json_path,angle):
    '''
    随机图像旋转、仿射、透射、压缩和对应坐标旋转
    '''
    w, h = img.size
    center = (int(w / 2), int(h / 2))
    new_center = (int(w / 2), int(h / 2))

    with open(json_path, "r") as f:
        json_data = json.load(f)
        new_shapes = []
        for category in json_data['shapes']:
            points = category['points']
            # 随机旋转
            #background_image, angle = rotate_bound(img, background_image, w, h)
            newrect = image_rotate.get_rotate_box([np.array(points).astype(int)], center, angle, new_center)[0]
            logger.info("图片旋转后的坐标:%s", newrect)

            # 随机仿射
            img, newrect = random_affine(img, newrect)
            # 随机透射
            #img, newrect = random_perspective(img, newrect) # TODO:中间报错，待处理
            # 随机压缩
            #img, newrect = image_resize(img, newrect) # TODO:图片压缩2次，坐标压缩一次，待修改

            new_label = {
                "label": category['label'],
                "points": newrect,
                "shape_type": category['shape_type']
            }
            new_shapes.append(new_label)

        new_json = {
            "version": json_data["version"],
            "flags": json_data["flags"],
            "shapes": new_shapes,
            "imagePath": json_data["imagePath"],
            "imageData": json_data["imageData"],
            "imageHeight": json_data["imageHeight"],
            "imageWidth": json_data["imageWidth"]
        }
    return new_json


def img_enhance(image, files, json_path):
    w, h = image.size

    # 在整张图上随机添加噪音、干扰点和干扰线
    image = random_add_noise(image)

    # 随机抽取背景图片
    file = np.random.choice(files)
    background_image = Image.open(os.path.join(bg_path + file))
    # 背景图片压缩成跟需要增强的图片一样大小
    if w >= h:
        background_image = background_image.resize((int(w), int(w)), Image.ANTIALIAS)
    else:
        background_image = background_image.resize((int(h), int(h)), Image.ANTIALIAS)

    # 随机图像旋转
    background_image, angle = rotate_bound(image, background_image, w, h)
    # 图像旋转、仿射、透射、压缩和对应坐标旋转
    new_json = img_label_rotate(image, background_image, json_path, angle)

    return background_image, new_json


def save_file(background_image, new_json,image_name_1,label_name_1):
    background_image = background_image.convert('RGB')
    background_image.save(image_name_1)

    with open(label_name_1, "w", encoding='utf-8') as g:
        json.dump(new_json, g, indent=2, sort_keys=True, ensure_ascii=False)


def main(p_no, bg_path, file_list, origin_image_path, origin_json_path):
    for file in file_list:
        filename, ext = os.path.splitext(file)
        if ext != ".jpg":
            continue
        elif file != ".DS_Store":
            for num in range(0, 15):
                image_name_1 = os.path.join(enhance_path, filename + "_" + str(num) + ".jpg")
                label_name_1 = os.path.join(enhance_path, filename + "_" + str(num) + ".json")

                files = os.listdir(bg_path)
                img_path = os.path.join(origin_image_path, file)
                logger.info("线程：%r,读取图片：%s", p_no, img_path)

                image = Image.open(img_path)
                json_path = os.path.join(origin_json_path + filename + ".json")

                # 图像增强
                background_image, new_json = img_enhance(image, files, json_path)
                # 保存图片和标签
                save_file(background_image, new_json,image_name_1,label_name_1)
            logger.info("线程：%r,处理图片结束：%s", p_no, file)



if __name__ == "__main__":
    # 线程数
    worker = 20

    # bg_path = "data/test/bj/"
    # origin_image_path = "data/test/images/"
    # origin_json_path = "data/test/labels/"
    # enhance_path = "data/test/enhance/"

    bg_path = "data/summary/bj/"
    # origin_image_path = "data/summary/card_rotate/"
    # origin_json_path = "data/summary/card_rotate/"
    # enhance_path = "data/summary/enhance/"

    origin_image_path = "data/djz/labelme_split_180/"
    origin_json_path = "data/djz/labelme_split_180/"
    enhance_path = "data/djz/enhance/"

    if not os.path.exists(enhance_path): os.makedirs(enhance_path)

    image_all = os.listdir(origin_image_path)
    # 分批多线程处理
    file_list_arr = np.array_split(image_all, worker)
    logger.info("线程数：%r", worker)
    p_no = 0
    pool = Pool(processes=worker)

    for file_list in file_list_arr:
        print("file_list:",file_list)
        pool.apply_async(main, args=(p_no, bg_path, file_list, origin_image_path, origin_json_path))
        p_no += 1
    pool.close()
    pool.join()
    logger.info("程序处理结束，全部增强完毕！")


# def main(bg_path, file, origin_image_path, origin_json_path):
#     files = os.listdir(bg_path)
#     img_path = os.path.join(origin_image_path, file)
#     print(img_path)
#     image = Image.open(img_path)
#     json_path = os.path.join(origin_json_path + filename + ".json")
#
#     # 图像增强
#     background_image, new_json = img_enhance(image, files, json_path)
#     # 保存图片和标签
#     save_file(background_image, new_json)
#
#
# if __name__ == "__main__":
#     #ceshi
#     bg_path = "data/test/bj/"
#     origin_image_path = "data/test/images/"
#     origin_json_path = "data/test/labels/"
#     enhance_path = "data/test/enhance/"
#
#     # bg_path = "data/summary/bj/"
#     # origin_image_path = "data/summary/card_rotate/"
#     # origin_json_path = "data/summary/card_rotate/"
#     # enhance_path = "data/summary/enhance/"
#
#     if not os.path.exists(enhance_path): os.makedirs(enhance_path)
#
#     i = 0
#     j = 5
#     for file in os.listdir(origin_image_path):
#         filename, ext = os.path.splitext(file)
#         if ext != ".jpg":
#             continue
#         elif file != ".DS_Store":
#             for num in range(0, j):
#                 image_name_1 = os.path.join(enhance_path, str(i+num) + ".jpg")
#                 label_name_1 = os.path.join(enhance_path, str(i+num) + ".json")
#                 main(bg_path, file, origin_image_path, origin_json_path)
#
#             i += j
#             print("处理完成!")
