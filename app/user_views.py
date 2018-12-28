from io import BytesIO
import re
from flask import Blueprint, request, render_template, session, url_for, redirect, g, jsonify,make_response
from werkzeug.security import generate_password_hash
import os
from app.models import User, Order, House
from utils.functions import create_validate_code
from utils import status_code
from utils.setting import MEDIA_PATH

blue = Blueprint('user',__name__)


@blue.route('/code/')
def get_code():
    # 把strs发给前端,或者在后台使用session保存
    code_img, strs = create_validate_code()
    buf = BytesIO()
    code_img.save(buf, 'jpeg')

    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['img'] = strs.upper()
    return response


@blue.route('/login/',methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@blue.route('/login/',methods=['POST'])
def my_login():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        pattern = re.compile(r'^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$')
        if not re.match(pattern, mobile):
            return jsonify(status_code.USER_LOGIN_MOBILE_MATCHING)
        if not password:
            return jsonify(status_code.USER_LOGIN_NOT_PASSWORD)
        user = User.query.filter(User.phone == mobile).first()
        if not user:
            return jsonify(status_code.USER_LOGIN_USER_EXIST)
        if user.check_pwd(password):
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_ERROR)


@blue.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        mobile = request.form.get('mobile')
        imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')


        pattern = re.compile(r'^(13(7|8|9|6|5|4)|17(0|8|3|7)|18(2|3|6|7|9)|15(3|5|6|7|8|9))\d{8}$')
        if not re.match(pattern,mobile):
            return jsonify (status_code.USER_REGITSER_MOBILE_MATCHING)
        if session.get('img') == imagecode.upper():
            if password != password2:
                return jsonify(status_code.USER_REGITSER_PASSWORD_PASSWORD2)
            if len(password) < 6:
                return jsonify(status_code.USER_REGITSER_PASSWORD_MIN)

            user = User()
            user.phone = mobile
            password = generate_password_hash(password)
            user.pwd_hash = password
            user.save()
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_REGITSER_CODE)


@blue.route('/index/',methods=['GET','POSY'])
def index():
    if request.method == 'GET':
        try:
            user_id = session.get('user_id')
            user = User.query.get(user_id)
        except:
            user = ''

        return render_template('index.html',user=user)

@blue.before_request
def login_middle_button():
    not_need_path = ['/user/login/','/user/register/','/user/index/','/user/code/']
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


@blue.route('/my/<int:id>/',methods=['GET','POST'])
def my(id):
    if request.method == 'GET':
        user = User.query.filter(User.id == id).first()

        return render_template('my.html',user=user)


@blue.route('/profile/<int:id>/', methods=['GET','POST'])
def profile(id):
    if request.method == 'GET':

        user = User.query.filter(User.id == id).first()
        return render_template('profile.html', user=user)

@blue.route('/avatar/',methods=['GET','POST'])
def avatar():
    if request.method == 'POST':
        avatar = request.files.get('avatar')
        path = os.path.join(MEDIA_PATH, avatar.filename)
        avatar.save(path)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.avatar = avatar.filename
        user.save()
        return jsonify({'code':200,'msg':'成功','avatar':avatar.filename})


@blue.route('/name/',methods=['GET','POST'])
def name():
    if request.method == 'POST':
        name = request.form.get('name')
        user = User.query.filter(User.name == name).first()
        if user:
            return jsonify(status_code.USER_SAME_NAME)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.name = name
        user.save()
        return jsonify(status_code.SUCCESS)


@blue.route('/auth/<int:id>/',methods=['GET'])
def auth(id):
    if request.method == 'GET':
        user = User.query.get(id)

        return render_template('auth.html',user=user)

@blue.route('/auth/',methods=['POST'])
def first_auth():
    if request.method == 'POST':
        user_id = session.get('user_id')
        id_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        pattern = re.compile(r'[\u4e00-\u9fa5]{2,}')
        if not re.match(pattern, id_name):
            return jsonify(status_code.USER_ID_NAME_ERROR)
        pattern = re.compile(r"(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)")
        if not re.match(pattern, id_card):
            return jsonify(status_code.USER_ID_CARD_ERROR)
        user = User.query.get(user_id)
        user.id_name = id_name
        user.id_card = id_card
        user.save()
        return jsonify({'code':200,'msg':'请求成功','user_id':user_id})


# @blue.route('/orders/',methods=['GET','POST'])
# def orders():
#     if request.method == 'GET':
#         user_id = session.get('user_id')
#         order = Order.query.filter(Order.user_id == user_id)
#         user = User.query.get(user_id)
#         return render_template('orders.html',order=order,user=user)


@blue.route('/myhouse/',methods=['GET','POST'])
def myhouse():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        page = int(request.args.get('page',1))
        pre_page = 24
        paginate = House.query.filter(House.user_id==user_id).paginate(page,pre_page)
        houses = paginate.items
        return render_template('myhouse.html',user=user,houses=houses,paginate=paginate)


@blue.route('/user/')
def user():
    user_id = session.get('user_id')
    if user_id:
        return jsonify(status_code.SUCCESS)
    return jsonify(status_code.USER_LOGIN_USER_EXIST)

@blue.route('/logout/')
def logout():
    session['user_id'] = ''
    return jsonify(status_code.SUCCESS)

