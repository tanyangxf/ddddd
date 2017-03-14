$(function(){
	datagrid_resize('monitor_alarm_list');
	obj = {
		//选中删除
		alarm_remove : function () {
			var rows = $('#monitor_alarm_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的告警吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].id);
											};//循环结束
											alarm_id = ids.join(',');
											$.ajax({
												type:"post",
												url:"/monitor/del_alarm/",
												data:{alarm_id:alarm_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '告警删除失败', 'error');
														return
													}
													$.messager.alert('删除成功！', '告警删除成功', 'info');
													$('#monitor_alarm_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '告警删除失败', 'error');
												}
											});//ajax结束
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的告警', 'warning');
			}
		},	
		//刷新
		alarm_reload : function(){
			$('#monitor_alarm_list').datagrid('reload');
		},
		//查询作业
		alarm_search : function(){
			 $('#monitor_alarm_list').datagrid('load',{
				 host_name : $.trim($('input[name="host_name"]').val()),
				 date_from : $.trim($('input[name="date_from"]').val()),
				 date_to : $.trim($('input[name="date_to"]').val()),
			 });
		},
	};//obj结束
	//设置首页job数据表格
	 $('#monitor_alarm_list').datagrid({
		 width : 'auto',
		 url : '/monitor/get_monitor_alarm/',
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
				 field : 'alarm_name',
				 title : '告警名称',
				 sortable : true,
				 //resizeable : true,
				 width : 100, 
			 },
			 {
				 field : 'alarm_level',
				 title : '告警级别',
				 sortable : true,
				 width : 100, 
			 },
			 {
				 field : 'alarm_detail',
				 title : '告警描述',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'c_time',
				 title : '告警时间',
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
		 toolbar : '#monitor_alarm_button',
		 //remoteSort : false,
	 });//设置首页job数据表格结束
});
