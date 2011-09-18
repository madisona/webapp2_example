

from base_handlers import BaseHandler

from webapp2 import uri_for
from events import models, forms

class EventListHandler(BaseHandler):
    template = "events/event_list.html"

    def get(self):
        return self.render_response(self.template)


class FormMixin(object):
    form_class = None
    redirect_url = None

    def get_redirect_url(self):
        return self.redirect_url or None

    def form_valid(self,  form):
        model = form.save()

        # add message and redirect?
        return self.redirect(self.get_redirect_url())

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
        return self.form_class(**self.get_form_kwargs())


class FormHandler(FormMixin, BaseHandler):

    def get(self, **kwargs):
        self.kwargs = kwargs

        return self.render_response(self.template, **self.get_context_data(
            form=self.get_form(),
        ))

    def post(self, **kwargs):
        self.kwargs = kwargs

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EventAddHandler(FormHandler):
    model = models.Event
    template = "events/event_change.html"
    form_class = forms.EventForm

    def get_redirect_url(self):
        return uri_for('admin_event_add')



class EventChangeHandler(FormHandler):
    model = models.Event
    template = "events/event_change.html"
    form_class = forms.EventForm

class EventDeleteHandler(BaseHandler):
    template = "events/event_delete.html"

    def get(self, **kwargs):
        return self.render_response(self.template)