# -*- coding: utf-8 -*-

"""BadgrLite module for automating Badr awards (assertions)"""

# pylint: disable=R1710
# pylint: disable=R1710

import json
import os

import requests
from requests.models import Response

from badgr_lite import exceptions
from .helpers import pythonic, to_datetime


class Badge:
    """Pythonic representation of API BadgeClass

    Given a dictionary when instantiating the object, create a Pythonic
    representation of a OpenBadge.

    The JSON object given by the Badgr API, loaded as a dict, can be used to
    instantiate the Badge class.
    """
    # There are enough public methods; pylint: disable=R0903
    # Attrs are dynamically assigned;  pylint: disable=E1101

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
            raise exceptions.RequiredAttributesMissingError(
                ", ".join(missing_but_required))

    def _add_dynamic_attrs(self):
        for key in self._attrs.keys():
            pythonic_key = pythonic(key)
            if pythonic_key == "created_at":
                self._attrs[key] = to_datetime(self._attrs[key])
            setattr(self, pythonic_key, self._attrs[key])

    def __str__(self):
        url = "https://badgr.io/public/assertions/{}".format(self.entity_id)
        name = "<No name>"
        if hasattr(self, 'name'):
            name = self.name

        return "{}\t{}\t{}".format(self.entity_id, url, name)


class BadgrLite:
    """Automate using Badgr API without the overhead of badgr-server"""
    # pylint: disable=R0903

    def __init__(self, token_filename: str) -> None:
        self.token_filename = token_filename
        self._token_data = None

    def load_token(self) -> None:
        """Given initialization with token_filename, load token data

        Ensure token_filename exists. Load JSON data from the filename.
        Store in self._token_data
        """
        if not os.path.exists(self.token_filename):
            raise exceptions.TokenFileNotFoundError(
                "Token File Not Found.",
                exceptions.TokenFileNotFoundError.__doc__)

        with open(self.token_filename, 'r') as token_handler:
            self._token_data = json.load(token_handler)

    def refresh_token(self):
        """Refresh access token from refresh_token"""

        response = requests.post(
            'https://api.badgr.io/o/token',
            data={'grant_type': 'refresh_token',
                  'refresh_token': self._token_data['refresh_token']})

        # An else after a raise is perfectly valid here; pylint: disable=R1720
        if response.status_code == 401:
            raise exceptions.TokenAndRefreshExpiredError
        else:
            assert response.status_code == 200
            raw_data = response.json()
            self._token_data = raw_data
            with open(self.token_filename, 'w') as token_handler:
                token_handler.write(json.dumps(raw_data))

    def prepare_headers(self):
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
                raise exceptions.TokenAndRefreshExpiredError
        assert response.status_code == 200
        return response.json()

    @property
    def badges(self) -> list:
        """Get list of badges from Server

        Example:

        >>> badgr = BadgrLite(token_filename='./token.json')
        >>> for badge in badgr.badges:
        ...     print(badge)
        ...
        cTjxL52HQBiSgIp5JuVq5w: Bay Area Python Interest Group TDD Participant
        5YhFytMUQb2loOMEy63gQA: Bay Area Python Interest Group TDD Quizmaster
        yzExTDvOTnOx_R3YhwPf3A: Test Driven Development Fundamentals Champion
        yNjcY70FSn603SO9vMGhBA: Install Python with Virtual Environments
        """
        self.load_token()
        raw_data = self.get_from_server(
            'https://api.badgr.io/v2/badgeclasses')['result']

        return [Badge(b) for b in raw_data]

    def _validate_award_badge_response(self, response: Response) -> None:
        """Review response from Badge().award and raise any exceptions"""
        # It's okay as a function here; pylint: disable=R0201

        if response.status_code == 404:
            raise exceptions.BadBadgeIdError(
                exceptions.BadBadgeIdError.__doc__)

        if response.status_code == 400:
            raise exceptions.AwardBadgeBadDataError(str(response.json()))

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

        self.load_token()
        base = 'https://api.badgr.io/v2'
        url = '{}/badgeclasses/{}/assertions'.format(base, badge_id)
        headers = self.prepare_headers()
        response = requests.post(url, headers=headers, json=badge_data)
        if response.status_code == 401:
            self.refresh_token()
            response = requests.post(url, headers=headers, json=badge_data)
            if response.status_code == 401:
                raise exceptions.TokenAndRefreshExpiredError

        self._validate_award_badge_response(response)
        return Badge(response.json()['result'][0])
