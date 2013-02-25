from flask import g, request
from utils.sqlite import query

class RSVP:

    def handle(self):
        form_errors = self._get_form_errors()
        if form_errors:
            g.templatevars['form_errors'] = form_errors
            return

    def _get_form_errors(self):
        values = request.form
        parser = RSVPFormParser()
        parser.set_values(values)
        if parser.has_errors():
            error_message = parser.get_error_message()
        else:
            error_message = ''
        return error_message

class RSVPFormParser():

    required_fields = [
        {'attending': 'Please select whether you are attending'},
        {'name': 'Please put your full name in the "Name" field'}
    ]

    parsed = False

    def set_values(self, values):
        self.values = values
        self.parsed = False

    def has_errors(self):
        if not self.parsed:
            self._parse_values()
        if self.errors:
            return True
        else:
            return False

    def get_error_message(self, values):
        if not self.parsed:
            self._parse_values()
        if not self.errors:
            return ''
        error_message = self._create_error_message()
        return error_message

    def _create_error_message(self):
        # TODO
        pass

    def _parse_values(self):
        # TODO
        self.parsed = True
        self.errors = []

class RSVPDatabase():

    columns = [
        'attending',
        'name',
        'guest',
        'allergies',
        'comments'
    ]

    def set_query_method(self, query_method):
        self.query_method = query_method

    def save(self, values):
        self.values = values
        insert_query = self._get_insert_query()
        args = self._get_insert_args()
        result = self.query_method(insert_query, args)
        return result

    def _get_insert_query(self):
        escaped_columns = ['"{0}"'.format(x) for x in self.columns]
        fields = ', '.join(escaped_columns)
        placeholder_values = ['?'] * len(self.columns)
        placeholder_values = ', '.join(placeholder_values)
        insert_query = 'INSERT INTO main.rsvps ({0}) VALUES ({1})'.format(
            fields, placeholder_values
        )
        return insert_query

    def _get_insert_args(self):
        args = []
        for column in self.columns:
            value = self.values.get(column, '')
            escaped_value = '"{0}"'.format(value)
            args.append(escaped_value)
        args = tuple(args)
        return args
