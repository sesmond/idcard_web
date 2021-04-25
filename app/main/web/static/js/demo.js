//各页面的输入输出参数项
page_param_json = {
    "demo": {
        "title": "功能DEMO展示",
        "url": "/case/demo.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "case_type",
                "name_zh": "用例类型",
                "type": "select",
                "value": {
                    "jsz": "驾驶证",
                    "xsz": "行驶证",
                    "vrc": "机动车登记证",
                    "ivc": "发票",
                    "sali": "交强险",
                    "idcard": "身份证",
                    "handwriting": "手写体",
                    "v_contract": "合同签名",
                    "plate_barcode": "车牌条码",
                    "license_validation": "驾照格式",
                }
            },
            {
                "name": "contract_type",
                "name_zh": "合同类型",
                "type": "select",
                "parent_node": "case_type",
                "value": {
                    "v_contract": {
                        "01": "融资合同",
                        "02": "抵押合同",
                    }
                }
            },
        ],
        "output_type": "idcard",
        "output": {}
    }, "demo1": {
        "title": "功能DEMO展示",
        "url": "/case/demo.ajax",
        "input": [
            {
                "name": "img",
                "name_zh": "识别图片",
                "type": "image",
            },
            {
                "name": "case_type",
                "name_zh": "用例类型",
                "type": "select",
                "value": {
                    "jsz": "驾驶证",
                    "xsz": "行驶证",
                    "vrc": "机动车登记证",
                    "sali": "交强险",
                    "idcard": "身份证",
                    "handwriting": "手写体",
                    "v_contract": "合同签名",
                    "plate_barcode": "车牌条码",
                    "license_validation": "驾照格式"
                }
            },
            {
                "name": "contract_type",
                "name_zh": "合同类型",
                "type": "select",
                "parent_node": "case_type",
                "value": {
                    "v_contract": {
                        "01": "融资合同",
                        "02": "抵押合同",
                    }
                }
            },
        ],
        "output_type": "idcard",
        "output": {}
    }

}

var g_page_type = "demo"

function init_image(image_id, image_name) {
    $("#" + image_id).change(function () {
        var v = $(this).val();
        var reader = new FileReader();
        reader.readAsDataURL(this.files[0]);
        reader.onload = function (e) {
            var result = reader.result.split(",")[1]
            $("input[name='" + image_name + "']").val(result)
            load_origin_image(result)
        };
    });
}


function load_origin_image(base64_img) {
    $("#orgin_image").attr("src", "data:image/jpg;base64," + base64_img)
}


function submit_ocr() {
    var ajaxbg = $("#background,#progressBar");
    ajaxbg.show()
    $('#table tbody').empty();
    var param = {}
    var page_param = page_param_json[g_page_type]
    $.each(page_param.input, function (index, item) {
        let temp_val = $("input[name='" + item.name + "']").val()
        if (item.type == 'bool') {
            temp_val = JSON.parse(temp_val)
        }
        //数组元素则多拼
        if (item.is_array) {
            param[item.name] = [temp_val]
        } else {
            param[item.name] = temp_val
        }
    })
    //最外侧是数组
    if (page_param.input_is_array) {
        param = [param]
    }

    $.ajax({
        url: page_param.url,
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            ajaxbg.hide()
            $('html,body').animate({
                scrollTop: $("#show_output").offset().top - 50
            }, 300);

            // 成功处理逻辑
            load_result(res)
        },
        error: function (res) {
            ajaxbg.hide()
            // 错误时处理逻辑
            //debugger
        }
    });
}


function load_result(result) {
    $("#show_output").show()
    var data = result
    var $table = $("#table");
    data.forEach(function (e, i, array) {
        var $tr = '<tr class="pure-table-odd">'
            + '<td>' + e.name + '</td>'
            + '<td>' + e.value + '</td>'
            + '</tr>'
        $table.append($tr)
    });
}


function init_main(case_type, page_type) {
    g_page_type = "demo"
    if (page_type) {
        g_page_type = page_type
    }
    var page_param = page_param_json[g_page_type]
    init_query_page('toolbar', page_param)

    $('#submit_ocr').click(function () {
        return submit_ocr();
    });
    //初始化赋值
    let item_cls = 'case_type' + '_' + case_type
    var case_e = $("." + item_cls)
    //debugger
    query_select(case_type, case_e, "case_type")

}
