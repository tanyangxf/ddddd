$(function(){
	obj = {
			open_window : function (id) {
				$('#'+id).window({
					loadingMessage : 'loading....',
				});
				var folder_name = $('body').attr('id');
				if (folder_name!='content'){
					$('#'+id).children('iframe').attr('src','/clusmgr/file_upload_index/');
					$('#'+id).window('open');
				}else{
					$.messager.alert('错误！', '请在左侧选择需要上传文件的目录', 'error');
				};
			},
			close_window : function(id){
				$('#'+id).children('iframe').removeAttr('src');
				$('#'+id).window('close');
			},
			file_download : function(){
				var rows = $('#dir_content_nav').datagrid('getSelections');
				if(rows.length>0){
					if (rows[0].name != '没有任何文件或者文件夹!'){
						if (rows[0].file_type == '文件夹'){
							$.messager.alert('警告！', '不能下载文件夹，请选择文件', 'warning');
						}else{
							var ids = [];
							var folder_name = $('body').attr('id');
							file_name = rows[0].name;
							url = '/clusmgr/file_download/?file_name=' + file_name + '&'+ 'folder_name=' + folder_name 
							console.log(url)
							location.href = url;
						}//内嵌if结束
					}else{
						$.messager.alert('警告！', '请在下方选择需要下载的文件', 'warning');
					}
				}else {
					$.messager.alert('警告！', '请在下方选择需要下载的文件', 'warning');
				}
			},
			file_delete : function(){
				var rows = $('#dir_content_nav').datagrid('getSelections');
				if (rows.length >0){
					if(rows[0].name != '没有任何文件或者文件夹!') {
						$.messager.confirm('确定操作', '您确定要删除选中的文件吗？ ',
							function (flag) {
								if (flag) {
									var ids = [];
									var folder_name = $('body').attr('id');
									for (var i = 0; i < rows.length; i ++) {
										ids.push(rows[i].name);
									};//循环结束
									file_name = ids.join(',');
									$.messager.progress({
										title : '删除文件',
										msg : '正在删除中,请稍后...',
									});
									$.ajax({
										type:"post",
										url:"/clusmgr/file_delete/",
										data:{folder_name:folder_name,file_name:file_name},
										success:function(arg){
											if(arg == 'failed'){
												$.messager.alert('错误！', '删除失败', 'error');
												$.messager.progress('close');
												return
											}
											$.messager.alert('删除成功！', '删除成功', 'info');
											$.messager.progress('close');
											$('#dir_content_nav').datagrid('reload');
										},
										error:function(arg){
											$.messager.alert('错误！', '删除失败', 'error');
											$.messager.progress('close');
										}
									});//ajax结束
								};//if结束
							});//messages.confirm结束
					}else{
						$.messager.alert('警告！', '请在下方选择要删除的文件或文件夹', 'warning');
					};//
				}else {
					$.messager.alert('警告！', '请在下方选择要删除的文件或文件夹', 'warning');
				}
			},
			file_reload : function(){
				$('#dir_content_nav').datagrid('reload');
			},
		};//obj结束
	//设置点击事件
	$('#mgr_file_info iframe',window.parent.document).contents().find('#container').on('click', '.jstree-anchor', function (e) {
		var folder_id = $(this).parent().attr('id'); 
		$('body').attr('id',folder_id);
	});	
	//设置首页用户数据表格
	$('#mgr_file_info iframe',window.parent.document).contents().find('#container').on('click', '.jstree-anchor', function (e) {
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
						 if(row.lenght>0){
							 return row.size + ' 字节';
						 };
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
			 singleSelect : true,
			 fit : true,
			 scrollbarSize : 0, 
			 fitColumns : true,
			 toolbar : '#mgr_file_button',
		 });//datagrid
	});//设置首页数据表格结束
});
