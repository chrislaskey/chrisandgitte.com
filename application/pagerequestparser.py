from lib.requestparser import RequestParser

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
