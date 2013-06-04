from flask import g, request
from lib.templateparser import TemplateVariableParser

from application.pagerequestparser import PageRequestParser

def common_page_processing():
    g.requestvars = _return_page_requestvars()
    g.templatevars = _return_page_templatevars()

def _return_page_requestvars():
    return PageRequestParser(request).return_requestvars()

def _return_page_templatevars():
    templatevar_parser = TemplateVariableParser(request, g.requestvars)
    templatevar_parser.set_templatevar('post', request.form)
    templatevar_parser.set_templatevar('uri', request.url)
    return templatevar_parser.return_templatevars()