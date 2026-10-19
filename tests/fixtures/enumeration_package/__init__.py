#! python
"""Package fixture for enumerate_object_callables
The actual code lives in a submodule (re-exported here), and there are some names imported from unrelated modules.
"""

from functools import partial
from os import getcwd
from pathlib import Path

from .submodule import FixtureSubmoduleClass, fixture_submodule_function


def fixture_package_function(arg):
	"""Function defined in the package itself

	:param arg: Any argument
	:returns Any: the argument received
	"""

	return arg


class FixturePackageClass:
	"""Class defined in the package itself"""

	pass


fixture_partial = partial(fixture_package_function, 'partial')


def fixture_unknown_module_function():
	"""Function whose module can't be told"""

	pass
fixture_unknown_module_function.__module__ = None

fixture_data = 'not callable'
