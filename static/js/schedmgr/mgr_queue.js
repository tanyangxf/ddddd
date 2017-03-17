$(function(){
	datagrid_resize('mgr_queue_list');
	obj = {
		create_queue : function(){
			$('#create_queue_form').form('reset');
			$('input[name="create_queue_name"').prev().removeAttr('disabled');
			
		},
		//选中删除
		remove_queue : function () {
			var rows = $('#mgr_queue_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的队列吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].queue_name);
											};//循环结束
											queue_name = ids.join(',');
											$.messager.progress({
												title : '删除队列',
												msg : '正在删除队列，请稍后...',
											}); 
											$.ajax({
												type:"post",
												url:"/schedmgr/del_queue/",
												data:{queue_name:queue_name},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '队列删除失败', 'error');
														$('#mgr_queue_list').datagrid('reload');
														$.messager.progress('close');
													}
													$.messager.alert('删除成功！', '队列删除成功', 'info');
													$('#mgr_queue_list').datagrid('reload');
													$.messager.progress('close');
												},
												error:function(arg){
													$.messager.alert('错误！', '队列删除失败', 'error');	
													$('#mgr_queue_list').datagrid('reload');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
				},'question');//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的队列', 'warning');
			}
		},		
		//刷新
		reload_queue : function(){
			$('#mgr_queue_list').datagrid('reload');
		},
		open_window : function (id) {
			$('#'+id).window('open');
		},
		close_window : function(id){
			$('#'+id).window('close');
		},
	};//obj结束
	//节点改变事件
	$('#create_acl_host_enable').combobox({
		onSelect:function(newVal,oldVal){
			if(newVal.value == '0'){
				$('button[name="node_button"]').removeAttr('disabled','true');
				$('input[name="create_acl_hosts"').prev().removeAttr('disabled');
			}else{
				$('button[name="node_button"]').attr('disabled','true');
				$('input[name="create_acl_hosts"').prev().validatebox({disabled:'disabled'});
			};
		}
	});
	//用户改变事件
	$('#create_acl_user_enable').combobox({
		onSelect:function(newVal,old){
			if(newVal.value == '0'){
				$('button[name="user_button"]').removeAttr('disabled','true');
				$('input[name="create_acl_users"').prev().removeAttr('disabled');
			}else{
				$('button[name="user_button"]').attr('disabled','true');
				$('input[name="create_acl_users"').prev().validatebox({disabled:'disabled'});
			};
		}
	});
	//用户创建表单
	$('#create_queue_form').form({
		url : '/schedmgr/create_queue/',
		onSubmit : function (param) {
			//提交之前取消输入框禁用
			$("input").prop("disabled",false);
			return $(this).form('validate');
			},
		success : function(data){
			$.messager.progress({
				title : '',
				msg : '正在处理中，请稍后...',
			}); 
			if(data=='ok'){
				$.messager.alert('成功！', '队列操作成功', 'info');
				$.messager.progress('close');
			}else{
				$.messager.alert('失败！', '队列操作失败', 'error');
				$.messager.progress('close');
			};	
			$.messager.progress('close');
			$('#create_queue_form').form('reset');
			$('input[name="create_queue_name"').prev().removeAttr('disabled');
			$('#mgr_queue_list').datagrid('reload');
		},
	});
	//设置首页用户数据表格
	 $('#mgr_queue_list').datagrid({
		 width : 'auto',
		 url : '/schedmgr/get_queue_list/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : false,
				checkbox : true,
				width : 100,
			},
			{
				 field : 'queue_name',
				 title : '队列名称',
				 sortable : false,
				 width : 100,   //百分比
			 },
			 {
				 field : 'queue_run_job',
				 title : '运行作业数',
				 sortable : false,
				 width : 100, 
				 formatter : function(value,row,index){
					 return row.queue_run_job
				 },
			 },
			 {
				 field : 'is_default',
				 title : '默认队列',
				 sortable : false,
				 width : 100, 
				 formatter : function(value,row,index){
					 if(row.is_default){
						 is_default = '是'
					 }else{
						 is_default = '否'
					 }
					 return is_default
				 },
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
		 toolbar : '#queue_button',
		 onClickRow : function(index, row){
			 //用户访问控制
			 if (row.acl_user_enable){
				 var acl_user_enable = '0';
				 $('button[name="user_button"]').removeAttr('disabled','true');
				 $('input[name="create_acl_users"').prev().removeAttr('disabled');
				 
			 }else{
				 var acl_user_enable = '1';
				 $('button[name="user_button"]').attr('disabled','true');
				 $('input[name="create_acl_users"').prev().validatebox({disabled:'disabled'});
			 };
			 //队列是否启用
			 if (row.queue_is_enable){
				 var queue_is_enable = '0';
			 }else{
				 var queue_is_enable = '1';
			 };
			 //是否默认队列
			 if (row.is_default){
				 var is_default = '0';
			 }else{
				 var is_default = '1';
			 };
			 //节点访问控制
			 if (row.acl_host_enable){
				 var acl_host_enable = '0';
				 $('button[name="node_button"]').removeAttr('disabled','true');
				 $('input[name="create_acl_hosts"').prev().removeAttr('disabled');
			 }else{
				 var acl_host_enable = '1';
				 $('button[name="node_button"]').attr('disabled','true');
				 $('input[name="create_acl_hosts"').prev().validatebox({disabled:'disabled'});
			 };
			 //队列优先级
			 if(row.Priority > 0){     
				 var Priority = 2;
			 }else if(row.Priority < 0){
				 var Priority = 0;
			 }else{
				 var Priority = 1;
			 };
			 //填充输入框
			 $('#create_queue_form').form('load',{
				 create_queue_name : row.queue_name, 
				 create_max_user_run : row.max_user_run,
				 create_max_run_time : row.walltime,
				 create_acl_hosts : row.acl_hosts,
				 create_acl_users : row.acl_users,
				 create_queue_max_run : row.queue_max_run,
				 create_acl_host_enable : acl_host_enable,
				 create_acl_user_enable : acl_user_enable,
				 create_queue_is_enable : queue_is_enable,
				 create_is_default : is_default,
				 create_queue_nice : Priority,
			 });
			 $('input[name="create_queue_name"]').prev().validatebox({disabled:'disabled'});
			 $('input[name="create_queue_name"]').prev().validatebox({required:true});
			 $('input[name="create_is_default"]').prev().validatebox({'readonly':true});
			 $('input[name="create_queue_nice"]').prev().validatebox({'readonly':true});
			 $('input[name="create_acl_host_enable"]').prev().validatebox({'readonly':true});
			 $('input[name="create_acl_user_enable"]').prev().validatebox({'readonly':true});
			 $('input[name="create_queue_is_enable"]').prev().validatebox({'readonly':true});
		 },
	 });//设置首页数据表格结束
	 $('input[name="create_is_default"]').prev().validatebox({'readonly':true});
	 $('input[name="create_queue_nice"]').prev().validatebox({'readonly':true});
	 $('input[name="create_acl_host_enable"]').prev().validatebox({'readonly':true});
	 $('input[name="create_acl_user_enable"]').prev().validatebox({'readonly':true});
	 $('input[name="create_queue_is_enable"]').prev().validatebox({'readonly':true});
});
