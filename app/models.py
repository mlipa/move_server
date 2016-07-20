#!/usr/bin/env python
# coding: utf-8

from app import database


class Users(database.Model):
    id = database.Column(database.Integer,
                         primary_key=True)
    name = database.Column(database.String(64),
                           index=True,
                           unique=False)
    username = database.Column(database.String(32),
                               index=True,
                               unique=True)
    password = database.Column(database.String(32),
                               index=False,
                               unique=False)
    salt = database.Column(database.String(8),
                           index=False,
                           unique=False)

    def __repr__(self):
        return '<User %r>' % self.username
