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
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-cdown/badge/?style=flat
    :target: https://readthedocs.org/projects/python-cdown
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/gh/andreoliwa/python-cdown/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/andreoliwa/python-cdown

.. |version| image:: https://img.shields.io/pypi/v/cdown.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cdown

.. |wheel| image:: https://img.shields.io/pypi/wheel/cdown.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/cdown

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cdown.svg
    :alt: Supported versions
    :target: https://pypi.org/project/cdown

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cdown.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/cdown

.. |commits-since| image:: https://img.shields.io/github/commits-since/andreoliwa/python-cdown/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/andreoliwa/python-cdown/compare/v0.1.0...master



.. end-badges

Tools for code owners files

* Free software: MIT license

Installation
============

::

    pip install cdown

You can also install the in-development version with::

    pip install https://github.com/andreoliwa/python-cdown/archive/master.zip


Documentation
=============


https://python-cdown.readthedocs.io/


Development
===========

To run all the tests run::

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
