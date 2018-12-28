import re

from flask import Blueprint, request, render_template, session, url_for, redirect, g, jsonify,make_response
from datetime import datetime
from app.models import User, Order, House
from utils import status_code

blueprint = Blueprint('order',__name__)

@blueprint.route('/orders/',methods=['GET','POST'])
def orders():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        order = Order.query.filter(Order.user_id==user_id).all()
        return render_template('orders.html',user=user,order=order)

@blueprint.route('/booking/',methods=['GET','POST'])
def booking():
    if request.method == 'GET':

        return render_template('booking.html')


@blueprint.route('/book_house/')
def book_house():
    user_id = session.get('user_id')
    house_id = request.args.get('house_id')
    try:
        house = House.query.get(house_id)
        hou_info = house.to_dict()
        hou_info['user_id'] = user_id
    except:
        hou_info = {}
    return jsonify({'code':200,'msg':'请求成功','hou_info':hou_info})


@blueprint.route('/lorders/',methods=['GET','POST'])
def lorders():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:
            return render_template('lorders.html',user=user)
        else:
            return redirect(url_for('user.login'))


@blueprint.route('/myorder/')
def myorder():
    user_id = session.get('user_id')
    list = []
    order_list = []
    house_id_list = []
    houses = House.query.filter(House.user_id==user_id).all()
    orders = Order.query.all()
    for order in orders:
        order_list.append(order.house_id)
    for house in houses:
        if house.id in order_list:
            house_id_list.append(house.id)
    orders = Order.query.filter(Order.house_id.in_(house_id_list)).all()
    houses = House.query.filter(House.id.in_(house_id_list)).all()
    for order in orders:
        for house in houses:
            if order.house_id == house.id:
                order_dict = order.to_dict()
                order_dict['image'] = house.index_image_url
                order_dict['title'] = house.title

                status = [("WAIT_ACCEPT",'待接单'),
                          ("WAIT_PAYMENT", '待支付'),
                          ("PAID", '已支付'),
                          ("WAIT_COMMENT", '待评价'),
                          ("COMPLETE", '已完成'),
                          ("CANCELED", '已取消'),
                          ("REJECTED" , '已拒单')]
                for statu in status:
                    if order_dict['status'] == statu[0]:
                        order_dict['status'] = statu[1]
                list.append(order_dict)
    return jsonify({'code':200,'msg':'请求成功','orders':list})


@blueprint.route('/user_order/')
def user_order():
    list = []
    house_id = []
    user_id = session.get('user_id')
    orders = Order.query.filter(Order.user_id==user_id).all()
    for order in orders:
        hou_id = order.house_id
        house_id.append(hou_id)
    houses = House.query.filter(House.id.in_(house_id)).all()
    for order in orders:
        for house in houses:
            if order.house_id == house.id:
                order_dict = order.to_dict()
                order_dict['title'] = house.title
                order_dict['image'] = house.index_image_url
                status = [("WAIT_ACCEPT", '待接单'),
                          ("WAIT_PAYMENT", '待支付'),
                          ("PAID", '已支付'),
                          ("WAIT_COMMENT", '待评价'),
                          ("COMPLETE", '已完成'),
                          ("CANCELED", '已取消'),
                          ("REJECTED", '已拒单')]
                for statu in status:
                    if order_dict['status'] == statu[0]:
                        order_dict['status'] = statu[1]
                list.append(order_dict)
    return jsonify({'code': 200, 'msg': '请求成功', 'orders': list})



@blueprint.route('/accept/',methods=['GET','POST'])
def accept():
    order_id = request.form.get('id')
    order = Order.query.get(order_id)
    order.status = "WAIT_PAYMENT"
    order.save()
    return jsonify(status_code.SUCCESS)


@blueprint.route('/reject/',methods=['GET','POST'])
def reject():
    order_id = request.form.get('id')
    text = request.form.get('text')
    if text:
        order = Order.query.get(order_id)
        order.status = "REJECTED"
        order.comment = text
        order.save()
        return jsonify(status_code.SUCCESS)
    return jsonify(status_code.ORDER_COMMENT)


# @blueprint.route('/deal/',methods=['GET','POST'])
# def deal():
#     house_id = request.form.get('house_id')
#     house = House.query.get(house_id)
#     price = house.price
#
#     money = request.form.get('money')
#     user_id = session.get('user_id')
#     begin_date = request.form.get('start_date')
#     end_date = request.form.get('end_date')
#     days = int(request.form.get('days'))
#     beg = datetime.strptime(begin_date, '%Y-%m-%d')
#     end = datetime.strptime(end_date, '%Y-%m-%d')
#     day = end - beg
#     list = str(day).split(' ')
#     day = int(list[0])
#     if not all([house_id,money,user_id,begin_date,end_date,days]):
#         return jsonify({'code':12177,'msg':'创建失败，请检查信息完整不'})
#     if day+1 != days:
#         return jsonify({'code':12555,'msg':'天数错误'})
#     amount = int(days) * int(price)
#     # begin_date = str(beg)
#     # end_date = str(end)
#     # 2018 - 12 - 25 20: 16:22
#     orders = Order()
#     orders.days = days
#     orders.user_id = user_id
#     orders.house_id = house_id
#     orders.begin_date = beg
#     orders.end_date = end
#     orders.amount = amount
#     orders.add_update()
#     return jsonify(status_code.SUCCESS)

@blueprint.route('/deal/',methods=['GET','POST'])
def deal():
    dict = request.form
    house_id = int(dict.get('house_id'))
    '''将日期字符串转化成datatime对象'''
    start_date = datetime.strptime(dict.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')
    '''验证数据的完整性'''
    if not all([house_id, start_date, end_date]):
        return jsonify({'code':12177,'msg':'创建失败，请检查信息完整不'})
    if start_date > end_date:
        return jsonify(status_code.CREATE_OEDER )
    '''查询房屋对象'''
    try:
        '''根据房屋的id去查询房屋的对象'''
        house = House.query.get(house_id)
    except:
        return jsonify(status_code.CREATE_OEDER )
    '''创建订单'''
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = (end_date - start_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price
    '''调用对象方法去创建一个订单对象'''
    try:
        order.add_update()
        num = house.order_count
        house.order_count = num+1
    except:
        return jsonify(status_code.CREATE_OEDER )

    '''返回信息'''
    return jsonify({'code':200,'msg':'创建订单成功'})


@blueprint.before_request
def login_middle_button():
    not_need_path = ['/user/login/','/user/register/','/user/index/']
    path = request.path
    for not_path in not_need_path:
        # 匹配当前路径是否为不需要登录验证的路径
        if re.match(not_path, path):
            return None
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    user = User.query.filter(User.id == user_id).first()
    if not user:
        return redirect(url_for('user.login'))
    session['user_id'] = user.id