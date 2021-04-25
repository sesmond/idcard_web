let g_detail_page_param = null
let g_flow_no = null

function init_detail(flow_no, case_type) {
    var param = {"flow_no": flow_no}
    g_flow_no = flow_no
    $("#case_type").val(case_type)
    $("#title_memo").text("用例测试详情：" + case_all_config[case_type]['name_ch'])
    $.ajax({
        url: "/case/detail.ajax",
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            $("#detail").append(res)
            debugger
        },
        error: function (res) {
            // 错误时处理逻辑
            debugger
        }
    });
}


function submit_detail_query() {
    //清空
    var page_param = g_detail_page_param
    var param = get_query_param(page_param)
    param['flow_no'] = g_flow_no
    $.ajax({
        url: page_param.url,
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            // 成功处理逻辑
            $("#detail").html(res)
        },
        error: function (res) {
            // 错误时处理逻辑
            //debugger
            alert(res)
        }
    });
}


function back_list() {
    var url = 'case_list.html'
    var case_type = $("#case_type").val()
    $(".main-content .main-content-inner").load(url, function () {
        init_list(case_type)
    });
}

function init_detail_query() {
    let case_type = $("#case_type").val()
    $("#detail_query_div").show()
    $("#toolbar").empty()
    let case_config = case_all_config[case_type]
    var page_param = {
        "title": "用例正确率测试",
        "url": "/case/detail/query.ajax",
        "input": [
            {
                "name": "prob_list",
                "name_zh": "概率筛选",
                //多选框
                "type": "multi_select",
                "is_array": true,
                "value": {
                    '1': '认为正确',
                    '2': '需要确认',
                    '3': '认为错误',
                }
            },
            {
                "name": "show_diff_only",
                "name_zh": "只展示不同",
                "type": "bool",
            }
        ],
        "output_type": "text",
        "output": {}
    }
    let field_list = case_config['field_list']
    if (field_list != undefined && field_list != null) {
        let input_field = {
            "name": "field_list",
            "name_zh": "比较字段",
            "type": "multi_select",
            "is_array": true,
            "value": field_list
        }
        page_param.input.push(input_field)
    }
    let field_map = case_config['field_map']
    if (field_map != undefined && field_map != null) {
        var extra_param_list = []
        for (var p_name in field_map) {
            var parent_value = field_list[p_name]
            var p_value = field_map[p_name]
            var extra_value = {}
            extra_value[p_name] = p_value
            var extra_param = {
                "name": p_name + "_detail",
                "name_zh": parent_value + "详情",
                //多选框
                "type": "multi_select",
                "is_array": true,
                "parent_node": "field_list",
                "value": extra_value
            }
            extra_param_list.push(extra_param)
        }
        page_param.input = page_param.input.concat(extra_param_list)
    }


    init_query_page('toolbar', page_param)
    g_detail_page_param = page_param
}

$(function () {
    $("#back_btn").click(function () {
            back_list()
        }
    );
    $("#start_filter").click(function () {
            init_detail_query()
        }
    );

    $('#submit_detail_query').click(function () {
        return submit_detail_query();
    });

});