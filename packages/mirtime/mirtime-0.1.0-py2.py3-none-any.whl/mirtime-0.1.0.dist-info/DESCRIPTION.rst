========
Overview
========



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


Changelog
=========

0.1.0 (2019-01-14)
------------------

* First release on PyPI.


