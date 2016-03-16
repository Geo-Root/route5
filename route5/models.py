#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com


import pymongo
from pymongo import MongoClient as Connection
from PyExp import AbstractModel
from flask.ext.bcrypt import Bcrypt, generate_password_hash
from flask import session
import datetime

db_users = Connection("localhost", 27017)["Route5"]["Users"]
db_code5 = Connection("localhost", 27017)["Route5"]["Code5"]


class Code5(AbstractModel):
    pass

class Promotions(AbstractModel):
    pass

class User(AbstractModel):

    dumpable_attributes = [
        'username',
        'password',
        'code5',
        'is_shipper',
        'is_user',
        'is_business',
        'email',
        'first_name',
        'last_name',
        'mobile',
        'is_email_confirmed',
        'address',
    ]

    def __init__(self, form=None):
        super(AbstractModel, self).__init__()


class ShipperUser(User):
    
    def __init__(self, form=None):
        super(User, self).__init__()


class BusinessUser(User):
    
    def __init__(self, form=None):
        super(User, self).__init__()


def helper_signup(form, utype="user", update=False):
    """ Helper function for any user registration.
    """
    # user = User(form=form) # TODO: not dict fix it
    key_field = form.user_username.data.lower()
    if not update:
        user = db_users.find_one({"_id": key_field})
        if user:
            form.user_username.errors.append("User exists")
            return False, form, None
        user = {}
        user['_id'] = key_field
        user['user_username'] = form.user_username.data
        user['user_promotion_code'] = form.user_promotion_code.data
        user['user_email'] = form.user_email.data
        user['user_registration_date'] = datetime.datetime.utcnow()
        user['user_type'] = utype
        user['user_code5'] = session["code5"]
        password = form.user_password1.data
        user["user_password"] = generate_password_hash(password, 12)

        code5_obj = db_code5.find_one({"_id": user["user_code5"]})
        if not code5_obj:
            ### get other code5
            pass
        code5_obj["is_used"] = key_field
        code5_obj["is_booked"] = 0
        db_code5.save(code5_obj)

    else:
        user = db_users.find_one({"_id": key_field})
        if not user:
            return False, form, None


    user['user_name'] = form.user_name.data
    user['user_lastname'] = form.user_lastname.data
    user['user_mobile'] = form.user_mobile.data
    user['user_language'] = form.user_language.data

    db_users.save(user)



    return True, form, user
