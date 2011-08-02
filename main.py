
import os
import sys
import logging

# putting third party libs in lib directory
lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from google.appengine.dist import use_library
use_library('django', '1.2')




import webapp2

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
config = {
    'STATIC_URL': '/static/',
}

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler='events.handlers.Index', name='index'),
    webapp2.Route(r'/events/<event_key:[\w-]+>/', handler='events.handlers.EventDetail', name='event-detail'),
    webapp2.Route(r'/events/', handler='events.handlers.EventList', name='event-list'),

], debug=debug, config=config)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    app.run()

if __name__ == '__main__':
    main()