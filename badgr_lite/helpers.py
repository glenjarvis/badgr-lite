# -*- coding: utf-8 -*-

"""BadgrLite Helper functions"""

import re
import datetime

import pytz


UTC = pytz.timezone("UTC")
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_MILLISECOND_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def pythonic(name: str) -> str:
    """Convert camelCase identifier to pythonic identifier

    Citaton: (https://stackoverflow.com/questions/1175208/
              elegant-python-function-to-convert-camelcase-
              to-snake-case/17328907)

    The Badgr API returns attributes in camel case (e.g., issuerOpenBadgeId).
    We wish to also see those attributes in a pythonic way
    (e.g., issuer_open_badgee_id).
    """
    regex_s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', regex_s1).lower()


def to_datetime(potential_datetime):
    """Given string, return UTC aware datetime"""

    final_datetime = potential_datetime
    if isinstance(potential_datetime, str):
        try:
            final_datetime = datetime.datetime.strptime(
                potential_datetime, DATETIME_FORMAT)
        except ValueError:
            final_datetime = datetime.datetime.strptime(
                potential_datetime, DATETIME_MILLISECOND_FORMAT)
        final_datetime = UTC.localize(final_datetime)
    return final_datetime
