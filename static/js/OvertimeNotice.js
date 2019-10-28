$(function () {
    //alert(1);
    //$(document).ready(function () {});

    //检测待办事项
    function checkOverTodo() {
        $.ajax({
            type: 'GET',
            url: "/dqe/overtime/ov/overtime/message", //"{% url 'dqe:mt-loanconfirm-message' %}",
            //data: { csrfmiddlewaretoken: '{{ csrf_token }}' },
            success: function (data) {
                // console.log('111', data);
                // console.log(typeof (data));
                // console.log(data['data'][0]['applyState']);
                //如果用户没有该地址相应的权限，那么data返回的是一个html
                if (typeof (data) != 'string') {
                    showOverTodo(data['data'][0]['applyState'], data['data'][0]['count'], data['data'][0]['confirmUnit']);
                }

            },
            error: function (e) {

            }
        })
    }

    //显示有几条待办事项
    function showOverTodo(as, count, unit) {
        // $('#todo_over').css({
        //     "font-color": "#2536ff",
        //     'display': 'inline-block',
        //     'min-width': '10px',
        //     'padding': '3px 7px',
        //     'text-align': 'center',
        //     'white-space': 'nowrap',
        //     'vertical-align': 'baseline',
        //     'background-color': '#ff2235',
        //     'border-radius': '10px',
        //     'font-size': '12px',
        //     'font-weight': 'bold',
        //     'line-height': '8',
        // });
        //假如两个参数都有值，那么将值赋予到标签中
        if (as | count | unit) {
            if (unit == "Leader") {
                // console.log('111111--', count)
                if (count != 0) {
                    // console.log('111---', count)
                    $('#todo_over').text(count);
                    $('#message_over').text("您有" + count + "份待签核的申请单");
                } else {
                    $('#todo_over').remove();
                    $('#message_over').text("出去放鬆一下吧！！！");
                }
            }
        }


    }

    setTimeout(function () {
        checkOverTodo();
    }, 1000);

    setInterval(function () {
        checkOverTodo();
    }, 60000);

})