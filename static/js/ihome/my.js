function logout() {
    $.get("/user/logout/", function(data){
        if (data.code==200) {
            location.href = "/user/index/";
        }
    })
}

$(document).ready(function(){
})