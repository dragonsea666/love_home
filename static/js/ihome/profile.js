function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$('#form-avatar').submit(function(e) {
    e.preventDefault();
    $(this).ajaxSubmit( {
        url:'/user/avatar/',
        type:'POST',
        dataType: 'json',
        success: function(data){
            if (data.code==200){
                $('#user-avatar').attr('src','/static/media/' + data.avatar)
            }
        }
     })
})

$('#form-name').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/user/name/',
        type:'POST',
        dataType:'json',
        success:function(data){
            if (data.code==200){
                showSuccessMsg()
            }else{
                $('.error-msg').css({'display':'block'})
            }
        }
    })
})
