"""badgr_lite unit tests"""

import unittest
from badgr_lite import BadgrLite

class TestBadgrLiteMethods(unittest.TestCase):
    # pylint: disable=R0201
    # pylint: disable=C0111

    def test_instantiates_badgr_lite_class(self):
        """It instantiates a BadgrLite class"""
        BadgrLite(token_file=None)

    def test_takes_a_token_file(self):
        """It takes a token file argument"""
        BadgrLite(token_file='./test_token_file.json')

if __name__ == '__main__':
    unittest.main()
