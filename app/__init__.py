# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')


# Init extends.
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
lm = LoginManager(app)


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
