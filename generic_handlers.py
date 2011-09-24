
import webapp2
from webapp2_extras import jinja2

from utils import jinja2_factory, intget

__all__ = (
    'BaseHandler',
    'DetailHandler',
    'FormHandler',
    'ListHandler',
)

class ImproperlyConfigured(Exception):
    "Generic Handler is improperly configured"
    pass

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(factory=jinja2_factory)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

class SingleObjectMixin(object):
    """
    Provides the ability to retrieve a single object for further manipulation.
    """
    model = None
    context_object_name = None

    @webapp2.cached_property
    def object(self):
        """
        by default this requires key_name to look up object
        If id is provided in url kwargs, it MUST be an integer/long
        """
        key_name = self.kwargs.get('key_name')
        id = self.kwargs.get('id')

        obj = None
        if key_name is not None:
            obj = self.model.get_by_key_name(key_name)
        elif id is not None:
            obj = self.model.get_by_id(intget(id, -1))
        else:
            raise ImproperlyConfigured(
                u'Generic detail view %s must have a url parameter of '
                u'either key_name or id.' % self.__class__.__name__)

        if obj:
            return obj
        else:
            self.abort(404, 'Requested object not found')

    def get_context_object_name(self, obj):
        """
        Get the name to use for the object.
        """
        return self.context_object_name

    def get_context_data(self, **context):
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            context[context_object_name] = self.object
        return context

class MultipleObjectMixin(object):
    allow_empty = True
    model = None
    context_object_name = None

    def get_object_list(self):
        if self.model:
            return self.model.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'model'"
                                       % self.__class__.__name__)

    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """
        Get the name of the item to be used in the context.
        """
        return self.context_object_name

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        object_list = kwargs.pop('object_list')
        context = {
            'object_list': object_list
        }
        context.update(kwargs)
        context_object_name = self.get_context_object_name(object_list)
        if context_object_name:
            context[context_object_name] = object_list
        return context

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


class ListHandler(MultipleObjectMixin, BaseHandler):
    template = None

    def get(self, **kwargs):
        self.object_list = self.get_object_list()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise self.abort(404, u"Empty list and '%(class_name)s.allow_empty' is False."
                                    % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list)
        return self.render_response(self.template, **context)

class DetailHandler(SingleObjectMixin, BaseHandler):
    template = None

    def get(self, **kwargs):
        self.kwargs = kwargs

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_response(self.template, **context)

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