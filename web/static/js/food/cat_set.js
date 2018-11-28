;


let food_cat_set_ops = {
    init: function () {
        this.evenBind();
    },
    evenBind: function () {

        $("#save").click(function () {
            let btn_target = $(this);

            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理,请勿重复提交");
                return;
            }

            let name_target = $("#name");
            let name = name_target.val();

            let weight_target = $("#weight");
            let weight = weight_target.val();

            if (name.length < 1) {
                common_ops.tip("请输入符合规范的名称", name_target);
                return;
            }

            if (weight.length < 1) {
                common_ops.tip("请输入符合规范权重", weight_target);
                return;
            }

            btn_target.addClass("disabled");

            let data = {
                name: name,
                weight:weight,
                id: $("#id").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/food/cat-set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled');
                    let callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/food/cat');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }


            });

        });
    }


};


$(document).ready(function () {
    food_cat_set_ops.init();
});