import re
from unicodedata import normalize

class Utilities():

    def create_slug(self, text, delimiter=u'-'):
        '''
        Return ascii-only slugs from unicode.
        See: http://flask.pocoo.org/snippets/5/
        '''
        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        result = []
        for word in _punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delimiter.join(result))

    def return_uri_segments(self, uri):
        '''
        Return a list of uri segments
        Value at index 0 is the domain name
        '''
        return uri.split('/')
