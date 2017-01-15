$(function(){
	obj = {
		//刷新
		reload_sched : function(){
			$('#mgr_sched_list').datagrid('reload');
		},
		//服务管理
		mgr_sched : function (oper_type) {
			var rows = $('#mgr_sched_list').datagrid('getSelections');
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
												ids.push(rows[i].service_process);
											};//循环结束
											service_process = ids[0];
											$.messager.progress({
												title : oper_msg + '服务',
												msg : '正在'+ oper_msg + '服务,' + '请稍后...',
											}); 
											$.ajax({
												type:"post",
												url:"/schedmgr/mgr_sched_service/",
												data:{oper_type:oper_type,service_process:service_process},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '服务' + oper_msg +'失败', 'error');
														$('#mgr_sched_list').datagrid('reload');
														$.messager.progress('close');
													}
													$.messager.alert('成功！', '服务' + oper_msg +'成功', 'info');
													$('#mgr_sched_list').datagrid('reload');
													$.messager.progress('close');
												},
												error:function(arg){
													$.messager.alert('错误！', '服务'+ oper_msg + '失败', 'error');
													$('#mgr_sched_list').datagrid('reload');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
										
				},'question');//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要' + oper_msg + '的服务', 'warning');
			}
		},	
	};//obj结束
	//设置首页用户数据表格
	 $('#mgr_sched_list').datagrid({
		 width : 'auto',
		 url : '/schedmgr/get_sched_service/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : false,
				checkbox : true,
				width : 30,
			},
			{
				 field : 'service_name',
				 title : '服务名称',
				 sortable : false,
				 width : 30,   //百分比
				 formatter : function(value,row,index){
					 var service_name = '未知服务名';
					 switch(row.service_name)
					 {
					 case 'pbs_server':
						 var service_name = '主服务';
						 break;
					 case 'pbs_mom':
						 var service_name = '计算服务';
						 break;
					 case 'maui':
						 var service_name = '调度服务';
						 break;
					 };
					 return service_name
				 },
			 },
			 {
				 field : 'service_type',
				 title : '服务类型',
				 sortable : false,
				 width : 30, 
			 },{
				 field : 'service_process',
				 title : '服务进程',
				 sortable : false,
				 width : 100, 
			 },{
				 field : 'servcie_status',
				 title : '服务状态',
				 sortable : false,
				 width : 30, 
				 formatter : function(value,row,index){
					 return row.servcie_status
				 },
			 },{
				 field : 'service_process_num',
				 title : '进程号',
				 sortable : false,
				 width : 30, 
				 formatter : function(value,row,index){
					 return row.service_process_num
				 },
			 },
			 {
				 field : 'service_info',
				 title : '备注信息',
				 sortable : false,
				 width : 30, 
				 formatter : function(value,row,index){
					 return row.service_info
				 },
			 },
		 ]],
		 nowrap : true,
		 singleSelect : true,
		 fit : false,
		 scrollbarSize : 0, 
		 fitColumns : true,
		 toolbar : '#sched_button',
	 });//设置首页数据表格结束
});
