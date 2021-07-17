from config import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect


bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CsrfProtect()
login_manager = LoginManager()
moment = Moment()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    
    """ Register blueprints """
    
    # main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # instructor blueprint
    from .examiner import examiner as examiner_blueprint
    app.register_blueprint(examiner_blueprint)
    
    # student blueprint
    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint)
    
    # authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app