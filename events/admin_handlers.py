

from base_handlers import BaseHandler

from webapp2 import uri_for
from events import models, forms


class EventAdd(BaseHandler):
    model = models.Event
    template = "events/event_add.html"

    def get(self):
        return self.render_response(self.template, **self.get_context_data(
            form=self.get_form(),
        ))

    def post(self):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,  form):
        model = form.save()
        
        # add message and redirect?
        return self.redirect(uri_for('event-add'))

    def form_invalid(self, form):
        return self.render_response(self.template, **self.get_context_data(
            form=form,
        ))

    def get_context_data(self, **context):
        return context

    def get_form_kwargs(self):
        return {
            'data': self.request.POST or None,
            'initial': self.get_initial(),
        }

    def get_initial(self):
        pass

    def get_form(self):
        return forms.EventForm(**self.get_form_kwargs())

