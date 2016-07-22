#!/usr/bin/env python
# coding: utf-8

from app import application, hashing, login_manager, models
from flask import flash, g, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_user


@application.before_request
def before_request():
    g.user = current_user


@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
def home():
    return redirect(url_for('sign_in'))


@application.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = unicode(request.form['username'])
        password = unicode(request.form['password'])

        if username is None or not username:
            flash(Markup('<strong>Psst!</strong> You forgot username.'), 'warning')
        elif password is None or not password:
            flash(Markup('<strong>Psst!</strong> You forgot password.'), 'warning')
        else:
            user = models.Users.query.filter_by(username=username).first()

            if user is None:
                flash(Markup("<strong>Oops!</strong> The username and password don't match."), 'danger')
            else:
                if not hashing.check_value(user.password, password, user.salt):
                    flash(Markup("<strong>Oops!</strong> The username and password don't match."), 'danger')
                elif not login_user(user):
                    flash(Markup('<strong>Ugh!</strong> ' + str(user.name) + ', your account is banned.'), 'danger')
                else:
                    flash(Markup('<strong>Welcome ' + str(g.user.name) + '!</strong>'), 'success')

                    # return redirect(url_for('dashboard'))
                    return render_template('base.html')

    return render_template('sign_in.html')


@login_manager.user_loader
def user_loader(id):
    return models.Users.query.get(id)