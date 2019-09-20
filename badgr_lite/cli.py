# -*- coding: utf-8 -*-
# pylint: disable=E1120

"""Console script for badgr_lite."""

import click


@click.group()
@click.option('--token-file', type=click.Path(exists=True),
              default='./token.json',
              help="File holding token credentials")
def main(token_file):
    """Automate Badgr tasks without the overhead of badgr-server"""


if __name__ == "__main__":
    main()
