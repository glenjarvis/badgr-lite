"""BadgrLite module for automating Badr awards (assertions)"""

import json
import os


class TokenFileNotFoundError(BaseException):
    """Token file not found

    The token_file argument that you passed into BadgrLite is not found.
    Please consider:
        - Using using `prime_initial_token` (see Installation instructions)
        - Checking the filename is correct
        - Ensuring the filename exists and is in JSON format
    """


class BadgrLite:
    """BadgrLite: Automate without the overhead of badgr-server"""
    # pylint: disable=R0903

    def __init__(self, token_file):
        if not os.path.exists(token_file):
            raise TokenFileNotFoundError(
                "Token File Not Found.",
                TokenFileNotFoundError.__doc__)

        with open(token_file, 'r') as token_handler:
            self._token_data = json.load(token_handler)
