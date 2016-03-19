from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config_by_name

db = SQLAlchemy()

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"

def create_app(config_name):
    """Flask app creation factory"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    login_manager.init_app(app)

    return app

app = create_app('dev')


import blagging.models
import blagging.views
import blagging.forms

