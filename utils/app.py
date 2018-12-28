
from flask import Flask

from app.house_views import blues
from app.models import db
from app.order_views import blueprint
from app.user_views import blue
from utils.config import Conf
from utils.setting import STATIC_PATH, TEMPLATES_PATH


def create_app():
    app = Flask(__name__,
                static_folder=STATIC_PATH,
                template_folder=TEMPLATES_PATH)
    # 加载配置
    app.config.from_object(Conf)

    # 蓝图
    app.register_blueprint(blueprint=blue, url_prefix='/user')
    app.register_blueprint(blueprint=blues, url_prefix='/house')
    app.register_blueprint(blueprint=blueprint, url_prefix='/order')

    # 初始化
    db.init_app(app)

    return app