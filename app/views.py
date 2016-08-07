#!/usr/bin/env python
# coding: utf-8

import random
import string

from flask import flash, g, Markup, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import application, database, hashing, login_manager, models
from forms import LoginForm, UserForm

USER_SALT_LENGTH = models.Users.salt.property.columns[0].type.length


@application.before_request
def before_request():
    g.user = current_user


@application.route('/', methods=['GET'])
def home():
    return redirect(url_for('sign_in'))


@application.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = unicode(login_form.username.data)
        password = unicode(login_form.password.data)

        if not username:
            flash(Markup('<strong>Psst!</strong> You forgot username.'), 'warning')
        elif not password:
            flash(Markup('<strong>Psst!</strong> You forgot password.'), 'warning')
        else:
            user = models.Users.query.filter_by(username=username).first()

            if not user:
                flash(Markup("<strong>Whops!</strong> The username and password don't match."), 'danger')
            else:
                if not hashing.check_value(user.password, password, user.salt):
                    flash(Markup("<strong>Whops!</strong> The username and password don't match."), 'danger')
                elif not login_user(user):
                    flash(Markup('<strong>Ugh!</strong> ' + str(user.name) + ', your account is banned.'), 'danger')
                else:
                    flash(Markup('<strong>Welcome ' + str(g.user.name) + '!</strong>'), 'success')

                    return redirect(request.args.get('next')) if request.args.get('next') \
                        else redirect(url_for('dashboard'))

    return render_template('sign_in.html', form=login_form)


@application.route('/sign_out', methods=['GET'])
@login_required
def sign_out():
    logged_name = g.user.name

    logout_user()

    flash(Markup('<strong>Bye, bye ' + str(logged_name) + '!</strong> Come back soon!'), 'success')

    return redirect(url_for('sign_in'))


@application.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')


# TODO: ADD POST FUNCTIONALITY & CHANGE TO FLASK-WTF FORM
@application.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@application.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')


@application.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_form = UserForm()

    user_form.name.render_kw['placeholder'] = g.user.name
    user_form.username.render_kw['placeholder'] = g.user.username
    user_form.email.render_kw['placeholder'] = g.user.email

    if user_form.validate_on_submit():
        name = unicode(user_form.name.data)
        username = unicode(user_form.username.data)
        email = unicode(user_form.email.data)
        new_password = unicode(user_form.new_password.data)
        # TODO: CHECK IF ".data" IS RIGTH PROPERTY
        avatar = user_form.avatar.data

        user = models.Users.query.get(g.user.id)

        if name and name != user.name:
            user.name = name

        if username and username != user.username:
            user.username = username

        if email and email != user.email:
            user.email = email

        if new_password:
            user.salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(USER_SALT_LENGTH))
            user.password = hashing.hash_value(new_password, user.salt)

        database.session.commit()

        # TODO: CHANGE AVATAR

        flash(Markup('<strong>Yahoo!</strong> All data has been changed successfully!'), 'success')

        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=user_form)


@application.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('about.html')


@application.route('/validate', methods=['GET'])
def validate():
    if request.args.get('username') != g.user.username \
            and models.Users.query.filter_by(username=request.args.get('username')).first():
        return redirect(url_for('edit_profile')), 406

    if request.args.get('email') != g.user.email \
            and models.Users.query.filter_by(email=request.args.get('email')).first():
        return redirect(url_for('edit_profile')), 406

    if request.args.get('old_password') \
            and not hashing.check_value(g.user.password, request.args.get('old_password'), g.user.salt):
        return redirect(url_for('edit_profile')), 406

    return redirect(url_for('edit_profile')), 200


@login_manager.user_loader
def user_loader(id):
    return models.Users.query.get(id)
