# Author: Felix Wallner
# Contact: felix.wallner@protonmail.com

"""A simple Python library to generate all combinations of possible splits
 for a stack with given height."""

# submodule import or imported with 'from stacksplit import *'
__all__ = ['split']

# version info (as described in PEP 396 -- Module Version Numbers)
from .__version__ import __version__, __version_info__

# import all methods reachable directly from package:
from .core import split
# Eg.
# >>> import stacksplit
# >>> stacksplit.split(num, parts)
# <generator object split at ...>
#
# or import split directly
# >>> from stacksplit import split
# >>> split(num, parts)
# <generator object split at ...>
