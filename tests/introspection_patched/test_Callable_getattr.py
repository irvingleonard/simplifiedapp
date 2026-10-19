#! python
"""Testing the introspection_patched.Callable.__getattr__ method (the lazily resolved attributes)"""

from copy import copy, deepcopy
from pickle import dumps, loads
from unittest import TestCase

from fixtures import introspection_patched as fixtures_module
from fixtures.introspection_patched import FixtureClassWMethods, FixtureOuterClass, FixtureSubclassWMethods, fixture_documented_function, fixture_function, fixture_local_class_factory, fixture_nested_function_factory
from simplifiedapp.introspection_patched import Callable, CallableType


class TestCallableGetattr(TestCase):
	"""Tests for the Callable.__getattr__ method"""

	def test_is_method(self):
		"""Test the "is_method" attribute"""

		self.assertTrue(Callable(FixtureClassWMethods(1).instance_method).is_method)
		self.assertFalse(Callable(fixture_function).is_method)

	def test_metadata(self):
		"""Test the "metadata" attribute"""

		self.assertEqual('fixture_function', Callable(fixture_function).metadata['name'])

	def test_module(self):
		"""Test the "module" attribute"""

		self.assertIs(fixtures_module, Callable(fixture_function).module)

	def test_parents_function(self):
		"""Test the "parents" attribute with a module level function"""

		self.assertEqual([], Callable(fixture_function).parents)

	def test_parents_nested_function(self):
		"""Test the "parents" attribute with a function defined inside another function"""

		self.assertEqual([], Callable(fixture_nested_function_factory()).parents)

	def test_parents_method(self):
		"""Test the "parents" attribute with a method of a module level class"""

		self.assertEqual([FixtureClassWMethods], Callable(FixtureClassWMethods.instance_method).parents)

	def test_parents_deep_method(self):
		"""Test the "parents" attribute with a method of a nested class (closest parent first)"""

		expected_result = [FixtureOuterClass.FixtureMiddleClass.FixtureInnerClass, FixtureOuterClass.FixtureMiddleClass, FixtureOuterClass]
		self.assertEqual(expected_result, Callable(FixtureOuterClass.FixtureMiddleClass.FixtureInnerClass.inner_method).parents)

	def test_parents_local_class_w_super(self):
		"""Test the "parents" attribute with a method of a class defined inside a function, using "super()" (found through the "__class__" closure cell)"""

		local_class = fixture_local_class_factory()
		self.assertEqual([local_class], Callable(local_class.method_w_super).parents)

	def test_parents_local_class_wo_super(self):
		"""Test the "parents" attribute with a method of a class defined inside a function, not using "super()" (the class can't be found)"""

		self.assertRaises(ValueError, getattr, Callable(fixture_local_class_factory().method_wo_super), 'parents')

	def test_parents_wo_qualname(self):
		"""Test the "parents" attribute with a callable that has no "__qualname__" (a callable instance)"""

		self.assertEqual([], Callable(FixtureClassWMethods(1)).parents)

	def test_parent_bound_method(self):
		"""Test the "parent" attribute with a bound method (the instance it's bound to)"""

		instance = FixtureClassWMethods(1)
		self.assertIs(instance, Callable(instance.instance_method).parent)

	def test_parent_method_descriptor(self):
		"""Test the "parent" attribute with a C implemented method (the class it belongs to)"""

		self.assertIs(str, Callable(str.upper).parent)

	def test_parent_method(self):
		"""Test the "parent" attribute with a function retrieved from a class (the class that defines it)"""

		self.assertIs(FixtureClassWMethods, Callable(FixtureClassWMethods.instance_method).parent)

	def test_parent_function(self):
		"""Test the "parent" attribute with functions (builtin functions are bound to their module, which isn't a parent)"""

		self.assertIsNone(Callable(fixture_function).parent)
		self.assertIsNone(Callable(len).parent)

	def test_parent_metadata(self):
		"""Test the "parent_metadata" attribute and the attributes forwarded to it"""

		callable_ = Callable(FixtureClassWMethods.instance_method)
		self.assertEqual('FixtureClassWMethods', callable_.parent_metadata['name'])
		self.assertEqual('FixtureClassWMethods', callable_.parent_name)
		self.assertEqual('4.5.6', callable_.parent_version)

	def test_parent_metadata_wo_parent(self):
		"""Test the "parent_metadata" attribute and the attributes forwarded to it, for a callable without a parent"""

		callable_ = Callable(fixture_function)
		self.assertRaises(AttributeError, getattr, callable_, 'parent_metadata')
		self.assertRaises(AttributeError, getattr, callable_, 'parent_name')
		self.assertFalse(hasattr(callable_, 'parent_name'))

	def test_missing_parent_metadata(self):
		"""Test an attribute forwarded to the parent metadata that the parent doesn't have"""

		callable_ = Callable(FixtureClassWMethods.instance_method)
		self.assertRaises(AttributeError, getattr, callable_, 'parent_long_description')
		self.assertFalse(hasattr(callable_, 'parent_long_description'))

	def test_forwarded_metadata(self):
		"""Test the attributes forwarded to the metadata"""

		callable_ = Callable(fixture_documented_function)
		self.assertEqual('fixture_documented_function', callable_.name)
		self.assertEqual('0.1.3.dev1', callable_.version)
		self.assertEqual('Documented function', callable_.description)

	def test_missing_forwarded_metadata(self):
		"""Test an attribute forwarded to the metadata that the callable doesn't have"""

		callable_ = Callable(fixture_function)
		self.assertRaises(AttributeError, getattr, callable_, 'version')
		self.assertFalse(hasattr(callable_, 'version'))

	def test_forwarded_to_callable(self):
		"""Test any other attribute, forwarded to the callable"""

		self.assertEqual('fixture value', Callable(fixture_function).fixture_attribute)

	def test_special_attribute_not_forwarded(self):
		"""Test that special ("__dunder__") attributes aren't forwarded to the callable"""

		self.assertRaises(AttributeError, getattr, Callable(fixture_function), '__qualname__')
		self.assertFalse(hasattr(Callable(FixtureClassWMethods(1)), '__setstate__'))

	def test_callable_not_set(self):
		"""Test an instance created without "__init__" (like copy and pickle do), which doesn't have the callable yet"""

		self.assertRaises(AttributeError, getattr, Callable.__new__(Callable), 'is_method')

	def test_copy(self):
		"""Test copying the instance, shallow and deep"""

		for copier in (copy, deepcopy):
			with self.subTest(copier=copier.__name__):
				original = Callable(fixture_function)
				duplicate = copier(original)
				self.assertIsNot(original, duplicate)
				self.assertIs(fixture_function, duplicate._callable_)
				self.assertEqual((1, 2, (), 3, {}), duplicate(1, 2, kw_only=3))

	def test_copy_resolved(self):
		"""Test copying an instance after its attributes were resolved (the module isn't copyable, it gets resolved again)"""

		original = Callable(FixtureClassWMethods.instance_method, parent=FixtureSubclassWMethods)
		self.assertIs(CallableType['INSTANCE_METHOD'], original.type)
		duplicate = deepcopy(original)
		self.assertNotIn('type', vars(duplicate))
		self.assertIs(FixtureSubclassWMethods, duplicate.parent)
		self.assertEqual(('init', 'pos', (), 'kw', {}), duplicate(('init',), {}, ('pos',), {}))

	def test_pickle(self):
		"""Test pickling and unpickling an instance, after its attributes were resolved"""

		original = Callable(fixture_function)
		self.assertIs(fixtures_module, original.module)
		duplicate = loads(dumps(original))
		self.assertIs(fixture_function, duplicate._callable_)
		self.assertIs(CallableType['FUNCTION'], duplicate.type)

	def test_signature_and_type(self):
		"""Test the "signature" and "type" attributes (both are stored when either one is requested)"""

		callable_ = Callable(fixture_function)
		self.assertIs(CallableType['FUNCTION'], callable_.type)
		self.assertIn('signature', vars(callable_))
		self.assertEqual('(pos_only, /, pos_or_kw, *args, kw_only, **kwargs)', str(callable_.signature))

		callable_ = Callable(fixture_function)
		self.assertEqual('(pos_only, /, pos_or_kw, *args, kw_only, **kwargs)', str(callable_.signature))
		self.assertIn('type', vars(callable_))

	def test_stored(self):
		"""Test that resolved attributes are stored in the instance, so they're only resolved once"""

		callable_ = Callable(fixture_function)
		self.assertNotIn('module', vars(callable_))
		module = callable_.module
		self.assertIs(module, vars(callable_)['module'])
