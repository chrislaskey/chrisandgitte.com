#!/usr/bin/python

# if __name__ == '__main__':
#     print('testing it')

# import sys
# sys.path.insert(0, '<your_path>/lib/python2.6/site-packages')
# '''
from flup.server.fcgi import WSGIServer
from main import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()
# '''
