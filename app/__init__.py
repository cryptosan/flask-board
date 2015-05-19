# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.mail import Mail


app = Flask(__name__)
app.config.from_object('config')

# Mail server setting.
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# You have to set up MAIL_USERNAME, and MAIL_PASSWORD into your bash.
# for Linux or Mac OSX
# (venv) $ export MAIL_USERNAME=<Gmail username>
# (venv) $ export MAIL_PASSWORD=<Gmail password>
# for Windows
# (venv) $ set MAIL_USERNAME=<Gmail username>
# (venv) $ set MAIL_PASSWORD=<Gmail password
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_RECEIVER'] = os.environ.get('MAIL_RECEIVER')

import top
app.config['MAIL_USERNAME'] = top.USERNAME
app.config['MAIL_PASSWORD'] = top.PASSWORD
app.config['MAIL_RECEIVER'] = top.RECEIVER

# Custom setting on Mail
app.config['MAIL_SUBJECT_PREFIX'] = 'FROSTLAB - '
app.config['MAIL_SENDER'] = 'FrostLab'


# Init extends.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager(app)
mail = Mail(app)


# Blueprint
from app.auth import auth
from app.board import board
from app.profile import profile
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(board, url_prefix='/board')
app.register_blueprint(profile, url_prefix='/profile')


# A function that system requests login to users.
lm.session_protection = 'strong'
lm.login_view = 'auth.login'


from app import views, errors
