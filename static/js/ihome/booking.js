function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);

            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });
    var url = window.location.search
    var id = url.split('=')
    id = id[1]
    $.ajax({
        url:'/order/book_house/',
        type:'GET',
        dataType:'json',
        data:{'house_id':id},
        success:function(data){
            if (data.code==200){
                if (data.hou_info.id > 700){
                    $('.house-info img').attr('src','/static/media/' + data.hou_info.image)
                }else{
                    $('.house-info img').attr('src',data.hou_info.image)
                }
                $('.house-text h3').text(data.hou_info.title)
                $('.house-text p span').text(data.hou_info.price)
                $('.house-text').attr('id',data.hou_info.id)
                if (data.hou_info.user_id==data.hou_info.house_user_id){
                    $('.submit-btn').css({'display':'none'})
                }

            }
        }
    })

    $('.submit-btn').on('click',function(){
        var money = $('.order-amount span').text()
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        var sd = new Date(startDate);
        var ed = new Date(endDate);
        days = (ed - sd)/(1000*3600*24) + 1;
        money = money.split('(')[0]
        $.ajax({
            url:'/order/deal/',
            type:'POST',
            dataType:'json',
            data:{'house_id':id,'money':money,'start_date':startDate,'end_date':endDate,'days':days},
            success:function(data){
                if (data.code==200){
                    location.href='/order/orders/'
                }
            }
        })
    })
})
