function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    })
    $(".book-house").show();
    var url = window.location.href;
    var id = url.split('/')
    var id = id[id.length-2]
    console.log(url,id)
    $.ajax({
        url:'/house/detail_info/',
        type:'GET',
        data:{'house_id':id},
        dataType:'json',
        success:function(data){
            if (data.code==200){
                $('.house-price span').text(data.house_info.price)
                $('.detail-header .house-title').text(data.house_info.title)
                if (data.house_info.id > 700) {
                    $('.landlord-pic img').attr('src','/static/media/'+ data.house_info.user_avatar)
                }else{
                    $('.landlord-pic img').attr('src',data.house_info.user_avatar)
                };
                $('.landlord-pic img').attr('src','/static/media/'+ data.house_info.user_avatar)
                $('.landlord-name span').text(data.house_info.user_name)
                $('.text-center li').text(data.house_info.address)
                $('#room_num').text('出租'+ data.house_info.room_count + '间')
                $('#area').text('房屋面积:' + data.house_info.acreage + '平米')
                $('#huxing').text('房屋户型:' + data.house_info.unit)
                $('#people').text('宜住' + data.house_info.capacity + '人')
                $('#bed p').text(data.house_info.beds)
                $('#money span').text(data.house_info.deposit)
                $('#min span').text(data.house_info.min_days)
                if (data.house_info.max_days == 0){
                    $('#max span').text('无限制')
                }else{$('#max span').text(data.house_info.max_days)}
                for (var i=0;i<data.house_info.facilities.length;i++){
                    var span = $('<span>').attr('class',data.house_info.facilities[i].css)
                    var li = $('<li>').text(data.house_info.facilities[i].name)
                    li.append(span)
                    $('.clearfix').append(li)
                }
                $('.book-house').attr('href','/order/booking/?house_id=' + data.house_info.id)
                if (data.house_info.user_id==data.house_info.house_user_id){
                    $('.book-house').css({'display':'none'})
                }
            }

        }
    })


})

