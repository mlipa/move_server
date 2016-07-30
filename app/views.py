#!/usr/bin/env python
# coding: utf-8

import os

from flask import flash, g, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import application, database, hashing, login_manager, models
from forms import UserForm

USER_SALT_LENGTH = models.Users.salt.property.columns[0].type.length


@application.before_request
def before_request():
    g.user = current_user


@application.route('/', methods=['GET'])
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

                    return redirect(url_for('dashboard'))

    return render_template('sign_in.html')


@application.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@application.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('settings.html')


@application.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        logged_name = str(g.user.name)

        logout_user()

        flash(Markup('<strong>Bye, bye ' + logged_name + '!</strong> Come back soon!'), 'success')

        return redirect(url_for('sign_in'))

    return render_template('profile.html', user=g.user, avatar=g.user.get_avatar())


@application.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserForm()

    form.name.render_kw['placeholder'] = g.user.name
    form.username.render_kw['placeholder'] = g.user.username
    form.email.render_kw['placeholder'] = g.user.email

    if request.method == 'POST' and form.validate_on_submit():
        name = unicode(request.form['name'])
        username = unicode(request.form['username'])
        email = unicode(request.form['email'])
        old_password = unicode(request.form['old_password'])
        new_password = unicode(request.form['new_password'])
        confirm_new_password = unicode(request.form['confirm_new_password'])
        avatar = unicode(request.form['avatar'])

        user = models.Users.query.filter_by(id=g.user.id).first()

        if name == user.name:
            flash(Markup('<strong>Oops!</strong> The given name was the same as your current one.'), 'warning')
        elif not name is None and name:
            user.name = name

            flash(Markup('<strong>Hello ' + str(name) + '!</strong> Your name has been changed successfully!'),
                  'success')

        if username == user.username:
            flash(Markup('<strong>Oops!</strong> The given username was the same as your current one.'), 'warning')
        elif username == 'default_avatar' or username == 'admin':
            flash(Markup('<strong>Error!</strong> The given username is restricted.'), 'danger')
        elif models.Users.query.filter_by(username=username).first():
            flash(Markup('<strong>Bad luck!</strong> The given username is reserved by another user.'), 'danger')
        elif not username is None and username:
            app_directory = os.path.abspath(os.path.dirname(__file__))
            avatar = g.userget_avatar()

            if g.user.username in avatar:
                os.rename(app_directory + avatar,
                          app_directory + url_for('static', filename='img/' + username + '.png'))

            user.username = username

            flash(Markup('<strong>Hello ' + str(username) + '!</strong> Your username has been changed successfully!'),
                  'success')

        if email == user.email:
            flash(Markup('<strong>Oops!</strong> The given e-mail was the same as your current one.'), 'warning')
        elif models.Users.query.filter_by(email=email).first():
            flash(Markup('<strong>Bad luck!</strong> The given e-mail is reserved by another user.'), 'danger')
        elif not email is None and email:
            user.email = email

            flash(Markup('<strong>Hello ' + str(email) + '!</strong> Your e-mail has been changed successfully!'),
                  'success')

        database.session.commit()

        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form, avatar=g.user.get_avatar())


@application.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('about.html')


@login_manager.user_loader
def user_loader(id):
    return models.Users.query.get(id)
