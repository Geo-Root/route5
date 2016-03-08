#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com


import pymongo
from pymongo import MongoClient as Connection
from PyExp import AbstractModel

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

