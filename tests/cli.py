#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badgr_lite` package."""


import unittest

from click.testing import CliRunner

from badgr_lite import cli

class TestBadgrLiteCLI(unittest.TestCase):
    """Tests for `badgr_lite` package."""

    def setUp(self):
        self.runner = CliRunner()

    def test_main_cli_entry_point(self):
        """Installation calls into cli.main()"""
        result = self.runner.invoke(cli.main)
        self.assertEqual(0, result.exit_code)
        self.assertIn('Automate Badgr tasks without the overhead of badgr-server', result.output)


    def test_token_file_option(self):
        """CLI takes --token argument"""

        help_result = self.runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--token-file PATH  File holding token credentials' in help_result.output

if __name__ == '__main__':
    unittest.main()
