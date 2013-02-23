#!/usr/bin/env python

from lib.environment import Environment
Environment().add_virtualenv_site_packages_to_path(__file__)

from flask import Flask, g, render_template, request
from lib.requestparser import PageRequestParser
from lib.templateparser import TemplateVariableParser
from lib.weddingphotoalbum import *

app = Flask(__name__)

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
    photo_album_images = WeddingPhotoAlbumImages().get_images()
    g.templatevars['photo_album_images'] = photo_album_images
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

@app.errorhandler(404)
def not_found(error):
    common_page_processing()
    return render_template('errors/404.html', **g.templatevars), 404

def common_page_processing():
    g.requestvars = return_page_requestvars()
    g.templatevars = return_page_templatevars()

def return_page_requestvars():
    return PageRequestParser(request).return_requestvars()

def return_page_templatevars():
    templatevar_parser = TemplateVariableParser(request, g.requestvars)
    templatevar_parser.set_templatevar('debug', app.debug)
    return templatevar_parser.return_templatevars()

if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '%'
    app.run(debug=True)
