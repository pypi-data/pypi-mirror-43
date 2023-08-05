.. CHANGELOG.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details

Changelog
=========

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
