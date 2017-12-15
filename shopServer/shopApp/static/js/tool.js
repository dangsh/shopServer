function myPost(url , data , fn){
    $.post("http://localhost:8000/" + url + "/", data ,
        function(data){
            fn(data);
        });
}

