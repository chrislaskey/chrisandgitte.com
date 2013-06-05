class RequestParser():

    def __init__(self, request):
        self.request = request
        self.requestvars = {}
        self._parse_request()

    def _parse_request(self):
        self.parsing = self.request.base_url.__str__()
        self._validate_url()
        self._parse_protocol()
        self._parse_domain()
        self._parse_uri_segments()
        self._parse_uri()

    def _validate_url(self):
        has_protocol_string = (self.parsing.find('://') != -1)
        if not has_protocol_string:
            raise Exception('Invalid URL')

    def _parse_protocol(self):
        protocol, self.parsing = self.parsing.split('://')
        self.requestvars['protocol'] = protocol

    def _parse_domain(self):
        self._segments = self.parsing.split('/')
        self.requestvars['domain'] = self._segments[0]

    def _parse_uri_segments(self):
        self.requestvars['uri_segments'] = self._segments[1:]

    def _parse_uri(self):
        uri_segments = self.requestvars.get('uri_segments')
        self.requestvars['uri'] = '/' + '/'.join(uri_segments)

    def return_requestvars(self):
        return self.requestvars
