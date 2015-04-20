#!/usr/bin/env python

import logging

import webapp2

import os

from handlers import MainHandler, SignupHandler, VerificationHandler, SetPasswordHandler, LoginHandler, LogoutHandler, \
    ForgotPasswordHandler, AuthenticatedHandler

# debug only in local development
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

# TODO(russomi): Find a better place to put this
logging.getLogger().setLevel(logging.DEBUG)

# config dictionary
config = {
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['name']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY'
    }
}

# routes dictionary
routes = [
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
                  handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated')
]

# exposed WSGI app referenced in app.yaml
app = webapp2.WSGIApplication(routes=routes, debug=debug, config=config)


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('404 Not Found!!1!')
    response.set_status(404)


def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)


app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
