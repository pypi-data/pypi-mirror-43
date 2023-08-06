================
nose-progress
================

Give your tests a progress before testcase name 3 lines::

    pip install nose-progress
    cd your_project
    nosetests --with-progress


Features
========

Progress Like this
------------

::
  (venv) E:\workspace>nosetests -v -s test_case_0000.py --with-scheduling
   nose.config: INFO: Ignoring files matching ['^\\.', '^_', '^setup\\.py$']
   [1/2] test_case.test_case_0000.test_learn_3 ... ok
   [2/2] test_case.test_case_0000.test_lear_4 ... ok


Installation
============

::

  pip install nose-progressive


Upgrading
=========

To upgrade from an older version of nose-progressive, assuming you didn't
install it from git::

  pip install --upgrade nose-progress

Use
===

The simple way::

  nosetests --with-scheduling


Author
======

landhu, while waiting for tests to complete ;-)

Version History
===============


0.1
  * Initial release


