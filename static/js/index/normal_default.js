$(function(){
	$('#normal_default_tabs').tabs({
		border:false,
	});

	$('#menu_nav').tree({
		url : 'static/js/index/normal_tree.json',
		onClick : function(node){
			if(node.url){
				if ($('#normal_default_tabs').tabs('exists', node.text)){
					$('#normal_default_tabs').tabs('select', node.text);
				} else {
					$('#normal_default_tabs').tabs('addIframeTab', {
						tab : {
							title : node.text,
							closable : true,
							state : 'open',
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
});//自执行函数结束
