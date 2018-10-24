;

var user_login_ops = {

    init: function () {

        this.eventBind();
    },

    eventBind: function () {
        $(".login_wrap .do-login").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理,请稍后~~");
                return;
            }

            var login_name = $(".login_wrap input[name=login_name]").val();
            var login__pwd = $(".login_wrap input[name=login_pwd]").val();

            if (login_name == undefined || login_name.length < 1) {
                common_ops.alert("请输入正确的登录名~");
                return
            }

            if (login__pwd == undefined || login__pwd.length < 1) {
                common_ops.alert("请输入正确的登录名~");
                return
            }


            btn_target.addClass("disabled");


            $.ajax({
                url: common_ops.buildUrl("/user/login"),
                type: "POST",
                data: {'login_name': login_name, 'login_pwd': login__pwd},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/");
                        };
                    }
                    common_ops.alert(res.msg, callback);

                }
            });

        });
    }
};


$(document).ready(function () {
    user_login_ops.init();
});