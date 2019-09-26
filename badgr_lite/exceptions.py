# -*- coding: utf-8 -*-

"""BadgrLite Custom Exceptions"""


class TokenFileNotFoundError(BaseException):
    """Token file not found

    The token_filename argument that you passed into BadgrLite is not found.
    Please consider:

    - Using using `prime_initial_token` (see Installation instructions)
    - Checking the filename is correct
    - Ensuring the filename exists and is in JSON format
    """


class TokenAndRefreshExpiredError(BaseException):
    """Token and refresh expired

     The token has expired. We tried refreshing the token from the refresh
     token and are still not able to get authorization to work correctly.

     Use `prime_initial_token` (see Installation instructions) to reconfigure
     tokens.
     """


class RequiredAttributesMissingError(BaseException):
    """Required Badge Attributes Missing"""


class BadBadgeIdError(BaseException):
    """Award Badge given bad badge_id

    Please consider the badge ID that you are trying to award is correct.
    """


class AwardBadgeBadDataError(BaseException):
    """Award Badge given bad data"""
