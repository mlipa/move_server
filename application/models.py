#!/usr/bin/env python
# coding: utf-8

import os

from flask import url_for

from application import database

APPLICATION_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Classifiers(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), index=True, unique=True)
    users = database.relationship('Users', backref='classifier', lazy='dynamic')

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Classifier %r>' % self.name


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), index=True, unique=False)
    username = database.Column(database.String(32), index=True, unique=True)
    email = database.Column(database.String(128), index=True, unique=True)
    password = database.Column(database.String(64), index=False, unique=False)
    salt = database.Column(database.String(8), index=False, unique=False)
    classifier_id = database.Column(database.Integer, database.ForeignKey('classifiers.id'))

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
        avatar = url_for('static', filename='images/avatars/' + str(self.id) + '.png')

        if not os.path.exists(APPLICATION_DIRECTORY + avatar):
            avatar = url_for('static', filename='images/avatars/default.png')

        return avatar

    def __init__(self, name, username, email, password, salt):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.salt = salt
        self.classifier_id = 1

    def __repr__(self):
        return '<User %r>' % self.username
