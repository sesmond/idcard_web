# encoding:utf-8
# !/usr/bin/python3

import os
import cv2

dir = "data/split_images/"
label_path = "data/label.txt"

def main(dir):
    files = os.listdir(dir)
    img_names = []
    for file in files:
        filename, ext = os.path.splitext(file)
        if ext == ".jpg":
            img_names.append(file)
        else:
            continue

    with open(label_path, "w", encoding="utf-8") as f:
        for img_name in img_names:
            f.write(str(img_name + " " + str(0)) + "\n")



def check_and_mk_path(path):
    """
    检测路径不存在则新建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.mkdir(path)


new_dir = "data/group/zn/"
txt_path = "data/group/zn.txt"
check_and_mk_path(new_dir)

def get_images(dir, new_dir, txt_path):
    with open(txt_path, "r", encoding="utf-8") as f1:
        for line in f1.readlines():
            name, label = line.split(" ")
            img_path = os.path.join(dir, name)
            image = cv2.imread(img_path)
            cv2.imwrite(os.path.join(new_dir,name),image)



if __name__ == "__main__":
   # main(dir)

    get_images(dir, new_dir, txt_path)
