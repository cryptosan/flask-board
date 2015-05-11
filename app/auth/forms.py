# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.wtf import Form
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo, Required


class LoginForm(Form):
    title = "Login Page"
    email = StringField('Email',
                        [DataRequired(),
                         Length(1, 64),
                         Email('It\'s not an Email!')])
    password = PasswordField('Password',
                             [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Submit')


class RegisterForm(Form):
    title = "Register Page"
    email = StringField('Email',
                        [DataRequired(),
                         Email('It\'s not an Email!')])
    nickname = StringField('Nickname',
                           [DataRequired(),
                            Length(min=4, max=12)])
    password = PasswordField('New Password',
                             [DataRequired(),
                              EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
