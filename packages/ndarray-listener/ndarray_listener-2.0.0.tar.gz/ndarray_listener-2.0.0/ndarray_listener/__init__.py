from __future__ import absolute_import as _absolute_import

from ._ndl import float64, ndl
from ._testit import test

__version__ = "2.0.0"

ndarray_listener = ndl

__all__ = ["__version__", "test", "ndl", "float64", "ndarray_listener"]
