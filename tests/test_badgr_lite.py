#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ignore methods that could be functions; pylint: disable=R0201

"""Tests for `badgr_lite` package."""


import datetime
import json
import os
from tempfile import mkdtemp
import unittest

import vcr

from badgr_lite.models import BadgrLite, Badge
from badgr_lite import exceptions


class BadgrLiteTestBase(unittest.TestCase):
    """BadgrLite setUp, tearDown and helper methods"""

    def setUp(self):
        """Create temporary input files of varying flavors"""

        self._tempdir = mkdtemp()
        self._sample_token = "FVQ__sample_token__QYzzRracgjH"
        self._sample_url = 'https://api.badgr.io/v2/badgeclasses'
        self.sample_token_file =\
            os.path.join(self._tempdir, "sample_token_file.json")

        with open(self.sample_token_file, 'w') as stf_h:
            stf_h.write(json.dumps(
                {"access_token": self._sample_token,
                 "token_type": "Bearer",
                 "refresh_token": "vK__sample_refresh_token__AlPZ"}
            ))

    def tearDown(self):
        """Remove temporary files"""

        os.remove(self.sample_token_file)
        os.rmdir(self._tempdir)

    def get_badgr_setup(self):
        """Return BadgrLite instance for testing"""

        badgr = BadgrLite(token_filename=self.sample_token_file)
        badgr.load_token()
        return badgr

    def get_sample_badge(self):
        """Fetch single badge for other tests"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('tests/vcr_cassettes/badge_retrieval.yaml'):
            return badgr.badges[0]


class TestBadgeInstantiation(BadgrLiteTestBase):
    """Badge class instantiation tests"""

    def get_sample_attrs(self):
        """Return dictionary of test attributes for creating Badge"""

        return {
            'entity_type': 'BadgeClass',
            'entity_id': 'cTjxL52HQBiSgIp5JuVq5x',
            'open_badge_id': 'https://api.badgr.io/public/'
                             'badges/cTjxL52HQBiSgIp5JuVq5x',
            'created_at': '2019-09-04T19:03:24Z',
            'created_by': 'Lj__badge_creator__VIB',
            'description': 'sample badge description',
            'issuer': '5D__sample_issuer__4Kg',
            'issuer_open_badge_id': 'https://api.badgr.io/'
                                    'public/issuers/5D__sample_issuer__4Kg',
            'name': 'Sample badge for Unit Tests',
            'image': 'https://media.badgr.io/uploads/badges/'
                     'issuer_badgeclass_'
                     '488caae0-6fb7-42b5-b94e-d4ea0ac7d22d.png',
            'alignments': [],
            'expires': {'amount': None, 'duration': None},
            'criteria_narrative': 'Sample criteria narrative text',
            'criteria_url': 'http://example.com/',
            'tags': ['python', 'unit-test'],
            'extensions': {}
        }

    def test_instantiates_badge(self):
        """Badge() instantiates a Badge class"""

        attrs = self.get_sample_attrs()
        self.assertIsInstance(Badge(attrs), Badge)

    def test_has_required_attrs(self):
        """Badge has a list of required attributes for initialization"""

        for attr in ['entity_id', 'open_badge_id', 'created_at',
                     'created_by', 'issuer', 'issuer_open_badge_id',
                     'image', 'expires', 'extensions']:
            self.assertIn(attr, Badge.REQUIRED_ATTRS)

    def test_fails_if_required_attrs_not_included(self):
        """Badge() fails if required attributes not included"""

        with vcr.use_cassette('test/vcr_cassettes/badge_retrieval.yaml'):
            with self.assertRaises(exceptions.RequiredAttributesMissingError):
                # We need more attrs than just created_at
                Badge({'created_at': '2019-09-04T19:03:24Z'})


class TestBadgeBadgesMethod(BadgrLiteTestBase):
    """Badge.badges() related tests"""

    def test_should_give_a_list_for_badges(self):
        """Badge.badges() should give a list for badges"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('tests/vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(badgr.badges, list))

    def test_should_contain_badge_classes(self):
        """Badge.badges() should contain badge classes"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('tests/vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(badgr.badges[0], Badge))


class TestBadgeRequiredAttributes(BadgrLiteTestBase):
    """Badge() required attribute related tests"""

    def test_badge_should_have_entity_id(self):
        """Badge() should have an entity_id attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.entity_id, str)

    def test_badge_should_have_open_badge_id(self):
        """Badge() should have an open_badge_id attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.open_badge_id, str)

    def test_badge_should_have_created_at(self):
        """Badge() should have a created_at attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.created_at, datetime.datetime)

    def test_badge_should_have_created_by(self):
        """Badge() should have a created_by attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.created_by, str)

    def test_badge_should_have_issuer(self):
        """Badge() should have an issuer attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.issuer, str)

    def test_badge_should_have_issuer_open_badge_id(self):
        """Badge() should have an issuer_open_badge_id attribute"""

        badge = self.get_sample_badge()
        # It's a string, even though it often looks like a URL
        self.assertIsInstance(badge.issuer_open_badge_id, str)

    def test_badge_should_have_image(self):
        """Badge() should have an image attribute"""

        badge = self.get_sample_badge()
        # It's a string, even though it often looks like a URL
        self.assertIsInstance(badge.image, str)

    def test_badge_should_have_expires(self):
        """Badge() should have an expires attribute

        At the time of this writing, there isn't enough clarity about what the
        actual value of expires should be. The only assertion that can be made
        with confidence is that it exists.

        According to the OpenBadges FAQ (https://openbadges.org/faq/),

        "Some badges contain links to detailed evidence, expiration dates,
        searchable tags, and alignments to educational standards or
        frameworks."

        This would make one expect that it should be a datetime. However,
        instead of a datestring, the Badgr API returns:

        'expires': {'amount': None, 'duration': None},
        """

        badge = self.get_sample_badge()
        self.assertTrue(hasattr(badge, 'expires'))

    def test_badge_should_have_extensions(self):
        """Badge() should have an extensions attribute

        There are ways of extending OpenBadges:

        https://www.imsglobal.org/sites/default/
            files/Badges/OBv2p0Final/extensions/index.html

        However, we currently only ensure that the attribute exists.
        """

        badge = self.get_sample_badge()
        self.assertTrue(hasattr(badge, 'extensions'))


class TestBadgeOptionalAttributes(BadgrLiteTestBase):
    """Badge() optional() attribute related tests"""

    def test_badge_should_have_description(self):
        """Badge() may have an optional description attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.description, str)

    def test_badge_should_have_name(self):
        """Badge() may have an optional name attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.name, str)

    def test_badge_should_have_alignments(self):
        """Badge() may have an optional alignments attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.alignments, list)

    def test_badge_should_have_criteria_narrative(self):
        """Badge() may have an optoinal criteria_narrative attribute"""

        badge = self.get_sample_badge()
        self.assertIsInstance(badge.criteria_narrative, str)

    def test_badge_should_have_criteria_url(self):
        """Badge() may have an optional criteria_url attribute"""

        badge = self.get_sample_badge()
        # It's a string, even though it is used as a URL
        self.assertIsInstance(badge.criteria_url, str)

    def test_badge_should_have_tags(self):
        """Badge() may have an optional tags attribute"""

        badge = self.get_sample_badge()
        # It's a string, even though it is used as a URL
        self.assertIsInstance(badge.tags, list)


class TestBadgrLiteInstantiation(BadgrLiteTestBase):
    """Test BadgrLite Instantiation"""

    def test_instantiates_badgr_lite_class(self):
        """BadgrLite() instantiates a BadgrLite class"""
        badgr = self.get_badgr_setup()
        self.assertIsInstance(badgr, BadgrLite)

    def test_takes_a_token_file(self):
        """BadgrLite() takes a token file argument"""
        with self.assertRaises(TypeError):
            # TypeError: __init__() missing 1 required
            # positional argument: 'token_filename'

            # Intentionally no args; pylint: disable=E1120
            BadgrLite()

    def test_verifies_token_file_exists(self):
        """BadgrLite() verifies token file exists"""

        with self.assertRaises(exceptions.TokenFileNotFoundError):
            badgr = BadgrLite(token_filename='./non_existent_token_file.json')
            badgr.load_token()

    def test_verifies_token_file_contains_json(self):
        """BadgrLite() verifies token file exists"""

        with open(self.sample_token_file, 'w') as stf_h:
            stf_h.write("Bad JSON")

        with self.assertRaises(json.decoder.JSONDecodeError):
            badgr = BadgrLite(token_filename=self.sample_token_file)
            badgr.load_token()

    def test_verifies_bearer_token(self):
        """BadgrLite() has a bearer token when instantiated"""

        badgr = self.get_badgr_setup()

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        self.assertEqual(badgr._token_data['token_type'], "Bearer")
        self.assertEqual(badgr._token_data['access_token'],
                         self._sample_token)

    @unittest.mock.patch('badgr_lite.models.BadgrLite.refresh_token')
    def test_attempts_to_refresh_token_when_appropriate(self, mock):
        """BadgrLite() attempts to refresh token when http 401"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('tests/vcr_cassettes/try_refresh_token.yaml'):
            with self.assertRaises(exceptions.TokenAndRefreshExpiredError):
                badgr.get_from_server(self._sample_url)
        self.assertTrue(mock.called)

    def test_raises_token_expired_when_applicable(self):
        """BadgrLite() raises TokenExpired when applicable"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('tests/vcr_cassettes/no_valid_auth_token.yaml'):
            with self.assertRaises(exceptions.TokenAndRefreshExpiredError):
                badgr.get_from_server(self._sample_url)

    def test_refreshes_token_when_expired(self):
        """BadgrLite() refreshes the token when it is expired"""

        badgr = self.get_badgr_setup()

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        original_token = badgr._token_data['access_token']
        with vcr.use_cassette('tests/vcr_cassettes/expired_auth_token.yaml'):
            badgr.get_from_server(self._sample_url)
            self.assertNotEqual(original_token,
                                badgr._token_data['access_token'])


class TestBadgrLiteAwardMethod(BadgrLiteTestBase):
    """Test BadgrLite.award Method"""

    def get_sample_award_badge_data(self):
        """Sample data for .award() tests"""
        return {
            "recipient": {
                "identity": "joe@exmple.com"
            },
            "notify": True,
            "evidence": [{
                "url": "http://example.com/",
                "narrative": "Joe completed all..."
            }]
        }

    def get_sample_award_badge_id(self):
        """Sameple badge_id for .award() tests"""

        return '2TfNNqMLT8CoAhfGKqSv6Q'

    def test_award_badge_gives_badge_when_successful(self):
        """.award_badge() returns a badge when successful"""

        badgr = self.get_badgr_setup()

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            result = badgr.award_badge(
                self.get_sample_award_badge_id(),
                self.get_sample_award_badge_data())
            self.assertIsInstance(result, Badge)

    def test_award_badge_gives_error_when_given_bad_badge_id(self):
        """.award_badge() raises a BadBadgeIdError when given bad_id"""

        badgr = self.get_badgr_setup()

        with vcr.use_cassette('tests/vcr_cassettes/award_bad_badge_id.yaml'):
            with self.assertRaises(exceptions.BadBadgeIdError):
                badgr.award_badge('bad_badge_id',
                                  self.get_sample_award_badge_data())

    def test_award_badge_gives_error_when_given_bad_badge_data(self):
        """.award_badge() raises an wardBadgeBadDataError when given data

        Note that the details from the API are given to the exception for more
        details.
        """

        badgr = self.get_badgr_setup()

        with vcr.use_cassette('tests/vcr_cassettes/award_badge_bad_data.yaml'):
            with self.assertRaises(exceptions.AwardBadgeBadDataError):
                badgr.award_badge(
                    self.get_sample_award_badge_id(),
                    {'bad_badge_data': 1}
                )


if __name__ == '__main__':
    unittest.main()
