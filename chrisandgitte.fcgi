#!/usr/bin/python

import os
import sys

from flup.server.fcgi import WSGIServer
from main import app

def add_to_sys_path ():
    this_dir = os.path.dirname(__file__)
    site_packages_dir = '{0}/.meta/virtualenv/lib/python2.7/site-packages'.format(this_dir) 
    sys.path.insert(0, this_dir)
    sys.path.insert(0, site_packages_dir)

add_to_sys_path()

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '%'
    WSGIServer(app).run()
