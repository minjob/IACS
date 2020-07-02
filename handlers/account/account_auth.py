import json
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, make_response
from dbset.log.BK2TLogger import logger
from dbset.main.BSFramwork import AlchemyEncoder
from flask_login import login_required, logout_user, login_user, LoginManager
from dbset.database.db_operate import db_session
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
from io import BytesIO
import time
from models.system import User
import datetime

# from models.SystemManagement.system import User

# flask_login的初始化
login_manager = LoginManager()
login_manager.db_session_protection = 'strong'
login_manager.login_view = 'login_auth.login'

login_auth = Blueprint('login_auth', __name__, template_folder='templates')

'''登录'''


@login_manager.user_loader
def load_user(user_id):
    return db_session.query(User).filter_by(ID=int(user_id)).first()


@login_auth.route('/account/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('./main/login.html')
        if request.method == 'POST':
            data = request.values
            WorkNumber = data.get('WorkNumber')
            password = data.get('password')
            # 验证账户与密码
            if WorkNumber:
                user = db_session.query(User).filter_by(WorkNumber=WorkNumber).first()
                if user and (user.confirm_password(password) or user.Password == password):
                    login_user(user)  # login_user(user)调用user_loader()把用户设置到db_session中
                    user.session_id = str(time.time())
                    db_session.commit()
                    # roles = db_session.query(User.RoleName).filter_by(WorkNumber=WorkNumber).all()
                    # menus = []
                    # for role in roles:
                    #     for index in role:
                    #         role_id = db_session.query(Role.ID).filter_by(RoleName=index).first()
                    #         menu = db_session.query(Menu.ModuleCode).join(Role_Menu, isouter=True).filter_by(Role_ID=role_id).all()
                    #         for li in menu:
                    #             menus.append(li[0])
                    # session['menus'] = menus
                    # user.Status = "1"
                    # db_session.commit()
                    use = db_session.query(User).filter_by(WorkNumber=WorkNumber).first()
                    # return redirect('/')
                    return render_template('./main/heatmap.html')
            # 认证失败返回登录页面
            error = '用户名或密码错误'
            return render_template('./main/login.html', error=error)
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)


# 退出登录
@login_auth.route('/account/logout')
@login_required
def logout():
    logout_user()
    flash(u'用户已经退出')
    # current_user.Name
    # user = db_session.query(User).filter_by(WorkNumber=work_number).first()
    # user.Status = "0"
    return redirect(url_for('login_auth.login'))


# from wtforms import StringField,SubmitField
# from wtforms.validators import Required, DataRequired
#
# from flask_wtf import FlaskForm
# class LoginForm(FlaskForm):
#     verify_code = StringField('验证码', validators=[DataRequired()])
#     submit = SubmitField('登录')
#
# @login_auth.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if session.get('image') != form.verify_code.data:
#             flash('验证码错误')
#         # 验证用户的登录密码
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user,form.remember_me.data)
#             flash('验证通过，登录成功')
#             return redirect(request.args.get('next') or
#             url_for('main.index'))
#         else:
#             flash('用户名或者密码不正确')
#     return render_template('auth/login.html',form=form)
@login_auth.route('/account/code')
def get_code():
    image, str = validate_picture()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = str
    return response


def validate_picture():
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    # 图片大小130 x 50
    width = 130
    heighth = 50
    # 先生成一个新图片对象
    im = Image.new('RGB', (width, heighth), 'white')
    # 设置字体
    font = ImageFont.truetype("symbol.ttf", 16, encoding="symb")
    # 创建draw对象
    draw = ImageDraw.Draw(im)
    str = ''
    # 输出每一个文字
    for item in range(5):
        text = random.choice(total)
        str += text
        draw.text((5 + random.randint(4, 7) + 20 * item, 5 + random.randint(3, 7)), text=text, fill='black')

    # 划几根干扰线
    for num in range(8):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, heighth / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(heighth / 2, heighth)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    # 模糊下,加个帅帅的滤镜～
    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str


@login_auth.route('/account/userloginauthentication', methods=['GET', 'POST'])
def userloginauthentication():
    '''
    用户登陆认证
    :return:
    '''
    try:
        if request.method == 'POST':
            data = request.values
            WorkNumber = data.get('WorkNumber')
            password = data.get('password')
            # 验证账户与密码
            user = db_session.query(User).filter_by(WorkNumber=WorkNumber).first()
            resp = make_response()
            if user and (user.confirm_password(password) or user.Password == password):
                login_user(user)  # login_user(user)调用user_loader()把用户设置到db_session中
                user.session_id = str(time.time())
                user.LastLoginTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db_session.commit()
                return 'OK'
            else:
                return '用户名密码错误'
    except Exception as e:
        print(e)
        db_session.rollback()
        logger.error(e)
        return json.dumps([{"status": "Error:" + str(e)}], cls=AlchemyEncoder, ensure_ascii=False)
