$(function(){
	$('#default_tabs').tabs({
		border:false,
		fit:true
	});
	$("div.westBar a").on("click", function(node){
        // 添加选中样式
        $("div.westBar a").removeClass('active');
        $(this).addClass('active');
        var url = $(this).attr('rel');
        var title = $.trim($(this).text());
        var iconCls = $(this).attr('iconCls')
        //var iconCls = $(this).find("span").attr('class');
        addTabs(url, title, iconCls);
    });
	 /*右侧菜单控制部分*/
	/*布局部分*/
	$('#master-layout').layout({
		fit:true/*布局框架全屏*/
	});  
    var left_control_status=true;
    var left_control_panel=$("#master-layout").layout("panel",'west');

    $(".left-control-switch").on("click",function(){
        if(left_control_status){
            left_control_panel.panel('resize',{width:70});
            left_control_status=false;
            $(".theme-left-normal").hide();
            $(".theme-left-minimal").show();
        }else{
            left_control_panel.panel('resize',{width:180});
            left_control_status=true;
            $(".theme-left-normal").show();
            $(".theme-left-minimal").hide();
        }
        $("#master-layout").layout('resize', {width:'100%'})
    });

    /*右侧菜单控制结束*/
	/*
	$('#menu_nav').tree({
		//url : 'static/js/index/admin_tree.json',
		onClick : function(node){
			console.log(node)
			if(node.url){
				if ($('#default_tabs').tabs('exists', node.text)){
					$('#default_tabs').tabs('select', node.text);
				} else {
					$('#default_tabs').tabs('addIframeTab', {
						tab : {
							title : node.text,
							closable : true,
							state : 'open',
							fit:true
						},
						iframe : {
							src : node.url,
							message : '数据正在加载中,请稍后...'
						},
					});//addtabs结束
				};//判断tab是否存在结束				
			};//if结束
		},//onclick结束
	});//tree结束
	*/
});//自执行函数结束
function addTabs(url, title, iconCls){
    if($('#default_tabs').tabs('exists',title)){ // 处理已打开过的tab
        $('#default_tabs').tabs('select',title);
        return;
    }
    if(!iconCls){
        iconCls = 'icon-ok';
    }
    $('#default_tabs').tabs('addIframeTab', {
		tab : {
			title : title,
			closable : true,
			state : 'open',
			iconCls: iconCls,
			fit:true
		},
		iframe : {
			src : url,
			message : '数据正在加载中,请稍后...'
		},
		onLoadError:function(data){
            // 这里对于非200状态码的都会加载不出来界面，而需要在这里手动处理
            var tab = $('#default_tabs').tabs('getSelected');
            var body = tab.panel('body');
            if(data.status == 401){
                body.html(data.responseText)
            }else{
                body.html('<h1>加载出错</h1>');
            }
        },
	});//addtabs结束

}
