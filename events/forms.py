

from google.appengine.ext.db import djangoforms

from events import models

class EventForm(djangoforms.ModelForm):
    class Meta(object):
        model = models.Event

