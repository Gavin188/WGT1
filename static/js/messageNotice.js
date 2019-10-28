$(function () {
    //alert(1);
    //$(document).ready(function () {});

    //检测待办事项
    function checkTodo() {
        $.ajax({
            type: 'GET',
            url: "/dqe/mt/loanconfirm/message", //"{% url 'dqe:mt-loanconfirm-message' %}",
            //data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
            success: function (data) {
                // console.log('1-', data);
                // console.log(typeof(data));
                // console.log(data['data'][0]['applyState']);
                //如果用户没有该地址相应的权限，那么data返回的是一个html
                if (typeof (data) != 'string') {
                    showTodo(data['data'][0]['applyState'], data['data'][0]['count'], data['data'][0]['confirmUnit']);
                }

            },
            error: function (e) {

            }
        })
    }

    // //检测待办事项
    // function checkOvertTodo() {
    //     $.ajax({
    //         type: 'GET',
    //         url: "/dqe/overtime/ov/overtime/message", //"{% url 'dqe:mt-loanconfirm-message' %}",
    //         //data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
    //         success: function (data) {
    //             // console.log(data);
    //             // console.log(typeof(data));
    //             console.log('2-', data);
    //             //如果用户没有该地址相应的权限，那么data返回的是一个html
    //             if (typeof (data) != 'string') {
    //                 showTodo(data['data'][0]['applyState'], data['data'][0]['count'], data['data'][0]['confirmUnit']);
    //             }
    //
    //         },
    //         error: function (e) {
    //
    //         }
    //     })
    // }

    //显示有几条待办事项
    function showTodo(as, count, unit) {

        $('#todo').css({
            "font-color": "#2536ff",
            'display': 'inline-block',
            'min-width': '10px',
            'padding': '3px 7px',
            'text-align': 'center',
            'white-space': 'nowrap',
            'vertical-align': 'baseline',
            'background-color': '#ff2235',
            'border-radius': '10px',
            'font-size': '12px',
            'font-weight': 'bold',
            'line-height': '1',
        });
        //假如两个参数都有值，那么将值赋予到标签中
        if (as | count | unit) {

            // if (unit == "仓管") {
            //     console.log('3', unit, as, count);
            //     if (count != 0) {
            //         $('#todo').text(count);
            //         $('#message').text("您有" + count + "份待簽核的單據");
            //     } else {
            //         $('#todo').remove();
            //         $('#message').text("出去放鬆一下吧！！！");
            //     }
            // } else if (unit == "Leader") {
            //     console.log('4', unit, as, count);
            //     if (count != 0) {
            //         $('#todo').text(count);
            //         $('#message').text("您有" + count + "份待簽核的申请单");
            //     } else {
            //         $('#todo').remove();
            //         $('#message').text("出去放鬆一下吧！！！");
            //     }
            // }

            if (count != 0) {
                $('#todo').text(count);
                $('#message').text("您有" + count + "份待簽核的單據");
            } else {
                $('#todo').remove();
                $('#message').text("出去放鬆一下吧！！！");
            }

        }


    }

    setTimeout(function () {
        checkTodo();
    }, 1000);

    setInterval(function () {
        checkTodo();
    }, 60000);

    // setTimeout(function () {
    //     checkOvertTodo();
    // }, 1000);
    //
    // setInterval(function () {
    //     checkOvertTodo();
    // }, 60000);


})