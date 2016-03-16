#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flaskext.auth import permission_required
from flask import render_template, url_for, redirect, g, Response, request, flash, session
from route5 import app, roles
from route5.forms import *
from route5.models import db_users, helper_signup
from route5.views.code5 import get_next_code5
from flask.ext.bcrypt import Bcrypt, generate_password_hash
import datetime
from route5.views.helpers import get_context


def amdin_certification():
    return ""


def amdin_users():
    d = get_context()
    d["users"] = [x for x in db_users.find()]
    return render_template("admin_users.html", d=d)

app.add_url_rule('/root/users', 'amdin_users', amdin_users, methods=['GET'])
app.add_url_rule('/root/certification', 'amdin_certification', amdin_certification, methods=['POST'])






