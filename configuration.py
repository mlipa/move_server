#!/usr/bin/env python
# coding: utf-8

import os

project_directory = os.path.abspath(os.path.dirname(__file__))


class Configuration(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(project_directory, 'move.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(project_directory, 'database')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
