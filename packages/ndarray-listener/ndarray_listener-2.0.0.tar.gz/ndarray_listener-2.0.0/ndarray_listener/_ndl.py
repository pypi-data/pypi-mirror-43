from distutils.version import LooseVersion

import numpy as np


class float64(np.float64):
    r"""

    Examples
    --------

    .. doctest::

        >>> from ndarray_listener import ndl, float64
        >>>
        >>> print(float64(1.5))
        1.5
        >>> print(ndl(1.5))
        1.5
    """

    def __new__(cls, *args):
        return np.float64.__new__(cls, *args)

    def talk_to(self, me):
        r"""Not implemented.

        Array-scalars are immutable.
        """
        pass


class ndl(np.ndarray):
    r"""

    Examples
    --------

    A scalar is stored as a zero-dimensional array much like a NumPy scalar:

    .. doctest::

        >>> from __future__ import print_function
        >>> from ndarray_listener import ndl
        >>> from numpy import atleast_1d
        >>>
        >>> class Watcher(object):
        ...     def __init__(self, msg):
        ...         self._msg = msg
        ...
        ...     def __call__(self):
        ...         print(self._msg + " called me")
        ...
        >>> scalar = ndl(-0.5)
        >>>
        >>> you0 = Watcher("First guy")
        >>> you1 = Watcher("Second guy")
        >>>
        >>> scalar.talk_to(you0)
        >>> scalar.itemset(-1.0)
        First guy called me
        >>> s0 = scalar.copy()
        >>> s0.itemset(-0.5)
        First guy called me
        >>> s0.talk_to(you1)
        >>> scalar.itemset(0.0)
        First guy called me
        Second guy called me
        >>>
        >>> s1 = atleast_1d(scalar)
        >>> s1[0] = 1.0
        First guy called me
        Second guy called me

    One-dimension arrays are also supported:

    .. doctest::

        >>> from ndarray_listener import ndl
        >>> from numpy import atleast_1d
        >>> from numpy import set_printoptions
        >>>
        >>> set_printoptions(precision=2, suppress=True)
        >>>
        >>> vector = ndl([-0.5, 0.1])
        >>>
        >>> you0 = Watcher("First guy")
        >>> you1 = Watcher("Second guy")
        >>>
        >>> vector.talk_to(you0)
        >>>
        >>> vector[0] = 0.0
        First guy called me
        >>> vector[:] = 1.0
        First guy called me
        >>>
        >>> v0 = vector.copy()
        >>> v0.itemset(0, 1.1)
        First guy called me
        >>>
        >>> v0.itemset(1, 2.2)
        First guy called me
        >>>
        >>> v1 = v0.ravel()
        >>>
        >>> v1.talk_to(you1)
        >>> vector[-1] = 9.9
        First guy called me
        Second guy called me
    """

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)

        if hasattr(input_array, "_listeners"):
            obj._listeners = input_array._listeners
        else:
            obj._listeners = []

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._listeners = getattr(obj, "_listeners", [])

    if LooseVersion(np.__version__) < LooseVersion("1.13"):

        def __setslice__(self, *args, **kwargs):
            super(ndl, self).__setslice__(*args, **kwargs)
            self.__notify()

    def __setitem__(self, *args, **kwargs):
        super(ndl, self).__setitem__(*args, **kwargs)
        self.__notify()

    def __setattr__(self, *args, **kwargs):
        super(ndl, self).__setattr__(*args, **kwargs)
        if len(args) > 0 and args[0] == "_listeners":
            return
        self.__notify()

    def __getitem__(self, *args, **kwargs):
        v = super(ndl, self).__getitem__(*args, **kwargs)
        if isinstance(v, ndl):
            return v

        if np.isscalar(v):
            v = float64(v)
        else:
            v = ndl(v)

        for l in self._listeners:
            v.talk_to(l)

        return v

    def talk_to(self, me):
        self._listeners.append(me)

    def __notify(self):
        for l in self._listeners:
            l()

    def itemset(self, *args, **kwargs):
        super(ndl, self).itemset(*args, **kwargs)
        self.__notify()
