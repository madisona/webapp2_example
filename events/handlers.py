

from base_handlers import BaseHandler

from events.models import Event


class EventList(BaseHandler):
    template_name = "events/event_list.html"

    def get(self):
        return self.render_response(self.template_name, object_list={})


class EventDetail(BaseHandler):
    template_name = "events/event_detail.html"

    def get(self, url_path):
        return self.render_response(self.template_name, object=self.get_object(url_path))

    def get_object(self, url_path):
        return Event.get_by_key_name(url_path)
