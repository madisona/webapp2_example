
import datetime
import unittest

from google.appengine.ext import db

from test_utils import BaseAppEngineTestCase

from events import models

class EventModelTests(BaseAppEngineTestCase):

    def test_get_slug_returns_model_slug(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        self.assertEqual('2011/7/event-1', event.get_slug())

    def test_uses_slug_as_key_name(self):
        event = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        self.assertEqual(event.get_slug(), event.key().name())

    def test_returns_upcoming_events(self):
        # doing the right thing, but models don't have equal operator...
        # will need to do something else to check the test.
        event1 = models.Event(name="Event 1", start_time=datetime.datetime(2011,7,31))
        event2 = models.Event(name="Event 2", start_time=datetime.datetime(2011,8,1,0))
        event3 = models.Event(name="Event 3", start_time=datetime.datetime(2011,8,2,1))
        event4 = models.Event(name="Event 4", start_time=datetime.datetime(2011,8,2,2))
        event5 = models.Event(name="Event 5", start_time=datetime.datetime(2011,8,2,3))
        event6 = models.Event(name="Event 6", start_time=datetime.datetime(2011,8,2,4))
        event7 = models.Event(name="Event 7", start_time=datetime.datetime(2011,8,3,5))
        db.put([event1, event2, event3, event4, event5, event6, event7])
        def get_today():
            return datetime.date(2011,8,1)

        event_list = models.Event.get_upcoming_events(num=5, today=get_today)
        expected_list = [event2, event3, event4, event5, event6]
        for expected, event in zip(expected_list, event_list):
            self.assertEqual(expected.name, event.name)

if __name__ == '__main__':
    unittest.main()