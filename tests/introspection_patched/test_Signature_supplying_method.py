#! python
"""Testing the introspection_patched Signature.supplying_method static method"""

from unittest import TestCase

from introspection.errors import MethodNotFound

from fixtures.introspection_patched import FixtureBaseWInit, FixtureClassWMethods, FixtureEmptyClass, FixtureSubclassWMarkedInit
from simplifiedapp.introspection_patched import Signature


class TestSignatureSupplyingMethod(TestCase):
	"""Tests for the Signature.supplying_method static method"""

	def test_own_method(self):
		"""Test "Signature.supplying_method" with a method defined (unmarked) in the class itself"""

		self.assertIs(FixtureBaseWInit.__dict__['__init__'], Signature.supplying_method(FixtureBaseWInit, '__init__'))

	def test_marked_method(self):
		"""Test "Signature.supplying_method" with a method marked with "does_not_alter_signature" (the next implementation in the MRO is used)"""

		self.assertIs(FixtureBaseWInit.__dict__['__init__'], Signature.supplying_method(FixtureSubclassWMarkedInit, '__init__'))

	def test_inherited_from_object(self):
		"""Test "Signature.supplying_method" with a method only implemented by "object" """

		self.assertIs(object.__init__, Signature.supplying_method(FixtureEmptyClass, '__init__'))

	def test_raw_attribute(self):
		"""Test "Signature.supplying_method" returning the raw attribute from the class namespace (not bound, not unwrapped)"""

		self.assertIsInstance(Signature.supplying_method(FixtureClassWMethods, 'static_method'), staticmethod)

	def test_not_found(self):
		"""Test "Signature.supplying_method" with a method that isn't implemented anywhere in the MRO"""

		self.assertRaises(MethodNotFound, Signature.supplying_method, FixtureClassWMethods, 'missing_method')
