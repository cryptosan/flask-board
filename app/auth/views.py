# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Blueprint, render_template, abort, g, session, redirect, url_for, flash, request
from flask.ext.login import login_required, current_user, logout_user, login_user
from jinja2 import TemplateNotFound
from .forms import LoginForm, RegisterForm
from ..models import User, Role
from ..mail import send_email
from .. import db, app


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.before_request
def auth_bf_req():
    g.user = current_user


@auth.before_app_request
def before_request():
    if current_user.is_authenticated() and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/index', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # msg
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and User.check_password(user.pw_hash, form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


# Todo: logout unittest.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


# Todo: register unittest.
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.validate_email(form.email)
        form.validate_nickname(form.nickname)

        user_role = Role.query.filter_by(name='User').first()
        user = User(email=form.email.data,
                    nickname=form.nickname.data,
                    pw_hash=User.make_a_hash(form.password.data),
                    role_id=user_role.id)

        # Warning!,
        # If SQL field type and parameter type are different, if raise an error on DB commit
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(app.config['MAIL_RECEIVER'], 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# Todo: Implement confirm.
# Todo: confirm unittest.
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
        return redirect(url_for('index'))


# Todo: Implement unconfirm
@auth.route('/unconfirm')
def unconfirm():
    if current_user.is_anonymouse() or current_user.confirmed:
        return redirect('index')
    return render_template('auth/email/unconfirmed.html')
