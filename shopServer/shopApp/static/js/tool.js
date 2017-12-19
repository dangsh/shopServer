function myPost(url, data, fn) {
	var last = url.indexOf("?") == -1 ? "/" : "";
	$.post("http://localhost:8000/" + url + last, data,
		function(data) {
			fn(data);
		}
	);

	
}

var HomeUrl = "http://localhost:8000/"

// 订单状态规则
var tool_order_status = ["待审核", "已审核", "待支付", "已支付", "代发货", "已发货", "已取消", "已完成"];

// 创建分页
function createPageNav(selec, totalPages, cbFn) {
	$(selec).twbsPagination({
		totalPages: totalPages,
		first: "首页",
		last: "尾页",
		prev: '上一页',
		next: '下一页',
		startPage: 1,
		visiblePages: totalPages > 5 ? 5 : totalPages , 
		version: '1.1',
		onPageClick: function(event, page) {
			cbFn(event, page)
		}
	});
}

function myPostGoodsManage(url, data, fn) {
	$.ajax({
		url: "http://localhost:8000/" + url + "/",
		type: 'POST',
		data: data,
		traditional: true,
		success: function(data) {
			fn(data);
		}
	});
}