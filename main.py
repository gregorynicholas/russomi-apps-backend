#!/usr/bin/env python

import logging

import webapp2

from handlers import MainHandler, SignupHandler, VerificationHandler, SetPasswordHandler, LoginHandler, LogoutHandler, \
    ForgotPasswordHandler, AuthenticatedHandler

# TODO(russomi): Find a better place to put this
logging.getLogger().setLevel(logging.DEBUG)


config = {
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['name']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY'
    }
}

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

app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)
