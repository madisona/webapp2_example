
import os
import sys
import logging

# putting third party libs in lib directory
lib_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

# Setting the version of django. Need to import the template
# file before using any django module because that sets up the
# django settings stuff...
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext.webapp import template

import webapp2
from webapp2_extras import routes

import config

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    # todo: send email when not debug, include request path, error info and context, etc...
    logging.exception(exception)
    if debug:
        from traceback import format_exc
        response.write(format_exc(exception))
    else:
        response.write('A server error occurred!')
    response.set_status(500)

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication([
    routes.RedirectRoute(r'/admin/events/add/', handler='events.admin_handlers.EventAdd', name='event-add', strict_slash=True),

    routes.RedirectRoute(r'/', handler='base_handlers.Index', name='index', strict_slash=True),
    routes.RedirectRoute(r'/events/<url_path:\d{4}/\d{1,2}/[\w-]+>/', handler='events.handlers.EventDetail', name='event-detail', strict_slash=True),
    routes.RedirectRoute(r'/events/', handler='events.handlers.EventList', name='event-list', strict_slash=True),



], debug=debug, config=config.options)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    app.run()

if __name__ == '__main__':
    main()