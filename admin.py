
# need to import this first to set paths and load settings
import setup_env

import webapp2
from webapp2_extras import routes

import config
import utils
from error_handlers import handle_404, handle_500


app = webapp2.WSGIApplication([
    routes.RedirectRoute(r'/events/add/',
                         handler='events.admin_handlers.EventAdd',
                         name='admin_event_add', strict_slash=True),
], debug=utils.is_devel(), config=config.options)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    app.run()

if __name__ == '__main__':
    main()