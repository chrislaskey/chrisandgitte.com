from lib.templateparser import TemplateVariableParser

class PageTemplateVariableParser(TemplateVariableParser):

    parent = TemplateVariableParser

    def __init__(self, request, requestvars = {}):
        self.parent.__init__(self, request, requestvars)

    def set_templatevar(self, name, value):
        self.templatevars[name] = value

    def return_templatevars(self):
        self.parent._parse_templatevars(self)
        self._parse_templatevars()
        return self.templatevars

    def _parse_templatevars(self):
        self.templatevars['language'] = self.language
        self.templatevars['mirror_language_link'] = \
                self.parse_mirror_language_link()

    def parse_mirror_language_link(self):
        inactive_language = self._return_inactive_language()
        uri_segments = self._return_uri_segments_without_domain()
        if len(uri_segments) > 0 and uri_segments[0] in ('be', 'en'):
            uri_segments[0] = inactive_language
        else:
            uri_segments.insert(0, inactive_language)
        return '/' + '/'.join(uri_segments)

    def _return_inactive_language(self):
        if self.language == 'en':
            return 'be'
        else:
            return 'en'
