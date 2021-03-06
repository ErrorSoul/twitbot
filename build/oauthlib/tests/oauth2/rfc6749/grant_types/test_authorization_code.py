# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from ....unittest import TestCase

import json
import mock
from oauthlib.common import Request
from oauthlib.oauth2.rfc6749.errors import UnsupportedGrantTypeError
from oauthlib.oauth2.rfc6749.errors import InvalidRequestError
from oauthlib.oauth2.rfc6749.errors import InvalidClientError
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from oauthlib.oauth2.rfc6749.grant_types import AuthorizationCodeGrant
from oauthlib.oauth2.rfc6749.tokens import BearerToken


class AuthorizationCodeGrantTest(TestCase):

    def setUp(self):
        self.request = Request('http://a.b/path')
        self.request.scopes = ('hello', 'world')
        self.request.expires_in = 1800
        self.request.client = 'batman'
        self.request.client_id = 'abcdef'
        self.request.code = '1234'
        self.request.response_type = 'code'
        self.request.grant_type = 'authorization_code'

        self.request_state = Request('http://a.b/path')
        self.request_state.state = 'abc'

        self.mock_validator = mock.MagicMock()
        self.mock_validator.authenticate_client.side_effect = self.set_client
        self.auth = AuthorizationCodeGrant(request_validator=self.mock_validator)

    def set_client(self, request):
        request.client = mock.MagicMock()
        request.client.client_id = 'mocked'
        return True

    def test_create_authorization_grant(self):
        grant = self.auth.create_authorization_code(self.request)
        self.assertIn('code', grant)

        grant = self.auth.create_authorization_code(self.request_state)
        self.assertIn('code', grant)
        self.assertIn('state', grant)

    def test_create_token_response(self):
        bearer = BearerToken(self.mock_validator)
        h, token, s = self.auth.create_token_response(self.request, bearer)
        token = json.loads(token)
        self.assertIn('access_token', token)
        self.assertIn('refresh_token', token)
        self.assertIn('expires_in', token)
        self.assertIn('scope', token)

    def test_validate_token_request(self):
        mock_validator = mock.MagicMock()
        auth = AuthorizationCodeGrant(request_validator=mock_validator)
        request = Request('http://a.b/path')
        self.assertRaises(UnsupportedGrantTypeError,
                auth.validate_token_request, request)

        request.grant_type = 'authorization_code'
        self.assertRaises(InvalidRequestError,
                auth.validate_token_request, request)

        mock_validator.authenticate_client.return_value = False
        mock_validator.authenticate_client_id.return_value = False
        request.code = 'waffles'
        self.assertRaises(InvalidClientError,
                auth.validate_token_request, request)

        request.client = 'batman'
        mock_validator.authenticate_client = self.set_client
        mock_validator.validate_code.return_value = False
        self.assertRaises(InvalidGrantError,
                auth.validate_token_request, request)
