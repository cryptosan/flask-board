# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    pw_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '[User %r]' % (self.nickname)

    # Password hash check
    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    # A function for unittest
    @staticmethod
    def make_a_hash(password):
        return bcrypt.generate_password_hash(password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '[Role %r]' % (self.name)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '[Post %r]' % (self.body)
