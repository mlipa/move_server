#!/usr/bin/env python
# coding: utf-8

from configuration import Configuration
from flask import Flask, Markup
from flask_hashing import Hashing
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.secret_key = 'secret_key'
application.config.from_object(Configuration)

hashing = Hashing(application)

login_manager = LoginManager()
login_manager.login_view = 'sign_in'
login_manager.login_message = Markup('<strong>Prohibited!</strong> Unless you have an account.')
login_manager.login_message_category = 'info'
login_manager.init_app(application)

database = SQLAlchemy(application)

from app import views, models
