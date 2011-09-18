
import unittest

from test_utils import BaseAppEngineTestCase

import main

class HandlerTests(BaseAppEngineTestCase):

    def test_returns_200_on_home_page(self):
        response = main.app.get_response('/')
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_events_list_page(self):
        response = main.app.get_response('/events/')
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_events_detail_page(self):
        response = main.app.get_response('/events/2011/08/an-event/')
        self.assertEqual(200, response.status_int)

if __name__ == '__main__':
    unittest.main()