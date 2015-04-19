#!/usr/bin/env python

import logging
import webapp2


def user_required(handler):
    """
      Decorator that checks if there's a user associated with the current session.
      Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login



config = {
    'webapp2_extras.auth': {
        'user_model': 'models.User',
        'user_attributes': ['name']
    },
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY'
    }
}

app = webapp2.WSGIApplication([
                                  webapp2.Route('/', MainHandler, name='home'),
                                  webapp2.Route('/signup', SignupHandler),
                                  webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
                                                handler=VerificationHandler, name='verification'),
                                  webapp2.Route('/password', SetPasswordHandler),
                                  webapp2.Route('/login', LoginHandler, name='login'),
                                  webapp2.Route('/logout', LogoutHandler, name='logout'),
                                  webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
                                  webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated')
                              ], debug=True, config=config)

logging.getLogger().setLevel(logging.DEBUG)
