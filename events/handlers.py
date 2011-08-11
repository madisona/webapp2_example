
from google.appengine.ext.webapp import template

import webapp2
from utils import render_template

class TemplateHandlerMixin(object):
    template_name = None

    def render_response(self, **context):
        return webapp2.Response(render_template(self.template_name, context))


class Index(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "index.html"

    def get(self):
        return self.render_response()

class EventList(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "events/event_list.html"

    def get(self):
        return self.render_response(object_list={})


class EventDetail(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "events/event_detail.html"

    def get(self, event_key=None):
        return self.render_response(object='something')
