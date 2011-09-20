
import datetime
import unittest

from test_utils import BaseAppEngineTestCase

import admin

from events import models

class AdminHandlerTests(BaseAppEngineTestCase):

    def test_returns_200_on_event_list(self):
        response = admin.app.get_response('/admin/event/')
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_add(self):
        response = admin.app.get_response('/admin/event/add/')
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_change(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        event.put()

        response = admin.app.get_response('/admin/event/change/{url_path}'.format(url_path=event.get_slug()))
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_event_delete(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        event.put()

        response = admin.app.get_response('/admin/event/delete/{url_path}'.format(url_path=event.get_slug()))
        self.assertEqual(200, response.status_int)

class AdminListHandlerTests(BaseAppEngineTestCase):

    def test_list_handler_returns_all_objects_in_list(self):
        pass

if __name__ == '__main__':
    unittest.main()