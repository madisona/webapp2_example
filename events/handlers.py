
from google.appengine.ext.webapp import template

import webapp2

class TemplateHandlerMixin(object):
    template_name = None

    def render_response(self, **context):
        context.update(STATIC_URL=self.app.config.get('STATIC_URL', '/static/'))
        return webapp2.Response(template.render(self.template_name, context))


class Index(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "templates/index.html"

    def get(self):
        return self.render_response()

class EventList(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "templates/event_list.html"

    def get(self):
        return self.render_response(object_list={})


class EventDetail(TemplateHandlerMixin, webapp2.RequestHandler):
    template_name = "templates/event_detail.html"

    def get(self, event_key=None):
        return self.render_response(object='something')
