
from google.appengine.ext import db
import unittest

from test_utils import BaseAppEngineTestCase

import generic_handlers
from webapp2 import HTTPException

__all__ = (
    'SingleObjectMixinTests',
    'FormMixinTests',
)

class TestModel(db.Model):
    name = db.StringProperty()

class MixedSingleObject(generic_handlers.SingleObjectMixin, generic_handlers.BaseHandler):
    pass

class SingleObjectMixinTests(BaseAppEngineTestCase):

    def setUp(self):
        super(SingleObjectMixinTests, self).setUp()
        
        self.sut = generic_handlers.SingleObjectMixin()

    def test_get_object_returns_model_by_key_name(self):
        model_key = TestModel(name="test_model", key_name="test_model").put()

        self.sut.model = TestModel
        self.sut.kwargs = {'key_name': 'test_model'}

        self.assertEqual(model_key, self.sut.object.key())

    def test_get_object_returns_model_by_id(self):
        model_key = TestModel(name="test_model").put()

        self.sut.model = TestModel
        self.sut.kwargs = {'id': str(model_key.id())}

        self.assertEqual(model_key, self.sut.object.key())

    def test_get_object_raises_404_when_id_given_is_invalid_id(self):
        self.sut = MixedSingleObject()
        self.sut.model = TestModel
        self.sut.kwargs = {'id': "123A"} # id can only be int or long

        with self.assertRaises(HTTPException) as ctx:
            self.sut.object
        self.assertEqual('Requested object not found', ctx.exception.message)
        self.assertEqual(404, ctx.exception.code)

    def test_get_object_raises_improperly_configured_when_no_id_or_key_name_in_kwargs(self):
        self.sut.model = TestModel
        self.sut.kwargs = {}

        with self.assertRaises(generic_handlers.ImproperlyConfigured) as ctx:
            self.sut.object
        self.assertEqual('Generic detail view %s must have a url parameter of '
                u'either key_name or id.' % self.sut.__class__.__name__, ctx.exception.message)

    def test_raises_404_when_object_not_found(self):
        self.sut = MixedSingleObject()
        self.sut.model = TestModel
        self.sut.kwargs = {'id': '1234'}

        with self.assertRaises(HTTPException) as ctx:
            self.sut.object
        self.assertEqual('Requested object not found', ctx.exception.message)
        self.assertEqual(404, ctx.exception.code)

    def test_get_context_object_name_returns_class_context_object_name(self):
        object_name = "test_model"
        self.sut.context_object_name = object_name
        self.assertEqual(object_name, self.sut.context_object_name)

    def test_get_context_data_returns_context_passed_as_kwargs(self):
        model_key = TestModel(name="test_model").put()

        self.sut.model = TestModel
        self.sut.kwargs = {'id': str(model_key.id())}

        context = {'first': 'thing'}
        self.assertEqual(context, self.sut.get_context_data(**context))

    def test_get_context_data_returns_context_with_object_keyed_on_object_name(self):
        model_key = TestModel(name="test_model").put()

        self.sut.model = TestModel
        self.sut.kwargs = {'id': str(model_key.id())}
        self.sut.context_object_name = 'test_model'

        context = {'first': 'thing'}
        expected_dict = dict(test_model=self.sut.object, **context)
        self.assertEqual(expected_dict, self.sut.get_context_data(**context))

class FormMixinTests(BaseAppEngineTestCase):

    def setUp(self):
        super(FormMixinTests, self).setUp()
        self.sut = generic_handlers.FormMixin()

    def test_get_redirect_url_returns_redirect_url_defined(self):
        url = '/thanks/'
        self.sut.redirect_url = url
        self.assertEqual(url, self.sut.get_redirect_url())

    def test_get_redirect_url_raises_improperly_configured_when_redirect_url_not_defined(self):
        with self.assertRaises(generic_handlers.ImproperlyConfigured) as ctx:
            self.sut.get_redirect_url()
        self.assertEqual('No URL to redirect to, please define a redirect url.', ctx.exception.message)

    def test_get_form_class_returns_form_class_on_instance(self):
        class FormClass(object):
            pass

        self.sut.form_class = FormClass
        self.assertEqual(FormClass, self.sut.get_form_class())

if __name__ == '__main__':
    unittest.main()