#!/usr/bin/env python
# coding: utf-8

from flask_wtf import Form
from flask_wtf.html5 import EmailField
from wtforms import FileField, PasswordField, StringField
from wtforms.validators import Length

from app import models

USER_USERNAME_LENGTH = models.Users.username.property.columns[0].type.length
USER_PASSWORD_LENGTH = models.Users.password.property.columns[0].type.length
USER_NAME_LENGTH = models.Users.name.property.columns[0].type.length
USER_EMAIL_LENGTH = models.Users.email.property.columns[0].type.length


class LoginForm(Form):
    username = StringField('username', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH,
                                                  'placeholder': 'Username'},
                           validators=[Length(max=USER_USERNAME_LENGTH)])
    password = PasswordField('password', render_kw={'class': 'form-control', 'maxlength': USER_PASSWORD_LENGTH,
                                                    'placeholder': 'Password'},
                             validators=[Length(max=USER_PASSWORD_LENGTH)])


class UserForm(Form):
    name = StringField('name', render_kw={'class': 'form-control', 'maxlength': USER_NAME_LENGTH},
                       validators=[Length(max=USER_NAME_LENGTH)])
    username = StringField('username', render_kw={'class': 'form-control', 'maxlength': USER_USERNAME_LENGTH},
                           validators=[Length(max=USER_USERNAME_LENGTH)])
    email = EmailField('email', render_kw={'class': 'form-control', 'maxlength': USER_EMAIL_LENGTH},
                       validators=[Length(max=USER_EMAIL_LENGTH)])
    old_password = PasswordField('old_password', render_kw={'class': 'form-control', 'maxlength': USER_PASSWORD_LENGTH,
                                                            'placeholder': 'Enter old password'},
                                 validators=[Length(max=USER_PASSWORD_LENGTH)])
    new_password = PasswordField('new_password', render_kw={'class': 'form-control', 'maxlength': USER_PASSWORD_LENGTH,
                                                            'placeholder': 'Enter new password'},
                                 validators=[Length(max=USER_PASSWORD_LENGTH)])
    confirm_new_password = PasswordField('confirm_new_password',
                                         render_kw={'class': 'form-control', 'maxlength': USER_PASSWORD_LENGTH,
                                                    'placeholder': 'Confirm new password'},
                                         validators=[Length(max=USER_PASSWORD_LENGTH)])
    avatar = FileField('avatar', render_kw={'class': 'form-control-file'})
