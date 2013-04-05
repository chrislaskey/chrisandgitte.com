#!/usr/bin/env python

from lib.environment import Environment
Environment().add_virtualenv_site_packages_to_path(__file__)

from flask import Flask, g, render_template, request
from flask.ext.sendmail import Mail
from lib.pageprocessing import common_page_processing
from lib.weddingphotoalbum import WeddingPhotoAlbumImages
from lib.rsvp import RSVP, send_rsvp_email

app = Flask(__name__)
mail = Mail(app)

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
    photo_album_images = WeddingPhotoAlbumImages().get_images_shuffled()
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

@app.route('/<lang>/rsvp/', methods = ['GET', 'POST'])
def rsvp(lang):
    common_page_processing()
    if request.method == 'POST':
        values = request.form.copy()
        new_vars = RSVP().\
                   parse_and_save_request_and_return_templatevars(values)
        g.templatevars.update(new_vars)
        send_rsvp_email(mail, new_vars)
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

@app.errorhandler(500)
def server_error(error):
    common_page_processing()
    return render_template('errors/500.html', **g.templatevars), 500

if __name__ == '__main__':
    app.jinja_env.line_statement_prefix = '%'
    app.run(debug=True)
