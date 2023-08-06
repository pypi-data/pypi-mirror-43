=============================
Django Shift Work
=============================

.. image:: https://badge.fury.io/py/django-shift-work.svg
    :target: https://badge.fury.io/py/django-shift-work

.. image:: https://travis-ci.org/reyvel/django-shift-work.svg?branch=master
    :target: https://travis-ci.org/reyvel/django-shift-work

.. image:: https://codecov.io/gh/reyvel/django-shift-work/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/reyvel/django-shift-work

Middleware to check what shift is this

Documentation
-------------

The full documentation is at https://django-shift-work.readthedocs.io.

Quickstart
----------

Install Django Shift Work::

    pip install django-shift-work

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_shift_work.apps.DjangoShiftWorkConfig',
        ...
    )

Add Django Shift Work's URL patterns:

.. code-block:: python

    from django_shift_work import urls as django_shift_work_urls


    urlpatterns = [
        ...
        url(r'^', include(django_shift_work_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
