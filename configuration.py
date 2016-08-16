#!/usr/bin/env python
# coding: utf-8

import os

PROJECT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = True
    HASHING_METHOD = 'sha256'
    HASHING_ROUND = 1
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_DIRECTORY, 'move.db')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_DIRECTORY, 'database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_AVATARS_DEST = os.path.join(PROJECT_DIRECTORY, 'application/static/images/avatars')
