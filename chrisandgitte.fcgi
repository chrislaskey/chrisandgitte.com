#!/usr/bin/python

from lib.environment import Environment
Environment().add_virtualenv_site_packages_to_path()

from flup.server.fcgi import WSGIServer
from main import app
from flask.ext.sendmail import Mail

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)
app.jinja_env.line_statement_prefix = '%'
mail = Mail(app)
WSGIServer(app).run()
