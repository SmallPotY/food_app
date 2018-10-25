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

            var old_password_target = $("#old_password");
            var old_password = old_password_target.val();

            var new_password_target = $("#new_password");
            var new_password = new_password_target.val();

            if (!old_password || old_password.length < 1) {
                common_ops.tip("请输入新密码~~", old_password_target);
                return false;
            }

            if (!new_password || new_password.length < 1) {
                common_ops.tip("请再输入密码~~", new_password_target);
                return false;
            }


            if (new_password != old_password) {
                common_ops.tip("两次密码不一致~~", new_password_target);
                return false;
            }

            btn_target.addClass("disabled");

            var data = {
                new_password: new_password,
                old_password: old_password
            };

            $.ajax({
                url: common_ops.buildUrl("/user/reset-pwd"),
                type:'POST',
                data:data,
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
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