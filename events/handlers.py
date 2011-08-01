
import webapp2

class EventsList(webapp2.RequestHandler):

    def get(self):
        return webapp2.Response("Events Page")