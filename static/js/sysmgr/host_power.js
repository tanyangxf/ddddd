$(function(){
	datagrid_resize('host_power_list');
	obj = {
		//选中删除
		power_mgr : function (power_change) {
			var rows = $('#host_power_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要操作选中主机的电源吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].host_name);
											};//循环结束
											var host_name = ids.join(',');
											if (power_change == 'soft_shut'){
												var msg_tip = '软关机';
											}else if (power_change == 'soft_reboot'){
												var msg_tip = '软重启';
											}else if (power_change == 'hard_shut'){
												var msg_tip = '硬关机';
											}else if (power_change == 'hard_reboot'){
												var msg_tip = '硬重启';
											};
											$.messager.progress({
												title : msg_tip,
												msg : '主机正在'+ msg_tip + '中，请稍后...',
											}); 
											$.ajax({
												type:"post",
												url:"/sysmgr/host_power_mgr/",
												async:true,
												data:{host_name:host_name,power_change:power_change},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '主机' + msg_tip + '操作失败', 'error');
														$('#mgr_storage_list').datagrid('reload');
														$.messager.progress('close');
													}else{
														$.messager.alert('操作成功！', '主机' + msg_tip + '操作成功', 'info');
														$('#mgr_storage_list').datagrid('reload');
														$.messager.progress('close');
													}
												},
												error:function(arg){
													$.messager.alert('错误！', '主机' + msg_tip + '操作失败', 'error');
													$('#mgr_storage_list').datagrid('reload');
													$.messager.progress('close');
												},
											});//ajax结束
										};//if结束
				},'question');//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要操作的主机', 'warning');
			}
		},	
		//刷新
		power_reload : function(){
			$('#host_power_list').datagrid('reload');
		},
	};//obj结束

	//设置首页用户数据表格
	 $('#host_power_list').datagrid({
		 width : 'auto',
		 url : '/sysmgr/get_host_power/',
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
				 width : 100, 
			 },
			 {
				 field : 'host_ipmi',
				 title : '主机IPMI地址',
				 sortable : true,
				 width : 100, 
			 },
			 {
				 field : 'power_status',
				 title : '主机电源状态',
				 sortable : false,
				 width : 100, 
				 formatter : function(value,row,index){
					return row.power_status
				 },
			 },
		 ]],
		 pagination : true,
		 pageSize : 20,
		 pageList : [20, 25, 30, 35, 40],
		 nowrap : true,
		 fit : false,
		 scrollbarSize : 0, //滚动条宽度
		 //rownumbers : true,
		 fitColumns : true,
		 toolbar : '#power_button',
	 });//设置首页数据表格结束
});
