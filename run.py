#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 03.03.2016
#@author: Alex Ferechin
#@contact: alex.ferechin@gmail.com

'''
Wrapper for local server running.
'''
import sys
import os
from route5.settings import TEST_SERVER_PORT, WORKING_DIR, DEV_WORKING_DIR
import yaml

def load_settings(file_name):
	pass

### Load settings from yaml file

file_name = os.path.join("instance/settings.yaml")
settings = load_settings(file_name)

current_dir = WORKING_DIR #os.path.dirname(os.path.realpath(__file__))
if not os.path.isdir(WORKING_DIR):
	current_dir = DEV_WORKING_DIR
	if not os.path.isdir(DEV_WORKING_DIR):
		print("Wrong working dir: %s" % WORKING_DIR)
		sys.exit(2)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

print parent_dir

from route5 import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=TEST_SERVER_PORT)
