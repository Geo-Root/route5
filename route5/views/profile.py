#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

import os
from collections import defaultdict

from flask import session, render_template, url_for, redirect, request, flash
from route5 import app, roles
from route5.views.helpers import get_context, redirect_url
from route5 import ALLOWED_EXTENSIONS
from route5.settings import SECRET_KEY
from route5.models import db_users, helper_signup, db_contacts, db_messages
import hashlib
from route5.forms import *
import time
import datetime


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


def get_profile(username):
    d = get_context()
    user_obj = db_users.find_one({"_id":username.lower()})
    if not user_obj:
        flash("Profile for %s not found" % username)
        return redirect(redirect_url())
    d["profile"] = user_obj
    key = "%s:%s" % (session["user"]["user_username"], username.lower())
    d["incontacts"] = False
    if db_contacts.find_one({"_id": key}):
        d["incontacts"] = True
    return render_template("profile_view.html", d=d)


def add_to_contacts(username):
    user_obj = db_users.find_one({"_id": username.lower()})
    if not user_obj:
        flash("User %s not found" % username)
        return redirect(redirect_url())
    me = session["user"]["user_username"].lowet()
    key = "%s:%s" % (me, username.lower())
    db_contacts.save({"_id": key, "a": me, "b": username.lower(), "type": user_obj["user_type"]})
    return redirect(redirect_url())


def del_from_contacts(username):
    user_obj = db_users.find_one({"_id": username.lower()})
    if not user_obj:
        flash("User %s not found" % username)
        return redirect(redirect_url())
    key = "%s:%s" % (session["user"]["user_username"], username.lower())
    db_contacts.remove({"_id": key})
    return redirect(redirect_url())


def send_email(username):
    d = get_context()
    me = session["user"]["user_username"].lower()
    user_obj = db_users.find_one({"_id": username.lower()})
    if not user_obj:
        flash("Profile for %s not found" % username)
        return redirect(redirect_url())
    if request.method == "POST":
        obj = {
            "a": me,
            "b": username.lower(),
            "type": user_obj["user_type"],
            "message": request.form["message"],
            "stamp": time.time(),
            "unread": True,
        }
        db_messages.save(obj)

    d["profile"] = user_obj
    d["messages"] = [x for x in db_messages.find({'a': me, 'b': username.lower()})] + [x for x in db_messages.find({'b': me, 'a': username.lower()})]
    d["messages"].sort(key=lambda x: x["_id"])
    now = time.time()
    for i, x in enumerate(d["messages"]):
        c = now - x["stamp"]
        d["messages"][i]["minutes"] = int(c/60)
        if x["b"] == me:
            x["unread"] = False
        db_messages.save(x)

    return render_template("messages.html", d=d)


def show_contacts():
    d = get_context()
    me = session["user"]["user_username"].lower()
    d["messages"] = [x for x in db_messages.find({'a': me})] + [x for x in db_messages.find({'b': me})]

    user2m = defaultdict(list)
    for m in d["messages"]:
        if m['a'] != me:
            user2m[m['a']].append(m)
        else:
            user2m[m['b']].append(m)
    unreads = defaultdict(int)
    for user, messages in user2m.items():
        unreads[user] = len([x for x in messages if x["unread"]])
    d["unreads"] = unreads
    d["user2m"] = user2m

    my_contacts = db_contacts.find({"a":me})
    for obj in my_contacts:
        if obj["b"] in user2m:
            continue
        d["unreads"][obj["b"]] = 0
        d["user2m"][obj["b"]] = []

    return render_template("contacts.html", d=d)

app.add_url_rule('/profile', 'user_profile', user_profile, methods=['GET'])
app.add_url_rule('/profile', 'shipper_profile', shipper_profile, methods=['GET'])
app.add_url_rule('/profile', 'business_profile', business_profile, methods=['GET'])
app.add_url_rule('/rpc/save/user_profile', 'save_user_profile', save_user_profile, methods=['POST'])
app.add_url_rule('/upload/profile', 'upload_profile_photo', upload_profile_photo, methods=['GET', 'POST'])
app.add_url_rule('/rpc/me/image', 'get_my_image', get_my_image, methods=['GET'])
app.add_url_rule('/user/<username>', 'get_profile', get_profile, methods=['GET'])
app.add_url_rule('/rpc/contacts/add/<username>', 'add_to_contacts', add_to_contacts, methods=['GET'])
app.add_url_rule('/rpc/contacts/del/<username>', 'del_from_contacts', del_from_contacts, methods=['GET'])
app.add_url_rule('/messages/<username>', 'send_email', send_email, methods=['GET', 'POST'])
app.add_url_rule('/messages', 'show_contacts', show_contacts, methods=['GET'])
