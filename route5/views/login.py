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

bcrypt = Bcrypt(app)


def login():
    """ Controller for log in user into Route5.
    """
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
            session["code5"] = obj["user_code5"]
            str_code5 = "".join(["0"*(3-len(x))+x for x in str(session["code5"])])
            session["str_code5"] = "%s-%s-%s-%s-%s" % (str_code5[:3], str_code5[3:6], str_code5[6:9], str_code5[9:12], str_code5[12:16])
            flash("Welcome back %s" % obj["user_username"])
            return redirect(url_for("index"))
    return redirect(url_for("signup"))


def logout():
    """ Controller for log out user.
    """
    session.clear()
    return redirect(url_for("index"))



def signup():
    """ Controller for generic signup/login page.
    """
    d = get_context()
    if "user" in session:
        flash("Please logout")
        return redirect(url_for("index"))
    d["focus"] = "login"
    if "code5" not in session:
        code5, str_code5 = get_next_code5()
        session["code5"] = code5
        session["str_code5"] = str_code5
    d["user_code5"] = session["str_code5"]
    d["login_form"] = LoginForm(request.form)
    d["shipper_form"] = ShipperRegisterForm(request.form)
    d["user_form"] = UserRegisterForm(request.form)
    return render_template('signup.html', d=d)


def signup_user():
    """ Controller for user signup page.
    """
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
    if "user_code5" not in d:
        code5, d["user_code5"] = get_next_code5()
    return render_template('signup.html', d=d)


def signup_shipper():
    """ Controller for shipper signup page.
    """
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
    if "user_code5" not in d:
        code5, d["user_code5"] = get_next_code5()
    return render_template('signup.html', d=d)


def signup_code5():
    raise NotImplemented


def signup_business():
    """ Controller for business signup page.
    """
    d = get_context()

    form = BusinessRegisterForm(request.form)
    d["shipper_form"] = ShipperRegisterForm()
    d["focus"] = "business"

    d["business_form"] = form
    d["user_form"] = UserRegisterForm()

    if request.method == "POST" and form.validate():
        status, form, user = helper_signup(form, utype="business")
        if not status:
            d["from"] = form
            return render_template('signup_business.html', d=d)
        flash('Thank you for registering')
        session["user"] = user
        return redirect(url_for("index"))
    if "user_code5" not in d:
        code5, d["user_code5"] = get_next_code5()
    return render_template('signup_business.html', d=d)


app.add_url_rule('/signup', 'signup', signup, methods=['GET'])
app.add_url_rule('/user-signup', 'signup_user', signup_user, methods=['POST'])
app.add_url_rule('/code5-signup', 'signup_code5', signup_code5, methods=['POST'])
app.add_url_rule('/shipper-signup', 'signup_shipper', signup_shipper, methods=['POST'])
app.add_url_rule('/business', 'signup_business', signup_business, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/logout', 'logout', logout, methods=['GET', 'POST'])





