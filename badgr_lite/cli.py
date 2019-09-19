# -*- coding: utf-8 -*-

"""Console script for badgr_lite."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for badgr_lite."""
    click.echo("Replace this message by putting your code into "
               "badgr_lite.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
