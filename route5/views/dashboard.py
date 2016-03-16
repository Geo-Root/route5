#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com


from flask import session, render_template, url_for, redirect
from route5 import app, roles
from route5.views.helpers import get_context


# @permission_required(resource='all', action='view')
def dashboard():
    """ Controller for main page.
    """
    d = get_context()
    if "user" not in session:
        return redirect(url_for("signup"))
    template_name = "dashboard_%s.html" % d["user"]["user_type"]

    return render_template(template_name, d=d)


def index():
    return redirect(url_for("dashboard"))


app.add_url_rule('/', 'index', index, methods=['GET'])
app.add_url_rule('/index', 'index', index, methods=['GET'])
app.add_url_rule('/dashboard', 'dashboard', dashboard, methods=['GET'])
