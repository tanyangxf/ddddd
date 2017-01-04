$(function(){
	obj = {
		create_share : function(){
			$('#create_share_form').form('reset');
			$('input[name="create_folder_name"').removeAttr('disabled','true');
			$('input[name="create_share_host"').removeAttr('disabled','true');
		},
		//选中删除
		share_remove : function () {
			var rows = $('#mgr_storage_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的共享吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].id);
											};//循环结束
											folder_id = ids.join(',');
											$.ajax({
												type:"post",
												url:"/sysmgr/del_share_storage/",
												data:{folder_id:folder_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '共享删除失败', 'error');
													}else{
														$.messager.alert('删除成功！', '共享删除成功', 'info');
													}
													$('#mgr_storage_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '共享删除失败', 'error');
												}
											});//ajax结束
											obj.create_share();
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的共享', 'warning');
			}
		},	
		//刷新
		share_reload : function(){
			$('#mgr_storage_list').datagrid('reload');
		},
	};//obj结束
	
	//用户创建表单
	$('#create_share_form').form({
		url : '/sysmgr/create_share_storage/',
		onSubmit : function (param) {
			//提交之前取消输入框禁用
			$("input").prop("disabled",false);
			return $(this).form('validate');
			},
		success : function(data){
			if(data=='ok'){
				$.messager.alert('创建成功！', '共享创建成功', 'info');
			}else{
				$.messager.alert('创建失败！', '共享创建失败', 'warning');
			};
			obj.create_share();
			$('#mgr_storage_list').datagrid('reload');
		},
	});
	//设置首页用户数据表格
	 $('#mgr_storage_list').datagrid({
		 width : 'auto',
		 url : '/sysmgr/get_storage_list/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : true,
				checkbox : true,
				width : 100,
			},
			{
				 field : 'folder_name',
				 title : '共享名称',
				 sortable : true,
				 //resizeable : true, 
				 width : 100,   //百分比
			 },
			 {
				 field : 'share_host',
				 title : '共享主机',
				 sortable : true,
				 //resizeable : true,
				 width : 100, 
				 /*
				 formatter : function(value,row,index){
					 return '[' + value + ']'
				 },
				 */
			 },
		 ]],
		 pagination : true,
		 pageSize : 20,
		 pageList : [20, 25, 30, 35, 40],
		 nowrap : true,
		 singleSelect : true,
		 fit : false,
		 scrollbarSize : 0, //滚动条宽度
		 //rownumbers : true,
		 fitColumns : true,
		 toolbar : '#storage_button',
		 //remoteSort : false,
		 queryParams : {},
		 onClickRow : function(index, row){
			 if (row.share_permission == 'rw'){
				 var share_permission = '0';
			 }else{
				 var share_permission = '1';
			 }; 
			 $('input[name="create_folder_name"]').val(row.folder_name);
			 $('input[name="create_share_host"]').val(row.share_host);
			 $('select[name="create_share_type"]').val(row.share_type);
			 $('input[name="create_share_parameter"]').val(row.share_parameter);
			 $('input[name="create_allow_ip"]').val(row.allow_ip)
			 $('select[name="create_share_permission"]').val(share_permission);
			 $('input[name="create_folder_name"').attr('disabled','true');
			 $('input[name="create_share_host"').attr('disabled','true');
		 },
	 });//设置首页数据表格结束
});
