$(function(){
	$('#default_tabs').tabs({
		border:false,
		fit:true,
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
	/*
	$('#menu_nav').tree({
		url : 'static/js/index/normal_tree.json',
		onClick : function(node){
			if(node.url){
				if ($('#default_tabs').tabs('exists', node.text)){
					$('#default_tabs').tabs('select', node.text);
				} else {
					$('#default_tabs').tabs('addIframeTab', {
						tab : {
							title : node.text,
							closable : true,
							state : 'open',
							fit:true,
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
