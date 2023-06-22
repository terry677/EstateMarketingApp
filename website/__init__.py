from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from os import path

import psycopg2

db = SQLAlchemy()
DB_NAME = "texestate"
# pymysql.install_as_MySQLdb()
def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'test'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://terryabu:Terry&1234@localhost:5432/{DB_NAME}'

    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:{config.DB_PASSWORD}@localhost/{DB_NAME}'

    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    db.init_app(app)

    

    from .views import views
    from .auth import auth
    from .models import User, Property, Image

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.jinja_env.filters['format_price'] = format_price

    # Create the "uploads" directory if it doesn't exist
    uploads_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(uploads_dir, exist_ok=True)

    # create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def login_user(id):
        return User.query.get(int(id))

    return app

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Database created successfully')

def format_price(price):
    return "₦" + format(price, ",.2f")