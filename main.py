#!/Users/laskey/.virtualenv/chrisandgitte/bin/python

# from flask import Flask, abort, request, redirect, url_for, render_template, g
from flask import Flask, request, g
from app.config.appsetup import AppSetup
from app.library.requestparser import PageRequestParser, AdminPageRequestParser

# Setup app
# -----------------------------------------------------------------------------
app = Flask(__name__)

# Use a single % rather than {% %} in templates
app.jinja_env.line_statement_prefix = '%'

# Routing functions
# -----------------------------------------------------------------------------
@app.route('/admin')
def route_admin():
    common_admin_page_processing()
    return 'admin'

@app.route('/', defaults={'lang': 'en'})
@app.route('/<lang>')
def route_homepage(lang):
    common_page_processing()
    return 'homepage'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def route_catch_all(path):
    common_page_processing()
    return str(g.requestvars['language'])

# Routing error functions
# -----------------------------------------------------------------------------
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('error.html'), 404

# Utility functions
# -----------------------------------------------------------------------------
def common_page_processing():
    set_page_requestvars()

def set_page_requestvars():
    g.requestvars = PageRequestParser(request).return_requestvars()

def common_admin_page_processing():
    set_admin_page_requestvars()

def set_admin_page_requestvars():
    g.requestvars = AdminPageRequestParser(request).return_requestvars()

# Load app
# =============================================================================
if __name__ == '__main__':
    app_config = {
        'debug_mode_on_hostnames': ('laskey.local', 'cnsmac3.bu.edu')
    }
    app_setup = AppSetup(app_config).return_setup()
    app.run(**app_setup)
