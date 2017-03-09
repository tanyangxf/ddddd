$(function(){
	obj = {
			open_window : function (id) {
				var folder_name = $('body').attr('id');
				if (folder_name!='content'){
					$('#'+id).window('open');
				}else{
					$.messager.alert('错误！', '请在左侧选择需要上传文件的目录', 'error');
				}
			},
			close_window : function(id){
				$('#'+id).window('close');
			},
		};
	//设置点击事件
	$('#mgr_file_info iframe',window.parent.document).contents().find('#container').on('click', '.jstree-anchor', function (e) {
		var folder_id = $(this).parent().attr('id'); 
		$('body').attr('id',folder_id);
	});	
	//设置首页用户数据表格
	$('#mgr_file_info iframe',window.parent.document).contents().find('#container').on('dblclick', '.jstree-anchor', function (e) {
		var folder_id = $(this).parent().attr('id'); 
		 $('#dir_content_nav').datagrid({
			 width : 'auto',
			 url : '/clusmgr/get_dir_content/',
			 queryParams : {folder_id:folder_id},
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
					 title : '名称',
					 sortable : false,
					 width : 100,   //百分比
					 formatter : function(value,row,index){
						 return row.name
					 },
				 },
				 {
					 field : 'size',
					 title : '大小',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.size + ' 字节'
					 },
				 },{
					 field : 'file_type',
					 title : '类型',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.file_type
					 },
				 },{
					 field : 'modify_time',
					 title : '修改时间',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.modify_time
					 },
				 },{
					 field : 'permission',
					 title : '权限',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.permission
					 },
				 },{
					 field : 'username',
					 title : '所属用户',
					 sortable : false,
					 width : 30, 
					 formatter : function(value,row,index){
						 return row.username
					 },
				 },{
					 field : 'group',
					 title : '所属用户组',
					 sortable : false,
					 width : 100, 
					 formatter : function(value,row,index){
						 return row.group
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
			 toolbar : '#mgr_file_button',
		 });//datagrid
	});//设置首页数据表格结束
});
