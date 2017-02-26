$(function(){
	$('#admin_default_tabs').tabs({
		border:false,
		fit:true
	});
	
	$('#menu_nav').tree({
		url : 'static/js/index/admin_tree.json',
		onClick : function(node){
			if(node.url){
				if ($('#admin_default_tabs').tabs('exists', node.text)){
					$('#admin_default_tabs').tabs('select', node.text);
				} else {
					$('#admin_default_tabs').tabs('addIframeTab', {
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
});//自执行函数结束
