#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Entry point for badgr_lite Command Line Interface"""

import click
from badge import commands as badge_commands


@click.group()
def cli():
    """badgr-lite command line tool"""


@cli.command()
def version():
    """Print current version"""
    click.echo("1.2.3")


cli.add_command(badge_commands.badge)

if __name__ == "__main__":
    cli()
