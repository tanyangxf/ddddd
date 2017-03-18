$(function(){
	obj = {
		open_window : function (id,name) {
			$('#'+id).window('open');
			if(name && id=='open_workdir'){
				$('#'+id).children('iframe').attr('src','/clusmgr/dir_tree/')
				$('#'+id).children('iframe').attr('name',name);//iframe设置名字，dir_tree获取改名字确定何处调用
			}else if(name && id=='open_jobscript'){
				$('#'+id).children('iframe').attr('src','/clusmgr/file_tree/')
				$('#'+id).children('iframe').attr('name',name);//iframe设置名字，file_tree获取改名字确定何处调用
			};
		},
		close_window : function(id){
			$('#'+id).children('iframe').removeAttr('src');
			$('#'+id).window('close');
		},
	};//obj结束
	$('#general_job_form').form({
		url : '/job/create_general_job/',
		onSubmit  : function(para){
			$.messager.progress({
				title : '提交作业',
				msg : '正在提交作业,请稍后...',
			});
		},
		success : function(data){
			if(data=='failed'){
				$.messager.alert('提交失败！', '作业提交失败', 'error');
				$.messager.progress('close');
			}else{
				$.messager.alert('提交成功！', data, 'info');
				$.messager.progress('close');
			};
			$('#general_job').window('close');
			$.messager.progress('close');
		},
	});
	/*
	$('#general_job_form1').form({
		//url : '/job/create_job/',
		success : function(data){
			alert(data);
			//$('#general_job1').window('close');
		},
	});
	*/
	$('input[name="general_queue_name"').prev().validatebox({'readonly':true});
});