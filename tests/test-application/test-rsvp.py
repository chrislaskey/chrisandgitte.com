# -*- coding: utf8 -*-

# nosetests --with-coverage --cover-package=<package> \
# --nocapture ./tests

import os
from lib.environment import Environment
base_dir = '{0}/../../'.format(__file__)
abs_base_dir = os.path.abspath(base_dir)
Environment().add_virtualenv_site_packages_to_path(abs_base_dir)

from nose.tools import *
from application.rsvp import *

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
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guests", "allergies", "comments", "date") VALUES (?, ?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '""', '""', '""', '"2013-03-10T15:55:07"')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {}
        assert_raises(Exception, self.db.save, input_values)

    def test_minimum_input(self):
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guests", "allergies", "comments", "date") VALUES (?, ?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '""', '""', '""', '"2013-03-10T15:55:07"')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {
            'attending': 'yes',
            'name': 'chris',
            'date': '2013-03-10T15:55:07',
        }
        self.db.save(input_values)

    def test_all_input_values(self):
        expected_query = 'INSERT INTO main.rsvps ("attending", "name", "guests", "allergies", "comments", "date") VALUES (?, ?, ?, ?, ?, ?)'
        expected_args = ('"yes"', '"chris"', '"guests"', '"my allergies"', '"somecomment \t with \r\n things"', '"2013-03-10T15:55:07"')
        mock_query_method = query_mock(expected_query, expected_args)
        self.db.set_query_method(mock_query_method)

        input_values = {
            'attending': 'yes',
            'name': 'chris',
            'guests': 'guests',
            'allergies': 'my allergies',
            'comments': 'somecomment \t with \r\n things',
            'date': '2013-03-10T15:55:07'
        }
        self.db.save(input_values)

class query_stub:

    def __init__(self, *args, **kwargs):
        pass

class TestRSVP:

    def setup(self):
        "Set up test fixtures"
        rsvp = RSVP()
        rsvp.set_query_method(query_stub)
        self.rsvp = rsvp

    def teardown(self):
        "Tear down test fixtures"

    def test_parse_no_values_returns_errors(self):
        form_values = {}
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        result_error_count = len(result['form_errors'])
        assert_equal(result_error_count, 2)

    def test_parse_empty_values_returns_errors(self):
        form_values = {
            'attending': '',
            'name': ''
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        result_error_count = len(result['form_errors'])
        assert_equal(result_error_count, 2)

    def test_parse_missing_name_value_returns_error(self):
        form_values = {
            'attending': 'yes',
            'name': ''
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        result_error_count = len(result['form_errors'])
        assert_equal(result_error_count, 1)

    def test_parse_missing_attending_value_returns_error(self):
        form_values = {
            'attending': '',
            'name': 'Gitte Venicx'
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        result_error_count = len(result['form_errors'])
        assert_equal(result_error_count, 1)

    def test_parse_invalid_attending_value_returns_false(self):
        form_values = {
            'attending': 'invalid value that should return False',
            'name': 'Chris Laskey'
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        assert_equal(result['form_errors'], [])
        assert_equal(result['form_success'], True)
        assert_equal(result['is_attending'], False)

    def test_parse_required_values_returns_is_attending_value(self):
        form_values = {
            'attending': 'no',
            'name': 'Chris Laskey'
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        assert_equal(result['form_errors'], [])
        assert_equal(result['form_success'], True)
        assert_equal(result['is_attending'], False)

    def test_parse_required_values_returns_successfully(self):
        form_values = {
            'attending': 'yes',
            'name': 'Chris Laskey'
        }
        method = self.rsvp.parse_and_save_request_and_return_templatevars
        result = method(form_values)
        assert_equal(result['form_errors'], [])
        assert_equal(result['form_success'], True)
        assert_equal(result['is_attending'], True)
