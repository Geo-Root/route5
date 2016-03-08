#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

from flask.ext import wtf
from flask.ext.wtf import Form
import wtforms
from wtforms.fields import TextField, BooleanField, PasswordField, TextAreaField, SelectField, HiddenField
from wtforms import validators


class LoginForm(Form):
    
    user_username = TextField(label="Username", validators=[validators.Required(), validators.Length(min=4, max=25)])
    user_password = PasswordField(label="Password", validators=[validators.Required()])


class RegisterForm(Form):

    user_username = TextField(label="Username", validators=[validators.Required(), validators.Length(min=4, max=25)])
    user_password1 = PasswordField(label="Password", validators=[validators.Required(), validators.Length(min=3)])
    user_password2 = PasswordField(label="Repeat password", validators=[validators.Required(),  validators.EqualTo('user_password1', message='Passwords must match')])
    user_email = TextField(label="Email", validators=[validators.Required(), wtforms.validators.Email()])
    user_name = TextField(label="Your name", validators=[validators.optional()])
    user_lastname = TextField(label="Your lastname", validators=[validators.optional()])
    user_mobile = TextField(label="Mobile number", validators=[validators.Required()])
    user_language = SelectField(label="Language", choices=[("Eng", "English")], default=("Eng", "English"), validators=[validators.optional()])
    user_code5 = HiddenField(label="Code5", validators=[]) # TODO: add custom validator for code5
    user_promotion_code = TextField(label="Promotion", validators=[validators.optional()])

    def validate_user_code5(self, field):
        pass

    def generate_code5(self):
        pass

class UserRegisterForm(RegisterForm):
    pass

class ShipperRegisterForm(RegisterForm):
    pass

class BusinessRegisterForm(RegisterForm):
    pass


class PromotionCodeForm(Form):

    promotion_code = None
