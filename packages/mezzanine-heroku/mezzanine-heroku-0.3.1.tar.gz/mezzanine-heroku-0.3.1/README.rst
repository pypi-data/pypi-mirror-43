mezzanine-heroku (Python Library)
=================================

.. image:: https://travis-ci.org/heroku/mezzanine-heroku.svg?branch=master
    :target: https://travis-ci.org/heroku/mezzanine-heroku

This is a `Mezzanine <http://mezzanine.jupo.org/>`_ library for `Heroku <https://www.heroku.com/>`_ applications that ensures a seamless deployment and development experience.

Based on `django-heroku <https://github.com/heroku/django-heroku>`_

This library provides:

-  Settings configuration (Static files / WhiteNoise).
-  Logging configuration.
-  Test runner (important for `Heroku CI <https://www.heroku.com/continuous-integration>`_).

--------------

Mezzanine 4.3.1 and Django 1.11.20 is targeted, and Python 3 is supported.

Usage of mezzanine-heroku
-------------------------

In ``settings.py``, at the very bottom::

    …
    # Configure Mezzanine for Heroku.
    import mezzanine_heroku
    mezzanine_heroku.settings(locals())

This will automatically configure ``DATABASE_URL``, ``ALLOWED_HOSTS``, WhiteNoise (for static assets), Logging, and Heroku CI for your application.

**Bonus points!** If you set the ``SECRET_KEY`` environment variable, it will automatically be used in your Mezzanine settings, too!

Disabling Functionality
///////////////////////

``settings()`` also accepts keyword arguments that can be passed ``False`` as a value, which will disable automatic configuration for their specific areas of responsibility:

- ``databases``
- ``test_runner``
- ``staticfiles``
- ``allowed_hosts``
- ``logging``
- ``secret_key``
