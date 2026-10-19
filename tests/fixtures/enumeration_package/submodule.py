#! python
"""Submodule of the package fixture for enumerate_object_callables"""

from pathlib import PurePath

from .sibling import fixture_sibling_function


def fixture_submodule_function(arg):
	"""Function defined in the submodule

	:param arg: Any argument
	:returns Any: the argument received
	"""

	return arg


class FixtureSubmoduleClass:
	"""Class defined in the submodule"""

	pass
