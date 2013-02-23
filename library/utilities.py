import re
from unicodedata import normalize

class Utilities():

    def create_slug(self, text, delimiter=u'-'):
        '''
        Return ascii-only slugs from unicode.
        See: http://flask.pocoo.org/snippets/5/
        '''
        try:
            _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
            result = []
            for word in _punct_re.split(text.lower()):
                word = normalize('NFKD', word).encode('ascii', 'ignore')
                if word:
                    result.append(word)
            return unicode(delimiter.join(result))
        except TypeError:
            text = unicode(text)
            return self.create_slug(text, delimiter)

    def create_title_from_slug(self, text):
        stripped_text = text.strip()
        replaced_text = re.sub(r'[-_]+', ' ', stripped_text)
        return replaced_text.title()

    def create_page_title(self, uri_segments):
        sections = self._process_page_title_segments(uri_segments)
        if len(sections) > 1:
            return ' | '.join(sections)
        else:
            return sections[0]

    def _process_page_title_segments(self, uri_segments):
        sections = []
        for piece in uri_segments:
            if piece in ('be', 'en'):
                continue
            title = self.create_title_from_slug(piece)
            sections.append(title)
        sections.reverse()
        return sections

    def create_body_class(self, segments):
        classes = ['body']
        for section in segments:
            previous_class = classes[-1][:]
            section_slug = self.create_slug(section)
            new_class = previous_class + '-{0}'.format(section_slug)
            classes.append(new_class)
        classes_string = ' '.join(classes)
        return classes_string

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
