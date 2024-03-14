import os
import pymysql
from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent.parent / "docker" / "env" / ".env"
load_dotenv(env_path)

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    pymysql.install_as_MySQLdb()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PYTHONIOENCODING'] = 'utf-8'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') + "?charset=utf8mb4"

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        from .models import User  # Переместите импорт сюда
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
