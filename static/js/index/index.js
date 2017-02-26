$(function(){
	window.onresize = function(){
		//重新计算图高度
		setTimeout(function(){
			myChart_node.resize();
			myChart_cpu.resize();
			myChart_queue.resize();
		},100);
	};
	//自适应表格大小
	datagrid_resize('index_job_list');
	obj = {
		job_search : function(){
			 $('#index_job_list').datagrid('load',{
				 job_user_name : $.trim($('input[name="job_user_name"]').val()),
				 date_from : $.trim($('input[name="date_from"]').val()),
				 date_to : $.trim($('input[name="date_to"]').val()),
			 });
		},
	};
	//设置首页job数据表格
	 $('#index_job_list').datagrid({
		 width : 'auto', 
		 height : 'auto',
		 url : '/job/get_job_list/',
		 columns : [[
			 {
				 field : 'job_id',
				 title : '作业ID',
				 sortable : true,
				 width : 100
				 //resizeable : true, 
			 },
			 {
				 field : 'job_name',
				 title : '作业名称',
				 sortable : true,
				 width : 100
				 //resizeable : true,
				 /*
				 formatter : function(value,row,index){
					 return '[' + value + ']'
				 },
				 */
			 },
			 {
				 field : 'job_user_name',
				 title : '用户名',
				 sortable : true,
				 //resizeable : false,
				 width : 100
			 },
			 {
				 field : 'job_queue',
				 title : '队列',
				 sortable : true,
				 //resizeable : false,
				 width : 100
			 },
			 {
				 field : 'job_start_time',
				 title : '创建时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100
			 },
			 {
				 field : 'job_run_time',
				 title : '运行时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100
			 },
			 {
				 field : 'job_status',
				 title : '运行状态',
				 sortable : true,
				 //resizeable : false,
				 width : 100
			 },
		 ]],
		 pagination : true,
		 pageSize : 10,
		 pageList : [10, 15, 20, 25, 30],
		 nowrap : false,
		 fit : false,
		 scrollbarSize : 0, //滚动条宽度
		 //rownumbers : true,
		 fitColumns : true,
		 toolbar : '#job_button',
		 //remoteSort : false,
	 });//设置首页job数据表格结束

});


