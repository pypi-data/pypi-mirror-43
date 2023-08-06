.. README.rst
.. Copyright (c) 2018-2019 Pablo Acosta-Serafini
.. See LICENSE for details

.. image:: https://badge.fury.io/py/pytest-pmisc.svg
    :target: https://pypi.org/project/pytest-pmisc
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/pytest-pmisc.svg
    :target: https://pypi.org/project/pytest-pmisc
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/pytest-pmisc.svg
    :target: https://pypi.org/project/pytest-pmisc
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/pytest-pmisc.svg
    :target: https://pypi.org/project/pytest-pmisc
    :alt: Format

|

.. image::
    https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pip.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation status

|

Description
===========

.. role:: bash(code)
	:language: bash

This module contains a simple Pytest plugin for the pmisc test module.

When using the functions in the `test
<https://pmisc.readthedocs.io/en/stable/api.html#test>`_ module of the
`pmisc <https://pmisc.readthedocs.io>`_ package
(`assert_arg_invalid <https://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_arg_invalid>`_,
`assert_exception <https://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_exception>`_,
`assert_prop <https://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_prop>`_,
`assert_ro_prop <https://pmisc.readthedocs.io/en/stable/api.html#pmisc.assert_ro_prop>`_, and
`compare_strings <https://pmisc.readthedocs.io/en/stable/api.html#pmisc.compare_strings>`_),
`Pytest <https://docs.pytest.org/en/latest/>`_ assertion failure reports stop at
the code line using these functions and do not continue into the pmisc test
module.  This focuses attention on the actual assertion failing, and improves
clarity and conciseness

Interpreter
===========

The plugin has been developed and tested with Python 2.7, 3.5, 3.6 and 3.7 under
Linux (Debian, Ubuntu), Apple macOS and Microsoft Windows

Installing
==========

.. code-block:: bash

	$ pip install pytest-pmisc

Documentation
=============

Available at `Read the Docs <https://pytest-pmisc.readthedocs.io>`_

License
=======

The MIT License (MIT)

Copyright (c) 2018-2019 Pablo Acosta-Serafini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
.. CHANGELOG.rst
.. Copyright (c) 2018-2019 Pablo Acosta-Serafini
.. See LICENSE for details

Changelog
=========

* 1.0.7 [2019-03-21]: Updated dependencies

* 1.0.6 [2019-03-02]: Updated dependencies to fix functionality

* 1.0.5 [2019-03-02]: Entry point bug fix

* 1.0.4 [2019-03-02]: Critical entry point bug fix

* 1.0.3 [2019-03-01]: Updated package management framework

* 1.0.2 [2019-02-19]: Documentation update

* 1.0.1 [2019-02-19]: Updated to newest dependency versions

* 1.0.0 [2018-02-18]: Initial release


