# -*- coding: utf-8 -*-

__version__ = "0.1"

import os
import logging

from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
login = LoginManager()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config["APP_VERSION"] = __version__

    login.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    # register the blueprints
    from image_labeller.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from image_labeller.main import bp as main_bp
    app.register_blueprint(main_bp)
    from image_labeller.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    # create database tables
    with app.app_context():
        db.create_all()
    return app

from image_labeller import schema
