var SubaddTabs = function (options) {
	  var url = window.location.protocol + '//' + window.location.host;
	  options.url = url + options.url;
	  id = "tab_" + options.id;
	  $(".active",window.parent.document).removeClass("active");
	  //如果TAB不存在，创建一个新的TAB
	  if (!$("#" + id)[0],window.parent.document) {
	    //固定TAB中IFRAME高度
	    //mainHeight = $(document.body).height() - 90;
		//创建新TAB的title
	    title = '<li role="presentation" id="tab_' + id + '"><a href="#' + id + '" aria-controls="' + id + '" role="tab" data-toggle="tab">' + options.title;
	    //是否允许关闭
	    if (options.close) {
	      title += ' <i class="glyphicon glyphicon-remove" tabclose="' + id + '"></i>';
	    }
	    title += '</a></li>';
	    //是否指定TAB内容
	    if (options.content) {
	      content = '<div role="tabpanel" class="tab-pane" id="' + id + '">' + options.content + '</div>';
	    } else {//没有内容，使用IFRAME打开链接
	    	content = '<div role="tabpanel" class="tab-pane" id="' + id + '"><iframe src="' + options.url + '" width="105%" height="' + mainHeight +
	    	'" frameborder="no" border="0" marginwidth="0" allowfullscreen="" marginheight="0" scrolling="yes" allowtransparency="yes"></iframe></div>';	
	    }
	    //加入TABS
	    $(".nav-tabs",window.parent.document).append(title);
	    $(".tab-content",window.parent.document).append(content);
	  }
	  //激活TAB
	  $("#tab_" + id,window.parent.document).addClass('active');
	  $("#" + id,window.parent.document).addClass("active");
	};
	var closeTab = function (id) {
	  //如果关闭的是当前激活的TAB，激活他的前一个TAB
	  if ($("li.active",window.parent.document).attr('id') == "tab_" + id) {
	    $("#tab_" + id,window.parent.document).prev().addClass('active');
	    $("#" + id,window.parent.document).prev().addClass('active');
	  }
	  //关闭TAB
	  $("#tab_" + id,window.parent.document).remove();
	  $("#" + id,window.parent.document).remove();
	};
	$(function () {
	  mainHeight = $(window.parent.document.body).height() - 92;
		//mainHeight = $(document.body).height();
	  $('.main-left,.main-right',window.parent.document).height(mainHeight);
	  $("[addtabs]",window.parent.document).click(function () {
	    SubaddTabs({ id: $(this).attr("id"), title: $(this).attr('title'), close: true });
	  });

	  $(".nav-tabs",window.parent.document).on("click", "[tabclose]", function (e) {
	    id = $(this).attr("tabclose");
	    closeTab(id);
	  });
	});