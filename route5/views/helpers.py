#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com


from flask import session
from route5.settings import ROOT_USER

### Context related helpers
from route5.models import db_users
from route5.views.code5 import get_str_code5, get_api_token


def get_context():
    ### check db sync
    if "user" in session and not db_users.find_one({"_id": session["user"]["_id"]}):
        session.clear()
    context = {}
    if "user" in session:
        session["user"] = db_users.find_one({"_id": session["user"]["_id"]})
        context["user"] = session["user"]
        context["str_code5"] = get_str_code5(session["user"]["user_code5"])
        session["code5"] = session["user"]["user_code5"]

        if session["user"]["user_type"] == "business":
            context["user"]["api_token"] = get_api_token(session["user"]["user_code5"])

        session["isroot"] = False
        if session["user"]["user_username"] == ROOT_USER:
            session["isroot"] = True
            context["admin"] = True

    return context
