$(function(){
	$('#report_job a').click(function() {
		$.ajaxSetup({
		    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
		});
		var url = "/job/report_job"
		//window.open(url);
		window.location.href = url;
	});
})