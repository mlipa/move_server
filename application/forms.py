#!/usr/bin/env python
# coding: utf-8

from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import FileField, PasswordField, RadioField, StringField

from application import models

USER_NAME_LENGTH = models.Users.name.property.columns[0].type.length
USER_USERNAME_LENGTH = models.Users.username.property.columns[0].type.length
USER_EMAIL_LENGTH = models.Users.email.property.columns[0].type.length


class LogInForm(Form):
    username = StringField('username', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH})
    password = PasswordField('password', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH})


class SettingsForm(Form):
    classifier = RadioField('classifier', choices=[('1', 'Artificial neural network')])


class DataForm(Form):
    name = StringField('name', render_kw={'class': 'form-control', 'maxlength': USER_NAME_LENGTH,
                                          'pattern': '^[A-z]+( [A-z]+)*( [A-z]+)?(-[A-z]+)?$'})
    username = StringField('username', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                  'pattern': '^[a-z0-9]+([._-][a-z0-9]+)*$', 'data-remote': '/validate',
                                                  'data-remote-error': 'Username is not available. Please select the another one.'})
    email = EmailField('email', render_kw={'class': 'form-control', 'maxlength': USER_EMAIL_LENGTH,
                                           'pattern': '^[a-z0-9]+([._-][a-z0-9]+)*@[a-z0-9]+([._-][a-z0-9]+)*\.[a-z]{2,4}$',
                                           'data-type-error': 'Please match the requested format.',
                                           'data-remote': '/validate',
                                           'data-remote-error': 'E-mail is not available. Please select the another one.'})


class PasswordForm(Form):
    old_password = PasswordField('old_password', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                            'data-remote': '/validate',
                                                            'data-remote-error': 'Password does not match. Please enter the correct one.'})
    new_password = PasswordField('new_password', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                            'id': 'new_password'})
    confirm_new_password = PasswordField('confirm_new_password',
                                         render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                    'data-match': '#new_password',
                                                    'data-match-error': 'Password does not match. Please repeat the above one.'})


class AvatarForm(Form):
    avatar = FileField('avatar', render_kw={'class': 'form-control-file', 'accept': 'image/png'})
