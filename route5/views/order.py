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
from route5.views.code5 import get_next_code5
from route5.views.helpers import get_context, redirect_url
from route5 import ALLOWED_EXTENSIONS
from route5.settings import SECRET_KEY
from route5.models import db_users, helper_signup, db_contacts, db_messages, db_orders, db_places
import hashlib
from route5.forms import *
import time
import datetime


def create_order():
    d = get_context()
    return ""

def delete_order():
    return ""

def update_order():
    return ""

def confirm_order():
    return ""

def get_shippers():
    return ""


def orders():
    d = get_context()

    form = ShipmentForm(request.form)
    d["form"] = form
    me = session["user"]["user_username"].lower()
    d["my_orders"] = db_orders.find({"sh_user": me})
    return render_template("orders.html", d=d)


def order(oid):
    d = get_context()
    me = session["user"]["user_username"].lower()
    d["order"] = db_orders.find({"sh_user": me, '_id': oid})
    return render_template("order_view.html", d=d)


def order_shipment():
    d = get_context()
    form = ShipmentForm(request.form)
    d["form"] = form
    return render_template("order.html", d=d)

def helper_address(form):
    obj = {
        "user": session["user"]["_id"],
        "street1": form["street1"],
        "street2": form["street2"],
        "city": form["city"],
        "state": form["state"],
        "zip": form["zip"],
        "country": form["country"],
        "code5": form["code5"],
        "str_code5": form["str_code5"],
        "type": form["type"],
        "address": form["user_address"],
        "lat": form["lat"],
        "lon": form["lon"],
    }
    db_places.save(obj)
    return True, form, obj


def manage_places():
    d = get_context()
    if request.method == "POST":
        status, form, address = helper_address(request.form)
        if not status:
            flash(u"Failed to add address, please, choose other", "error")
            return render_template('manage_places.html', d=d)
        flash('Address added')
        return redirect(url_for("manage_places"))
    d["code5"], d["str_code5"] = get_next_code5()
    d["places"] = [x for x in db_places.find({"user":session["user"]["_id"]})]
    return render_template("manage_places.html", d=d)


def delete_place(code5):
    db_places.remove({"user":session["user"]["_id"], "code5": code5})
    return redirect(url_for("manage_places"))
    

app.add_url_rule('/orders', 'orders', orders, methods=['GET', 'POST'])
app.add_url_rule('/order', 'order_shipment', order_shipment, methods=['GET', 'POST'])
app.add_url_rule('/order/<oid>', 'order', order, methods=['GET', 'POST'])

app.add_url_rule('/places', 'manage_places', manage_places, methods=['GET', 'POST'])
app.add_url_rule('/rpc/place/delete/<code5>', 'delete_place', delete_place, methods=['GET', 'POST'])

app.add_url_rule('/rpc/order/create', 'create_order', create_order, methods=['GET', 'POST'])
app.add_url_rule('/rpc/order/delete', 'delete_order', delete_order, methods=['POST'])
app.add_url_rule('/rpc/order/update', 'update_order', update_order, methods=['POST'])
app.add_url_rule('/rpc/order/confirm', 'confirm_order', update_order, methods=['POST'])
app.add_url_rule('/rpc/order/shippers', 'confirm_order', update_order, methods=['GET', 'POST'])

