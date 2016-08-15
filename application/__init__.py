#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Markup
from flask_hashing import Hashing
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import configure_uploads, patch_request_class, UploadSet

from configuration import Configuration

application = Flask(__name__)
application.secret_key = 'JqhsGUN1rdi0azQZDIrBMyGNE3TS3TPl'
application.config.from_object(Configuration)

hashing = Hashing(application)

login_manager = LoginManager()
login_manager.login_view = 'log_in'
login_manager.login_message = Markup('<strong>Hey you!</strong> Access only for logged in users.')
login_manager.login_message_category = 'info'
login_manager.init_app(application)

database = SQLAlchemy(application)

avatars = UploadSet('avatars', 'png')
configure_uploads(application, avatars)
patch_request_class(application, 5 * 1024 * 1024)

from application import views, models
