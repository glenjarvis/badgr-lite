"""badgr_lite unit tests"""

import os
import json
from tempfile import mkdtemp
import unittest

from badgr_lite import BadgrLite
import badgr_lite


class TestBadgrLiteMethods(unittest.TestCase):
    """Test BadgrLite methods"""

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

    def tearDown(self):
        """Remove temporary files"""

        os.remove(self.sample_token_file)
        os.rmdir(self._tempdir)

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""

        BadgrLite(token_file=self.sample_token_file)

    def test_takes_a_token_file(self):
        """It takes a token file argument"""

        BadgrLite(token_file=self.sample_token_file)

    def test_verifies_token_file_exists(self):
        """It verifies token file exists"""

        with self.assertRaises(badgr_lite.TokenFileNotFoundError):
            BadgrLite(token_file='./non_existent_token_file.json')

    def test_verifies_token_file_contains_json(self):
        """It verifies token file exists"""

        BadgrLite(token_file=self.sample_token_file)

    def test_verifies_bearer_token(self):
        """It has a bearer token when instantiated"""

        badgr = BadgrLite(token_file=self.sample_token_file)

        # _token_data isn't meant to be exposed; pylint: disable=W0212
        self.assertEqual(badgr._token_data['token_type'], "Bearer")
        self.assertEqual(badgr._token_data['access_token'], self._sample_token)


if __name__ == '__main__':
    unittest.main()
