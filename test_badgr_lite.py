"""badgr_lite unit tests"""

import json
import os
from tempfile import mkdtemp
import unittest
from unittest.mock import patch

from badgr_lite import BadgrLite, TokenFileNotFoundError


class BadgrLiteTestBase(unittest.TestCase):
    """BadgrLite setUp and tearDown"""

    def setUp(self):
        """Create temporary input files of varying flavors"""

        self._tempdir = mkdtemp()
        self._sample_token = "FVQ__sample_token__QYzzRracgjH"
        self.sample_token_file =\
            os.path.join(self._tempdir, "sample_token_file.json")

        with open(self.sample_token_file, 'w') as stf_h:
            stf_h.write(json.dumps(
                {"access_token": self._sample_token,
                 "token_type": "Bearer"}
            ))

        self.badgr = BadgrLite(token_file=self.sample_token_file)

    def tearDown(self):
        """Remove temporary files"""
        # tearDown should be a class not a function; pylint: disable=R0201

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
        """It attemps to refresh token when http 401 has been received"""

        sample_url = 'https://api.badgr.io/v2/badgeclasses'
        self.badgr.communicate_with_server(sample_url)
        self.assertTrue(mock.called)


class TestBadgrLiteMethods(BadgrLiteTestBase):
    """TestBadgrLite Methods"""

    def test_should_give_a_list_for_badges(self):
        """It should give a list for badges"""

        self.assertTrue(isinstance(self.badgr.badges, list))


if __name__ == '__main__':
    unittest.main()
