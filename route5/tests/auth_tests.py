#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

import os
import route5
import unittest
import tempfile
from pymongo import MongoClient as Connection


class Route5TestCase(unittest.TestCase):

    def setUp(self):
        self.db_users = Connection("localhost", 27017)["Route5test"]["Users"]
        self.db_code5 = Connection("localhost", 27017)["Route5test"]["Code5"]
        route5.app.config["TESTING"] = True
        self.app = route5.app.test_client()

    def tearDown(self):
        self.db_users.drop()
        self.db_code5.drop()

    def test_empty_db(self):
        assert not [x for x in self.db_users.find()]
        assert not [x for x in self.db_code5.find()]

    def login(self, username, password):
        return self.app.post('/login', data=dict(
                user_username=username, user_password=password),
                follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('Alex', '12345')
        print rv.data


if __name__ == '__main__':

    unittest.main()
