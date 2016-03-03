#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flask.ext import wtf
from flask.ext.wtf import Form
import wtforms
from wtforms.fields import TextField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required 

class LoginForm(Form):
    
    user_nickname = None
    user_password = None

class RegisterForm(Form):
    
    user_nickname = None
    user_password1 = None
    user_password2 = None
    user_email = None
    user_name = None
    user_surname = None
    user_mobile = None
    user_code5 = None
    user_promotion_code = None

class PromotionCodeForm(Form):

    promotion_code = None
