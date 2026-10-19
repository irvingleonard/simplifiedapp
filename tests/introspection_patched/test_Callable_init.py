#! python
"""Testing the introspection_patched.Callable.__init__ and Callable._check_parent methods"""

from unittest import TestCase

from fixtures.introspection_patched import FixtureClassWMethods, FixtureEmptyClass, FixtureSubclassWMethods, FixtureSubclassWOverride, fixture_function
from simplifiedapp.introspection_patched import Callable


class TestCallableInit(TestCase):
	"""Tests for the Callable.__init__ method"""

	def test_not_callable(self):
		"""Test "Callable" with something that isn't callable"""

		self.assertRaises(ValueError, Callable, None)

	def test_wo_parent(self):
		"""Test "Callable" without a parent (it's inferred later, when needed)"""

		callable_ = Callable(fixture_function)
		self.assertIs(fixture_function, callable_._callable_)
		self.assertNotIn('parent', vars(callable_))

	def test_w_parent(self):
		"""Test "Callable" with a valid parent, which is stored"""

		self.assertIs(FixtureSubclassWMethods, Callable(FixtureClassWMethods.instance_method, parent=FixtureSubclassWMethods).parent)


class TestCallableCheckParent(TestCase):
	"""Tests for the Callable._check_parent method"""

	def test_not_a_class(self):
		"""Test "Callable._check_parent" with a parent that isn't a class"""

		self.assertRaises(TypeError, Callable, FixtureClassWMethods.instance_method, parent=FixtureClassWMethods(1))

	def test_bound_method(self):
		"""Test "Callable._check_parent" with a method bound to an instance of the parent (the instance is kept as the parent)"""

		instance = FixtureSubclassWMethods(1)
		self.assertIs(instance, Callable(instance.instance_method, parent=FixtureClassWMethods).parent)

	def test_class_method(self):
		"""Test "Callable._check_parent" with a method bound to a subclass of the parent (the subclass is kept as the parent)"""

		self.assertIs(FixtureSubclassWMethods, Callable(FixtureSubclassWMethods.class_method, parent=FixtureClassWMethods).parent)

	def test_bound_to_unrelated(self):
		"""Test "Callable._check_parent" with methods bound to an instance or a class unrelated to the parent"""

		self.assertRaises(ValueError, Callable, FixtureClassWMethods(1).instance_method, parent=FixtureEmptyClass)
		self.assertRaises(ValueError, Callable, FixtureClassWMethods.class_method, parent=FixtureSubclassWMethods)

	def test_method_descriptor(self):
		"""Test "Callable._check_parent" with a C implemented method and a subclass of the class it belongs to"""

		self.assertIs(FixtureSubclassWMethods, Callable(object.__repr__, parent=FixtureSubclassWMethods).parent)

	def test_method_descriptor_unrelated(self):
		"""Test "Callable._check_parent" with a C implemented method and a class unrelated to the one it belongs to"""

		self.assertRaises(ValueError, Callable, str.upper, parent=bytes)

	def test_inherited_function(self):
		"""Test "Callable._check_parent" with a function inherited by the parent"""

		self.assertIs(FixtureSubclassWMethods, Callable(FixtureClassWMethods.instance_method, parent=FixtureSubclassWMethods).parent)

	def test_static_method(self):
		"""Test "Callable._check_parent" with a static method (the "staticmethod" object in the class is unwrapped)"""

		self.assertIs(FixtureClassWMethods, Callable(FixtureClassWMethods.static_method, parent=FixtureClassWMethods).parent)

	def test_attached_function(self):
		"""Test "Callable._check_parent" with a function attached to the class under a different name (found by identity, not by name)"""

		self.assertIs(FixtureClassWMethods, Callable(FixtureClassWMethods.attached_method, parent=FixtureClassWMethods).parent)

	def test_overridden_function(self):
		"""Test "Callable._check_parent" with a function overridden in the parent"""

		self.assertRaises(ValueError, Callable, FixtureClassWMethods.varargs_method, parent=FixtureSubclassWOverride)

	def test_unrelated_function(self):
		"""Test "Callable._check_parent" with a function that isn't a member of the parent"""

		self.assertRaises(ValueError, Callable, fixture_function, parent=FixtureClassWMethods)

	def test_other_callable(self):
		"""Test "Callable._check_parent" with a callable that can't belong to a class (a callable instance)"""

		self.assertRaises(ValueError, Callable, FixtureClassWMethods(1), parent=FixtureClassWMethods)
