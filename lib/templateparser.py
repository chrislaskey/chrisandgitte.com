import re
from unicodedata import normalize

class TemplateVariableParser():

    def __init__(self, request, requestvars = {}):
        self._set_classvars(request, requestvars)

    def _set_classvars(self, request, requestvars):
        self.request = request
        self.requestvars = requestvars
        self.language = requestvars.get('language', 'en')
        self.templatevars = {}

    def set_templatevar(self, name, value):
        self.templatevars[name] = value

    def return_templatevars(self):
        self._parse_templatevars()
        return self.templatevars

    def _parse_templatevars(self):
        self.templatevars['page_title'] = self._parse_page_title()
        self.templatevars['body_class'] = self._parse_body_class()

    def _parse_page_title(self):
        uri_segments = self._return_uri_segments()
        return Utilities().create_page_title(uri_segments)
    
    def _return_uri_segments(self):
        return self.requestvars.get('uri_segments')[:]

    def _parse_body_class(self):
        segments = self._return_uri_segments_without_domain()
        return Utilities().create_body_class(segments)

    def _return_uri_segments_without_domain(self):
        uri_segments = self._return_uri_segments()
        if len(uri_segments) > 1:
            del(uri_segments[0])
            return uri_segments
        else:
            return []

class Utilities():

    def create_slug(self, text, delimiter=u'-'):
        '''
        Return ascii-only slugs from unicode.
        See: http://flask.pocoo.org/snippets/5/
        '''
        try:
            _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
            result = []
            text = text.strip()
            text = text.lower()
            for word in _punct_re.split(text):
                word = normalize('NFKD', word).encode('ascii', 'ignore')
                if word:
                    result.append(word)

            return unicode(delimiter.join(result))
        except TypeError:
            text = unicode(text)
            return self.create_slug(text, delimiter)

    def create_title_from_slug(self, text):
        replaced_text = re.sub(r'[-_]+', ' ', text)
        stripped_text = replaced_text.strip()
        return stripped_text.title()

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
