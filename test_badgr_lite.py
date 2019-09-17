"""badgr_lite unit tests"""

# Ignore methods that could be functions; pylint: disable=R0201


import json
import os
from tempfile import mkdtemp
import unittest
from unittest.mock import patch
import vcr

from badgr_lite import (BadgrLite, TokenFileNotFoundError,
                        RequiredBadgeAttributesMissing,
                        TokenAndRefreshExpired, Badge)


class BadgrLiteTestBase(unittest.TestCase):
    """BadgrLite setUp and tearDown"""

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

        return BadgrLite(token_filename=self.sample_token_file)

    def get_sample_attrs(self):
        """Return dictionary of test attributes for creating Badge"""

        return {
            'entity_type': 'BadgeClass',
            'entity_id': 'cTjxL52HQBiSgIp5JuVq5x',
            'open_badge_id': 'https://api.badgr.io/public/badges/cTjxL52HQBiSgIp5JuVq5x',
            'created_at': '2019-09-04T19:03:24Z',
            'created_by': 'Lj__badge_creator__VIB',
            'description': 'sample badge description',
            'issuer': '5D__sample_issuer__4Kg',
            'issuer_open_badge_id': 'https://api.badgr.io/public/issuers/5D__sample_issuer__4Kg',
            'name': 'Sample badge for Unit Tests',
            'image': 'https://media.badgr.io/uploads/badges/issuer_badgeclass_488caae0-6fb7-42b5-b94e-d4ea0ac7d22d.png',
            'alignments': [],
            'expires': {'amount': None, 'duration': None},
            'criteria_narrative': 'Sample criteria narrative text',
            'criteria_url': 'http://example.com/',
            'tags': ['python', 'unit-test'],
            'extensions': {}
        }


class TestBadgrLiteInstantiation(BadgrLiteTestBase):
    """Test BadgrLite Instantiation"""

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""
        badgr = self.get_badgr_setup()
        self.assertIsInstance(badgr, BadgrLite)

    def test_takes_a_token_file(self):
        """It takes a token file argument"""
        with self.assertRaises(TypeError):
            # TypeError: __init__() missing 1 required
            # positional argument: 'token_filename'

            # Intentionally no args; pylint: disable=E1120
            BadgrLite()

    def test_verifies_token_file_exists(self):
        """It verifies token file exists"""

        with self.assertRaises(TokenFileNotFoundError):
            BadgrLite(token_filename='./non_existent_token_file.json')

    def test_verifies_token_file_contains_json(self):
        """It verifies token file exists"""

        with open(self.sample_token_file, 'w') as stf_h:
            stf_h.write("Bad JSON")

        with self.assertRaises(json.decoder.JSONDecodeError):
            BadgrLite(token_filename=self.sample_token_file)

    def test_verifies_bearer_token(self):
        """It has a bearer token when instantiated"""

        badgr = self.get_badgr_setup()

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        self.assertEqual(badgr._token_data['token_type'], "Bearer")
        self.assertEqual(badgr._token_data['access_token'],
                         self._sample_token)

    @patch('badgr_lite.BadgrLite.refresh_token')
    def test_attempts_to_refresh_token_when_appropriate(self, mock):
        """It attempts to refresh token when http 401 has been received"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('vcr_cassettes/attempt_refresh_token.yaml'):
            with self.assertRaises(TokenAndRefreshExpired):
                badgr.communicate_with_server(self._sample_url)
        self.assertTrue(mock.called)

    def test_raises_token_expired_when_applicable(self):
        """It raises TokenExpired when applicable"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('vcr_cassettes/no_valid_auth_token.yaml'):
            with self.assertRaises(TokenAndRefreshExpired):
                badgr.communicate_with_server(self._sample_url)

    def test_refreshes_token_when_expired(self):
        """It refreshes the token when it is expired"""

        badgr = self.get_badgr_setup()

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        original_token = badgr._token_data['access_token']
        with vcr.use_cassette('vcr_cassettes/expired_auth_token.yaml'):
            badgr.communicate_with_server(self._sample_url)
            self.assertNotEqual(original_token,
                                badgr._token_data['access_token'])


class TestBadgrLiteBadgeMethods(BadgrLiteTestBase):
    """TestBadgrLite Badge related Methods"""

    def test_instantiates_badge(self):
        """It instantiates a Badge class"""
        attrs = self.get_sample_attrs()
        self.assertIsInstance(Badge(attrs), Badge)

    def test_has_required_attrs(self):
        """It has a list of required attributes for initialization"""
        for attr in ['entity_id', 'open_badge_id', 'created_at',
                     'created_by', 'issuer', 'issuer_open_badge_id', 'name',
                     'image', 'description', 'criteria_url',
                     'criteria_narrative', 'alignments', 'tags', 'expires',
                     'extensions']:
            self.assertIn(attr, Badge.REQUIRED_ATTRS)

    def test_fails_if_required_attrs_not_included(self):
        """It fails if required attributes not included"""

        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            with self.assertRaises(RequiredBadgeAttributesMissing):
                # We need more attrs than just created_at
                Badge({'created_at': '2019-09-04T19:03:24Z'})

    def test_should_give_a_list_for_badges(self):
        """It should give a list for badges"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(badgr.badges, list))

    def test_should_contain_badge_classes(self):
        """It should contain badge classes"""

        badgr = self.get_badgr_setup()
        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(badgr.badges[0], Badge))

    def test_badge_should_have_entity_id(self):
        badgr = self.get_badgr_setup()
        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            badge = badgr.badges[0]
            self.assertIsInstance(badge.entity_id, str)


if __name__ == '__main__':
    unittest.main()
