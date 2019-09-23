# -*- coding: utf-8 -*-
# pylint: disable=E1120, R0913, R0903, C0103
"""Console script for badgr_lite."""

import click


from badgr_lite.models import BadgrLite


class Config:
    """Share configuration accross commands"""

    def __init__(self):
        self.token_file = None


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--token-file', type=click.Path(),
              default='./token.json',
              help="File holding token credentials")
@pass_config
def main(config, token_file):
    """Automate Badgr tasks without the overhead of badgr-server"""


@main.command()
@pass_config
def list_badges(config):
    """Pull and print a list of badges from server"""

    badgr = BadgrLite(token_filename=config.token_file)
    for badge in badgr.badges:
        click.echo(badge)


if __name__ == "__main__":
    main()
