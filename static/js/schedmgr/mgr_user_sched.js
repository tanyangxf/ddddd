$(function(){
	datagrid_resize('mgr_user_sched');
	obj = {
		open_window : function (id) {
			$('#'+id).children('iframe').attr('src','/schedmgr/queue_tree/')
			$('#'+id).window('open');
		},
		close_window : function(id){
			$('#'+id).children('iframe').removeAttr('src')
			$('#'+id).window('close');
		},
	};//obj结束
	//用户创建表单
	$('#user_sched_form').form({
		url : '/schedmgr/modify_user_sched/',
		onSubmit : function (param) {
			//提交之前取消输入框禁用
			$("input").prop("disabled",false);
			return $(this).form('validate');
			},
		success : function(data){
			$.messager.progress({
				title : '修改队列',
				msg : '正在修改队列，请稍后...',
			}); 
			if(data=='ok'){
				$.messager.alert('成功！', '队列修改成功', 'info');
			}else{
				$.messager.alert('失败！', '队列修改失败', 'error');
			};
			$.messager.progress('close');
			$('#mgr_user_sched').datagrid('reload');
			$('input[name="user_name"]').prev().validatebox({disabled:'disabled'});
			$('table tbody').find('tr:first-child').click();
		},
	});
	
	//设置首页用户数据表格
	 $('#mgr_user_sched').datagrid({
		 width : 'auto',
		 url : '/schedmgr/get_user_sched/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : false,
				checkbox : true,
				width : 100,
			},{
				 field : 'user_name',
				 title : '用户名称',
				 sortable : false,
				 width : 100,   //百分比
			 },
		 ]],
		 pagination : true,
		 pageSize : 20,
		 pageList : [20, 25, 30, 35, 40],
		 nowrap : true,
		 singleSelect : true,
		 fit : false,
		 scrollbarSize : 0, //滚动条宽度
		 fitColumns : true,
		 onClickRow : function(index, row){
			 //填充输入框
			 $('#user_sched_form').form('load',{
				 user_name : row.user_name, 
				 user_max_node : row.user_max_node,
				 user_max_core : row.user_max_core,
				 user_max_job : row.user_max_job,
				 acl_queue : row.acl_queue,
			 });
			 $('input[name="user_name"]').prev().validatebox({disabled:'disabled'});
		 },
		 onLoadSuccess : function(data){
			 $('table tbody').find('tr:first-child').click();
		 },
	 });//设置首页数据表格结束
});
