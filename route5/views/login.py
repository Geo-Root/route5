#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flaskext.auth import permission_required
from flask import render_template, url_for, redirect, g, Response, request, flash, session
from route5 import auth
from route5 import app, roles
from route5.forms import *
from route5.models import db_users
from route5.views.code5 import get_next_code5
from flask.ext.bcrypt import Bcrypt, generate_password_hash
import datetime

bcrypt = Bcrypt(app)

def login():
    d = get_context()
    form = LoginForm(request.form)
    d["login_form"] = form
    d["shipper_form"] = ShipperRegisterForm()
    d["user_form"] = UserRegisterForm()
    d["focus"] = "login"
    if request.method == "POST" and form.validate():
        key_field = form.user_username.data.lower()
        obj = db_users.find_one({"_id":key_field})
        if not obj:
            email_field = form.user_username.data.lower()
            obj = db_users.find_one({"user_email":email_field})
            if not obj:
                form.user_username.errors.append("No such user")
                d["login_form"] = form
                return render_template('signup.html', d=d)

        if not bcrypt.check_password_hash(obj["user_password"], form.user_password.data):
            form.user_password.errors.append("Wrong password")
            d["login_form"] = form
            return render_template('signup.html', d=d)
        else:
            session["user"] = obj
            flash("Welcome back %s" % obj["user_username"])
            return redirect(url_for("index"))
    return render_template("signup.html", d=d)
    
    # callback=url_for('authorized', _external=True)
    # return google.authorize(callback=callback)


def logout():
    session.clear()
    flash("You can login back")
    return redirect(url_for("index"))


def get_access_token():
    return session.get('access_token')


def helper_signup(form, utype="user"):

    status = None
    # user = User(form=form) # TODO: not dict fix it
    user = {
        'user_username': form.user_username.data,
        'user_password1': form.user_password1.data, # TODO: now raw, fix it
        'user_email': form.user_email.data,
        'user_name': form.user_name.data,
        'user_lastname': form.user_lastname.data,
        'user_mobile': form.user_mobile.data,
        'user_language': form.user_language.data,
        'user_code5': session["code5"],
        'user_promotion_code': form.user_promotion_code.data,
        'user_registration_date': datetime.datetime.utcnow(),
        'user_type': utype,
    }
    user["user_password"] = generate_password_hash(user["user_password1"], 12)
    del user["user_password1"]

    key_field = user['user_username'].lower()
    obj = db_users.find_one({"_id":key_field})
    if obj:
        form.user_username.errors.append("User exists")
        return False, form, None
    user["_id"] = key_field
    db_users.save(user)
    return True, form, user

def signup():
    ''' Shipper signup page, currently generic.
    '''
    if "user" in session:
        flash("Please logout")
        return redirect(url_for("index"))

    d = get_context()
    d["focus"] = "login"
    if not code5 in session:
        code5, str_code5 = get_next_code5()
        session["code5"] = code5
        session["str_code5"] = str_code5
    d["user_code5"] = session["str_code5"]
    d["login_form"] = LoginForm(request.form)
    d["shipper_form"] = ShipperRegisterForm(request.form)
    d["user_form"] = UserRegisterForm(request.form)
    return render_template('signup.html', d=d)

def signup_user():
    ''' User signup page, currently generic.
    '''
    d = get_context()
    form = UserRegisterForm(request.form)
    d["user_form"] = form

    d["login_form"] = LoginForm()
    d["shipper_form"] = ShipperRegisterForm()
    
    d["focus"] = "user"
    if request.method == "POST" and form.validate():
        status, form, user = helper_signup(form, utype="user")
        if not status:
            d["from"] = form
            return render_template('signup.html', d=d)
        flash('Thank you for registering')
        session["user"] = user
        return redirect(url_for("index"))
    if not "user_code5" in d:
        code5, d["user_code5"] = get_next_code5()
    return render_template('signup.html', d=d)

def signup_shipper():
    ''' Shipper signup page, currently generic.
    '''
    d = get_context()
    form = ShipperRegisterForm(request.form)
    d["shipper_form"] = form
    d["focus"] = "shipper"

    d["login_form"] = LoginForm()
    d["user_form"] = UserRegisterForm()

    if request.method == "POST" and form.validate():
        status, form, user = helper_signup(form, utype="shipper")
        if not status:
            d["from"] = form
            return render_template('signup.html', d=d)
        flash('Thank you for registering')
        session["user"] = user
        return redirect(url_for("index"))
    if not "user_code5" in d:
        code5, d["user_code5"] = get_next_code5()
    return render_template('signup.html', d=d)

def signup_code5():
    pass

### Context related controllers and helpers

def get_context():
    context = {}
    if "user" in session:
        context["user"] = session["user"]
    return context

### Main controllers
# @permission_required(resource='all', action='view')
def index():
    ''' Index page.
    '''
    if not "user" in session:
        return redirect(url_for("signup"))
    d = get_context()
    return render_template('index.html', d=d)


app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/signup', 'signup', signup, methods=['GET'])
app.add_url_rule('/user-signup', 'signup_user', signup_user, methods=['POST'])
app.add_url_rule('/code5-signup', 'signup_code5', signup_code5, methods=['POST'])
app.add_url_rule('/shipper-signup', 'signup_shipper', signup_shipper, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])
app.add_url_rule('/index', 'index', index, methods=['GET'])





