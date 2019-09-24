#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badgr_lite` package."""


import os
import tempfile
import unittest

from click.testing import CliRunner
import vcr

from badgr_lite import cli


class TestBadgrLiteBase(unittest.TestCase):
    """Test Base for setUp tearDown and test helper methods"""

    def setUp(self):
        self.runner = CliRunner()


class TestBadgrLiteCLI(TestBadgrLiteBase):
    """Tests for `badgr_lite` package."""

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

    def test_cli_help_shows_subcommand_without_token(self):
        """CLI shows subcommands help without token

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

    def test_cli_subcommand_with_token(self):
        """CLI subcommands should take --token-file argument

        Even though we should still get `--help` on subcommands, the
        subcommands should use the `--token-file` argument (or
        it's default).
        """

        _, token_file = tempfile.mkstemp(suffix='.json', prefix='token')
        result = self.runner.invoke(
            cli.main,
            ['--token-file', token_file, 'list-badges', '--help'])
        self.assertEqual(0, result.exit_code)
        os.remove(token_file)


class TestBadgrLiteCLIListBadges(TestBadgrLiteBase):
    """BadgrLite CLI list-badge subcommand tests

    See also .models badges property tests
    """

    def test_cli_subcommand_list_badges_help(self):
        """CLI has subcommand list-badges"""

        result = self.runner.invoke(cli.main, ['list-badges', '--help'])
        self.assertEqual(0, result.exit_code)


class TestBadgrLiteCLIAwardBadge(TestBadgrLiteBase):
    """BadgrLite CLI award-badge subcommand tests"""

    def test_cli_subcommand_award_badge_help(self):
        """CLI has subcommand award-badge"""

        result = self.runner.invoke(cli.main, ['award-badge', '--help'])
        self.assertEqual(0, result.exit_code)

    def test_cli_subcommand_award_badge_badge_id(self):
        """CLI award-badge requires --badge-id

        If a Badge ID is not provided, it will be prompted.

        In this test, we'll add "Some Badge ID" for the
        prompt input.
        """

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            result = self.runner.invoke(
                cli.main, ['award-badge', ],
                input="Some Badge ID")
            self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
