//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
//    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
//    $(window).on('resize', centerModals);
//    $(".order-accept").on("click", function(){
//        var orderId = $(this).parents("li").attr("order-id");
//        console.log(orderId)
//        $(".modal-accept").attr("order-id", orderId);
//    });
//    $(".order-reject").on("click", function(){
//        var orderId = $(this).parents("li").attr("order-id");
//        $(".modal-reject").attr("order-id", orderId);
//    });
    $.ajax({
        url:'/order/myorder/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            for(var i=0;i<data.orders.length;i++){
                var order = '<li order-id=' + data.orders[i].order_id + '>'
                     order += '<div class="order-title">'
                     order += '<h3>订单编号：'+ data.orders[i].order_id + '</h3>'
                     order += '<div class="fr order-operate">'
                     order += '<button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal" id="accept' + i + '">接单</button>'
                     order += '<button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal" id="reject' + i + '">拒单</button>'
                     order += '</div>'
                     order += '</div>'
                     order += '<div class="order-content">'
                     order +=  '<img src="' + data.orders[i].image +  '" id="img' + i + '">'
                     order +=  '<div class="order-text">'
                     order += '<h3>' + data.orders[i].title + '</h3>'
                     order += '<ul>'
                     order += '<li>创建时间：' + data.orders[i].create_date + '</li>'
                     order += '<li>入住日期：' + data.orders[i].begin_date + '</li>'
                     order += '<li>离开日期：' + data.orders[i].end_date + '</li>'
                     order += '<li>合计金额：￥' + data.orders[i].amount + '(共'+ data.orders[i].days + '晚)</li>'
                     order += '<li>订单状态：'
                     order += '<span id="status' + i + '">' + data.orders[i].status + '</span>'
                     order += '</li>'
                     order += '<li>客户评价： 挺好的</li>'
                     order += '</ul>'
                     order += '</div>'
                     order += '</div>'
                     order += '</li>'
                     $('.orders-list').append(order)
                     if (parseInt(data.orders[i].house_id) > 700) {
                        $('#img'+i).attr('src','/static/media/'+data.orders[i].image)
                     }
                     var sta = $('#status'+i).text()
                    if (sta!='待接单'){
                        $('#accept'+i).css({'display':'none'})

                        $('#reject'+i).css({'display':'none'})
                    }
            }
            $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
            $(window).on('resize', centerModals);
            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");

                $(".modal-accept").attr("order-id", orderId);
                $('.modal-accept').on('click',function(){
                    $.ajax({
                        url:'/order/accept/',
                        type:'POST',
                        data:{'id':orderId},
                        dataType:'json',
                        success:function(data){
                            $('.modal-body p').text('接单成功')
                            location.href='/order/lorders/'
                        }
                    })
                })
            });

            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
                $('.modal-reject').on('click',function(){
                    var text = $('#reject-reason').val();
                    if (text){
                        $.ajax({
                            url:'/order/reject/',
                            type:'POST',
                            data:{'id':orderId,'text':text},
                            dataType:'json',
                            success:function(data){
                                if (data.code==200){
                                    location.href='/order/lorders/'
                                }
                            }
                        })
                    }
                })
            });
        }
    });


});