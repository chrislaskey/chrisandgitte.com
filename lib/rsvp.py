from utils.sqlite import query as sqlite_query
from datetime import datetime

class RSVP:

    def __init__(self):
        self.set_query_method(sqlite_query)

    def set_query_method(self, db_query_method):
        self.query = db_query_method

    def parse_and_save_request_and_return_templatevars(self, input_values):
        self.input_values = input_values
        self._set_templatevars()
        if not self.errors:
            self._save_rsvp()
        return self.templatevars

    def _set_templatevars(self):
        templatevars = {}
        self.errors = self._get_form_errors()
        templatevars['form_errors'] = self.errors
        if not self.errors:
            templatevars['form_success'] = True
            templatevars['is_attending'] = self._is_attending()
        self.templatevars = templatevars

    def _get_form_errors(self):
        self._load_parser()
        errors = self.parser.get_errors()
        return errors

    def _load_parser(self):
        if not hasattr(self, 'parser') or not self.parser:
            values = self.input_values
            parser = RSVPFormParser()
            parser.set_values(values)
            self.parser = parser

    def _is_attending(self):
        self._load_parser()
        is_attending = self.parser.is_attending()
        return is_attending

    def _save_rsvp(self):
        values = self._get_database_values()
        database = RSVPDatabase()
        database.set_query_method(self.query)
        database.save(values)

    def _get_database_values(self):
        values = self.input_values.copy()
        values['date'] = datetime.now().isoformat()
        return values

class RSVPFormParser():

    required_fields = {
        'attending': 'Please select whether you are attending',
        'name': 'Please put your full name in the "Name" field'
    }
    attending_field = 'attending'

    def set_values(self, values):
        self.values = values
        self._parse_values()

    def get_errors(self):
        return self.errors

    def is_attending(self):
        return self.attending

    def _parse_values(self):
        self._parse_error_values()
        self._parse_attending_value()

    def _parse_error_values(self):
        errors = []
        for key, error in self.required_fields.iteritems():
            if key not in self.values or not self.values[key]:
                errors.append(error)
        self.errors = errors

    def _parse_attending_value(self):
        attending = False
        field = self.attending_field
        if field in self.values:
            response = self.values[field]
            if response == "yes":
                attending = True
        self.attending = attending

class RSVPDatabase():

    columns = [
        'attending',
        'name',
        'guests',
        'allergies',
        'comments',
        'date'
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
