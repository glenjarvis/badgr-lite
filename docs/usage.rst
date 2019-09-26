=====
Usage
=====

To use badgr-lite in a project:

1. Create an account on either `Badgr`_ or an equivalent server.

2. Use your `Badgr`_ (or equivalent) username and password
   to generate OAuth tokens for use with your project:

  .. code-block:: bash

    curl -X POST 'https://api.badgr.io/o/token' -d "username=YOUREMAIL&password=YOURPASSWORD" > token.json

3. Install the `badgr-lite` package:

  .. code-block:: bash

    pip install badgr-lite

  Or (using the newly recommended way from Python.org:

  .. code-block:: bash

    pipenv install badgr-lite


Now you can award badges through either the Command Line (CLI) or Library (SDK).


.. _Badgr: https://badgr.io/


Command Line Example
--------------------

Sample Command Help:

  .. code-block:: bash

    $ badgr --help
    Usage: badgr [OPTIONS] COMMAND [ARGS]...

      Automate Badgr tasks without the overhead of badgr-server

    Options:
      --token-file PATH  File holding token credentials
      --help             Show this message and exit.

    Commands:
      award-badge  Award badge with BADGE_ID to RECIPIENT.
      list-badges  Pull and print a list of badges from server


``--token-file`` can be omitted if ``token.json`` filename is in current directory.

  .. code-block:: bash

    $ badgr --token-file token.json list-badges

    dTjxL52HQBiSgIp5JuVq5w  https://badgr.io/public/assertions/dTjxL52HQBiSgIp5JuVq5w       Bay Area Python Interest Group TDD Participant
    6YhFytMUQb2loOMEy63gQA  https://badgr.io/public/assertions/6YhFytMUQb2loOMEy63gQA       Bay Area Python Interest Group TDD Quizmaster
    zzExTDvOTnOx_R3YhwPf3A  https://badgr.io/public/assertions/zzExTDvOTnOx_R3YhwPf3A       Test Driven Development Fundamentals Champion
    zNjcY70FSn603SO9vMGhBA  https://badgr.io/public/assertions/zNjcY70FSn603SO9vMGhBA       Install Python with Virtual Environments
    ZN0CIo4NR7-GgrliDJzoTw  https://badgr.io/public/assertions/ZN0CIo4NR7-GgrliDJzoTw       Fivvr badge


  .. code-block:: bash

    $ badgr --token-file token.json award-badge --badge-id 2TfNNqMLT8CoAhfGKqSv6Q --recipient recipient@example.com

    IfK18iLWSNWhvnQxLPHSxA  https://badgr.io/public/assertions/IfK18iLWSNWhvnQxLPHSxA       <No name>


Library Examples
----------------

One could patch together curl commands to interact with the Badgr server
(although badgr-lite does make it much faster to get started).  However, the
real benefit of Badgr-Lite is directly using its library in whatever tool that
you are using to automate award assignments (e.g., Django server, Flask server,
etc.).


  .. code-block:: python

    >>> from badgr_lite.models import BadgrLite
    >>> badge_id = '2TfNNqMLT8CoAhfGKqSv6Q'
    >>> badge_data = {
    ...     "recipient": {
    ...         "identity": "recipient@example.com",
    ...     },
    ... }
    >>> badgr = BadgrLite(token_filename='./token.json')
    >>> badge = badgr.award_badge(badge_id, badge_data)
    >>> print(badge)
    q8nKaXMHTICZj7qhKEwutg  https://badgr.io/public/assertions/q8nKaXMHTICZj7qhKEwutg      <No name>


  .. warning::

     Do *not* check the ``token.json`` file into your code repository. This is a secret file and should
     be handled like any other file that stores passwords or secrets.


