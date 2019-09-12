"""BadgrLite module for automating Badr awards (assertions)"""

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
    # pylint: disable=R0903
    # pylint: disable=C0111

    def __init__(self, token_file):
        if not os.path.exists(token_file):
            raise TokenFileNotFoundError(
                "Token File Not Found.",
                TokenFileNotFoundError.__doc__)
