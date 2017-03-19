$(function(){
	$('div a').click(function(){
		title = $(this).attr('id');
		url = $(this).attr('url');
		iconCls = $(this).attr('iconCls');
		var jq = top.jQuery;
		if (jq('#default_tabs').tabs('exists', title)){
			jq('#default_tabs').tabs('select', title);
		} else {
			jq('#default_tabs').tabs('addIframeTab', {
				tab : {
					title : title,
					closable : true,
					state : 'open',
					iconCls : iconCls,
				},
				iframe : {
					src : url + '?' + 'host_name=' + title,
					message : '数据正在加载中,请稍后...',
				},
			});//addtabs结束
		};//判断tab是否存在结束	
	});
});