
import datetime
from google.appengine.ext import db

from utils import slugify
import config


class Event(db.Model):
    name = db.StringProperty(indexed=False, required=True)
    location = db.StringProperty(indexed=False)
    start_time = db.DateTimeProperty(required=True)
    description = db.TextProperty()

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._key_name = self.get_slug()

    @classmethod
    def get_upcoming_events(cls, num=5, today=datetime.datetime.today):
        return cls.all().filter("start_time >=", today()).order('start_time').fetch(num)

    def get_slug(self):
        date = self.start_time
        return config.options.get('event_path_format', '') % {
            'slug': slugify(unicode(self.name)),
            'year': date.year,
            'month': date.month,
            'day': date.day,
        }