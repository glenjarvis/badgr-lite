"""badgr_lite unit tests"""

import unittest

from badgr_lite import BadgrLite
import badgr_lite


class TestBadgrLiteMethods(unittest.TestCase):
    # pylint: disable=R0201
    # pylint: disable=C0111

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""
        BadgrLite(token_file='./previously_created_token_file.json')

    def test_takes_a_token_file(self):
        """It takes a token file argument"""
        BadgrLite(token_file='./previously_created_token_file.json')

    def test_verifies_token_file_exists(self):
        """It verifies Token file exists"""
        with self.assertRaises(badgr_lite.TokenFileNotFoundError):
            BadgrLite(token_file='./non_existent_token_file.json')


if __name__ == '__main__':
    unittest.main()
