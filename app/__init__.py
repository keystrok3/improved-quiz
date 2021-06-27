from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    
    """ Register blueprints """
    
    # main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # instructor blueprint
    from .examiner import examiner as examiner_blueprint
    app.register_blueprint(examiner_blueprint)
    
    # authentication blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app