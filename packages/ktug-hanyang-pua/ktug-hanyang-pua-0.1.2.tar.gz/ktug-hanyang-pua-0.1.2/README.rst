ktug-hanyang-pua
================

KTUG Hanyang PUA table reader/writer

This package provides reader/writer utility for files from `KTUG Hanyang PUA table project`_.

Note that this package does not handle HanyangPUA-to-UnicodeJamo conversion itself.

.. _KTUG Hanyang PUA table project: http://faq.ktug.org/faq/HanyangPuaTableProject


- Documentation: https://ktug-hanyang-pua.readthedocs.org


Development environment
-----------------------

To setup development environment::

   virtualenv -p python3.4 .
   bin/pip install -U setuptools pip pip-tools
   make
   make test test-report
