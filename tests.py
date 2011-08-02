
import unittest

from google.appengine.ext import testbed

import main
from events import models

class BaseAppEngineTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

class HandlerTests(BaseAppEngineTestCase):

    def test_returns_200_on_home_page(self):
        response = main.app.get_response('/')
        self.assertEqual(200, response.status_int)

    def test_returns_200_on_events_list_page(self):
        response = main.app.get_response('/events/')
        self.assertEqual(200, response.status_int)

#    def test_returns_200_on_events_list_page(self):
#        response = main.app.get_response('/events/an-event/')
#        self.assertEqual(200, response.status_int)

if __name__ == '__main__':
    unittest.main()