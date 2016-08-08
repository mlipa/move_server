#!/usr/bin/env python
# coding: utf-8

from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import FileField, PasswordField, StringField

from app import models

USER_USERNAME_LENGTH = models.Users.username.property.columns[0].type.length
USER_PASSWORD_LENGTH = models.Users.password.property.columns[0].type.length
USER_NAME_LENGTH = models.Users.name.property.columns[0].type.length
USER_EMAIL_LENGTH = models.Users.email.property.columns[0].type.length


class LoginForm(Form):
    username = StringField('username', render_kw={'class': 'form-control', 'placeholder': 'Username'})
    password = PasswordField('password', render_kw={'class': 'form-control', 'placeholder': 'Password'})


class DataForm(Form):
    name = StringField('name', render_kw={'class': 'form-control', 'maxlength': USER_NAME_LENGTH,
                                          'pattern': '^[A-z]+( [A-z]+)*( [A-z]+)?(-[A-z]+)?$',
                                          'data-pattern-error': 'Whoops! The name can contain only words with "A-z" letters, " " between words and "-" in last name.'})
    username = StringField('username', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                  'pattern': '^[a-z0-9]+([._-][a-z0-9]+)*$',
                                                  'data-pattern-error': 'Whoops! The username can contain only word with "a-z" letters or "0-9" digits, ".", "-" or "_" between characters.',
                                                  'data-remote': '/validate',
                                                  'data-remote-error': 'Whoops! The username chosen by other user!'})
    email = EmailField('email', render_kw={'class': 'form-control', 'maxlength': USER_EMAIL_LENGTH,
                                           'data-error': "Whoops! This isn't the e-mail address.",
                                           'pattern': '^[a-z0-9]+([._-][a-z0-9]+)*@[a-z0-9]+([._-][a-z0-9]+)*\.[a-z]{2,4}$',
                                           'data-pattern-error': 'Whoops! The e-mail can contain only address with "a-z" letters or "0-9" digits, "@", ".", "-" or "_" between characters',
                                           'data-remote': '/validate',
                                           'data-remote-error': 'Whoops! The e-mail chosen by other user!'})
    avatar = FileField('avatar', render_kw={'class': 'form-control-file', 'accept': 'image/png'})


class PasswordForm(Form):
    old_password = PasswordField('old_password',
                                 render_kw={'class': 'form-control', 'placeholder': 'Enter old password',
                                            'maxlength': USER_PASSWORD_LENGTH, 'data-remote': '/validate',
                                            'data-remote-error': "Whoops! The old password don't match.",
                                            'data-required-error': 'Whoops! The old password is required to change password.'})
    new_password = PasswordField('new_password', render_kw={'id': 'new_password', 'class': 'form-control',
                                                            'placeholder': 'Enter new password',
                                                            'maxlength': USER_PASSWORD_LENGTH,
                                                            'data-required-error': 'Whoops! The new password is required to change password.'})
    confirm_new_password = PasswordField('confirm_new_password',
                                         render_kw={'class': 'form-control', 'placeholder': 'Confirm new password',
                                                    'maxlength': USER_PASSWORD_LENGTH, 'data-match': '#new_password',
                                                    'data-match-error': "Whoops! These passwords don't match.",
                                                    'data-required-error': 'Whoops! The confirmation of new password is required to change password.'})
