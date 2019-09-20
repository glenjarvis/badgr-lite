#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `badgr_lite` package."""


import unittest

from click.testing import CliRunner

from badgr_lite import cli

class TestBadgrLiteCLI(unittest.TestCase):
    """Tests for `badgr_lite` package."""

    def test_main_cli_entry_point(self):
        """Installation calls into cli.main()"""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Automate Badgr tasks without the overhead of badgr-server' in result.output

if __name__ == '__main__':
    unittest.main()
