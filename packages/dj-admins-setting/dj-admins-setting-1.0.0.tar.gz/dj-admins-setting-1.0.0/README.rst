=================
dj-admins-setting
=================

.. image:: https://badge.fury.io/py/dj-admins-setting.svg
    :target: http://badge.fury.io/py/dj-admins-setting

This utility is based on ``dj-database-url`` by Kenneth Reitz.

It allows to utilize the `12factor <http://www.12factor.net/backing-services>`_
inspired environments variable to configure the `ADMINS <https://docs.djangoproject.com/en/2.2/ref/settings/#admins>`_ emails list in a Django application.


Usage
=====

Import the package in ``settings.py``:

.. code:: python

    import dj_admins_setting


Fetch your admins emails. The default option is fetch them from ``ADMINS``
environment variable:

.. code:: python

    ADMINS = dj_admins_setting.config()

Other option is parse an arbitrary emails list string:

.. code:: python

    ADMINS = dj_admins_setting.parse('"Support" <support@email.com>, "Admins" <webmaster@email.com>')

This will result in a list of tuples like:

.. code:: python
   
   [('Support', 'support@email.com'), ('Admins', 'webmaster@email.com')]


CI status
=========

Development (master):

.. image:: https://travis-ci.org/hernantz/dj-admins-setting.svg?branch=master
  :target: http://travis-ci.org/hernantz/dj-admins-setting

.. image:: https://codecov.io/gh/hernantz/dj-admins-setting/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/hernantz/dj-admins-setting
