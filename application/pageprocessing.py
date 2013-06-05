from flask import g, request
from application.pagetemplateparser import PageTemplateVariableParser
from application.pagerequestparser import PageRequestParser

def common_page_processing():
    g.requestvars = _return_page_requestvars()
    g.templatevars = _return_page_templatevars()

def _return_page_requestvars():
    return PageRequestParser().parse(request)

def _return_page_templatevars():
    templatevar_parser = PageTemplateVariableParser(request, g.requestvars)
    templatevar_parser.set_templatevar('post', request.form)
    templatevar_parser.set_templatevar('uri', request.url)
    return templatevar_parser.return_templatevars()
