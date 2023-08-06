""" Test the usecases supplied by the JWT Backend """
import os

from passlib.hash import pbkdf2_sha256
from protean.conf import active_config
from protean.core.tasklet import Tasklet

from authentic.backends import jwt
from authentic.usecases import LoginCallbackRequestObject
from authentic.usecases import LogoutRequestObject

from ..conftest import Account
from ..conftest import base_dir


class TestAuthenticBackends:
    """ Test the usecases of Authentic"""

    @classmethod
    def setup_class(cls):
        """ Setup instructions for this test case set """
        cls.account = Account.create({
            'email': 'johndoe@domain.com',
            'username': 'johndoe',
            'name': 'john doe',
            'password': pbkdf2_sha256.hash('duMmy@123'),
            'phone': '90080000800',
            'roles': ['ADMIN']
        })

    @classmethod
    def teardown_class(cls):
        """ Tear down instructions for this test case set"""
        cls.account.delete()

    def test_backend(self):
        """ Test jwt authentication backend """

        # Run the login callback usecase
        payload = {
            'account': Account.get(self.account.id)
        }
        response = Tasklet.perform(
            Account, jwt.LoginCallbackUseCase, LoginCallbackRequestObject,
            payload.copy())

        assert response is not None
        assert response.success is True
        access_token = response.value.get('access_token')
        assert access_token is not None

        # Use the token for authentication
        payload = {
            'auth_scheme': 'Bearer',
            'credentials': 'xxxxxxxxxxxxxxxxx',
        }
        response = Tasklet.perform(
            Account, jwt.AuthenticationUseCase,
            jwt.AuthenticationRequestObject, payload.copy())
        assert response is not None
        assert response.success is False
        assert response.value == {
            'code': 401,
            'message':
                {'credentials': 'Invalid JWT Token. Not enough segments'}}

        # Try again with the correct token
        payload['credentials'] = access_token
        response = Tasklet.perform(
            Account, jwt.AuthenticationUseCase,
            jwt.AuthenticationRequestObject, payload.copy())
        assert response is not None
        assert response.success is True

    def test_asymmetric_backend(self):
        """ Test jwt authentication backend with asymmetric alg"""
        # Update the config settings
        active_config.JWT_ALGORITHM = 'RS256'
        active_config.JWT_PRIVATE_KEY = os.path.join(
            base_dir, 'support/jwt_private_key.pem')
        active_config.JWT_PUBLIC_KEY = os.path.join(
            base_dir, 'support/jwt_public_key.pub')

        # Run the login callback usecase
        payload = {
            'account': Account.get(self.account.id)
        }
        response = Tasklet.perform(
            Account, jwt.LoginCallbackUseCase,
            LoginCallbackRequestObject, payload.copy())

        assert response is not None
        assert response.success is True
        access_token = response.value.get('access_token')

        assert access_token is not None

        # Use the token for authentication
        payload = {
            'auth_scheme': 'Bearer',
            'credentials': access_token,
        }
        response = Tasklet.perform(
            Account, jwt.AuthenticationUseCase,
            jwt.AuthenticationRequestObject, payload.copy())
        assert response is not None
        assert response.success is True

    def test_logout_callback(self):
        """ Test logout mechanism for the JWT Backend """
        # Run the login callback usecase
        payload = {
            'account': Account.get(self.account.id)
        }
        response = Tasklet.perform(
            Account, jwt.LoginCallbackUseCase,
            LoginCallbackRequestObject, payload.copy())

        assert response is not None
        assert response.success is True
        access_token = response.value.get('access_token')

        # Run the logout usecase
        response = Tasklet.perform(
            Account, jwt.LogoutCallbackUseCase, LogoutRequestObject,
            payload.copy())
        assert response is not None
        assert response.success is True

        # Authentication must fail
        # Use the token for authentication
        payload = {
            'auth_scheme': 'Bearer',
            'credentials': access_token,
        }
        response = Tasklet.perform(
            Account, jwt.AuthenticationUseCase,
            jwt.AuthenticationRequestObject, payload.copy())
        assert response is not None
        assert response.success is False
        assert response.value == {
            'code': 401, 'message': {'token': 'Invalid Token'}}
