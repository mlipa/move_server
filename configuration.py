#!/usr/bin/env python
# coding: utf-8

import os

projectDirectory = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(projectDirectory, 'move.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(projectDirectory, 'database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
