$(function(){
	obj = {
		//刷新
		reload_node_sched : function(){
			$('#node_sched_list').datagrid('reload');
		},
		//服务管理
		mgr_node_sched : function (oper_type) {
			var rows = $('#node_sched_list').datagrid('getSelections');
			switch(oper_type){
			case 'start':
				var oper_msg = '启动';
				break;
			case 'stop':
				var oper_msg = '停止';
				break;
			case 'restart':
				var oper_msg = '重新启动';
				break;
			};
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要' + oper_msg + '选中的服务吗？',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].host_name);
											};//循环结束
											host_name = ids.join(',');
											$.messager.progress({
												title : '服务',
												msg : '请稍后...',
											}); 
											$.messager.progress({
												title : oper_msg + '服务',
												msg : '正在'+ oper_msg + '服务,' + '请稍后...',
											}); 
											$.ajax({
												type:"post",
												url:"/schedmgr/mgr_node_sched/",
												data:{oper_type:oper_type,host_name:host_name},
												success:function(arg){
													$.messager.alert('操作结果！', arg, 'info');
													$('#node_sched_list').datagrid('reload');
													$.messager.progress('close');
												},
												error:function(arg){
													$('#node_sched_list').datagrid('reload');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
										
				},'question');//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要' + oper_msg + '服务的节点', 'warning');
			}
		},	
	};//obj结束
	//设置首页用户数据表格
	 $('#node_sched_list').datagrid({
		 width : 'auto',
		 url : '/schedmgr/get_node_sched/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : false,
				checkbox : true,
				width : 30,
			},{
				 field : 'host_name',
				 title : '节点名称',
				 sortable : false,
				 width : 30,   //百分比
			 },{
				 field : 'node_stats',
				 title : '节点状态',
				 sortable : false,
				 width : 30, 
			 },{
				 field : 'node_jobs',
				 title : '运行作业ID',
				 sortable : false,
				 width : 100, 
			 },{
				 field : 'config_ncpus',
				 title : 'CPU个数',
				 sortable : false,
				 width : 30, 
			 },{
				 field : 'mem_total',
				 title : '总内存(MB)',
				 sortable : false,
				 width : 30, 
			 },{
				 field : 'mem_percent',
				 title : '内存使用百分比(%)',
				 sortable : false,
				 width : 30, 
			 },{
				 field : 'node_load',
				 title : '平均负载',
				 sortable : false,
				 width : 30, 
				 formatter : function(value,row,index){
					 return row.node_load
				 },
			 },
		 ]],
		 nowrap : true,
		 pagination : true,
		 pageSize : 20,
		 pageList : [20, 25, 30, 35, 40],
		 singleSelect : false,
		 fit : false,
		 scrollbarSize : 0, 
		 fitColumns : true,
		 toolbar : '#node_sched_button',
	 });//设置首页数据表格结束
});
