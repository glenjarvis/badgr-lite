"""BadgrLite module for automating Badr awards (assertions)"""
# pylint: disable=R1710

import datetime
import json
import re
import os

import pytz
import requests


UTC = pytz.timezone("UTC")


def pythonic(name: str) -> str:
    """Convert camelCase identifier to pythonic identifier

    Citaton: (https://stackoverflow.com/questions/1175208/
              elegant-python-function-to-convert-camelcase-
              to-snake-case/17328907)

    The Badgr API returns attributes in camel case (e.g., issuerOpenBadgeId).
    We wish to also see those attributes in a pythonic way
    (e.g., issuer_open_badgee_id).
    """
    regex_s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', regex_s1).lower()


class TokenFileNotFoundError(BaseException):
    """Token file not found

    The token_filename argument that you passed into BadgrLite is not found.
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


class RequiredBadgeAttributesMissing(BaseException):
    """Required Badge Attributes Missing"""


class Badge:
    """Pythonic representation of API BadgeClass

    Given a dictionary when instantiating the object, create a Pythonic
    representation of a OpenBadge.

    The JSON object given by the Badgr API, loaded as a dict, can be used to
    instantiate the Badge class.

    JSON style attributes (e.g., `issuerOpenBadgeId`) are maintainced.
    However, the pythonic representation of the same object (e.g.,
    `issuer_open_badge_id`) is also created. This way Python consumers
    unfamiliar with the Badgr API will still have attributes that `git in their
    brain`.
    """
    # pylint: disable=R0903

    JSON_ATTRS = ['entityType', 'entityId', 'openBadgeId', 'createdAt',
                  'createdBy', 'issuer', 'issuerOpenBadgeId', 'name', 'image',
                  'description', 'criteriaUrl', 'criteriaNarrative',
                  'alignments', 'tags', 'expires', 'extensions']

    REQUIRED_ATTRS = [pythonic(attr) for attr in JSON_ATTRS]

    def __init__(self, attrs: dict) -> None:
        """Initialize with single dictionary

        All keys in REQUIRED_ATTRS are required to initialize properly.
        """
        self._attrs = attrs
        self._add_dynamic_attrs()

        pythonic_attrs = [pythonic(k) for k in attrs.keys()]
        missing_but_required = set(self.REQUIRED_ATTRS) - set(pythonic_attrs)

        if missing_but_required:
            raise RequiredBadgeAttributesMissing(
                ", ".join(missing_but_required))

    def __str__(self):
        return "{}: {}".format(self._attrs['entity_id'], self._attrs['name'])

    def _add_dynamic_attrs(self):
        for key in self._attrs.keys():
            pythonic_key = pythonic(key)
            if pythonic_key == "created_at" and \
                    isinstance(self._attrs[key], str):
                self._attrs[key] = datetime.datetime.strptime(
                    self._attrs[key], '%Y-%m-%dT%H:%M:%SZ')
                self._attrs[key] = UTC.localize(self._attrs[key])
            setattr(self, pythonic_key, self._attrs[key])


class BadgrLite:
    """BadgrLite: Automate without the overhead of badgr-server"""
    # pylint: disable=R0903

    def __init__(self, token_filename: str) -> None:
        self.token_filename = token_filename
        if not os.path.exists(token_filename):
            raise TokenFileNotFoundError(
                "Token File Not Found.",
                TokenFileNotFoundError.__doc__)

        with open(token_filename, 'r') as token_handler:
            self._token_data = json.load(token_handler)

    def refresh_token(self) -> None:
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
            with open(self.token_filename, 'w') as token_handler:
                token_handler.write(json.dumps(raw_data))

    def prepare_headers(self) -> dict:
        """Prepare headers for communication with the server"""

        return {'Authorization': 'Bearer {}'.format(
            self._token_data['access_token'])}

    def communicate_with_server(self, url: str) -> dict:
        """Communicate with the server"""

        response = requests.get(url, headers=self.prepare_headers())
        if response.status_code == 401:
            self.refresh_token()
            response = requests.get(url, headers=self.prepare_headers())
            if response.status_code == 401:
                raise TokenAndRefreshExpired
        assert response.status_code == 200
        return response.json()

    @property
    def badges(self) -> list:
        """Get list of badges from Server

        Example API usage:
        curl 'https://api.badgr.io/v2/badgeclasses'
            -H "Authorization: Bearer zEVAGKxdbw7i3gTD1hNqyb0l13mDmO"
        """
        raw_data = self.communicate_with_server(
            'https://api.badgr.io/v2/badgeclasses')['result']

        return [Badge(b) for b in raw_data]
