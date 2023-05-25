#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click

from badge.main import list_badges, award_badge


@click.group()
def badge():
    """Award Badges"""


# @click.option(
#   "--token-file",
#   type=click.Path(),
#   default="./token.json",
#   help="File holding token credentials",
# )
# @pass_config
# def main(config, token_file):
#    """Automate Badgr tasks without the overhead of badgr-server"""
#
#    config.token_file = token_file
#


# def list(config):
# @pass_config
@badge.command()
@click.option(
    "--token-file",
    type=click.Path(),
    default="./token.json",
    help="File holding token credentials",
)
def list(token_file):
    """Pull and print a list of badges from server"""
    list_badges(token_file)


# TODO
#    badgr = BadgrLite(token_filename=config.token_file)
#    try:
#        for badge in badgr.badges:
#            click.echo(badge)
#    except exceptions.TokenFileNotFoundError as err:
#        for line in err.args:
#            click.echo(line)


# @pass_config
# def award(config, badge_id, recipient, notify, evidence_url, evidence_narrative):
@badge.command()
@click.option("--badge-id", prompt="Badge ID", help="ID of badge to award")
@click.option(
    "--recipient", prompt="Recipient email", help="Email of recipient"
)
@click.option(
    "--notify/--no-notify", default=False, help="Should badgr notify recipient?"
)
@click.option("--evidence-url", help="Optional evidence-url for awarded badge")
@click.option(
    "--evidence-narrative", help="Optional evidence-narrative for awarded badge"
)
def award(badge_id, recipient, notify, evidence_url, evidence_narrative):
    """Award badge with BADGE_ID to RECIPIENT.

    If evidence is provided, both --evidence-url and --evidence-narrative
    should be used.
    """
    award_badge()


#    if xor(evidence_url, evidence_narrative):
#        raise click.UsageError(
#            """If one evidence paramater is used, both are needed:
#            --evidence-url and --evidence-narrative"""
#        )
#
#    badge_data = {
#        "recipient": {
#            "identity": recipient,
#        },
#        "notify": notify,
#    }
#
#    if evidence_url:
#        badge_data = ensure_evidence(badge_data)
#        badge_data["evidence"][0]["url"] = evidence_url
#        badge_data["evidence"][0]["narrative"] = evidence_narrative
#
#    try:
#        badgr = BadgrLite(token_filename=config.token_file)
#        result = badgr.award_badge(badge_id, badge_data)
#        click.echo(result)
#    except exceptions.TokenFileNotFoundError as err:
#        for line in err.args:
#            click.echo(line)


# from badgr_lite.models import BadgrLite
# from badgr_lite import exceptions
#
#
# class Config:
#    """Share configuration accross commands"""
#
#    def __init__(self):
#        self.token_file = None
#
#
# pass_config = click.make_pass_decorator(Config, ensure=True)
#
#
# def xor(first: bool, second: bool) -> bool:
#    """Return exclusive OR for boolean arguments"""
#
#    return (first and not second) or (not first and second)
#
#
# def ensure_evidence(badge_data: dict) -> dict:
#    """Given badge_data, ensure 'evidence' key exists with list value"""
#
#    if "evidence" not in badge_data:
#        badge_data["evidence"] = [{}]
#    return badge_data
#
