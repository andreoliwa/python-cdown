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

*(this project is a work in progress, still in alpha state)*

CLI interface and Python package to parse and validate CODEOWNERS files used by GitHub and GitLab (not tested with BitBucket yet).

Each CLI command tries to follow Unix's philosophy of `"Do one thing and do it well" <https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well>`_.

The commands mimic the interface of well-known tools like `grep <https://www.man7.org/linux/man-pages/man1/grep.1.html>`_, `ls <https://www.man7.org/linux/man-pages/man1/ls.1.html>`_, `git ls-files <https://git-scm.com/docs/git-ls-files>`_.
The very name of the project is a reference to `chown <https://www.man7.org/linux/man-pages/man1/chown.1.html>`_.


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

Motivation
==========

Why build yet another project instead of contributing to an existing one? There are other code owners tools, but none of them had all the features I'd like to use.

Below are alternatives to ``cdown`` with some of their features.

To the creators of these tools: thanks for the inspiration!

.. list-table::
    :stub-columns: 1

    * - Repository
      - Language
      - Features

    * - `beaugunderson/codeowners <https://github.com/beaugunderson/codeowners#cli-usage>`_
      - JavaScript
      - - Print files and its owners
        - List unowned files
        - Verify users/teams own a specific path

    * - `mszostok/codeowners-validator <https://github.com/mszostok/codeowners-validator>`_
      - Go
      - - Validator
        - GitHub action
        - Runs on Docker

    * - `toptal/codeowners-checker <https://github.com/toptal/codeowners-checker>`_
      - Ruby
      - - List all the changes grouped by an owner
        - Filter changes by owner

    * - `hmarr/codeowners <https://github.com/hmarr/codeowners>`_
      - Go
      - - Homebrew
        - Filter results by owner
        - Limit the files the tool looks at

    * - `hairyhenderson/go-codeowners <https://github.com/hairyhenderson/go-codeowners>`_
      - Go
      - - Go package without a CLI interface

    * - `timoschinkel/codeowners <https://github.com/timoschinkel/codeowners>`_
      - PHP
      - - PHP package without a CLI interface


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
