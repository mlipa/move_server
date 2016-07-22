#!/usr/bin/env python
# coding: utf-8

from app import database


class Users(database.Model):
    id = database.Column(database.Integer,
                         primary_key=True)
    username = database.Column(database.String(32),
                               index=True,
                               unique=True)
    password = database.Column(database.String(32),
                               index=False,
                               unique=False)
    salt = database.Column(database.String(8),
                           index=False,
                           unique=False)
    name = database.Column(database.String(64),
                           index=True,
                           unique=False)
    email = database.Column(database.String(128),
                            index=True,
                            unique=True)

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

    def __repr__(self):
        return '<User %r>' % self.username