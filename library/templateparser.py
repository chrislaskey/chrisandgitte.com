from library.utilities import Utilities 

class TemplateVariableParser():

    def __init__(self, request, requestvars = {}):
        self.set_classvars(request, requestvars)
        self.parse_templatevars()

    def set_classvars(self, request, requestvars):
        self.request = request
        self.requestvars = requestvars
        self.language = requestvars.get('language', 'en')
        self.templatevars = {}
    
    # Parse functions

    def parse_templatevars(self):
        self.templatevars['language'] = self.language
        self.templatevars['is_responsive'] = self.parse_is_responsive()
        self.templatevars['page_title'] = self.parse_page_title()
        self.templatevars['body_class'] = self.parse_body_class()
        self.templatevars['mirror_language_link'] = \
                self.parse_mirror_language_link()

    def parse_is_responsive(self):
        cookie = self.request.cookies.get('is_responsive')
        if cookie == 'true':
            return True
        else:
            return False

    def parse_page_title(self):
        uri_segments = self.return_uri_segments()
        return Utilities().create_page_title(uri_segments)

    def parse_body_class(self):
        segments = self.return_uri_segments_without_domain()
        return Utilities().create_body_class(segments)

    def parse_mirror_language_link(self):
        inactive_language = self.return_inactive_language()
        uri_segments = self.return_uri_segments_without_domain()
        if len(uri_segments) > 0 and uri_segments[0] in ('be', 'en'):
            uri_segments[0] = inactive_language
        else:
            uri_segments.insert(0, inactive_language)
        return '/' + '/'.join(uri_segments)

    # Utility and helper functions
    
    def return_uri_segments(self):
        return self.requestvars.get('uri_segments')[:]

    def return_uri_segments_without_domain(self):
        uri_segments = self.return_uri_segments()
        if len(uri_segments) > 1:
            del(uri_segments[0])
            return uri_segments
        else:
            return []

    def return_inactive_language(self):
        if self.language == 'en':
            return 'be'
        else:
            return 'en'
       
    # Interface functions

    def set_templatevar(self, name, value):
        self.templatevars[name] = value

    def return_templatevars(self):
        return self.templatevars
