function myPost(url , data , fn){
    $.post("http://localhost:8000/" + url + "/", data ,
        function(data){
            fn(data);
        });
}



function myPostGoodsManage(url , data , fn){
    $.ajax({
        url: "http://localhost:8000/" + url + "/",
        type: 'POST',
        data:data,
        traditional:true,
        success: function (data) {
            fn(data);
        }
    });
}
