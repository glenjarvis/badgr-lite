#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badgr_lite` package."""


import os
import json
import tempfile
import unittest

from click.testing import CliRunner
import vcr

from badgr_lite import cli


class TestBadgrLiteBase(unittest.TestCase):
    """Test Base for setUp tearDown and test helper methods"""

    SAMPLE_TOKEN_DATA = {
        "access_token": "FVQ__sample_token__QYzzRracgjH",
        "token_type": "Bearer",
        "expires_in": 86400,
        "refresh_token": "vK__sample_refresh_token__AlPZ",
        "scope": "rw:profile rw:issuer rw:backpack"}

    def setUp(self):
        self.runner = CliRunner()
        self.create_token_file()
        self.cli_options = [
            '--token-file', self.token_file,
            'award-badge',
            '--badge-id', '2TfNNqMLT8CoAhfGKqSv6Q',
            '--recipient', 'recipient@example.com',
            '--notify',
            '--evidence-url', 'https://example.com',
            '--evidence-narrative', 'John Doe performed...']

    def tearDown(self):
        os.remove(self.token_file)

    def create_token_file(self) -> None:
        """Create token file for tests

        Although this is slightly more like a factory than a fixture, it
        feels like a more crude way to do the tests. Instead of making a
        fake token file, it feels like the approach should be to mock
        out the calls that access the token data.

        However, as of the time of this writing, the initial author of
        this library was not able to cleanly do this. Since the great is
        often the enemy of the good, we will leave this functioning
        approach.

        There is a good opportunity to refactor these tests to make them
        more streamlined so that creating a temporary token file is not
        needed.
        """
        _, self.token_file = tempfile.mkstemp(suffix='.json', prefix='token')
        with open(self.token_file, 'w') as tmp_file:
            tmp_file.write(json.dumps(TestBadgrLiteBase.SAMPLE_TOKEN_DATA))


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
            self.cli_options.remove('--badge-id')
            self.cli_options.remove('2TfNNqMLT8CoAhfGKqSv6Q')
            result = self.runner.invoke(
                cli.main, self.cli_options,
                input="2TfNNqMLT8CoAhfGKqSv6Q")
            self.assertEqual(0, result.exit_code)
            self.assertIn('Badge ID: 2TfNNqMLT8CoAhfGKqSv6Q', result.output)

    def test_cli_subcommand_award_badge_recipient(self):
        """CLI award-badge requires --recipient

        If a recipient is not provided, it will be prompted.

        In this test, we'll add "recipient@example.com" for the
        prompt input.
        """

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            self.cli_options.remove('--recipient')
            self.cli_options.remove('recipient@example.com')
            result = self.runner.invoke(
                cli.main, self.cli_options,
                input="recipient@example.com")
            self.assertEqual(0, result.exit_code)
            self.assertIn('Recipient email: recipient@example.com',
                          result.output)

    def test_cli_subcommand_award_badge_notify(self):
        """CLI award-badge allows --notify / --no-notify"""

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            result = self.runner.invoke(cli.main, self.cli_options)
            self.assertEqual(0, result.exit_code)

    def test_cli_subcommand_award_badge_evidence_url(self):
        """CLI award-badge allows --evidence_url"""

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            result = self.runner.invoke(cli.main, self.cli_options)
            # See also self.cli_options.
            self.assertEqual(0, result.exit_code)

    def test_cli_subcommand_award_badge_evidence_narrative(self):
        """CLI award-badge allows --evidence-narrative"""

        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            result = self.runner.invoke(cli.main, self.cli_options)
            # See also self.cli_options.
            self.assertEqual(0, result.exit_code)

    def test_cli_xor(self):
        """CLI has Exclusive OR (XOR) function

        This CLI needs one, or the other, but not both:

        A | B   | Result
        --+-+---+-------
        T | T   | False
        T | F   | True
        F | F   | True
        F | F   | False
        """

        self.assertEqual(cli.xor(True, True), False)
        self.assertEqual(cli.xor(True, False), True)
        self.assertEqual(cli.xor(False, True), True)
        self.assertEqual(cli.xor(False, False), False)

    def test_cli_subcommand_award_badge_xor_evidence(self):
        """CLI award-badge evidence requires URL and Narrative

        If either `--evidence-url` or `--evidence-narrative` is provided,
        require both.
        """
        with vcr.use_cassette('tests/vcr_cassettes/award_badge.yaml'):
            self.cli_options.remove('--evidence-narrative')
            self.cli_options.remove('John Doe performed...')
            result = self.runner.invoke(cli.main, self.cli_options)
            self.assertNotEqual(0, result.exit_code)
            self.assertIn(
                "If one evidence paramater is used, both are needed",
                result.output)

    def test_cli_subcommand_award_badge_ensure_evidence(self):
        """CLI has ensure_evidence function

        Function ensures there is an 'evidence' key and the associated value is
        a list.
        """
        badge_data = cli.ensure_evidence({})
        self.assertIn('evidence', badge_data.keys())
        self.assertTrue(isinstance(badge_data['evidence'], list))


if __name__ == '__main__':
    unittest.main()
