"""BadgrLite module for automating Badr awards (assertions)"""
# pylint: disable=R1710

import datetime
import json
import re
import os

import pytz
import requests
from requests.models import Response


UTC = pytz.timezone("UTC")
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_MILLISECOND_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


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


def to_datetime(potential_datetime):
    """Given string, return UTC aware datetime"""

    final_datetime = potential_datetime
    if isinstance(potential_datetime, str):
        try:
            final_datetime = datetime.datetime.strptime(
                potential_datetime, DATETIME_FORMAT)
        except ValueError:
            final_datetime = datetime.datetime.strptime(
                potential_datetime, DATETIME_MILLISECOND_FORMAT)
        final_datetime = UTC.localize(final_datetime)
    return final_datetime


class TokenFileNotFoundError(BaseException):
    """Token file not found

    The token_filename argument that you passed into BadgrLite is not found.
    Please consider:
        - Using using `prime_initial_token` (see Installation instructions)
        - Checking the filename is correct
        - Ensuring the filename exists and is in JSON format
    """


class TokenAndRefreshExpiredError(BaseException):
    """Token expired

     The token has expired. We tried refreshing the token from the refresh
     token and are still not able to get authorization to work correctly.

     Use `prime_initial_token` (see Installation instructions) to reconfigure
     tokens.
     """


class RequiredAttributesMissingError(BaseException):
    """Required Badge Attributes Missing"""


class BadBadgeIdError(BaseException):
    """Award Badge Failed Error

    Please consider the badge ID that you are trying to award is correct.
    """


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

    REQUIRED_JSON = ['entityId', 'expires', 'entityType', 'extensions',
                     'openBadgeId', 'createdBy', 'issuer', 'image',
                     'issuerOpenBadgeId', 'createdAt']
    REQUIRED_ATTRS = [pythonic(attr) for attr in REQUIRED_JSON]

    def __init__(self, attrs: dict) -> None:
        """Initialize with single dictionary

        All keys in REQUIRED_ATTRS are required to initialize properly.
        """
        self._attrs = attrs
        self._add_dynamic_attrs()

        pythonic_attrs = [pythonic(k) for k in attrs.keys()]
        missing_but_required = set(self.REQUIRED_ATTRS) - set(pythonic_attrs)

        if missing_but_required:
            raise RequiredAttributesMissingError(
                ", ".join(missing_but_required))

    def _add_dynamic_attrs(self):
        for key in self._attrs.keys():
            pythonic_key = pythonic(key)
            if pythonic_key == "created_at":
                self._attrs[key] = to_datetime(self._attrs[key])
            setattr(self, pythonic_key, self._attrs[key])

    def __str__(self):
        # pylint: disable=R1705,E1101
        if hasattr(self, 'name'):
            # Name isn't technically required
            return "{}: {}".format(self.entity_id, self.name)
        else:
            return "{}: <No name>".format(self.entity_id)


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
            raise TokenAndRefreshExpiredError
        else:
            assert response.status_code == 200
            raw_data = response.json()
            self._token_data = raw_data
            with open(self.token_filename, 'w') as token_handler:
                token_handler.write(json.dumps(raw_data))

    def prepare_headers(self) -> dict:
        """Prepare headers for communication with the server"""

        return {'Authorization': 'Bearer {}'.format(
            self._token_data['access_token']),
                'Content-Type': 'application/json'}

    def get_from_server(self, url: str) -> dict:
        """Communicate with the server"""

        response = requests.get(url, headers=self.prepare_headers())
        if response.status_code == 401:
            self.refresh_token()
            response = requests.get(url, headers=self.prepare_headers())
            if response.status_code == 401:
                raise TokenAndRefreshExpiredError
        assert response.status_code == 200
        return response.json()

    @property
    def badges(self) -> list:
        """Get list of badges from Server

        Example API usage:
        curl 'https://api.badgr.io/v2/badgeclasses'
            -H "Authorization: Bearer zEVAGKxdbw7i3gTD1hNqyb0l13mDmO"
        """
        raw_data = self.get_from_server(
            'https://api.badgr.io/v2/badgeclasses')['result']

        return [Badge(b) for b in raw_data]

    def _validate_award_badge_response(self, response: Response) -> None:
        """Review response from Badge().award and raise any exceptions"""
        # It's okay as a function here; pylint: disable=R0201

        if response.status_code == 404:
            raise BadBadgeIdError(BadBadgeIdError.__doc__)

        assert response.status_code == 201 and\
            response.json()['status']['success']
        assert len(response.json()['result']) == 1

    def award_badge(self, badge_id: str, badge_data: dict) -> Badge:
        """Given a previously created badge_id and badge_data, award badge

        Example:

        >>> badgr = BadgrLite(token_filename='./token.json')
        >>> badge_data = {
        ...     "name": "Sample badge",
        ...     "recipient": {
        ...         "identity": "joe@example.com"
        ...     },
        ...     "notify": True,
        ...     "evidence": [{
        ...         "url": "http://example.com/",
        ...         "narrative": "Glen completed all the prereqs for..."
        ...     }]
        ... }
        >>>
        >>> badge_id = '2TfNNqMLT8CoAhfGKqSv6Q'
        >>> result = badgr.award_badge(badge_id, badge_data)
        >>> print(result)
        qv4DMvnYT0Gwz7wquRasvg: <No name>
        """

        base = 'https://api.badgr.io/v2'
        url = '{}/badgeclasses/{}/assertions'.format(base, badge_id)
        headers = self.prepare_headers()
        response = requests.post(url, headers=headers, json=badge_data)
        if response.status_code == 401:
            self.refresh_token()
            response = requests.post(url, headers=headers, json=badge_data)
            if response.status_code == 401:
                raise TokenAndRefreshExpiredError

        self._validate_award_badge_response(response)
        return Badge(response.json()['result'][0])
