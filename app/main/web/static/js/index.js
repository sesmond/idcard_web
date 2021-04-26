//所有页面共用的js

case_type_config = {
    "jsz": "驾驶证",
    "idcard": "身份证",
    "vrc": "机动车登记证",
    "ivc": "发票",
    "sali": "交强险",
    "xsz": "行驶证",
    "v_contract": "合同印签",
    "license_validation": "驾照校验",
    "plate_barcode": "车牌条码",
    "crnn": "crnn识别",
    "vrc.crz": "绿本.车融租",
    "vrc.34": "绿本.34页",
    "plate_ocr": "plate_ocr识别"
}

let case_all_config = {
    "jsz": {
        "name": "jsz",
        "name_ch": "驾驶证",
        "data_list": {
            "jsz": "驾驶证",
        },
        "channel": {
            "yitu": "宜图",
            "pfocr": "PFOCR",
            "ali": "阿里",
            "baidu": "百度",
            "huawei": "华为",
            "face": "旷视",
            "tencent": "腾讯",
        },
    },
    "vrc": {
        "name": "vrc",
        "name_ch": "机动车登记证(绿本)",
        "data_list": {
            "vrc": "绿本-30",
            "vrc.2": "135-普通(107)",
            "vrc.3": "135-模糊(12)",
            "vrc.4": "135-有转移记录(16)",
            "vrc.5": "新增-有转移记录(12)",
            "vrc.6": "新增-有转移记录(18)",
        },
        "channel": {
            "yitu": "宜图",
            "pfocr": "PFOCR",
            "dip": "DIP",
            "tencent": "腾讯",
            "etop": "译图",
            "qiniu": "七牛",
        },
        "field_list": {
            "info_list": "登记信息",
            "BH": "编号",
            // "SFZM": "身份证明",
            // "DJRQ": "登记日期",
            // "JDCDJBH": "机动车登记编号",
            "CLLX": "车辆类型",
            "CLPP": "车辆品牌",
            "CLXH": "车辆型号",
            "CSYS": "车身颜色",
            "CJH": "车辆识别代号/车架号",
            "FDJH": "发动机号",
            "RLZL": "燃料种类",
            "PL": "排量",
            "GL": "功率",
            "SYXZ": "使用性质",
            "CLHDFS": "车辆获得方式",
            "CLCCRQ": "车辆出厂日期",
            "FZRQ": "发证日期",
        },
        //二级对比
        "field_map": {
            "info_list": {
                "SFZM": "身份证明",
                "DJRQ": "登记日期",
                "JDCDJBH": "机动车登记编号"
            }
        }

    },
    "ivc": {
        "name": "ivc",
        "name_ch": "发票",
        "data_list": {
            "ivc": "发票",
        },
        "channel": {
            "yitu": "宜图",
            "pfocr": "PFOCR",
            "ali": "阿里",
            "baidu": "百度",
            "huawei": "华为",
        }
    },
    "sali": {
        "name": "sali",
        "name_ch": "交强险",
        "data_list": {
            "sali.e": "交强险电子",
            "sali.e2": "交强险电子2",
            "sali.p.good": "交强险套打清晰",
            "sali.p.bad": "交强险套打模糊",
            "sali.p2": "交强险套打2",
        },
        "channel": {
            "yitu": "宜图",
            "pfocr": "PFOCR",
            "qiniu": "七牛",
        }
    },
    "idcard": {
        "name": "idcard",
        "name_ch": "身份证",
        "data_list": {
            "idcard": "身份证",
        },
        "channel": {
            "yitu": "宜图",
            "baidu": "百度",
            "face": "旷世",
        }
    },
    "xsz": {
        "name": "xsz",
        "name_ch": "行驶证",
        "data_list": {
            "xsz": "行驶证",
        },
        "channel": {
            "yitu": "宜图",
        }
    },
    "v_contract": {
        "name": "v_contract",
        "name_ch": "合同印签",
        "data_list": {
            "v_contract.rongzi.good": "融资合同.正",
            "v_contract.rongzi.bad": "融资合同.负",
            "v_contract.diya.good": "抵押合同.正",
            "v_contract.diya.bad": "抵押合同.负",
        },
        "channel": {
            "yitu": "宜图",
        }
    },
    "license_validation": {
        "name": "license_validation",
        "name_ch": "驾照校验",
        "data_list": {},
        "channel": {
            "yitu": "宜图",
        }
    },
    "plate_barcode": {
        "name": "plate_barcode",
        "name_ch": "车牌条码",
        "data_list": {
            "plate_barcode": "车牌条码"
        },
        "channel": {
            "yitu": "宜图",
        }
    },
    "crnn": {
        "name": "crnn",
        "name_ch": "crnn识别",
        "data_list": {
            "crnn": "crnn数据"
        },
        "channel": {
            "yitu": "宜图",
        }
    },
    "psenet": {
        "name": "psenet",
        "name_ch": "psenet文本检测",
        "data_list": {
            "psenet": "单据样本"
        },
        "channel": {
            "yitu": "宜图",
        }
    },
    "vrc.crz": {
        "name": "vrc.crz",
        "name_ch": "机动车登记证(绿本)-车融租",
        "data_list": {
            "vrc": "绿本-30",
            "vrc.2": "135-普通(107)",
            "vrc.3": "135-模糊(12)",
            "vrc.4": "135-有转移记录(16)",
            "vrc.5": "新增-有转移记录(12)"
        },
        "channel": {
            "yitu": "宜图"
        },
        "field_list": {
            "FIRST_DJRQ": "首次登记日期",
            "LAST_JDCDJBH": "最新机动车登记编号",
            "CLPP": "车辆品牌",
            "CSYS": "车身颜色",
            "CJH": "车辆识别代号/车架号",
            // "FDJH": "发动机号",
            // "RLZL": "燃料种类",
            // "PL": "排量",
            // "GL": "功率",
            // "SYXZ": "使用性质",
            // "CLHDFS": "车辆获得方式",
            // "CLCCRQ": "车辆出厂日期",
            // "FZRQ": "发证日期",
        }
    },
    "vrc.34": {
        "name": "vrc.34",
        "name_ch": "机动车登记证(绿本)-34页",
        "data_list": {
            "vrc34.90": "90张张晨提供",
            "vrc34.140": "140张涛哥提供",
        },
        "channel": {
            "yitu": "宜图"
        }
    },
    "plate_ocr": {
        "name": "plate_ocr",
        "name_ch": "plate_ocr识别",
        "data_list": {
            "plate_ocr": "plate_ocr样本1-863",
            "plate_ocr.2": "plate_ocr样本2-150"
        },
        "channel": {
            "yitu": "宜图",
        }
    },
}


function load_main(name) {
    var url = 'main.html'
    $(".main-content .main-content-inner").load(url, function () {
        init_main(name)
    });
}

function load_case(case_type) {
    var url = 'case_list.html'
    $(".main-content .main-content-inner").load(url, function () {
        init_list(case_type)
    });
}

function load_demo(case_type, page_type) {
    var url = 'demo_show.html'
    $(".main-content .main-content-inner").load(url, function () {
        init_main(case_type, page_type)
    });
}

/**
 * 加载列表的共用方法，提到index里都能用到
 */
/**
 * 初始化类
 * @param element_name
 * @param item_value
 */
function get_select_cls(element_name, item_value) {
    let item_cls = element_name + '_' + item_value
    let cls_list = ['biz_type', 'btn', 'btn_primary']
    cls_list.push(element_name)
    cls_list.push(item_cls)
    let cls_str = cls_list.join(' ')
    return cls_str

}

function get_select_init_str(element_name, item_key, item_value) {
    let cls_str = get_select_cls(element_name, item_key)
    let select_str = "<a href=\"javascript:;\" class='" + cls_str + "'" +
        " onclick=\"query_select('" + item_key + "',this,'" + element_name + "');\">" + item_value + "</a>"

    return select_str
}

function get_input_config(all_input_config, input_key) {
    if (input_key == undefined || input_key == null)
        return null
    for (let item of all_input_config) {
        let item_name = item['name']
        if (item_name === input_key) {
            return item
        }
    }
    return null
}

function get_element_str(parent_id, element_config, image_arr, all_input_config) {
    let element_name = element_config.name
    let div_id = element_name + "_div_id"
    let input_cls_name = element_name + "_input"
    let parent_config = get_input_config(all_input_config, element_config.parent_node)
    let temp_str = ""
    let defaultValue = element_config.default;
    if (defaultValue == undefined) {
        defaultValue = ""
    }
    if (element_config.type == 'bool') {
        let true_class = "btn ";
        let false_class = "btn ";
        if (defaultValue === true)
            true_class += "btn-primary ";
        else if (defaultValue === false)
            false_class += "btn-primary ";
        temp_str += "<input type='hidden' class='form-control' name='" + element_name + "' value='" + defaultValue + "'>"

        temp_str +=
            "    <a href=\"javascript:;\" class='" + true_class + element_name + "' onclick=\"query_bool(true,this,'" + element_name + "');\">是</a>" +
            "    <a href=\"javascript:;\" class='" + false_class + element_name + "' onclick=\"query_bool(false,this,'" + element_name + "');\">否</a>"

    } else if (element_config.type == 'select') {
        let parent_cls_name = element_config.parent_node + "_input"
        temp_str += "<input  class='form-control select " + input_cls_name + "'  type='hidden' name='" + element_name + "' value='" + defaultValue + "'/>"
        if (element_config.parent_node) {
            //动态绑定事件
            $("body").on("change", '.' + parent_cls_name, function () {
                var parent_value = $(this).val();
                var value_config = element_config.value;
                var select_values = value_config[parent_value];
                var new_select_str = temp_str
                if (select_values != undefined) {
                    $.each(select_values, function (key, item) {
                        let sel_str = get_select_init_str(element_name, key, item)
                        new_select_str += sel_str
                    })
                    $("." + div_id).show()
                } else {
                    $("." + div_id).hide()
                }
                //TODO 怎么把这块追加上去，得有个地方能查找到然后贴进去
                $("#" + parent_id).html(new_select_str)
            });

        } else {
            $.each(element_config.value, function (key, item) {
                let sel_str = get_select_init_str(element_name, key, item)
                temp_str += sel_str
            })
        }
    } else if (element_config.type == 'multi_select') {
        let parent_cls_name = element_config.parent_node + "_input"
        temp_str += "<input  class='form-control select " + input_cls_name + "'  type='hidden' name='" + element_name + "' value=''/>"
        if (element_config.parent_node) {
            //动态绑定事件
            $("body").on("change", '.' + parent_cls_name, function () {
                let parent_value = $(this).val();
                if (parent_config == undefined || parent_config == null) {
                    alert("配置不正确，父节点配置错误，请查找代码！")
                    return
                }
                //TODO 如果父字段是多选
                let value_config = element_config.value;
                let select_values = {}
                if (parent_config.type == 'multi_select') {
                    if (parent_value != '') {
                        let parent_value_arr = parent_value.split(",")
                        for (let pv of parent_value_arr) {
                            if (value_config.hasOwnProperty(pv)) {
                                select_values = value_config[pv];
                                break
                            }
                        }
                    }
                } else {
                    select_values = value_config[parent_value];
                }
                let new_select_str = temp_str
                if (select_values != undefined && Object.keys(select_values).length > 0) {
                    $.each(select_values, function (key, item) {
                        new_select_str += "<a href=\"javascript:;\" class='btn btn_primary " + element_name + "'" +
                            " onclick=\"query_multi_select('" + key + "',this,'" + element_name + "');\" value='" + key + "'>" + item + "</a>"
                    })
                    $("." + div_id).show()
                } else {
                    $("." + div_id).hide()
                }
                //TODO 怎么把这块追加上去，得有个地方能查找到然后贴进去
                $("#" + parent_id).html(new_select_str)
            });

        } else {
            $.each(element_config.value, function (key, item) {
                temp_str += "<a href=\"javascript:;\" class='btn btn_primary " + element_name + "'" +
                    " onclick=\"query_multi_select('" + key + "',this,'" + element_name + "');\" value='" + key + "'>" + item + "</a>"
            })
        }
    } else if (element_config.type == 'image') {
        temp_str += "<input  class='form-control'  type='hidden' name='" + element_name + "' value=''/>"
        let img_id = element_name + "_file"
        temp_str += '<input  class="form-control"  type="file" id="' + img_id + '" multiple="multiple" />'
        image_arr.push(element_name)
    } else if (element_config.type == 'input') {
        temp_str += "<input  class='form-control'  type='text' name='" + element_name + "' value='" + defaultValue + "'/>"
    }
    let show = true
    if (element_config.parent_node) {
        show = false
    }
    return [show, temp_str]
}

/**
 * 给布尔项赋值
 * @param bool_flg ：true/false
 * @param e : 元素
 * @param cls ：对应的class
 */
function query_bool(bool_flg, e, cls) {
    $("." + cls).removeClass("btn-primary");
    $(e).addClass("btn-primary");
    $("input[name='" + cls + "']").val(bool_flg)
}

/**
 * 选择项赋值
 * @param select_type 选择元素的值
 * @param e 选择元素对象
 * @param cls 字段class
 */
function query_select(select_type, e, cls) {
    $("." + cls).removeClass("btn-primary");
    $(e).addClass("btn-primary");
    $("input[name='" + cls + "']").val(select_type)
    //手动触发change事件
    $("input[name='" + cls + "']").change()

}


function query_multi_select(select_type, e, cls) {
    //选中多选框
    const select_class_name = "btn-primary";
    if ($(e).hasClass(select_class_name)) {
        $(e).removeClass(select_class_name);
    } else {
        $(e).addClass(select_class_name);
    }
    var ele_arr = []
    $("." + cls).each(function (index, item) {
        if ($(item).hasClass(select_class_name)) {
            ele_arr.push($(item).attr("value"))
        }
    })
    $("input[name='" + cls + "']").val(ele_arr)
    //手动触发change事件
    $("input[name='" + cls + "']").change()
}

/**
 * 初始化查询条件
 * @param page_id
 * @param page_param
 */
function init_query_page(page_id, page_param) {
    var input_str = ""
    var image_arr = []
    $.each(page_param.input, function (index, value) {
        var field_name = value.name
        var field_name_zh = value.name_zh
        var dd_id = field_name + "_dd_id"
        var div_id = field_name + "_div_id"
        debugger
        var element_info = get_element_str(dd_id, value, image_arr, page_param.input);
        var style_str = ''
        if (!element_info[0]) {
            style_str = 'style="display:none;"'
        }
        var temp_str =
            '<div ' + style_str + 'class="form-group ' + div_id + '">' +
            " <dl>" +
            "  <label>" + field_name_zh + "：</label>" +
            "  <dd id='" + dd_id + "'>" +
            element_info[1] +
            "  </dd>" +
            "</dl>" +
            "</div>"
        input_str += temp_str
    })
    $("#" + page_id).prepend(input_str)
    //事件要加在后面
    $.each(image_arr, function (i, img_name) {
        init_image(img_name + "_file", img_name)
    })
}


function get_query_param(page_param) {
    var param = {}
    $.each(page_param.input, function (index, item) {
        let temp_val = $("input[name='" + item.name + "']").val()
        if (item.type == 'bool') {
            temp_val = JSON.parse(temp_val)
        }
        //数组元素则多拼
        if (item.is_array) {
            if (temp_val != undefined && temp_val.length > 0) {
                param[item.name] = temp_val.split(",")
            } else {
                param[item.name] = []
            }
        } else {
            param[item.name] = temp_val
        }
    })
    return param
}


function load_show(result) {
    debugger
    $("#show_output").show()
    $("#show_table").empty("");
    var $table = $("#show_table");
    var show_info = result['show_info']
    var title_list = show_info['title_list']
    //1. 先把标题加进去
    var title_str = '<tr>'
    title_list.forEach(function (e, i, array) {
        title_str += '<th width="' + e['percent'] + '%" align="left">' + e['name_ch'] + '</th>'
    });
    title_str += "</tr>"
    $table.append(title_str)
    if (show_info['type'] == 'img') {
        load_origin_image(show_info['content'])
    }
    var detail_list = show_info['detail_list']
    detail_list.forEach(function (cell, i, array) {
        var $tr = '<tr>';
        title_list.forEach(function (e, i, array) {
            var cell_value = cell[e['name']]
            if (e['content_type'] == 'img') {
                $tr += '<td width="' + e['percent'] + '%" align="left"><img style="min-height:20px;max-width:95%" src="data:image/jpg;base64,' + cell_value + '"></td>'
            } else {
                $tr += '<td width="' + e['percent'] + '%" style="WORD-WARP:break-word">' + cell_value + '</td>'
            }
        });
        $tr += '</tr>'
        $table.append($tr)
    });
}
