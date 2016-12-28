$(function(){
	
	
	setSouthHeight();
	 /*
    var heightMargin = $("#job_button").height() + 60;
    var widthMargin = $(document.body).width() - $("#cluster_info").width();
    // 第一次加载时和当窗口大小发生变化时，自动变化大小
    $('#index_job_list').resizeDataGrid(heightMargin, widthMargin, 0, 0);
    $(window).resize(function () {
        $('#index_job_list').resizeDataGrid(heightMargin, widthMargin, 0, 0);
    });
    
    $.fn.extend({
        resizeDataGrid: function (heightMargin, widthMargin, minHeight, minWidth) {
            var height = $(document.body).height() - heightMargin;
            var width = $(document.body).width() - widthMargin;
            height = height < minHeight ? minHeight : height;
            width = width < minWidth ? minWidth : width;
            $(this).datagrid('resize', {
                height: height,
                width: width
            });
        }
    });
    */
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
		 url : '/job/get_job_list/',
		 columns : [[
			 {
				 field : 'job_id',
				 title : '作业ID',
				 sortable : true,
				 //resizeable : true, 
				 width : 100,   //百分比
			 },
			 {
				 field : 'job_name',
				 title : '作业名称',
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
				 field : 'job_user_name',
				 title : '用户名',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'job_queue',
				 title : '队列',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'job_start_time',
				 title : '创建时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'job_run_time',
				 title : '运行时间',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'job_status',
				 title : '运行状态',
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
		 toolbar : '#job_button',
		 //remoteSort : false,
	 });//设置首页job数据表格结束
});

function setSouthHeight(){
	var c = $('#cluster_info');
	var south = c.layout('panel','south');	
	var center = c.layout('panel','center');
	var newHeight = c.height() - center.panel('panel').outerHeight();
	south.panel('resize', {height:newHeight});
	c.layout('resize');
};
