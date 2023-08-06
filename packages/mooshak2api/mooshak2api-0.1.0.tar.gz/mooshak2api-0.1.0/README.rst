mooshak2api
===========

.. image:: https://img.shields.io/pypi/v/mooshak2api.svg
    :target: https://pypi.python.org/pypi/mooshak2api
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/vCra/mooshak2api.png
   :target: https://travis-ci.org/vCra/mooshak2api
   :alt: Latest Travis CI build status

mooshak2api is a Python API for interacting with the Mooshak 2 REST API.

Usage
-----
Using this tool is super easy!

>>> import mooshak2api as api
>>> connection = api.login("http://localhost:8080/mooshak/api/", "test", "test", contest="ToPAS14")
>>> problem = api.problems.get(connection, "ToPAS14", "C")
>>> evaluation = problem.evaluate(connection, open("tests/example_code/test.c", "rb"))
>>> evaluation.status
'Wrong Answer'

Installation
------------

Simply run ``pip install mooshak2api``

Requirements
^^^^^^^^^^^^

`Python requests
<http://docs.python-requests.org/en/master/>`_ is required.

Compatibility
-------------

Only Python >= 3.6 is supported.
It is recommended you use the latest version of Mooshak 2, as some older versions do not work completely

Licence
-------

This software is released under the MIT License

Authors
-------

`mooshak2api` was written by `Aaron Walker <aaw13@aber.ac.uk>`_.
