#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import requests

from .exceptions import TokenFileNotFoundError


def load_token(token_filename) -> dict:
    """Given initialization with token_filename, load token data

    Ensure token_filename exists. Load JSON data from the filename.
    Store in self._token_data
    """
    token_filename = Path(token_filename)
    if not token_filename.exists():
        raise TokenFileNotFoundError(
            "Token File Not Found.",
            TokenFileNotFoundError.__doc__,
        )
    with token_filename.open("r") as token_handler:
        return json.load(token_handler)


def prepare_headers(token_data):
    """Prepare headers for communication with the server"""

    return {
        "Authorization": "Bearer {}".format(token_data["access_token"]),
        "Content-Type": "application/json",
    }


def get_from_server(url: str, token_data) -> dict:
    """Communicate with the server"""

    print("Requesting from server")
    response = requests.get(url, headers=prepare_headers(token_data), timeout=5)
    if response.status_code == 401:
        refresh_token()
        response = requests.get(url, headers=prepare_headers())
        if response.status_code == 401:
            raise exceptions.TokenAndRefreshExpiredError
    assert response.status_code == 200
    return response.json()


def list_badges(token_filename) -> dict:
    """Get list of badges from Server

    Example:

    >>> badgr = BadgrLite(token_filename='./token.json')
    >>> for badge in badgr.badges:
    ...     print(badge)
    ...
    cTjxL52HQBiSgIp5JuVq5w: Bay Area Python Interest Group TDD Participant
    5YhFytMUQb2loOMEy63gQA: Bay Area Python Interest Group TDD Quiz Champion
    yzExTDvOTnOx_R3YhwPf3A: Test Driven Development Fundamentals Champion
    yNjcY70FSn603SO9vMGhBA: Install Python with Virtual Environments
    """
    token_data = load_token(token_filename)
    raw_data = get_from_server(
        "https://api.badgr.io/v2/badgeclasses", token_data
    )["result"]
    import pprint

    pprint.pprint(raw_data)
    # return [Badge(b) for b in raw_data]


def award_badge():
    print("Award")


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


# @pass_config
# TODO
#    badgr = BadgrLite(token_filename=config.token_file)
#    try:
#        for badge in badgr.badges:
#            click.echo(badge)
#    except exceptions.TokenFileNotFoundError as err:
#        for line in err.args:
#            click.echo(line)


# @pass_config

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
