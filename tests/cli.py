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

    def test_cli_main_entry_point(self):
        """Installation calls into cli.main()"""
        result = self.runner.invoke(cli.main)
        self.assertEqual(0, result.exit_code)
        self.assertIn(
            'Automate Badgr tasks without the overhead of badgr-server',
            result.output)

    def test_cli_token_file_option(self):
        """CLI takes --token argument"""

        help_result = self.runner.invoke(cli.main, ['--help'])
        self.assertEqual(0, help_result.exit_code)
        self.assertIn(
            '--token-file PATH  File holding token credentials',
            help_result.output)

    def test_cli_subcommand_list_badges(self):
        """CLI has subcommand list-badges"""

        result = self.runner.invoke(cli.main, ['list-badges', '--help'])
        self.assertEqual(0, result.exit_code)

    def test_cli_help_shows_list_badges_without_token(self):
        """CLI help shows for list-badges subcommand without token

        If the `--token-file` option were required with
        `type=click.Path(exists=True)`, then the --token-file argument
        would need to point to a valid token before one could ask for
        syntactial help:

        >>> badgr list-badges --help

        We should be able to get help for the subcommand before the
        token file existence is enforced.
        """

        result = self.runner.invoke(cli.main, ['list-badges', '--help'])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
