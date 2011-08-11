
import datetime
import unittest

from google.appengine.ext import testbed, db

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


class EventModelTests(BaseAppEngineTestCase):

    def test_returns_recent_events(self):
        # doing the right thing, but models don't have equal operator...
        # will need to do something else to check the test.
        event_group = models.get_entity_key()
        event1 = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31), ancestor=event_group)
        event2 = models.Event(name="Event 2", start_time=datetime.datetime(2011,8,1,0), ancestor=event_group)
        event3 = models.Event(name="Event 3", start_time=datetime.datetime(2011,8,2,1), ancestor=event_group)
        event4 = models.Event(name="Event 4", start_time=datetime.datetime(2011,8,2,2), ancestor=event_group)
        event5 = models.Event(name="Event 5", start_time=datetime.datetime(2011,8,2,3), ancestor=event_group)
        event6 = models.Event(name="Event 6", start_time=datetime.datetime(2011,8,2,4), ancestor=event_group)
        event7 = models.Event(name="Event 7", start_time=datetime.datetime(2011,8,3,5), ancestor=event_group)
        db.put([event1, event2, event3, event4, event5, event6, event7])
        def get_today():
            return datetime.date(2011,8,1)

        event_list = models.Event.get_upcoming_events(num=5, today=get_today)
        expected_list = [event2, event3, event4, event5, event6]
        for expected, event in zip(expected_list, event_list):
            self.assertEqual(expected.name, event.name)

if __name__ == '__main__':
    unittest.main()