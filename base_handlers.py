
import webapp2
from webapp2_extras import jinja2

from utils import jinja2_factory
from events import models

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(factory=jinja2_factory)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)



class Index(BaseHandler):
    template_name = "index.html"
    model = models.Event

    def get(self):
        return self.render_response(self.template_name, **self.get_context_data())

    def get_context_data(self, **context):
        ctx = {
            'object_list': self.get_object_list()
        }
        ctx.update(context)
        return ctx

    def get_object_list(self):
        return self.model.get_upcoming_events()