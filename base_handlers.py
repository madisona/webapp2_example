

from generic_handlers import BaseHandler

from events import models

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