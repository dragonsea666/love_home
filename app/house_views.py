import os
import re

from datetime import datetime,timedelta
from flask import Blueprint, request, render_template, session, url_for, redirect, g, jsonify,make_response
from sqlalchemy import or_
import time
from app.models import Area, House, Facility, HouseImage, User, Order
from utils import status_code
from utils.setting import MEDIA_PATH

blues = Blueprint('house',__name__)

@blues.route('/newhouse/',methods=['GET','POST'])
def newhouse():
    if request.method == 'GET':
        house_id = session.get('house_id')
        return render_template('newhouse.html',house_id=house_id)

    if request.method == 'POST':
        user_id = session.get('user_id')
        title = request.form.get('title')
        area_id = request.form.get('area_id')
        price = request.form.get('price')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facilitys = request.form.getlist('facility')
        if not all([title, area_id,price,address,room_count,acreage,unit,capacity,beds,deposit,min_days,max_days,facilitys]):
            return jsonify(status_code.HOUSE_INFO)
        house = House()
        try:
            house.title = title
            house.user_id = user_id
            house.area_id = int(area_id)
            house.price = int(price)
            house.address = address
            house.room_count = int(room_count)
            house.acreage = int(acreage)
            house.unit = unit
            house.capacity = int(capacity)
            house.beds = beds
            house.deposit = int(deposit)
            house.min_days = int(min_days)
            house.max_days = int(max_days)
            house.save()
            house_id = House.query.order_by('-id').first().id
            session['house_id'] = house_id
            house = House.query.get(house_id)
            for i in facilitys:
                facility = Facility.query.get(int(i))
                house.facilities.append(facility)
            house.save()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.HOUSE_FORMAT_ERROR)


@blues.route('/image/', methods=['POST','GET'])
def add_image():
    house_id = session.get('house_id')
    image = request.files.get('house_image')
    house = House.query.get(house_id)
    if not house.index_image_url:
        path = os.path.join(MEDIA_PATH,image.filename)
        image.save(path)
        house.index_image_url = image.filename
        house.save()
        return jsonify(status_code.SUCCESS)
    path = os.path.join(MEDIA_PATH, image.filename)
    house_id = session.get('house_id')
    houseimage = HouseImage()
    image.save(path)
    houseimage.url = image.filename
    houseimage.house_id = house_id
    houseimage.save()
    return jsonify({'code':200,'msg':'请求成功','img':image.filename})


@blues.route('/area/',methods=['GET','POST'])
def area():
    if request.method == 'GET':
        area_dict = []
        areas = Area.query.all()
        for area in areas:
            dict = area.to_dict()
            area_dict.append(dict)
        return jsonify({'code':200,'msg':'请求成功','area_dict':area_dict})


@blues.route('/detail/<int:id>/',methods=['GET','POST'])
def detail(id):
    if request.method == 'GET':
        images = HouseImage.query.filter(HouseImage.house_id==id).all()
        return render_template('detail.html', images=images)

@blues.route('/detail_info/')
def detail_info():
    user_id = session.get('user_id')
    house_id = request.args.get('house_id')
    house = House.query.get(house_id)
    house_info = house.to_full_dict()
    house_info['user_id'] = user_id
    return jsonify({'code':200,'msg':'请求成功','house_info':house_info})

@blues.route('/search/',methods=['GET','POST'])
def search():
    if request.method == 'GET':
        order_hou_list = []
        aid = request.args.get('aid')
        # aname = request.args.get('aname')
        begin_date = request.args.get('sd')
        end_date = request.args.get('ed')
        beg = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        day = end - beg
        list = str(day).split(' ')
        days = int(list[0])
        orders = Order.query.all()
        for order in orders:
            order_hou_list.append(order.house_id)
        houses = House.query.filter(House.area_id==aid,or_(House.max_days>days,House.max_days==0),House.id.notin_(order_hou_list))
        # ?aid = 1 & aname = 锦江区 & sd = 2018 - 12 - 26 & ed = 2018 - 12 - 28

        page = int(request.args.get('page',1))
        pre_page = 12
        paginate = houses.paginate(page,pre_page)
        houses = paginate.items
        return render_template('search.html', houses=houses,paginate=paginate,aid=aid,sd=begin_date,ed=end_date)

@blues.route('/more_search/')
def more_search():
    order_hou_list = []
    houses_list = []
    # [('aid', '4'), ('sd', '2018-12-28'), ('ed', '2018-12-29'), ('sk', 'new'), ('p', '1')])
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    p = request.args.get('p')
    beg = datetime.strptime(sd, '%Y-%m-%d')
    end = datetime.strptime(ed, '%Y-%m-%d')
    day = end - beg
    list = str(day).split(' ')
    days = int(list[0])
    orders = Order.query.all()
    for order in orders:
        order_hou_list.append(order.house_id)

    skip_data = (int(p) - 1) * 12
    if sk == 'new':
        new_data = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        new_data = datetime.strptime(new_data,'%Y-%m-%d')
        last_12 = new_data - timedelta(hours = 24*12)
        houses = House.query.filter(House.area_id==aid,or_(House.max_days>days,House.max_days==0),House.id.notin_(order_hou_list),
                                House.create_time>last_12,).offset(skip_data).limit(12)
        for house in houses:
            house_dict = house.to_full_dict()
            houses_list.append(house_dict)

    if sk == 'booking':
        houses = House.query.filter(House.area_id==aid,or_(House.max_days>days,House.max_days==0),House.id.notin_(order_hou_list),
                                ).order_by('-order_count').offset(skip_data).limit(12)
        for house in houses:
            house_dict = house.to_full_dict()
            houses_list.append(house_dict)

    if sk == 'price-inc':
        houses = House.query.filter(House.area_id == aid, or_(House.max_days > days, House.max_days == 0),
                                    House.id.notin_(order_hou_list),
                                    ).order_by('price').offset(skip_data).limit(12)
        for house in houses:
            house_dict = house.to_full_dict()
            houses_list.append(house_dict)

    if sk == 'price-des':
        houses = House.query.filter(House.area_id == aid, or_(House.max_days > days, House.max_days == 0),
                                    House.id.notin_(order_hou_list),
                                    ).order_by('-price').offset(skip_data).limit(12)
        for house in houses:
            house_dict = house.to_full_dict()
            houses_list.append(house_dict)


    return jsonify({'code': 200, 'msg': '请求成功', 'houses_info': houses_list})



@blues.before_request
def login_middle_button():
    not_need_path = ['/house/area/','/house/detail/','/house/detail_info/','/house/search/','/house/more_search/']
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
