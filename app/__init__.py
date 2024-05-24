from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)

    from app.routes.routes import main
    app.register_blueprint(main)

    return app
