========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-mirtime/badge/?style=flat
    :target: https://readthedocs.org/projects/python-mirtime
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/mirtime.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/mirtime

.. |commits-since| image:: https://img.shields.io/github/commits-since/gpwls23/python-mirtime/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/gpwls23/python-mirtime/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mirtime.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/mirtime

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mirtime.svg
    :alt: Supported versions
    :target: https://pypi.org/project/mirtime

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mirtime.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/mirtime


.. end-badges

A new pipeline, mirTime, that predicts microRNA targets by integrating sequence features and time-series expression
profiles in a specific experimental condition.

* Free software: MIT license

Installation
============

::

    pip install mirtime

Documentation
=============


https://python-mirtime.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
