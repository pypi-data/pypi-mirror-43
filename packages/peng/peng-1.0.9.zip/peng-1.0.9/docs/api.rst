.. api.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details

###
API
###

****************
Global variables
****************

.. autodata:: peng.constants.FP_ATOL
.. autodata:: peng.constants.FP_RTOL

************
Named tuples
************

.. autofunction:: peng.functions.EngPower
.. autofunction:: peng.NumComp
.. autofunction:: peng.wave_core.Point

*********
Functions
*********

.. autofunction:: peng.functions.no_exp
.. autofunction:: peng.functions.peng
.. autofunction:: peng.functions.peng_float
.. autofunction:: peng.functions.peng_frac
.. autofunction:: peng.functions.peng_int
.. autofunction:: peng.functions.peng_mant
.. autofunction:: peng.functions.peng_power
.. autofunction:: peng.functions.peng_suffix
.. autofunction:: peng.functions.peng_suffix_math
.. autofunction:: peng.functions.pprint_vector
.. autofunction:: peng.touchstone.read_touchstone
.. autofunction:: peng.touchstone.write_touchstone
.. autofunction:: peng.functions.remove_extra_delims
.. autofunction:: peng.functions.round_mantissa
.. autofunction:: peng.functions.to_scientific_string
.. autofunction:: peng.functions.to_scientific_tuple


********************
Waveform pseudo-type
********************

.. _WaveformClass:

Class
=====

.. autoclass:: peng.wave_core.Waveform
	:members: __add__,
                  __and__,
                  __bool__,
                  __contains__,
                  __copy__,
                  __delitem__,
                  __div__,
                  __eq__,
                  __floordiv__,
                  __ge__,
                  __getitem__,
                  __gt__,
                  __invert__,
                  __iter__,
                  __le__,
                  __len__,
                  __lshift__,
                  __lt__,
                  __mod__,
                  __mul__,
                  __ne__,
                  __neg__,
                  __nonzero__,
                  __or__,
                  __pos__,
                  __pow__,
                  __sub__,
                  __radd__,
                  __rand__,
                  __repr__,
                  __rfloordiv__,
                  __rlshift__,
                  __rmod__,
                  __rmul__,
                  __ror__,
                  __rpow__,
                  __rrshift__,
                  __rshift__,
                  __rsub__,
                  __rtruediv__,
                  __rxor__,
                  __setitem__,
                  __str__,
                  __truediv__,
                  __xor__,
                  complex,
                  dep_scale,
                  dep_units,
                  dep_vector,
                  indep_scale,
                  indep_units,
                  indep_vector,
                  interp,
                  real,
                  vectors
	:show-inheritance:

.. _WaveformFunctions:

Functions
=========

.. autofunction:: peng.wave_functions.acos
.. autofunction:: peng.wave_functions.acosh
.. autofunction:: peng.wave_functions.asin
.. autofunction:: peng.wave_functions.asinh
.. autofunction:: peng.wave_functions.atan
.. autofunction:: peng.wave_functions.atanh
.. autofunction:: peng.wave_functions.average
.. autofunction:: peng.wave_functions.ceil
.. autofunction:: peng.wave_functions.cos
.. autofunction:: peng.wave_functions.cosh
.. autofunction:: peng.wave_functions.db
.. autofunction:: peng.wave_functions.derivative
.. autofunction:: peng.wave_functions.exp
.. autofunction:: peng.wave_functions.fft
.. autofunction:: peng.wave_functions.fftdb
.. autofunction:: peng.wave_functions.ffti
.. autofunction:: peng.wave_functions.fftm
.. autofunction:: peng.wave_functions.fftp
.. autofunction:: peng.wave_functions.fftr
.. autofunction:: peng.wave_functions.find
.. autofunction:: peng.wave_functions.floor
.. autofunction:: peng.wave_functions.group_delay
.. autofunction:: peng.wave_functions.ifft
.. autofunction:: peng.wave_functions.ifftdb
.. autofunction:: peng.wave_functions.iffti
.. autofunction:: peng.wave_functions.ifftm
.. autofunction:: peng.wave_functions.ifftp
.. autofunction:: peng.wave_functions.ifftr
.. autofunction:: peng.wave_functions.imag
.. autofunction:: peng.wave_functions.integral
.. autofunction:: peng.wave_functions.log
.. autofunction:: peng.wave_functions.log10
.. autofunction:: peng.wave_functions.naverage
.. autofunction:: peng.wave_functions.nintegral
.. autofunction:: peng.wave_functions.nmax
.. autofunction:: peng.wave_functions.nmin
.. autofunction:: peng.wave_functions.phase
.. autofunction:: peng.wave_functions.real
.. autofunction:: peng.wave_functions.round
.. autofunction:: peng.wave_functions.sin
.. autofunction:: peng.wave_functions.sinh
.. autofunction:: peng.wave_functions.sqrt
.. autofunction:: peng.wave_functions.subwave
.. autofunction:: peng.wave_functions.tan
.. autofunction:: peng.wave_functions.tanh
.. autofunction:: peng.wave_functions.wcomplex
.. autofunction:: peng.wave_functions.wfloat
.. autofunction:: peng.wave_functions.wint
.. autofunction:: peng.wave_functions.wvalue

**********************
Contracts pseudo-types
**********************

Introduction
============

The pseudo-types defined below can be used in contracts of the
`PyContracts <https://andreacensi.github.io/contracts>`_ or
`Pexdoc <http://pexdoc.readthedocs.org>`_ libraries. As an example, with the
latter:

    .. code-block:: python

        >>> from __future__ import print_function
        >>> import pexdoc
        >>> from peng.ptypes import engineering_notation_suffix
        >>> @pexdoc.pcontracts.contract(suffix='engineering_notation_suffix')
        ... def myfunc(suffix):
        ...     print('Suffix received: '+str(suffix))
        ...
        >>> myfunc('m')
        Suffix received: m
        >>> myfunc(35)
        Traceback (most recent call last):
            ...
        RuntimeError: Argument `suffix` is not valid

Alternatively each pseudo-type has a :ref:`checker function <ContractCheckers>`
associated with it that can be used to verify membership. For example:

    .. code-block:: python

        >>> import peng.ptypes
        >>> # None is returned if object belongs to pseudo-type
        >>> peng.ptypes.engineering_notation_suffix('m')
        >>> # ValueError is raised if object does not belong to pseudo-type
        >>> peng.ptypes.engineering_notation_suffix(3.5) # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: [START CONTRACT MSG: engineering_notation_suffix]...

Description
===========

.. _EngineeringNotationNumber:

EngineeringNotationNumber
^^^^^^^^^^^^^^^^^^^^^^^^^

Import as :code:`engineering_notation_number`. String with a number represented
in engineering notation. Optional leading whitespace can precede the mantissa;
optional whitespace can also follow the engineering suffix. An optional sign (+
or -) can precede the mantissa after the leading whitespace. The suffix must be
one of :code:`'y'`, :code:`'z'`, :code:`'a'`, :code:`'f'`, :code:`'p'`,
:code:`'n'`, :code:`'u'`, :code:`'m'`, :code:`' '` (space), :code:`'k'`,
:code:`'M'`, :code:`'G'`, :code:`'T'`, :code:`'P'`, :code:`'E'`, :code:`'Z'` or
:code:`'Y'`.  The correspondence between suffix and floating point exponent is:

+----------+-------+--------+
| Exponent | Name  | Suffix |
+==========+=======+========+
| 1E-24    | yocto | y      |
+----------+-------+--------+
| 1E-21    | zepto | z      |
+----------+-------+--------+
| 1E-18    | atto  | a      |
+----------+-------+--------+
| 1E-15    | femto | f      |
+----------+-------+--------+
| 1E-12    | pico  | p      |
+----------+-------+--------+
| 1E-9     | nano  | n      |
+----------+-------+--------+
| 1E-6     | micro | u      |
+----------+-------+--------+
| 1E-3     | milli | m      |
+----------+-------+--------+
| 1E+0     |       |        |
+----------+-------+--------+
| 1E+3     | kilo  | k      |
+----------+-------+--------+
| 1E+6     | mega  | M      |
+----------+-------+--------+
| 1E+9     | giga  | G      |
+----------+-------+--------+
| 1E+12    | tera  | T      |
+----------+-------+--------+
| 1E+15    | peta  | P      |
+----------+-------+--------+
| 1E+18    | exa   | E      |
+----------+-------+--------+
| 1E+21    | zetta | Z      |
+----------+-------+--------+
| 1E+24    | yotta | Y      |
+----------+-------+--------+

.. _EngineeringNotationSuffix:

EngineeringNotationSuffix
^^^^^^^^^^^^^^^^^^^^^^^^^

Import as :code:`engineering_notation_suffix`. A single character string, one
of :code:`'y'`, :code:`'z'`, :code:`'a'`, :code:`'f'`, :code:`'p'`,
:code:`'n'`, :code:`'u'`, :code:`'m'`, :code:`' '` (space), :code:`'k'`,
:code:`'M'`, :code:`'G'`, :code:`'T'`, :code:`'P'`, :code:`'E'`, :code:`'Z'`
or :code:`'Y'`. :ref:`EngineeringNotationNumber` lists the correspondence
between suffix and floating point exponent

.. _IncreasingRealNumpyVector:

IncreasingRealNumpyVector
^^^^^^^^^^^^^^^^^^^^^^^^^

Import as :code:`increasing_real_numpy_vector`. Numpy vector in which all
elements are real (integers and/or floats) and monotonically increasing
(each element is strictly greater than the preceding one)

.. _NumberNumpyVector:

NumberNumpyVector
^^^^^^^^^^^^^^^^^

Import as :code:`number_numpy_vector`. Numpy vector in which all elements are
integers and/or floats and/or complex

.. _RealNumpyVector:

RealNumpyVector
^^^^^^^^^^^^^^^

Import as :code:`real_numpy_vector`. Numpy vector in which all elements are
real (integers and/or floats)

.. _TouchstoneData:

TouchstoneData
^^^^^^^^^^^^^^

Import as :code:`touchstone_data`. A dictionary with the following structure:

* **points** (*integer*) -- Number of data points

* **freq** (:ref:`IncreasingRealNumpyVector`) -- Frequency vector

* **pars** (:ref:`NumberNumpyVector`) -- Parameter data, its size is equal to
  :code:`nports` x :code:`nports` x :code:`points` where :code:`nports`
  represents the number of ports in the file

The dictionary keys are case sensitive

.. _TouchstoneNoiseData:

TouchstoneNoiseData
^^^^^^^^^^^^^^^^^^^

Import as :code:`touchstone_noise_data`. A dictionary with the following
structure:

* **points** (*integer*) -- Number of data points

* **freq** (:ref:`IncreasingRealNumpyVector`) -- Frequency vector

* **nf** (:ref:`RealNumpyVector`) -- Minimum noise figure vector in decibels

* **rc** (:ref:`NumberNumpyVector`) -- Source source reflection coefficient to
  realize minimum noise figure

* **res** (:ref:`RealNumpyVector`) -- Normalized effective noise resistance

The dictionary keys are case sensitive

.. _TouchstoneOptions:

TouchstoneOptions
^^^^^^^^^^^^^^^^^

Import as :code:`touchstone_options`. A dictionary with the following
structure:

* **units** (*string*) -- Frequency units, one of :code:`'GHz'`, :code:`'MHz'`,
  :code:`'KHz'` or :code:`'Hz'` (case insensitive, default :code:`'GHz'`)

* **ptype** (*string*) -- Parameter type, one of :code:`'S'`, :code:`'Y'`,
  :code:`'Z'`, :code:`'H'` or :code:`'G'` (case insensitive, default
  :code:`'S'`)

* **pformat** (*string*) -- Data point format type, one of :code:`'DB'`
  (decibels), :code:`'MA'` (magnitude and angle), or :code:`'RI'` (real and
  imaginary) (case insensitive, default :code:`'MA'`)

* **z0** (float) -- Reference resistance in Ohms, default 50 Ohms

The dictionary keys are case sensitive

.. _WaveInterpOption:

WaveInterpOption
^^^^^^^^^^^^^^^^

Import as :code:`wave_interp_option`. String representing a waveform
interpolation type, one of :code:`'CONTINUOUS'` or :code:`'STAIRCASE'`
(case insensitive)

.. _WaveScaleOption:

WaveScaleOption
^^^^^^^^^^^^^^^

Import as :code:`wave_scale_option`. String representing a waveform scale
type, one of :code:`'LINEAR'` or :code:`'LOG'` (case insensitive)

.. _WaveVectors:

WaveVectors
^^^^^^^^^^^

Import as :code:`wave_vectors`. Non-empty list of tuples in which each tuple
is a waveform point. The first item of a point tuple is its independent
variable and the second item of a point tuple is its dependent variable. The
vector formed by the first item of the point tuples is of
:ref:`IncreasingRealNumpyVector` pseudo-type; the vector formed by the second
item of the point tuples is of :ref:`RealNumpyVector` pseudo-type

.. _ContractCheckers:

Checker functions
=================

.. autofunction:: peng.ptypes.engineering_notation_number
.. autofunction:: peng.ptypes.engineering_notation_suffix
.. autofunction:: peng.ptypes.increasing_real_numpy_vector
.. autofunction:: peng.ptypes.number_numpy_vector
.. autofunction:: peng.ptypes.real_numpy_vector
.. autofunction:: peng.ptypes.touchstone_data
.. autofunction:: peng.ptypes.touchstone_noise_data
.. autofunction:: peng.ptypes.touchstone_options
.. autofunction:: peng.ptypes.wave_interp_option
.. autofunction:: peng.ptypes.wave_scale_option
.. autofunction:: peng.ptypes.wave_vectors
