#! python
"""Module fixture for enumerate_object_callables, declaring its public names
Some of the declared names are imported from unrelated modules (a deliberate re-export, or a C accelerator module).
"""

from heapq import heappush
from os import getcwd
from pathlib import PurePath

__all__ = ['PurePath', 'fixture_public_function', 'heappush']


def fixture_public_function():
	"""Public function defined in the module itself"""

	pass


def fixture_unlisted_function():
	"""Function defined in the module itself, but not listed in "__all__" """

	pass
