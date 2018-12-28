function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    $.ajax({
        url:'/house/area/',
        type:'GET',
        dataType:'json',
        success:function(data){
            for (var i =0;i<data.area_dict.length;i++){
                var option = $('<option>').attr('value',data.area_dict[i].id).text(data.area_dict[i].name)
                $('#area-id').append(option)
            }
        }
    })

    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            type : 'POST',
            dataType:'json',
            success:function(data){
                $('#form-house-info').css({'display':'none'})
                $('#form-house-image').css({'display':'block'})
            }
        })
    })

    $('#form-house-image').submit(function(e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/image/',
            type:'POST',
            dataType:'json',
            success:function(data){
                if (data.code==200){
                    $('#image_success').empty();
                    var p = $('<p>').text('添加成功，可以继续添加上传图片').css({'display':'block','color':'red'})
                    var img = $('<img>').attr('src','/static/media/'+data.img).css({'width':200,'height':300})
                    $('#add_image').append(img)
                    $('#image_success').append(p)
                }else{

                    var p = $('<p>').text(data.msg).css({'display':'block'})
                    $('#image_success').append(p)
                }

            }
        })
    })
})