$(function(){
	datagrid_resize('mgr_user_list')
	obj = {
		open_window : function (id) {
			$('#'+id).window('open');
		},
		close_window : function(id){
			$('#'+id).window('close');
		},
		create_user_set : function(){
			$('input[name="create_user_type"]').val('普通用户');
			$('input[name="create_user_type"]').attr('disabled','true');
		},
		//选中删除
		user_remove : function () {
			var rows = $('#mgr_user_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的用户吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].user_name);
											};//循环结束
											user_name = ids.join(',');
											$.ajax({
												type:"post",
												url:"/sysmgr/del_user/",
												data:{user_name:user_name},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '用户删除失败', 'error');
													}else{
														$.messager.alert('删除成功！', '用户删除成功', 'info');
													}
													$('#mgr_user_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '用户删除失败', 'error');
												}
											});//ajax结束
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的用户', 'warning');
			}
		},	
		//选中修改
		user_modify : function () {
			var rows = $('#mgr_user_list').datagrid('getSelections');
			if (rows.length == 1) {
				//填充输入框
				 $('#modify_user_form').form('load',{
					 modify_user_name : rows[0].user_name, 
					 modify_user_password : 'nochange',
					 modify_user_home : rows[0].user_home,
					 modify_user_group : rows[0].user_group,
					 modify_other_group : rows[0].other_group,
					 modify_user_type : rows[0].user_type,
					 modify_user_mail : rows[0].user_mail,
					 modify_user_tel : rows[0].user_tel,
					 modify_user_comment : rows[0].user_comment,
					 modify_is_login : rows[0].is_login,
				 });
				//禁用某些属性
				$('input[name="modify_user_name"]').prev().validatebox({disabled:'disabled'});
				$('input[name="modify_user_home"]').prev().validatebox({disabled:'disabled'});
				$('input[name="modify_user_type"]').prev().validatebox({disabled:'disabled'});
				$('input[name="modify_is_login"]').prev().validatebox({'readonly':true});
				$('#modify_user').window('open');
				//用户修改表单
				$('#modify_user_form').form({
					url : '/sysmgr/modify_user/',
					onSubmit: function(param){
						//disabled被禁用，提交额外参数
						param.userid = rows[0].userid;
						param.modify_user_name = rows[0].user_name;
						param.modify_user_home = rows[0].user_home;
						param.modify_user_type = rows[0].user_type;
						},
					success : function(data){
						if(data == 'failed'){
							$.messager.alert('错误！', '用户修改失败', 'error');
						}else{
							$.messager.alert('修改成功！', '用户修改成功', 'info');
						};
						$('input[name="modify_user_name"').prev().removeAttr('disabled');
						$('input[name="modify_user_home"').prev().removeAttr('disabled');
						$('input[name="modify_user_type"').prev().removeAttr('disabled');
						$('#modify_user').window('close');
						$('#mgr_user_list').datagrid('reload');
					},
				});
			}else if(rows.length>1 ){
				$.messager.alert('警告！', '修改时需要或只能选择一行！', 'warning');
			}else{
				$.messager.alert('警告！', '请选择要修改的用户！', 'warning');
			}
		},	
		//刷新
		user_reload : function(){
			$('#mgr_user_list').datagrid('reload');
		},
		//查询作业
		user_search : function(){
			 $('#mgr_user_list').datagrid('load',{
				 search_user_name : $.trim($('input[name="search_user_name"]').val()),
			 });
		},
	};//obj结束
	
	//用户创建表单
	$('#create_user_form').form({
		url : '/sysmgr/create_user/',
		onSubmit : function (param) {
			return $(this).form('validate');
			},
		success : function(data){
			if(data=='ok'){
				$.messager.alert('创建成功！', '用户创建成功', 'info');
			}else{
				$.messager.alert('创建失败！', '用户创建失败', 'warning');
			};
			$('#create_user').window('close');
			$('#mgr_user_list').datagrid('reload');
		},
	});
	//设置首页用户数据表格
	 $('#mgr_user_list').datagrid({
		 width : 'auto',
		 url : '/sysmgr/get_user_list/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : true,
				checkbox : true,
				width : 100,
			},
			{
				 field : 'user_name',
				 title : '用户名',
				 sortable : true,
				 //resizeable : true, 
				 width : 100,   //百分比
			 },
			 {
				 field : 'userid',
				 title : '用户ID',
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
				 field : 'user_group',
				 title : '主要组',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'other_group',
				 title : '附加组',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'user_home',
				 title : '用户主目录',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'user_type',
				 title : '用户类型',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'user_mail',
				 title : '用户邮件',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'user_tel',
				 title : '用户电话',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'user_comment',
				 title : '用户描述',
				 sortable : true,
				 //resizeable : false,
				 width : 100, 
			 },
			 {
				 field : 'is_login',
				 title : '能否登录',
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
		 toolbar : '#user_button',
		 //remoteSort : false,
	 });//设置首页数据表格结束
	 $('input[name="create_user_is_login"]').prev().validatebox({'readonly':true});
});
