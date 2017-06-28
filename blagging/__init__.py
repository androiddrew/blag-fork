import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.markdown import Markdown
from .mdx_code_multiline import MultilineCodeExtension
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
    md = Markdown(app)
    md.register_extension(MultilineCodeExtension)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    return app


app = create_app('dev')

import blagging.models
import blagging.views
import blagging.forms
