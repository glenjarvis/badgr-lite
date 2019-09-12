"""BadgrLite module for automating Badr awards (assertions)"""

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


class TokenExpired(BaseException):
    """Token expired"""


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

    def communicate_with_server(self, url):
        """Communicate with the server"""

        headers = {'Authorization': 'Bearer {}'.format(
            self._token_data['access_token'])}
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            self.refresh_token()

    def get_badges(self):
        """Get list of badges from Server

        Example API usage:
        curl 'https://api.badgr.io/v2/badgeclasses'
            -H "Authorization: Bearer zEVAGKxdbw7i3gTD1hNqyb0l13mDmO"
        """
        # WIP; pylint: disable=R0201
        return []
    badges = property(get_badges)
