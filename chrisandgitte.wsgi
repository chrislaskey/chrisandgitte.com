#!/usr/bin/env python

import os
import sys

def add_to_sys_path ():
	this_dir = os.path.dirname(__file__)
	site_packages_dir = '{0}/.venv/lib/python2.7/site-packages'.format(this_dir) 
	sys.path.insert(0, this_dir)
	sys.path.insert(0, site_packages_dir)

add_to_sys_path()

from main import app as application
application.jinja_env.line_statement_prefix = '%'
