# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.ext.mail import Message
from flask import render_template
from threading import Thread
from app import app, mail

# If there are many email task, thread will make a new thread for every email.
# So let me see about 'Celery'

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# Todo: Build up mail service by Celery.
# Todo: Unittest.
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=list(to))
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email(), args=[app, msg])
    thr.start()
    return thr

