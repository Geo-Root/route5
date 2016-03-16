#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

import os
from flask import session, render_template, url_for, redirect, request
from route5 import app, roles
from route5.views.helpers import get_context
from route5 import ALLOWED_EXTENSIONS
from route5.settings import SECRET_KEY
from route5.models import db_users, helper_signup
import hashlib
from route5.forms import *
import time


def get_my_image():
    if "user_image" in session["user"]:
        return os.path.join("/static/uploads", session["user"]["user_image"])
    return "http://www.golenbock.com/wp-content/uploads/2015/01/placeholder-user-150x150.png"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_profile_photo():
    """ Upload profile image to user profile.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = hashlib.sha224(str(session["user"]["user_code5"])+SECRET_KEY).hexdigest()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session["user"]["user_image"] = filename
            db_users.save(session["user"])
    return redirect(url_for("user_profile"))


def save_user_profile():

    d = get_context()
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        status, form, user = helper_signup(form, utype="user", update=True)
        session["user"] = user
        redirect_url = "%s_profile" % session["user"]["user_type"]
        return redirect(url_for(redirect_url))
    d["form"] = form
    template_name = "profile_%s.html" % session["user"]["user_type"]
    return render_template(template_name, d=d)


# @permission_required(resource='all', action='view')
def user_profile():
    """ Controller for user profile page.
    """
    d = get_context()
    if not "user" in session:
        return redirect(url_for("signup"))
    template_name = "profile_%s.html" % d["user"]["user_type"]
    if "user_image" in d["user"]:
        d["user"]["profile_image"] = os.path.join("/static/uploads", d["user"]["user_image"]) + "?%s" % time.clock()
    form = UserForm(request.form)

    d["form"] = form
    for key, value in d["user"].items():
        if value and key in d["form"].data:
            if key in d["form"].data:
                getattr(d["form"], key).data = value

    return render_template(template_name, d=d)


def shipper_profile():
    """ Controller for user profile page.
    """
    d = get_context()
    if not "user" in session:
        return redirect(url_for("signup"))
    template_name = "profile_%s.html" % d["user"]["user_type"]
    if "user_image" in d["user"]:
        d["user"]["profile_image"] = os.path.join("/static/uploads", d["user"]["user_image"]) + "?%s" % time.clock()
    form = UserForm(request.form)

    d["form"] = form
    for key, value in d["user"].items():
        if value and key in d["form"].data:
            if key in d["form"].data:
                getattr(d["form"], key).data = value

    return render_template(template_name, d=d)

def business_profile():
    d = get_context()
    if not "user" in session:
        return redirect(url_for("signup"))
    template_name = "profile_%s.html" % d["user"]["user_type"]
    if "user_image" in d["user"]:
        d["user"]["profile_image"] = os.path.join("/static/uploads", d["user"]["user_image"]) + "?%s" % time.clock()
    form = UserForm(request.form)

    d["form"] = form
    for key, value in d["user"].items():
        if value and key in d["form"].data:
            if key in d["form"].data:
                getattr(d["form"], key).data = value

    return render_template(template_name, d=d)

app.add_url_rule('/profile', 'user_profile', user_profile, methods=['GET'])
app.add_url_rule('/profile', 'user_profile', shipper_profile, methods=['GET'])
app.add_url_rule('/profile', 'business_profile', business_profile, methods=['GET'])
app.add_url_rule('/rpc/save/user_profile', 'save_user_profile', save_user_profile, methods=['POST'])
app.add_url_rule('/upload/profile', 'upload_profile_photo', upload_profile_photo, methods=['GET', 'POST'])
app.add_url_rule('/rpc/me/image', 'get_my_image', get_my_image, methods=['GET'])
