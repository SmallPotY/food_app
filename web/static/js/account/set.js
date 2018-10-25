;


var user_edit_ops = {
    init: function () {
        this.eventBind();
    },

    eventBind: function () {

        $("#save").click(function () {

            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理,请不要重复提交~~");
                return;
            }

            var nickname_target = $("#nickname");
            var nickname = nickname_target.val();

            var mobile_target = $("#mobile");
            var mobile = mobile_target.val();

            var email_target = $("#email");
            var email = email_target.val();

            var login_name_target = $("#login_name");
            var login_name = login_name_target.val();

            var login_pwd_target = $("#login_pwd");
            var login_pwd = login_pwd_target.val();

            if (!nickname || nickname.length < 1) {
                common_ops.tip("请输入姓名~~", nickname_target);
                return false;
            }
            if (!mobile || mobile.length < 1) {
                common_ops.tip("请输入手机~~", mobile_target);
                return false;
            }

            if (!email || email.length < 1) {
                common_ops.tip("请输入邮箱~~", email_target);
                return false;
            }
            if (!login_name || login_name.length < 1) {
                common_ops.tip("请输入登陆账号~~", login_name_target);
                return false;
            }
            if (!login_pwd || login_pwd.length < 1) {
                common_ops.tip("请输入登陆密码~~", login_pwd_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                nickname: nickname,
                email: email,
                mobile: mobile,
                login_name: login_name,
                login_pwd: login_pwd
            };

            $.ajax({
                url: common_ops.buildUrl("/account/set"),
                type: 'POST',
                data: data,
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/account/index');
                        };
                    }
                    common_ops.alert(res.msg, callback);

                }
            })
        });


    }

};


$(document).ready(function () {

    user_edit_ops.init();

});