$(function(){
	obj = {
		open_window : function (id,name) {
			$('#'+id).window('open');
			if(name){
				$('#'+id).children('iframe').attr('name',name);//iframe设置名字，dir_tree获取改名字确定何处调用
			};
		},
		close_window : function(id){
			$('#'+id).window('close');
		},
	};//obj结束
	$('#general_job_form').form({
		url : '/job/create_general_job/',
		success : function(data){
			if(data=='failed'){
				$.messager.alert('提交失败！', '作业提交失败', 'error');
			}else{
				$.messager.alert('提交成功！', data, 'info');
			};
			$('#general_job').window('close');
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
});