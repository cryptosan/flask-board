# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, abort, g, session, redirect, url_for
from flask.ext.login import login_required, current_user
from jinja2 import TemplateNotFound
from .forms import LoginForm, RegisterForm
from app.models import User, Role


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.before_request
def auth_bf_req():
    g.user = current_user


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/index', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and User.check_password(user.pw_hash, form.password.data):
            session['email'] = form.email.data
            session['nickname'] = form.nickname.data
            return redirect(url_for('index'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    # if g.user.is
    return "Logout page"


@auth.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_role = Role.query.filter_by(name='User').first()
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            pw_hash=User.make_a_hash(form.password.data),
            role_id=user_role)
        db.session.add(user)
        db.session.commit()
    return render_template('auth/register.html', form=form)


@auth.route('/apply')
def register_apply():
    return "apply page"
