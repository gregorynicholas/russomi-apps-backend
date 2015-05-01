"""Hello World API implemented using Google Cloud Endpoints.
Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import logging

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from models import User as UserModel

import os


WEB_CLIENT_ID = '998327152018-ut8ct7qrd5hpjkj96a78gq04pbhk8qpt.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'Hello'


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!'),
    Greeting(message='goodbye world!'),
])


@endpoints.api(name='helloworld', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class HelloWorldApi(remote.Service):
    """Helloworld API v1."""

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
        Greeting,
        times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                    required=True))

    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.multiply')
    def greetings_multiply(self, request):
        """

        :param request:
        :return: :rtype:
        """
        return Greeting(message=request.message * request.times)

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        """

        :param unused_request:
        :return: :rtype:
        """
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        """

        :param request:
        :return: :rtype: :raise endpoints.NotFoundException:
        """
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' %
                                              (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreeting/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None
                 else 'Anonymous')
        return Greeting(message='hello %s' % (email,))


class UserLoginRequestMessage(messages.Message):
    """Message to accept a username and password."""
    user_id = messages.StringField(1)
    password = messages.StringField(2)


class UserLoginResponseMessage(messages.Message):
    """ Message to return
    """
    """
    'access_token': token.token,
    'token_type': 'Bearer',
    'expires_in': token.bearer_token_timedelta.total_seconds(),
    'refresh_token': token.refresh_token
    """
    access_token = messages.StringField(1)
    token_type = messages.StringField(2)
    expires_in = messages.IntegerField(3)
    refresh_token = messages.StringField(4)


@endpoints.api(name='user', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class User(remote.Service):
    """User Service API v1."""

    @endpoints.method(UserLoginRequestMessage, UserLoginResponseMessage,
                      path='login', http_method='POST',
                      name='login')
    def user_login(self, request):
        """ Handles POST with user_id and password and returns Token
        """
        """
        :param request:
        :type request:
        :return:
        :rtype:
        """
        token = os.getenv('HTTP_AUTHORIZATION')
        logging.info('token: {}'.format(token))
        logging.info('user: {}'.format(request.user_id))
        logging.info('password: {}'.format(request.password))

        # based on the user_id and password
        user_id = request.user_id
        password = request.password

        # lookup user
        try:
            user, timestamp = UserModel.get_by_auth_password(user_id, password)
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', user_id, type(e))
            raise endpoints.api_exceptions.UnauthorizedException(message='Username or password not valid.')

        # generate a jwt bearer token
        # return response

        return UserLoginResponseMessage(access_token='some_access_token', token_type='bearer', expires_in=3600,
                                        refresh_token='some_refresh_token')


app = endpoints.api_server([HelloWorldApi, User])