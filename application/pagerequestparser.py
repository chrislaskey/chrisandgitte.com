from lib.requestparser import RequestParser

class PageRequestParser:

    def parse(self, request):
        self.parsed = RequestParser().parse(request)
        self._additional_parsing()
        return self.parsed

    def _additional_parsing(self):
        self.parsed['language'] = self._parse_page_language()

    def _parse_page_language(self):
        uri_segments = self.parsed.get('uri_segments', [])
        if len(uri_segments) > 1 and uri_segments[1] in ('be', 'en'):
            return uri_segments[1]
        else:
            return 'en'
