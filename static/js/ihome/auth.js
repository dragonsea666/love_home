function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$('#form-auth').submit(function(e){
    e.preventDefault();
     $(this).ajaxSubmit({
        url:'/user/auth/',
        type:'POST',
        dataType:'json',
        success:function(data){
            if (data.code == 200){
                showSuccessMsg()
                $('#info').css({'display':'block'})
                location.href='/user/auth/'+data.user_id+'/'
            }else{
                $('.error-msg').css({'display':'block'})
            }

        }

     })

})

