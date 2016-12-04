$(function(){
	$('#tabs').tabs({
		border:false,
	});

	$('#menu_nav').tree({
		url : 'static/js/admin_tree.json',
		onClick : function(node){
			if(node.url){
				if ($('#tabs').tabs('exists', node.text)){
					$('#tabs').tabs('select', node.text);
				} else {
					$('#tabs').tabs('addIframeTab', {
						
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
