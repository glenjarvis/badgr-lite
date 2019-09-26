.. highlight:: shell

========
Tutorial
========


What is an Open Badge (And, how can I get one?)
-----------------------------------------------

`Open Badges <https://openbadges.org/>`_ are images with credential data baked
into them. They are like a signed certificate but are also an image that can
be displayed on the web, saved on your hard drive, shared on social media and
validated for authenticity.

There is data baked into the image that proves the badge is valid (and that it
was awarded to you). And, there are `verifier tools <https://badgecheck.io/>`_
that can be used to verify the vadge is genuine and even that it was awarded to
you.

Let's start by having you earn your first badge. Open a new tab and go to this
URL to earn your first badge:

`Get Your Web Explorer Badge Here <https://explore.badgr.io/>`_

If you get stuck in step 4 (like I did), the text is a lot larger than the box.
You will need to do the Ctrl-C, Command-C or equivalent for your computer to
copy the full text.

When you are finished, come back here to Validate Your Badge.


Validate your Badge
-------------------

After you have earned a badge, you should have an image that you can download
and keep. You should also have the option to store the badge in a Backpack.
A backpack is an easy way to collect and share your badges.

Now that you have your badge, let's pretend that we are someone else who sees
this image and wants to validate it's authenticity.

In another tab, open the `Open Badges 2.0 Validator`_
page. Choose the *upload badge image* and upload your badge. Choose the
*Verify* button. You should see a message similar to *This badge passed all
verification checks.*.

Now, that prooved the badge is valid. But, it didn't prove that it was awarded
to you. It can't do that until you enter the identifying information for the
user the badge was awarded to (often email address).

You probably see a message similar to this on the *This badge passed all
verification checks.* screen:

    "Recipient Not Verified: In order to test whether this badge has been awarded to
    the person or entity you expect, enter their profile data on the submission
    form."

Try again but, this time, use the personal identifiable information (like your
email) that you used to create the badge.


Validate someone else's badge
-----------------------------

Great! Now that you can validate badges, validate this one:

.. image:: https://media.badgr.io/uploads/badges/assertion-OnTs_y9OTvSMOYfHxrtu1g.png
        :target: https://badgr.io/public/assertions/OnTs_y9OTvSMOYfHxrtu1g

See if you can answer these questions (one answer is easy, one is harder):

* What day was it issued?
* To whom was it issued?

Since you have an image embedded within the webpage, you can try several ways
to validate it.  A simple way is to click on the link (it's target is the
public assertion which has a **Verify Badge** button.

However, you may also have chosen to right-click and *Copy Image Address* (or
similar function) and download the image from that address.

A more command-line, Unix-like approach would simply be to use the ``strings``
command against the file.  Among a lot of extra undecipherable data (images are
binary files), you should see this block of text.

  .. code-block:: bash

    IHDR
    siTXtopenbadges
      "@context": "https://w3id.org/openbadges/v2",
      "type": "Assertion",
      "id": "https://api.badgr.io/public/assertions/OnTs_y9OTvSMOYfHxrtu1g",
      "badge": "https://api.badgr.io/public/badges/U8cuzhs7T3SRJVhDCSFHEA",
      "image": "https://api.badgr.io/public/assertions/OnTs_y9OTvSMOYfHxrtu1g/image",
      "verification": {
        "type": "HostedBadge"
      },
      "issuedOn": "2019-09-04T20:19:49.371498+00:00",
      "recipient": {
        "salt": "2e6164fb38034b02ad663c6d7f90ce1f",
        "type": "email",
        "hashed": true,
        "identity": "sha256$c76d835413f6f2bd5daecebf84b49561c9b6c179ffa7099116790ef7bd333a9b"
    d:IDATx


.. _Open Badges 2.0 Validator: https://badgecheck.io/


Whichever approach that you took, you can verify the badge was issued on

  .. code-block:: bash

    2019-09-04T20:19:49.371498+00:00.

But, notice the recipient has an identity of

  .. code-block:: bash

    sha256$c76d835413f6f2bd5daecebf84b49561c9b6c179ffa7099116790ef7bd333a9b

as well as a salt (which is a good hint that encryption was used).

You know this was issued to an individual. You just don't know what individual.

However, if the individual told you the verification information was an email
of ``glen@glenjarvis.com``, then you should be able to verify it. It's easiest
just to use the `Open Badges 2.0 Validator`_ now that you understand what it is
doing.


Most badges must be earned
--------------------------

This first badge was a fairly easy badge to earn. It was a "Let's just get
started" easy badge.

However, some badges are harder to earn.

Also there are criteria and evidence portions to a badge. For example, see if
you can determine what I did to earn this badge. Also, see if you can find the
evidence URL for further proof.

.. image:: https://media.badgr.io/uploads/badges/assertion-4hmS9m3FQtyko40rkQ9bxQ.png
        :target: https://badgr.io/recipient/earned-badge/4hmS9m3FQtyko40rkQ9bxQ


Automating
----------

As you can see, `Concentric Sky`_ has done a fairly good job making Open Badges
accessible with their Badgr Server. You can create badges, award badges and do
most of what you need on their website.

If that is all you need, you do not need this `badgr-lite`_ software library.

However, what if you wanted to do most of the work of creating badges with nice
images, etc. on the Badgr server BUT you wanted a web page to automatically
award those badges from a website?  That's the problem `badgr-lite`_ solves.

You can get started quickly with `badgr-lite`_ by `clicking here
<https://github.com/glenjarvis/badgr-lite>`_ and scrolling down to the section
**Quick Start** section.

Can you do it for me?
---------------------

Yes! If you don't have the bandwith to handle this integration with your Badgr
(Canvas, Blackboard, etc.) system, we will happily do this for you.

We are a safe B2B vendor that can solve this problem so that you can work on
other issues.  Email **contact@glenjarvis.com**

.. _Concentric Sky: https://www.concentricsky.com/
.. _badgr-lite: https://github.com/glenjarvis/badgr-lite
