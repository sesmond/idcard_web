var g_page_type = ''
var g_page_param = null

function queryParams(params) {
    var case_type = $("#case_type").val()
    return {
        case_type: case_type,
        limit: params.limit,
        paging: true,
        offset: (params.pageNumber - 1) * params.limit,
    };
}

let g_force = false;

//操作栏的格式化
function actionFormatter(value, row, index) {
    var contents = []
    // var showInfo = '<a style="cursor: pointer;" onclick="show_detail(\'' + row.flow_no + '\',\'' + row.case_type + '\')">详情</a>';
    // contents.push(showInfo);
    var delInfo = '<a style="cursor: pointer;" onclick="delete_log(\'' + row.flow_no + '\',\'' + row.case_type + '\')">删除</a>';
    // contents.push("|");
    contents.push(delInfo);
    return contents.join('');
}

function flowFormatter(value, row, index) {
    var showInfo = '<a style="cursor: pointer;" onclick="show_detail(\'' + row.flow_no + '\',\'' + row.case_type + '\')">'
        + value + '</a>';
    return showInfo
}

function numberFormatter(value, row, index) {
    if (value != '' && value != null) {
        return value.toFixed(2)
    } else {
        return "-"
    }
}

function delete_log(flow_no, case_type) {
    let param = {
        "flow_no": flow_no,
        "case_type": case_type
    }
    $.ajax({
        url: "/case/delete.ajax",
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            // alert("删除成功")
            query()
        },
        error: function (res) {
            // 错误时处理逻辑
            //debugger
        }
    });
}

function show_detail(flow_no, case_type) {
    // alert(flow_no)
    $(".main-content .main-content-inner").load("case_detail.html", function () {
        init_detail(flow_no, case_type)
    });
}


function init_page(page_type) {
    var init_page_type = page_type
    if (page_type.indexOf('sali') > -1) {
        init_page_type = 'sali'
    }


    g_page_type = init_page_type
    //弹出框的页面初始化
    // let page_param = page_param_json[init_page_type]
    let page_config = case_all_config[g_page_type]
    let page_param = {
        "title": page_config.name_ch,
        "url": "/case/execute.ajax",
        "input": [
            {
                "name": "channel",
                "name_zh": "执行渠道",
                "type": "select",
                "value": page_config.channel,
            },
            {
                "name": "data_type_list",
                "name_zh": "数据类型",
                "type": "multi_select",
                "is_array": true,
                "value": page_config.data_list
            },
            {
                "name": "remark",
                "name_zh": "备注",
                "type": "input",
            }
        ]
    }
    g_page_param = page_param
    init_query_page('box_toolbar', page_param)
    if (page_param.title) {
        $("#result_title").html(page_param.title)
    }
}


function execute(force) {
    let case_type = $("#case_type").val()
    let page_param = g_page_param
    let param = get_query_param(page_param)
    param["case_type"] = case_type
    param["force"] = force
    $.ajax({
        url: "/case/execute.ajax",
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            // $("#detail").append(res[1])
            alert("执行成功")
            query()
            //debugger
        },
        error: function (res) {
            // 错误时处理逻辑
            //debugger
        }
    });

}

function init_table() {
    $('#table').bootstrapTable({
        // url: '/case/query.ajax',
        queryParams: "queryParams",
        method: 'post',
        toolbar: "#toolbar",
        sidePagination: "client",
        search: true,
        striped: true,
        uniqueId: "flow_no",
        pagination: true, // 是否分页
        paginationLoop: false,
        pageSize: 10,
        pageList: [5, 10, 25, 50, 100],
        showRefresh: true,
        showToggle: true,
        sortable: true, // 是否启用排序
        // singleSelect: true,
        columns: [
            {
                checkbox: true  //第一列显示复选框
            },
            {
                field: 'id',
                title: '详情',
                formatter: actionFormatter

            },
            {
                field: 'case_type',
                title: '用例类型',
                visible: false
            },
            {
                field: 'flow_no',
                title: '流水号',
                formatter: flowFormatter

            },
            // {
            //     field: 'ip_address',
            //     title: '操作用户'
            // },
            {
                field: 'all_correct_cnt',
                title: '整体正确'
            },
            {
                field: 'all_error_cnt',
                title: '整体错误'
            },
            {
                field: 'all_correct_rate',
                title: '整体正确率'
            },
            {
                field: 'correct_cnt',
                title: '正确'
            },
            {
                field: 'error_cnt',
                title: '错误'
            },
            {
                field: 'correct_rate',
                title: '正确率',
                formatter: numberFormatter
            },
            {
                field: 'status',
                title: '状态'
            },
            {
                field: 'channel',
                title: '执行渠道'
            },
            {
                field: 'remark',
                title: '备注信息'
            },
            {
                field: 'start_time',
                title: '开始时间'
            },
            {
                field: 'end_time',
                title: '结束时间'
            },
            {
                field: 'f_measure',
                title: 'F1值'
            },
            {
                field: 'precision',
                title: '准确率'
            },
            {
                field: 'recall',
                title: '召回率'
            }
        ]
    });
}

function query() {
    $('#table').bootstrapTable("refresh", {
        url: "/case/query.ajax?t=" + Math.random(),
    }).on('load-success.bs.table', function (e, data) {
        // //debugger
    });
}

function post_json(url, param, callback) {
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(param),
        success: function (res) {
            callback(res)
        },
        error: function (res) {
            // 错误时处理逻辑
            //debugger
        }
    });
}

function init_list(case_type) {
    $("#case_type").val(case_type)
    var case_memo = case_all_config[case_type]['name_ch']
    $("#title_memo").text(case_memo + "-测试列表")
    // #TODO
    init_page(case_type)
    query();
}

function show_chart() {
    $("#echart").show()
}

function noshow_chart() {
    $("#echart").hide()
}

function case_compare_two() {
    var rows = $("#table").bootstrapTable('getSelections');
    if (rows != null && rows.length == 2) {
        var url = 'main.html'
        $(".main-content .main-content-inner").load(url, function () {
            init_case_diff(rows[0].flow_no, rows[1].flow_no)
        });
    } else {
        alert("请确认只选中两条数据！")
    }
}

$(function () {
    $("#execute_btn").click(function () {
            g_force = false
            $("#confirm_box").show()
        }
    );
    $("#force_btn").click(function () {
            g_force = true
            $("#confirm_box").show()
        }
    );
    $("#box_yes").click(function () {
        execute(g_force)
        $("#confirm_box").hide()
    });

    $("#box_close").click(function () {
        $("#confirm_box").hide()
    });


    $("#echart").mouseout(function () {
        noshow_chart()
    })
    $("#echart_btn").click(function () {
        var myChart = echarts.init(document.getElementById('echart'));
        var case_type = $("#case_type").val()
        var param = {case_type: case_type}
        post_json("/case/query.ajax", param, function (res) {
            var x_arr = []
            var true_arr = []
            var false_arr = []
            var rate_arr = []
            var all_rate_arr = []

            $(res).each(function (i, v) {
                x_arr.push(v['start_time'])
                // true_arr.push(v['correct_cnt'])
                // false_arr.push(v['error_cnt'])
                rate_arr.push(v['correct_rate'])
                all_rate_arr.push(v['all_correct_rate'])
            })
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '用例图表展示'
                },
                tooltip: {},
                legend: {
                    data: ['字段正确率', "整体正确率"]
                },
                xAxis: {
                    data: x_arr
                },
                yAxis: [
                    // {
                    //     type: 'value',
                    //     name: '条数'
                    // },
                    {
                        type: 'value',
                        name: '比例%',
                        max: 100,
                        min: 0,
                        axisLabel: {
                            formatter: function (value, index) {
                                return value.toFixed(2);
                            }
                        }

                    },
                ],
                series: [
                    //     {
                    //     name: '正确条数',
                    //     type: 'line',
                    //     yAxisIndex: 0,
                    //     data: true_arr
                    // }, {
                    //     name: '错误条数',
                    //     type: 'line',
                    //     yAxisIndex: 0,
                    //     data: false_arr
                    // },
                    {
                        name: '字段正确率',
                        type: 'line',
                        yAxisIndex: 0,
                        data: rate_arr
                    },
                    {
                        name: '整体正确率',
                        type: 'line',
                        yAxisIndex: 0,
                        data: all_rate_arr
                    }
                ],
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            show_chart()
        })
    });

    $('#search_btn').click(function () {
        query();
    });
    $("#case_compare_btn").click(function () {
        // #TODO!
        // 校验选中两条，然后调用
        case_compare_two()
    });
    init_table();

});