# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import app
from .auth import auth
from .board import board
from flask import render_template


@app.errorhandler(404)
@auth.errorhandler(404)
@board.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
@auth.errorhandler(500)
@board.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


@app.errorhandler(403)
@auth.errorhandler(403)
@board.errorhandler(403)
def forbidden_error(e):
    return render_template('errors/403.html'), 403
