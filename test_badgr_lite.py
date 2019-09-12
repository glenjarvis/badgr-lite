"""badgr_lite unit tests"""

import os
from tempfile import mkdtemp
import unittest

from badgr_lite import BadgrLite
import badgr_lite


class TestBadgrLiteMethods(unittest.TestCase):
    # pylint: disable=R0201
    # pylint: disable=C0111

    def setUp(self):
        """Create temporary input files of varying flavors"""
        self._tempdir = mkdtemp()
        self.empty_token_file =\
            os.path.join(self._tempdir, "empty_token_file")
        open(self.empty_token_file, 'a').close()
        self.simple_token_file =\
            os.path.join(self._tempdir, "simple_token_file.json")
        with open(self.simple_token_file, 'w') as stf_h:
            stf_h.write("{}")

    def tearDown(self):
        """Remove temporary files"""
        os.remove(self.empty_token_file)
        os.remove(self.simple_token_file)
        os.rmdir(self._tempdir)

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""
        BadgrLite(token_file=self.simple_token_file)

    def test_takes_a_token_file(self):
        """It takes a token file argument"""
        BadgrLite(token_file=self.simple_token_file)

    def test_verifies_token_file_exists(self):
        """It verifies token file exists"""
        with self.assertRaises(badgr_lite.TokenFileNotFoundError):
            BadgrLite(token_file='./non_existent_token_file.json')

    def test_verifies_token_file_contains_json(self):
        """It verifies token file exists"""
        BadgrLite(token_file=self.simple_token_file)


if __name__ == '__main__':
    unittest.main()
