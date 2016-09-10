#!/usr/bin/env python
# coding: utf-8

import os

from flask import url_for

from application import database

APPLICATION_DIRECTORY = os.path.abspath(os.path.dirname(__file__))


class Activities(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), index=True, unique=True)
    predictions = database.relationship('Predictions', backref='activity', lazy='dynamic')

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Activity %r>' % self.name


class Classifiers(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(32), index=True, unique=True)
    predictions = database.relationship('Predictions', backref='classifier', lazy='dynamic')

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Classifier %r>' % self.name


class Predictions(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    timestamp = database.Column(database.String(23), index=True, unique=False)
    activity_id = database.Column(database.Integer, database.ForeignKey('activities.id'))
    classifier_id = database.Column(database.Integer, database.ForeignKey('classifiers.id'))
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def get_id(self):
        return unicode(self.id)

    def __init__(self, timestamp, activity_id, classifier_id, user_id):
        self.timestamp = timestamp
        self.activity_id = activity_id
        self.classifier_id = classifier_id
        self.user_id = user_id

    def __repr__(self):
        return '<Prediction %r>' % self.activity.name


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(64), index=True, unique=False)
    username = database.Column(database.String(32), index=True, unique=True)
    email = database.Column(database.String(128), index=True, unique=True)
    password = database.Column(database.String(64), index=False, unique=False)
    salt = database.Column(database.String(8), index=False, unique=False)
    predictions = database.relationship('Predictions', backref='user', lazy='dynamic')

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

    def __repr__(self):
        return '<User %r>' % self.username
