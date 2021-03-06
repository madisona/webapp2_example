
# need to import this first to set paths and load settings
import setup_env 

import webapp2
from webapp2_extras import routes

import config
import utils
from error_handlers import handle_404, handle_500


app = webapp2.WSGIApplication([
    routes.RedirectRoute(r'/', handler='base_handlers.Index', name='index', strict_slash=True),
    routes.RedirectRoute(r'/events/<url_path:\d{4}/\d{1,2}/[\w-]+>/', handler='events.handlers.EventDetail', name='event-detail', strict_slash=True),
    routes.RedirectRoute(r'/events/', handler='events.handlers.EventList', name='event-list', strict_slash=True),


], debug=utils.is_devel(), config=config.options)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    app.run()

if __name__ == '__main__':
    main()