from lib.requestparser import RequestParser

class PageRequestParser:

    def parse(self, request):
        self.parsed = RequestParser().parse(request)
        self.parsed['language'] = self._parse_page_language()
        return self.parsed

    def _parse_page_language(self):
        uri_segments = self.parsed.get('uri_segments', [])
        print(uri_segments)
        if len(uri_segments) > 0 and uri_segments[0] in ('be', 'en'):
            return uri_segments[0]
        else:
            return 'en'
