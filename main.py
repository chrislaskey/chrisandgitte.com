#!/usr/bin/env python

from lib.environment import Environment
Environment().add_virtualenv_site_packages_to_path()

# from flask import Flask, abort, request, redirect, url_for, render_template, g
from flask import Flask, g, render_template, request
from config.appsetup import AppSetup
from lib.requestparser import PageRequestParser, AdminPageRequestParser
from lib.templateparser import TemplateVariableParser

app = Flask(__name__)

# Routing

@app.route('/<lang>/ceremony-and-reception/')
def ceremony_and_reception(lang):
    common_page_processing()
    return render_template('site/ceremony-and-reception.html', **g.templatevars)

@app.route('/<lang>/wedding-party/')
def wedding_party(lang):
    common_page_processing()
    return render_template('site/wedding-party.html', **g.templatevars)

@app.route('/<lang>/getting-here/')
def getting_here(lang):
    common_page_processing()
    return render_template('site/getting-here.html', **g.templatevars)

@app.route('/<lang>/your-time-in-maine/')
def your_time_in_maine(lang):
    common_page_processing()
    return render_template('site/your-time-in-maine.html', **g.templatevars)

@app.route('/<lang>/photo-album/')
def photo_album(lang):
    common_page_processing()
    return render_template('site/photo-album.html', **g.templatevars)

@app.route('/<lang>/registry/')
def registry(lang):
    common_page_processing()
    return render_template('site/registry.html', **g.templatevars)

@app.route('/<lang>/guest-book/')
def guest_book(lang):
    common_page_processing()
    return render_template('site/guest-book.html', **g.templatevars)

@app.route('/<lang>/rsvp/')
def rsvp(lang):
    common_page_processing()
    return render_template('site/rsvp.html', **g.templatevars)

@app.route('/<lang>/save-the-date/')
def save_the_date(lang):
    common_page_processing()
    return render_template('site/save-the-date.html', **g.templatevars)

@app.route('/')
@app.route('/en/')
@app.route('/be/')
def homepage():
    common_page_processing()
    return render_template('site/homepage.html', **g.templatevars)

# Admin Routing functions

@app.route('/admin/')
def admin_homepage():
    common_admin_page_processing()
    return 'admin'

# Routing errors

@app.errorhandler(404)
def not_found(error):
    common_page_processing()
    return render_template('errors/404.html', **g.templatevars), 404

# Helpers

def common_page_processing():
    g.requestvars = return_page_requestvars()
    g.templatevars = return_page_templatevars()

def return_page_requestvars():
    return PageRequestParser(request).return_requestvars()

def return_page_templatevars():
    templatevar_parser = TemplateVariableParser(request, g.requestvars)
    templatevar_parser.set_templatevar('debug', app.debug)
    return templatevar_parser.return_templatevars()

def common_admin_page_processing():
    set_admin_page_requestvars()

def set_admin_page_requestvars():
    g.requestvars = AdminPageRequestParser(request).return_requestvars()


def set_jinja_config(app):
    # Use a single % in templates
    app.jinja_env.line_statement_prefix = '%'

if __name__ == '__main__':
    set_jinja_config(app);
    app_config = {
        'debug_mode_on_hostnames': ('laskey.local', 'cnsmac3.bu.edu')
    }
    app_setup = AppSetup(app_config).return_setup()
    app.jinja_env.line_statement_prefix = '%'
    app.run(**app_setup)
