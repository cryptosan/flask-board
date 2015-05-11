# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import app, lm
from app.auth import auth
from .models import User
from flask import render_template, redirect, g, url_for, request, session
from flask.ext.login import current_user, login_user, logout_user, login_required


@lm.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@login_required
def index():
    return render_template('index.html')
