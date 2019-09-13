"""badgr_lite unit tests"""

# Ignore methods that could be functions; pylint: disable=R0201


import json
import os
from tempfile import mkdtemp
import unittest
from unittest.mock import patch
import vcr

from badgr_lite import (BadgrLite, TokenFileNotFoundError,
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

        self.badgr = BadgrLite(token_file=self.sample_token_file)

    def tearDown(self):
        """Remove temporary files"""

        os.remove(self.sample_token_file)
        os.rmdir(self._tempdir)


class TestBadgrLiteInstantiation(BadgrLiteTestBase):
    """Test BadgrLite Instantiation"""

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""

    def test_takes_a_token_file(self):
        """It takes a token file argument"""

    def test_verifies_token_file_exists(self):
        """It verifies token file exists"""

        with self.assertRaises(TokenFileNotFoundError):
            BadgrLite(token_file='./non_existent_token_file.json')

    def test_verifies_token_file_contains_json(self):
        """It verifies token file exists"""

        BadgrLite(token_file=self.sample_token_file)

    def test_verifies_bearer_token(self):
        """It has a bearer token when instantiated"""

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        self.assertEqual(self.badgr._token_data['token_type'], "Bearer")
        self.assertEqual(self.badgr._token_data['access_token'],
                         self._sample_token)

    @patch('badgr_lite.BadgrLite.refresh_token')
    def test_attempts_to_refresh_token_when_appropriate(self, mock):
        """It attempts to refresh token when http 401 has been received"""

        with vcr.use_cassette('vcr_cassettes/attempt_refresh_token.yaml'):
            with self.assertRaises(TokenAndRefreshExpired):
                self.badgr.communicate_with_server(self._sample_url)
        self.assertTrue(mock.called)

    def test_raises_token_expired_when_applicable(self):
        """It raises TokenExpired when applicable"""

        with vcr.use_cassette('vcr_cassettes/no_valid_auth_token.yaml'):
            with self.assertRaises(TokenAndRefreshExpired):
                self.badgr.communicate_with_server(self._sample_url)

    def test_refreshes_token_when_expired(self):
        """It refreshes the token when it is expired"""

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        original_token = self.badgr._token_data['access_token']
        with vcr.use_cassette('vcr_cassettes/expired_auth_token.yaml'):
            self.badgr.communicate_with_server(self._sample_url)
            self.assertNotEqual(original_token,
                                self.badgr._token_data['access_token'])


class TestBadgrLiteBadgeMethods(BadgrLiteTestBase):
    """TestBadgrLite Badge related Methods"""

    def test_instantiates_badge(self):
        """It instantiates a Badge class"""
        Badge({})

    def test_should_give_a_list_for_badges(self):
        """It should give a list for badges"""

        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(self.badgr.badges, list))

    def test_should_contain_badge_classes(self):
        """It should contain badge classes"""

        with vcr.use_cassette('vcr_cassettes/badge_retrieval.yaml'):
            self.assertTrue(isinstance(self.badgr.badges[0], Badge))


if __name__ == '__main__':
    unittest.main()
