class RequestParser():
    " Centralizes the processing of a request "
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
            _Utilities().return_uri_segments(url)

    def return_requestvars(self):
        return self.requestvars


class _Utilities():

    def return_uri_segments(self, uri):
        '''
        Return a list of uri segments
        Value at index 0 is the domain name
        '''
        stripped_protocol = self._strip_http_protocol(uri)
        raw_segments = stripped_protocol.split('/')
        filtered_segments = [x for x in raw_segments if x]
        return filtered_segments

    def _strip_http_protocol(self, uri):
        double_forward_slash_position = uri.find('//')
        if double_forward_slash_position > 0:
            cut_from = double_forward_slash_position + 2
            return uri[cut_from:]
        else:
            return uri
