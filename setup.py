#!/usr/bin/env python

from lib.environment import Environment
Environment().add_virtualenv_site_packages_to_path(__file__)

from application.weddingphotoalbum import WeddingPhotoAlbumGenerator
WeddingPhotoAlbumGenerator().create()
