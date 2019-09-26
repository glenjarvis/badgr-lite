==========
badgr-lite
==========

Automate awarding Open Badges to recipients without the overhead of a server

.. image:: https://img.shields.io/pypi/v/badgr_lite.svg
        :target: https://pypi.python.org/pypi/badgr_lite


.. image:: https://img.shields.io/travis/glenjarvis/badgr-lite.svg
        :target: https://travis-ci.org/glenjarvis/badgr-lite


.. image:: https://readthedocs.org/projects/badgr-lite/badge/?version=latest
        :target: https://badgr-lite.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/glenjarvis/badgr-lite/shield.svg
     :target: https://pyup.io/repos/github/glenjarvis/badgr-lite/
     :alt: Updates


Quick Start
-----------

Manage your badges (with `Badgr`_ ), but automate the award and retrieval of
badges with `badger-lite <https://github.com/glenjarvis/badgr-lite>`_.

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


Purpose
-------

`Open Badges <https://openbadges.org/>`_ are images with credential data baked
into them. They are liked a digitally signed certificate that is also an image
that can be displayed on the web. They can be validated for authenticity and
are a nice award to grant to people for jobs well done, passing quizzes and
much more.

Mozilla recently partnered with `Concentric Sky
<https://www.concentricsky.com/>`_. They built `Badgr`_ which makes badge
management so much easier (and less buggy).

At the time this project was created, however, there was no easy way to
automate the award of badges (e.g., on your own website) without having to
build a full and complicated `badgr-server
<https://github.com/concentricsky/badgr-server>`_ of your own.

This `badgr-lite`_ project solves that problem.


Tutorial
--------
If you are new to Open Badges and want to see how to use them (and automate
them with this project), go to `this tutorial
<https://badgr-lite.readthedocs.io/en/latest/tutorial.html>`_.


* Free software: MIT license
* Documentation: https://badgr-lite.readthedocs.io.
