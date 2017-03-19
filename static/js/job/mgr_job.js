$(function(){
	datagrid_resize('mgr_job_list');
	obj = {
		//选中删除
		job_remove : function () {
			var rows = $('#mgr_job_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要删除选中的作业吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].job_id);
											};//循环结束
											job_id = ids.join(',');
											$.messager.progress({
												title : '删除作业',
												msg : '正在删除中,请稍后...',
											});
											$.ajax({
												type:"post",
												url:"/job/del_job/",
												data:{job_id:job_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '作业删除失败', 'error');
														$.messager.progress('close');
														return
													}
													$.messager.alert('删除成功！', '作业删除成功', 'info');
													$.messager.progress('close');
													$('#mgr_job_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '作业删除失败', 'error');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要删除的作业', 'warning');
			}
		},	
		//挂起作业
		job_hold : function(){
			var rows = $('#mgr_job_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要挂起选中的作业吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].job_id);
											};//循环结束
											job_id = ids.join(',');
											$.messager.progress({
												title : '挂起作业',
												msg : '正在挂起中,请稍后...',
											});
											$.ajax({
												type:"post",
												url:"/job/hold_job/",
												data:{job_id:job_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '作业挂起失败', 'error');
														$.messager.progress('close');
														return
													}
													$.messager.alert('挂起成功！', '作业挂起成功', 'info');
													$.messager.progress('close');
													$('#mgr_job_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '作业挂起失败', 'error');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要挂起的作业', 'warning');
			}
		},	
		//终止作业
		job_stop : function(){
			var rows = $('#mgr_job_list').datagrid('getSelections');
			if (rows.length > 0) {
				$.messager.confirm('确定操作', '您确定要终止选中的作业吗？ ',
									function (flag) {
										if (flag) {
											var ids = [];
											for (var i = 0; i < rows.length; i ++) {
												ids.push(rows[i].job_id);
											};//循环结束
											job_id = ids.join(',');
											$.messager.progress({
												title : '终止作业',
												msg : '正在终止中,请稍后...',
											});
											$.ajax({
												type:"post",
												url:"/job/stop_job/",
												data:{job_id:job_id},
												success:function(arg){
													if(arg == 'failed'){
														$.messager.alert('错误！', '作业终止失败', 'error');
														$.messager.progress('close');
														return
													}
													$.messager.alert('终止成功！', '作业终止成功', 'info');
													$.messager.progress('close');
													$('#mgr_job_list').datagrid('reload');
												},
												error:function(arg){
													$.messager.alert('错误！', '作业终止失败', 'error');
													$.messager.progress('close');
												}
											});//ajax结束
										};//if结束
				});//messages.confirm结束
			} else {
				$.messager.alert('警告！', '请选择要终止的作业', 'warning');
			}
		},	
		//刷新
		job_reload : function(){
			$('#mgr_job_list').datagrid('reload');
		},
		//查询作业
		job_search : function(){
			 $('#mgr_job_list').datagrid('load',{
				 job_user_name : $.trim($('input[name="job_user_name"]').val()),
				 date_from : $.trim($('input[name="date_from"]').val()),
				 date_to : $.trim($('input[name="date_to"]').val()),
			 });
		},
		addSubTab : function(title,url,iconCls){
			var jq = top.jQuery; 
			console.log(jq('#default_tabs').tabs('tabs'));
			if (jq('#default_tabs').tabs('exists', title)){
				jq('#default_tabs').tabs('select', title);
				return
			} else {
				jq('#default_tabs').tabs('addIframeTab', {
					tab : {
						title : title,
						closable : true,
						state : 'open',
						iconCls : iconCls,
						fit:true,
					},
					iframe : {
						src : url,
						message : '数据正在加载中,请稍后...'
					},
					onLoadError:function(data){
			            // 这里对于非200状态码的都会加载不出来界面，而需要在这里手动处理
			            var tab = $('#default_tabs').tabs('getSelected');
			            var body = tab.panel('body');
			            if(data.status == 401){
			                body.html(data.responseText)
			            }else{
			                body.html('<h1>加载出错</h1>');
			            }
			        },
				});//addtabs结束
			};//判断tab是否存在结束				
		},//addSubTab结束
	};//obj结束
	//设置首页job数据表格
	 $('#mgr_job_list').datagrid({
		 width : 'auto',
		 url : '/job/get_job_list/',
		 columns : [[
		    {
				field : 'id',
				title : '编号',
				sortable : true,
				checkbox : true,
				width : 100,
			},
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
