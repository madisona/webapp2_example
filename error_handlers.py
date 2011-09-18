
import logging


import webapp2

def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    # todo: send email when not debug, include request path, error info and context, etc...
    logging.exception(exception)

    app = webapp2.get_app()
    if app.debug:
        from traceback import format_exc
        response.write(format_exc(exception))
    else:
        response.write('A server error occurred!')
    response.set_status(500)