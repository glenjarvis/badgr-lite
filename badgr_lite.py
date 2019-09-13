"""BadgrLite module for automating Badr awards (assertions)"""
# pylint: disable=R1710

import json
import os

import requests


class TokenFileNotFoundError(BaseException):
    """Token file not found

    The token_file argument that you passed into BadgrLite is not found.
    Please consider:
        - Using using `prime_initial_token` (see Installation instructions)
        - Checking the filename is correct
        - Ensuring the filename exists and is in JSON format
    """


class TokenAndRefreshExpired(BaseException):
    """Token expired

     The token has expired. We tried refreshing the token from the refresh
     token and are still not able to get authorization to work correctly.

     Use `prime_initial_token` (see Installation instructions) to reconfigure
     tokens.
     """


class BadgrLite:
    """BadgrLite: Automate without the overhead of badgr-server"""
    # pylint: disable=R0903

    def __init__(self, token_file):
        self.token_file = token_file
        if not os.path.exists(token_file):
            raise TokenFileNotFoundError(
                "Token File Not Found.",
                TokenFileNotFoundError.__doc__)

        with open(token_file, 'r') as token_handler:
            self._token_data = json.load(token_handler)

    def refresh_token(self):
        """
        curl -X POST 'https://api.badgr.io/o/token' \
           -d "grant_type=refresh_token&
               refresh_token=iCIdZMmWpcnh3nhsi4tWK6WOtRAuKa"
            {
                "access_token": "qmwatCYpNVzg6BcbtYp7ff1boMce8p",
                "token_type": "Bearer",
                "expires_in": 86400,
                "refresh_token": "fka9YUHEmcRMYQr03JYtDmi9OUb3MN",
                "scope": "rw:profile rw:issuer rw:backpack"
            }
        """
        response = requests.post(
            'https://api.badgr.io/o/token',
            data={'grant_type': 'refresh_token',
                  'refresh_token': self._token_data['refresh_token']})

        # An else after a raise is perfectly valid here; pylint: disable=R1720
        if response.status_code == 401:
            raise TokenAndRefreshExpired
        else:
            assert response.status_code == 200
            raw_data = response.json()
            self._token_data = raw_data
            with open(self.token_file, 'w') as token_handler:
                token_handler.write(json.dumps(raw_data))

    def prepare_headers(self):
        """Prepare headers for communication with the server"""

        return {'Authorization': 'Bearer {}'.format(
            self._token_data['access_token'])}

    def communicate_with_server(self, url):
        """Communicate with the server"""

        response = requests.get(url, headers=self.prepare_headers())
        if response.status_code == 401:
            self.refresh_token()
            response = requests.get(url, headers=self.prepare_headers())
            if response.status_code == 401:
                raise TokenAndRefreshExpired
        if response.status_code == 200:
            return response.json()

    def get_badges(self):
        """Get list of badges from Server

        Example API usage:
        curl 'https://api.badgr.io/v2/badgeclasses'
            -H "Authorization: Bearer zEVAGKxdbw7i3gTD1hNqyb0l13mDmO"
        """
        return self.communicate_with_server(
            'https://api.badgr.io/v2/badgeclasses')['result']

    badges = property(get_badges)
