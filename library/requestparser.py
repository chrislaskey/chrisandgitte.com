from library.utilities import Utilities

'''
RequestParser centralizes the processing of a request.

Tasks common to every page request should abstracted away and be done inside
the RequestParser or one of it's child classes
'''
class RequestParser():

    def __init__(self, request):
        self.request = request
        self.requestvars = {}
        self.parse_request()

    def parse_request(self):
        self.parse_request_uri()

    def parse_request_uri(self):
        path = self.request.path.__str__() # excludes domain name
        url = self.request.url.__str__() # includes domain name
        self.requestvars['uri'] = path
        self.requestvars['uri_segments'] = \
            Utilities().return_uri_segments(url)

    def return_requestvars(self):
        return self.requestvars

class PageRequestParser(RequestParser):

    def __init__(self, request):
        RequestParser.__init__(self, request)
        self.parse_page()

    def parse_page(self):
        pagevars = {}
        pagevars['language'] = self.parse_page_language()
        self.requestvars.update(pagevars)

    def parse_page_language(self):
        uri_segments = self.requestvars.get('uri_segments', [])
        if len(uri_segments) > 1 and uri_segments[1] in ('be', 'en'):
            return uri_segments[1]
        else:
            return 'en'

class AdminPageRequestParser(RequestParser):

    def __init__(self, request):
        RequestParser.__init__(self, request)
        self.parse_admin_page()

    def parse_admin_page(self):
        pagevars = {}
        self.requestvars.update(pagevars)
