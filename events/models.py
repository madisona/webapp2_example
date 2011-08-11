
import datetime
from google.appengine.ext import db

from utils import slugify
import config


def get_entity_key(event_group=None):
    return db.Key.from_path('EventGroup', event_group or 'default_group')

class Event(db.Model):
    name = db.StringProperty(indexed=False)
    location = db.StringProperty(indexed=False)
    start_time = db.DateTimeProperty()
    description = db.TextProperty()

    def __str__(self):
        return self.name
    
    @classmethod
    def get_upcoming_events(cls, event_group=None, num=5, today=datetime.datetime.today):
        entity_key = get_entity_key(event_group)
        return cls.all().ancestor(entity_key).filter("start_time >=", today()).order('start_time').fetch(num)

    def get_url(self):
        date = self.start_time
        return config.event_path_format % {
            'slug': slugify(self.name),
            'year': date.year,
            'month': date.month,
            'day': date.day,
        }
