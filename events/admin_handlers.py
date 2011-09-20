
from base_handlers import BaseHandler
from generic_handlers import ListHandler, FormHandler

from webapp2 import uri_for
from events import models, forms


class EventListHandler(ListHandler):
    model = models.Event
    template = "events/event_list.html"

class EventAddHandler(FormHandler):
    model = models.Event
    template = "events/event_change.html"
    form_class = forms.EventForm

    def get_redirect_url(self):
        return uri_for('admin_event_list')

class EventChangeHandler(FormHandler):
    model = models.Event
    template = "events/event_change.html"
    form_class = forms.EventForm

    def get_redirect_url(self):
        return uri_for('admin_event_list')

class EventDeleteHandler(BaseHandler):
    template = "events/event_delete.html"

    def get(self, **kwargs):
        return self.render_response(self.template)