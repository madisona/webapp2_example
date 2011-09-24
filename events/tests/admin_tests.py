
import datetime
import unittest

import webapp2

from test_utils import BaseAppEngineTestCase

import admin

from events import models

class BaseAdminHandlerTestCase(BaseAppEngineTestCase):

    def setUp(self):
        super(BaseAdminHandlerTestCase, self).setUp()
        req = webapp2.Request.blank('/')
        req.app = admin.app
        admin.app.set_globals(app=admin.app, request=req)


class AdminHandlerTests(BaseAdminHandlerTestCase):

    def test_returns_200_on_event_list(self):
        response = admin.app.get_response(webapp2.uri_for('admin_event_list'))
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_add(self):
        response = admin.app.get_response(webapp2.uri_for('admin_event_add'))
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_change(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        event.put()

        response = admin.app.get_response(webapp2.uri_for('admin_event_change', url_path=event.get_slug()))
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_delete(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        event.put()

        response = admin.app.get_response(webapp2.uri_for('admin_event_delete', url_path=event.get_slug()))
        self.assertEqual(200, response.status_int)

class AdminListHandlerTests(BaseAppEngineTestCase):

    def test_list_handler_returns_all_objects_in_list(self):
        pass

if __name__ == '__main__':
    unittest.main()