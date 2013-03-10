from flask import g, request
from lib.requestparser import PageRequestParser
from lib.templateparser import TemplateVariableParser

def common_page_processing():
    g.requestvars = _return_page_requestvars()
    g.templatevars = _return_page_templatevars()

def _return_page_requestvars():
    return PageRequestParser(request).return_requestvars()

def _return_page_templatevars():
    templatevar_parser = TemplateVariableParser(request, g.requestvars)
    templatevar_parser.set_templatevar('post', request.form)
    return templatevar_parser.return_templatevars()



