========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |codacy| |codebeat| |codeclimate| |scrutinizer|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-mypy-structured-data/badge/?style=flat
    :target: https://readthedocs.org/projects/python-mypy-structured-data
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/mwchase/python-mypy-structured-data.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/mwchase/python-mypy-structured-data

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/mwchase/python-mypy-structured-data?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/mwchase/python-mypy-structured-data

.. |requires| image:: https://requires.io/github/mwchase/python-mypy-structured-data/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/mwchase/python-mypy-structured-data/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/mwchase/python-mypy-structured-data/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/mwchase/python-mypy-structured-data

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/e5dc55abb71e400094a09a5972b4e472
    :target: https://www.codacy.com/app/max-chase/python-mypy-structured-data?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mwchase/python-mypy-structured-data&amp;utm_campaign=Badge_Grade

.. |codebeat| image:: https://codebeat.co/badges/79cece12-06a9-48f8-8433-d802058c8d02
    :target: https://codebeat.co/projects/github-com-mwchase-python-mypy-structured-data-master
    :alt: Codebeat Code Quality Status

.. |codeclimate| image:: https://api.codeclimate.com/v1/badges/83c2f4c2395c0e76894a/maintainability
    :target: https://codeclimate.com/github/mwchase/python-mypy-structured-data/maintainability
    :alt: Code Climate Maintainability Score

.. |scrutinizer| image:: https://scrutinizer-ci.com/g/mwchase/python-mypy-structured-data/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/mwchase/python-mypy-structured-data/?branch=master
    :alt: Scrutinizer Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/mypy-structured-data.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/mypy-structured-data

.. |commits-since| image:: https://img.shields.io/github/commits-since/mwchase/python-mypy-structured-data/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mwchase/python-mypy-structured-data/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mypy-structured-data.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/mypy-structured-data

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mypy-structured-data.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/mypy-structured-data

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mypy-structured-data.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/mypy-structured-data


.. end-badges

A Mypy plugin for analyzing code written with the Structured Data library.

* Free software: MIT license

Installation
============

::

    pip install mypy-structured-data

Documentation
=============

https://python-mypy-structured-data.readthedocs.io/

Development
===========

To run the all tests run::

    tox
