# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=<package> \
# --nocapture ./tests

import os
from lib.environment import Environment
base_dir = '{0}/../../'.format(__file__)
abs_base_dir = os.path.abspath(base_dir)
Environment().add_virtualenv_site_packages_to_path(abs_base_dir)

from nose.tools import *
from lib.rsvp import *

def query_mock(expected_query, expected_args):
    def method(query, args):
        if query != expected_query:
            raise Exception('Invalid query, expected "{0}", received "{1}"'.format(expected_query, query))
        if args != expected_args:
            raise Exception('Invalid args, expected "{0}", received "{1}"'.format(expected_args, args))
    return method

class TestRSVPDatabase:

    def setup(self):
        "Set up test fixtures"
        db = RSVPDatabase()
        self.db = db

    def teardown(self):
        "Tear down test fixtures"
    
    def test_empty_inputs_raises_exception(self):
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guest", "allergies", "comments") VALUES (?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '""', '""', '""')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {}
        assert_raises(Exception, self.db.save, input_values)
    
    def test_minimum_input(self):
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guest", "allergies", "comments") VALUES (?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '""', '""', '""')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {
            'attending': 'yes',
            'name': 'chris'
        }
        self.db.save(input_values)

    def test_all_input_values(self):
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guest", "allergies", "comments") VALUES (?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '"guest"', '"my allergies"', '"somecomment \t with \r\n things"')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {
            'attending': 'yes',
            'name': 'chris',
            'guest': 'guest',
            'allergies': 'my allergies',
            'comments': 'somecomment \t with \r\n things'
        }
        self.db.save(input_values)
