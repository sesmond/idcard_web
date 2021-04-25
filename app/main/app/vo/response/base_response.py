"""
通用返回参数
"""


class BaseResponse:
    def __init__(self, code="0", message="success"):
        self.code = code
        self.message = message

    code = "0"
    message = "success"
    debug_info = None
    show_info = None

    def error(self, code, message):
        self.code = code
        self.message = message


class PositionEntity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    x = ''
    y = ''


class WordEntity:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos
        # self.prob = prob

    word = ''  # | 是        | string   |识别结果：文本
    pos = [PositionEntity]  # | 是        | int32    |识别结果：坐标
    # prob = []   # |否        | float     |逐字置信度


class DebugInfo:
    """ 页面debug用参数 """
    boxes = []
    # 切开的小图base64
    small_images = []
    # 矫正后的文本
    text_corrected = []
    # 识别的文本
    text = []
    #  划线后图片
    image = ''
    # # 置信度
    # prob = []


class DebugRowEntity:
    def __init__(self):
        self.content = {}

    def add_cell(self, cell_name, content):
        self.content[cell_name] = content


class DebugTitleEntity:
    def __init__(self, content_type, name, name_ch, percent):
        # 字段类型：img,text,num
        self.content_type = content_type
        # 字段名，要和行里面的字段名一一对应
        self.name = name
        self.name_ch = name_ch
        # 宽度百分比
        self.percent = percent


class DebugEntity:

    def __init__(self):
        # 主界面展示的内容类型：img/text
        self.type = ""
        # 主界面展示的内容
        self.content = ""
        # DebugEntity
        self.title_list = []
        self.detail_list = []
        # TODO!! 多个表格怎么办？

    def add_row(self, row: DebugRowEntity):
        self.detail_list.append(row.content)


if __name__ == '__main__':
    a = BaseResponse()
    print(a)
    import json
    from flask import jsonify, Flask

    app = Flask(__name__)
    app.run()
    a = BaseResponse("0", "success")
    print(a)
    b = json.dumps(a.__dict__)
    print(b)
    c = json.loads(b)
    bbb = jsonify({"a": 123})
    print(bbb)
    BaseResponse(code="9999", )
