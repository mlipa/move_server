#!/usr/bin/env python
# coding: utf-8

from configuration import Configuration
from flask import Flask, Markup
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.secret_key = 'secret_key'
application.config.from_object(Configuration)

loginManager = LoginManager()
loginManager.login_view = 'signin'
loginManager.login_message = Markup('<strong>Prohibited!</strong> Unless you have an account.')
loginManager.login_message_category = 'info'
loginManager.init_app(application)

database = SQLAlchemy(application)

from app import views, models
