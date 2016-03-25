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
from route5.models import db_users, helper_signup, db_contacts, db_messages, db_orders
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

app.add_url_rule('/orders', 'orders', orders, methods=['GET', 'POST'])
app.add_url_rule('/order', 'order_shipment', order_shipment, methods=['GET', 'POST'])
app.add_url_rule('/order/<oid>', 'order', order, methods=['GET', 'POST'])
app.add_url_rule('/rpc/order/create', 'create_order', create_order, methods=['GET', 'POST'])
app.add_url_rule('/rpc/order/delete', 'delete_order', delete_order, methods=['POST'])
app.add_url_rule('/rpc/order/update', 'update_order', update_order, methods=['POST'])
app.add_url_rule('/rpc/order/confirm', 'confirm_order', update_order, methods=['POST'])
app.add_url_rule('/rpc/order/shippers', 'confirm_order', update_order, methods=['GET', 'POST'])

