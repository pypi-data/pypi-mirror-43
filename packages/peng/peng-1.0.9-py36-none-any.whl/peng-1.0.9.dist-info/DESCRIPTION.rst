.. README.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details

.. image:: https://badge.fury.io/py/peng.svg
    :target: https://pypi.org/project/peng
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/l/peng.svg
    :target: https://pypi.org/project/peng
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/peng.svg
    :target: https://pypi.org/project/peng
    :alt: Python versions supported

.. image:: https://img.shields.io/pypi/format/peng.svg
    :target: https://pypi.org/project/peng
    :alt: Format

|

.. image::
    https://dev.azure.com/pmasdev/peng/_apis/build/status/pmacosta.peng?branchName=master
    :target: https://dev.azure.com/pmasdev/peng/_build?definitionId=6&_a=summary
    :alt: Continuous integration test status

.. image::
    https://img.shields.io/azure-devops/coverage/pmasdev/peng/6.svg
    :target: https://dev.azure.com/pmasdev/peng/_build?definitionId=6&_a=summary
    :alt: Continuous integration test coverage

.. image::
    https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pip.readthedocs.io/en/stable/?badge=stable
    :alt: Documentation status

|

Description
===========

.. role:: bash(code)
	:language: bash

.. _Cog: https://nedbatchelder.com/code/cog
.. _Coverage: https://coverage.readthedocs.io
.. _Decorator: https://raw.githubusercontent.com/micheles/decorator/mast
   er/docs/documentation.md
.. _Docutils: http://docutils.sourceforge.net/docs
.. _Funcsigs: https://pypi.org/project/funcsigs
.. _Mock: https://docs.python.org/3/library/unittest.mock.html
.. _Numpy: http://www.numpy.org
.. _Pexdoc: http://pexdoc.readthedocs.org
.. _Pmisc: https://pmisc.readthedocs.org
.. _Pydocstyle: http://www.pydocstyle.org
.. _Pylint: https://www.pylint.org
.. _PyParsing: https://pyparsing.wikispaces.com
.. _Pytest: http://pytest.org
.. _Pytest-coverage: https://pypi.org/project/pytest-cov
.. _Pytest-pmisc: http://pytest-pmisc.readthedocs.org
.. _Pytest-xdist: https://pypi.org/project/pytest-xdist
.. _Scipy: https://www.scipy.org
.. _Six: https://pythonhosted.org/six
.. _Sphinx: http://sphinx-doc.org
.. _ReadTheDocs Sphinx theme: https://github.com/rtfd/sphinx_rtd_theme
.. _Inline Syntax Highlight Sphinx Extension:
   https://bitbucket.org/klorenz/sphinxcontrib-inlinesyntaxhighlight
.. _Shellcheck Linter Sphinx Extension:
   https://pypi.org/project/sphinxcontrib-shellcheck
.. _Tox: https://testrun.org/tox
.. _Virtualenv: https://docs.python-guide.org/dev/virtualenvs

This package provides engineering-related classes and functions, including:

* A waveform class that is a first-class object:

    .. code-block:: python

        >>> import copy, numpy, peng
        >>> obj_a=peng.Waveform(
        ...     indep_vector=numpy.array([1, 2, 3]),
        ...     dep_vector=numpy.array([10, 20, 30]),
        ...     dep_name='obj_a'
        ... )
        >>> obj_b = obj_a*2
        >>> print(obj_b)
        Waveform: obj_a*2
        Independent variable: [ 1, 2, 3 ]
        Dependent variable: [ 20, 40, 60 ]
        Independent variable scale: LINEAR
        Dependent variable scale: LINEAR
        Independent variable units: (None)
        Dependent variable units: (None)
        Interpolating function: CONTINUOUS
        >>> obj_c = copy.copy(obj_b)
        >>> obj_a == obj_b
        False
        >>> obj_b == obj_c
        True

  Numerous functions are provided (trigonometric,
  calculus, transforms, etc.) and creating new functions that operate on
  waveforms is simple since all of their relevant information can be accessed
  through properties

* Handling numbers represented in engineering notation, obtaining
  their constituent components and converting to and from regular
  floats. For example:

    .. code-block:: python

        >>> import peng
        >>> x = peng.peng(1346, 2, True)
        >>> x
        '   1.35k'
        >>> peng.peng_float(x)
        1350.0
        >>> peng.peng_int(x)
        1
        >>> peng.peng_frac(x)
        35
        >>> str(peng.peng_mant(x))
        '1.35'
        >>> peng.peng_power(x)
        EngPower(suffix='k', exp=1000.0)
        >>> peng.peng_suffix(x)
        'k'

* Pretty printing Numpy vectors. For example:

    .. code-block:: python

        >>> from __future__ import print_function
        >>> import peng
        >>> header = 'Vector: '
        >>> data = [1e-3, 20e-6, 30e+6, 4e-12, 5.25e3, -6e-9, 70, 8, 9]
        >>> print(
        ...     header+peng.pprint_vector(
        ...         data,
        ...         width=30,
        ...         eng=True,
        ...         frac_length=1,
        ...         limit=True,
        ...         indent=len(header)
        ...     )
        ... )
        Vector: [    1.0m,   20.0u,   30.0M,
                             ...
                    70.0 ,    8.0 ,    9.0  ]

* Formatting numbers represented in scientific notation with a greater
  degree of control and options than standard Python string formatting.
  For example:

    .. code-block:: python

        >>> import peng
        >>> peng.to_scientific_string(
        ...     number=99.999,
        ...     frac_length=1,
        ...     exp_length=2,
        ...     sign_always=True
        ... )
        '+1.0E+02'

Interpreter
===========

The package has been developed and tested with Python 2.7, 3.5, 3.6 and 3.7
under Linux (Debian, Ubuntu), Apple macOS and Microsoft Windows

Installing
==========

.. code-block:: console

	$ pip install peng

Documentation
=============

Available at `Read the Docs <https://peng.readthedocs.io>`_

Contributing
============

1. Abide by the adopted `code of conduct
   <https://www.contributor-covenant.org/version/1/4/code-of-conduct>`_

2. Fork the `repository <https://github.com/pmacosta/peng>`_ from GitHub and
   then clone personal copy [#f1]_:

    .. code-block:: console

        $ github_user=myname
        $ git clone --recurse-submodules \
              https://github.com/"${github_user}"/peng.git
        Cloning into 'peng'...
        ...
        $ cd peng || exit 1
        $ export PENG_DIR=${PWD}
        $

3. The package uses two sub-modules: a set of custom Pylint plugins to help with
   some areas of code quality and consistency (under the ``pylint_plugins``
   directory), and a lightweight package management framework (under the
   ``pypkg`` directory). Additionally, the `pre-commit framework
   <https://pre-commit.com/>`_ is used to perform various pre-commit code
   quality and consistency checks. To enable the pre-commit hooks:

    .. code-block:: console

        $ cd "${PENG_DIR}" || exit 1
        $ pre-commit install
        pre-commit installed at .../peng/.git/hooks/pre-commit
        $

4. Ensure that the Python interpreter can find the package modules
   (update the :bash:`$PYTHONPATH` environment variable, or use
   `sys.paths() <https://docs.python.org/3/library/sys.html#sys.path>`_,
   etc.)

   .. code-block:: console

       $ export PYTHONPATH=${PYTHONPATH}:${PENG_DIR}
       $

5. Install the dependencies (if needed, done automatically by pip):

    * `Cog`_ (2.5.1 or newer)

    * `Coverage`_ (4.5.3 or newer)

    * `Decorator`_ (4.4.0 or newer)

    * `Docutils`_ (0.14 or newer)

    * `Funcsigs`_ (Python 2.x only, 1.0.2 or newer)

    * `Inline Syntax Highlight Sphinx Extension`_ (0.2 or newer)

    * `Mock`_ (Python 2.x only, 2.0.0 or newer)

    * `Numpy`_ (1.16.2 or newer)

    * `Pexdoc`_ (1.1.4 or newer)

    * `Pmisc`_ (1.5.8 or newer)

    * `PyParsing`_ (2.3.1 or newer)

    * `Pydocstyle`_ (3.0.0 or newer)

    * `Pylint`_ (Python 2.x: 1.9.4 or newer, Python 3.x: 2.3.1 or newer)

    * `Pytest`_ (4.3.1 or newer)

    * `Pytest-coverage`_ (2.6.1 or newer)

    * `Pytest-pmisc`_ (1.0.7 or newer)

    * `Pytest-xdist`_ (optional, 1.26.1 or newer)

    * `ReadTheDocs Sphinx theme`_ (0.4.3 or newer)

    * `Scipy`_ (1.2.1 or newer)

    * `Shellcheck Linter Sphinx Extension`_ (1.0.8 or newer)

    * `Six`_ (1.12.0 or newer)

    * `Sphinx`_ (1.8.5 or newer)

    * `Tox`_ (3.7.0 or newer)

    * `Virtualenv`_ (16.4.3 or newer)

6. Implement a new feature or fix a bug

7. Write a unit test which shows that the contributed code works as expected.
   Run the package tests to ensure that the bug fix or new feature does not
   have adverse side effects. If possible achieve 100\% code and branch
   coverage of the contribution. Thorough package validation
   can be done via Tox and Pytest:

   .. code-block:: console

       $ PKG_NAME=peng tox
       GLOB sdist-make: .../peng/setup.py
       py27-pkg create: .../peng/.tox/py27
       py27-pkg installdeps: -r.../peng/requirements/tests_py27.pip, -r.../peng/requirements/docs_py27.pip
       ...
         py27-pkg: commands succeeded
         py35-pkg: commands succeeded
         py36-pkg: commands succeeded
         py37-pkg: commands succeeded
         congratulations :)
       $

   `Setuptools <https://bitbucket.org/pypa/setuptools>`_ can also be used
   (Tox is configured as its virtual environment manager):

   .. code-block:: console

       $ PKG_NAME=peng python setup.py tests
       running tests
       running egg_info
       writing peng.egg-info/PKG-INFO
       writing dependency_links to peng.egg-info/dependency_links.txt
       writing requirements to peng.egg-info/requires.txt
       ...
         py27-pkg: commands succeeded
         py35-pkg: commands succeeded
         py36-pkg: commands succeeded
         py37-pkg: commands succeeded
         congratulations :)
       $

   Tox (or Setuptools via Tox) runs with the following default environments:
   ``py27-pkg``, ``py35-pkg``, ``py36-pkg`` and ``py37-pkg`` [#f3]_. These use
   the 2.7, 3.5, 3.6 and 3.7 interpreters, respectively, to test all code in
   the documentation (both in Sphinx ``*.rst`` source files and in
   docstrings), run all unit tests, measure test coverage and re-build the
   exceptions documentation. To pass arguments to Pytest (the test runner) use
   a double dash (``--``) after all the Tox arguments, for example:

   .. code-block:: console

       $ PKG_NAME=peng tox -e py27-pkg -- -n 4
       GLOB sdist-make: .../peng/setup.py
       py27-pkg inst-nodeps: .../peng/.tox/.tmp/package/1/peng-1.0.9.zip
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $

   Or use the :code:`-a` Setuptools optional argument followed by a quoted
   string with the arguments for Pytest. For example:

   .. code-block:: console

       $ PKG_NAME=peng python setup.py tests -a "-e py27-pkg -- -n 4"
       running tests
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $

   There are other convenience environments defined for Tox [#f3]_:

    * ``py27-repl``, ``py35-repl``, ``py36-repl`` and ``py37-repl`` run the
      Python 2.7, 3.5, 3.6 and 3.7 REPL, respectively, in the appropriate
      virtual environment. The ``peng`` package is pip-installed by Tox when
      the environments are created.  Arguments to the interpreter can be
      passed in the command line after a double dash (``--``).

    * ``py27-test``, ``py35-test``, ``py36-test`` and ``py37-test`` run Pytest
      using the Python 2.7, 3.5, 3.6 and 3.7 interpreter, respectively, in the
      appropriate virtual environment. Arguments to pytest can be passed in
      the command line after a double dash (``--``) , for example:

      .. code-block:: console

       $ PKG_NAME=peng tox -e py27-test -- -x test_peng.py
       GLOB sdist-make: .../peng/setup.py
       py27-pkg inst-nodeps: .../peng/.tox/.tmp/package/1/peng-1.0.9.zip
       ...
         py27-pkg: commands succeeded
         congratulations :)
       $
    * ``py27-test``, ``py35-test``, ``py36-test`` and ``py37-test`` test code
      and branch coverage using the 2.7, 3.5, 3.6 and 3.7 interpreter,
      respectively, in the appropriate virtual environment. Arguments to
      pytest can be passed in the command line after a double dash (``--``).
      The report can be found in
      :bash:`${PENG_DIR}/.tox/py[PV]/usr/share/peng/tests/htmlcov/index.html`
      where ``[PV]`` stands for ``2.7``, ``3.5``, ``3.6`` or ``3.7`` depending
      on the interpreter used.

8. Verify that continuous integration tests pass. The package has continuous
   integration configured for Linux, Apple macOS and Microsoft Windows (all via
   `Azure DevOps <https://dev.azure.com/pmasdev>`_).

9. Document the new feature or bug fix (if needed). The script
   :bash:`${PENG_DIR}/pypkg/build_docs.py` re-builds the whole package
   documentation (re-generates images, cogs source files, etc.):

   .. code-block:: console

       $ "${PENG_DIR}"/pypkg/build_docs.py -h
       usage: build_docs.py [-h] [-d DIRECTORY] [-r]
                            [-n NUM_CPUS] [-t]

       Build peng package documentation

       optional arguments:
         -h, --help            show this help message and exit
         -d DIRECTORY, --directory DIRECTORY
                               specify source file directory
                               (default ../peng)
         -r, --rebuild         rebuild exceptions documentation.
                               If no module name is given all
                               modules with auto-generated
                               exceptions documentation are
                               rebuilt
         -n NUM_CPUS, --num-cpus NUM_CPUS
                               number of CPUs to use (default: 1)
         -t, --test            diff original and rebuilt file(s)
                               (exit code 0 indicates file(s) are
                               identical, exit code 1 indicates
                               file(s) are different)

.. rubric:: Footnotes

.. [#f1] All examples are for the `bash <https://www.gnu.org/software/bash/>`_
   shell

.. [#f2] It is assumed that all the Python interpreters are in the executables
   path. Source code for the interpreters can be downloaded from Python's main
   `site <https://www.python.org/downloads/>`_

.. [#f3] Tox configuration largely inspired by
   `Ionel's codelog <https://blog.ionelmc.ro/2015/04/14/
   tox-tricks-and-patterns/>`_

License
=======

The MIT License (MIT)

Copyright (c) 2013-2019 Pablo Acosta-Serafini

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
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details

Changelog
=========

* 1.0.9 [2019-03-22]: Documentation and dependency update

* 1.0.8 [2019-03-08]: Speedup loading of large Touchstone files (Patch submitted
  by github/sotw1957). Minor other code style changes.

* 1.0.7 [2019-03-08]: Dropped support for Python 2.6, 3.3 and 3.4. Updates
  to support newest versions of dependencies. Abstracted package management to
  a lightweight framework

* 1.0.6 [2016-02-11]: Package build enhancements and fixes

* 1.0.5 [2016-02-09]: Python 3.6 support

* 1.0.4 [2016-09-19]: Fixed Touchstone read function for "MA" and "DB" formats
  where the angles were incorrectly treated as being in radians

* 1.0.3 [2016-07-29]: Fixed resolution loss when writing Touchstone files

* 1.0.2 [2016-07-25]:

   * Frequency vector is now always in Hertz regardless of unit used in
     Touchstone file

   * Minor documentation bug fixes

* 1.0.1 [2016-06-11]: Minor documentation build bug fix

* 1.0.0 [2016-05-12]: Final release of 1.0.0 branch

* 1.0.0rc1 [2016-05-11]: Initial commit, forked a subset from putil PyPI
  package


