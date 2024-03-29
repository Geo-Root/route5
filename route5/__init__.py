#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com
"""
Flask application initiation.
"""

import os
from flask import Flask, session
from settings import *
from flask.ext.basicauth import BasicAuth
from flaskext.auth import Auth, AuthUser, Permission, Role, permission_required
from flask_oauth import OAuth




app = Flask('route5')
app.config.from_object('route5.settings')
app.config['DEBUG'] = DEBUG

app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'

app.config['BASIC_AUTH_USERNAME'] = BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = BASIC_AUTH_PASSWORD
app.config['BASIC_AUTH_FORCE'] = BASIC_AUTH_FORCE

auth = Auth(app, login_url_name='login')

all_create = Permission('all', 'create')
all_view = Permission('all', 'view')
all_guest = Permission('all', 'guest')

roles = {
    'admin': Role('admin', [all_create, all_view]),
    'guest': Role('guest', [all_guest]),
    'user': Role('userview', [all_view]),
    'shipper': Role('userview', [all_view]),
    'business': Role('userview', [all_view]),
}


def load_role(role_name):
    return roles.get(role_name)

auth.load_role = load_role

# oauth = OAuth()
# google = oauth.remote_app('google',
#                           base_url='https://www.google.com/accounts/',
#                           authorize_url='https://accounts.google.com/o/oauth2/auth',
#                           request_token_url=None,
#                           request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
#                                                 'response_type': 'code'},
#                           access_token_url='https://accounts.google.com/o/oauth2/token',
#                           access_token_method='POST',
#                           access_token_params={'grant_type': 'authorization_code'},
#                           consumer_key=GOOGLE_CLIENT_ID,
#                           consumer_secret=GOOGLE_CLIENT_SECRET)


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



import views.code5
import views.login
import views.dashboard
import views.profile
import views.admin
import views.order
import filters
