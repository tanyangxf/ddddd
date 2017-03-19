$(function(){
	datagrid_resize('mgr_host_list');
	obj = {
		open_window : function (id) {
			$('#'+id).window('open');
		},
		close_window : function(id){
			$('#'+id).window('close');
		},
		//选中删除
		host_remove : function () {
			var rows = $('#mgr_host_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的主机吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].host_id);
											};//循环结束
											host_id = ids.join(',');
											$.messager.progress({
												title : '删除主机',
												msg : '主机正在删除中，请稍后...'
											}); 
											$.ajax({
												type:"post",
												url:"/sysmgr/del_host/",
												data:{host_id:host_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '主机删除失败', 'error');
														$('#mgr_host_list').datagrid('reload');
														$.messager.progress('close');
													}
													$.messager.alert('删除成功！', '主机删除成功', 'info');
													$('#mgr_host_list').datagrid('reload');
													$.messager.progress('close');
												},
												error:function(arg){
													$.messager.alert('错误！', '主机删除失败', 'error');
													$('#mgr_host_list').datagrid('reload');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
										
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的主机', 'warning');
			}
		},	
		//选中修改
		host_modify : function () {
			var rows = $('#mgr_host_list').datagrid('getSelections');
			if (rows.length == 1) {
				//填充输入框
				 $('#modify_host_form').form('load',{
					 modify_host_name : rows[0].host_name, 
					 modify_host_ip : rows[0].host_ip,
					 modify_host_ipmi : rows[0].host_ipmi,
					 modify_host_os : rows[0].host_os,
				 });
				 $('input[name="modify_host_name"]').prev().validatebox({disabled:'disabled'});
				 $('input[name="modify_host_os"]').prev().validatebox({'readonly':true});
				obj.open_window('modify_host');
				$('#modify_host_form').form({
					url : '/sysmgr/modify_host/',
					onSubmit: function(param){
						param.host_id = rows[0].host_id;
						},
					success : function(data){
						if(data=='ok'){
							$.messager.alert('修改成功！', '主机修改成功', 'info');
						}else{
							$.messager.alert('修改失败！', '主机修改失败', 'error');
						};
						$('input[name="modify_host_name"').prev().removeAttr('disabled');
						$('#modify_host').window('close');
						$('#mgr_host_list').datagrid('reload');
					},
				});
			} else if(rows.length > 1){
				$.messager.alert('警告！', '修改时需要或只能选择一行！', 'warning');
			}else{
				$.messager.alert('警告！', '请选择要修改的主机！', 'warning');
			}
		},	
		//刷新
		host_reload : function(){
			$('#mgr_host_list').datagrid('reload');
		},
		//查询作业
		host_search : function(){
			 $('#mgr_host_list').datagrid('load',{
				 host_name : $.trim($('input[name="host_name"]').val()),
				 date_from : $.trim($('input[name="date_from"]').val()),
				 date_to : $.trim($('input[name="date_to"]').val()),
			 });
		},
	};//obj结束
	//主机创建表单
	$('#create_host_form').form({
		url : '/sysmgr/create_host/',
		success : function(data){
			if(data=='ok'){
				$.messager.alert('创建成功！', '主机创建成功', 'info');
			}else{
				$.messager.alert('创建失败！', '主机创建失败', 'warning');
			};
			$('#create_host').window('close');
			$('#mgr_host_list').datagrid('reload');
		},
	});
	//设置首页job数据表格
	 $('#mgr_host_list').datagrid({
		 width : 'auto',
		 url : '/sysmgr/get_host_list/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : true,
				checkbox : true,
				width : 100,
			},
			{
				 field : 'host_name',
				 title : '主机名',
				 sortable : true,
				 //resizeable : true, 
				 width : 100,   //百分比
			 },
			 {
				 field : 'host_ip',
				 title : '主机IP地址',
				 sortable : true,
				 //resizeable : true,
				 width : 100, 
				 /*
				 formatter : function(value,row,index){
					 return '[' + value + ']'
				 },
				 */
			 },
			 {
				 field : 'host_ipmi',
				 title : '主机IPMI地址',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'host_os',
				 title : '主机操作系统',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'curr_datetime',
				 title : '创建时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'change_datetime',
				 title : '修改时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
		 ]],
		 pagination : true,
		 pageSize : 10,
		 pageList : [10, 15, 20, 25, 30],
		 nowrap : true,
		 fit : false,
		 scrollbarSize : 0, //滚动条宽度
		 //rownumbers : true,
		 fitColumns : true,
		 toolbar : '#host_button',
		 //remoteSort : false,
	 });//设置首页job数据表格结束
	 $('input[name="create_host_os"]').prev().validatebox({'readonly':true});
});
