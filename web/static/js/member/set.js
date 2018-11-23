;



var member_set_ops = {
    init:function () {
        this.evenBind();
    },
    evenBind:function () {

        $("#save").click(function () {
            var btn_target = $(this);

            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理,请勿重复提交");
                return;
            }

            var nickname_target = $("#nickname");
            var nickname = nickname_target.val();

            if(nickname.length<1){
                common_ops.tip("请输入符合规范的姓名",nickname_target);
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                nickname:nickname,
                id:$("#id").val()
            };

            $.ajax({
                url:common_ops.buildUrl("/member/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass('disabled');
                    var callback=null;
                    if(res.code==200){
                        callback=function () {
                            window.location.href = common_ops.buildUrl('/member/index');
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }


            });

        });
    }


};




$(document).ready(function () {
    member_set_ops.init();
});