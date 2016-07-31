#!/usr/bin/env python
# coding: utf-8

import os

from flask import url_for

from app import database


class Settings(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), index=False, unique=True)

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Setting %r>' % self.name


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(32), index=True, unique=True)
    password = database.Column(database.String(32), index=False, unique=False)
    salt = database.Column(database.String(8), index=False, unique=False)
    name = database.Column(database.String(64), index=True, unique=False)
    email = database.Column(database.String(128), index=True, unique=True)
    setting_id = database.Column(database.Integer, database.ForeignKey('settings.id'))

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    def is_authenticated():
        return True

    def get_id(self):
        return unicode(self.id)

    def get_avatar(self):
        app_directory = os.path.abspath(os.path.dirname(__file__))
        avatar = url_for('static', filename='img/' + self.username + '.png')

        if not os.path.exists(app_directory + avatar):
            avatar = url_for('static', filename='img/default_avatar.png')

        return avatar

    def __repr__(self):
        return '<User %r>' % self.username
