$(function(){
	obj = {
			//选中终止
			process_stop : function () {
				var rows = $('#process_content_nav').datagrid('getSelections');
				host_name = $('body').attr('id')
				if (rows.length > 0) {
					$.messager.confirm('确定操作', '您确定终止选中的进程吗？ ',
										function (flag) {
											if (flag) {
												var ids = [];
												for (var i = 0; i < rows.length; i ++) {
													ids.push(rows[i].pid);
												};//循环结束
												pid = ids.join(',');
												$.ajax({
													type:"post",
													url:"/clusmgr/process_stop/",
													data:{pid:pid,host_name:host_name},
													success:function(arg){
														if(arg == 'failed'){
															$.messager.alert('错误！', '进程终止失败', 'error');
															return
														}
														$.messager.alert('删除成功！', '进程终止成功', 'info');
														$('#process_content_nav').datagrid('reload');
													},
													error:function(arg){
														$.messager.alert('错误！', '进程终止失败', 'error');
													}
												});//ajax结束
											};//if结束
					});//messages.confirm结束
				} else {
					$.messager.alert('警告！', '请选择需要终止的进程', 'warning');
				}
			},	
			//刷新
			process_reload : function(){
				$('#process_content_nav').datagrid('reload');
			},
		};
	//设置点击事件
	$('#node_process_info a').click(function(){
		var host_name = $(this).html();
		$('body').attr('id',host_name);
		//设置首页用户数据表格
		 $('#process_content_nav').datagrid({
			 width : 'auto',
			 url : '/clusmgr/mgr_process/',
			 queryParams : {host_name:host_name},
			 columns : [[
			    {
					field : 'id',
					title : '编号',
					sortable : false,
					checkbox : true,
					width : 100,
				},
				{
					 field : 'name',
					 title : '进程名',
					 sortable : false,
					 width : 100,   //百分比
					 formatter : function(value,row,index){
						 return row.name
					 },
				 },
				 {
					 field : 'pid',
					 title : '进程ID',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.pid
					 },
				 },{
					 field : 'cpu',
					 title : '进程CPU%',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.cpu
					 },
				 },{
					 field : 'mem',
					 title : '进程MEM%',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.mem
					 },
				 },{
					 field : 'time',
					 title : 'TIME',
					 sortable : false,
					 width : 30, 
					 formatter : function(value,row,index){
						 return row.time
					 },
				 },{
					 field : 'user',
					 title : '用户',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.user
					 },
				 },
			 ]],
			 pagination : false,
			 pageSize : 20,
			 pageList : [20, 25, 30, 35, 40],
			 nowrap : true,
			 singleSelect : false,
			 fit : true,
			 scrollbarSize : 0, 
			 fitColumns : true,
			 toolbar : '#mgr_process_button',
		 });//datagrid
	});//点击事件结束
});
