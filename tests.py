"""badgr_lite unit tests"""

import unittest
from badgr_lite import BadgrLite

class TestBadgrLiteMethods(unittest.TestCase):
    # pylint: disable=R0201
    # pylint: disable=C0111

    def test_instantiates_badgr_lite_class(self):
        BadgrLite()

if __name__ == '__main__':
    unittest.main()
