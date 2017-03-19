$(function(){
	//<!-- 生成cpu报表 -->
		$('#report_cpu a').click(function() {
			$.ajaxSetup({
			    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
			});
			var url = "/monitor/report_monitor_cpu"
			//window.open(url);
			window.location.href = url;
		});
	//<!-- 生成内存报表 -->
		$('#report_mem a').click(function() {
			$.ajaxSetup({
			    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
			});
			var url = "/monitor/report_monitor_mem"
			//window.open(url);
			window.location.href = url;
		});
	//<!-- 生成网络报表 -->
		$('#report_net a').click(function() {
			$.ajaxSetup({
			    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
			});
			var url = "/monitor/report_monitor_net"
			//window.open(url);
			window.location.href = url;
		});
	//<!-- 生成磁盘报表 -->
		$('#report_disk a').click(function() {
			$.ajaxSetup({
			    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
			});
			var url = "/monitor/report_monitor_disk"
			//window.open(url);
			window.location.href = url;
		});
});