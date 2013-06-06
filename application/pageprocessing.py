from flask import g, request
from application.pagetemplateparser import PageTemplateVariableParser

def common_page_processing():
    g.templatevars = _return_page_templatevars()

def _return_page_templatevars():
    parser = PageTemplateVariableParser()
    parser.set('post', request.form)
    parser.set('uri', request.url)
    return parser.parse(request)
