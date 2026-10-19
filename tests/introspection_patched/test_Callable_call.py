#! python
"""Testing the introspection_patched.Callable.__call__ method"""

from unittest import TestCase

from fixtures.introspection_patched import FixtureClassWInit, FixtureClassWMethods, FixtureSubclassWMethods, fixture_function
from simplifiedapp.introspection_patched import Callable


class TestCallableCall(TestCase):
	"""Tests for the Callable.__call__ method"""

	def test_function(self):
		"""Test "Callable.__call__" with a function (the arguments are used as is)"""

		expected_result = (1, 2, (3,), 4, {'x': 5})
		self.assertEqual(expected_result, Callable(fixture_function)(1, 2, 3, kw_only=4, x=5))

	def test_builtin_function(self):
		"""Test "Callable.__call__" with a builtin function"""

		self.assertEqual(3, Callable(len)('abc'))

	def test_class(self):
		"""Test "Callable.__call__" with a class (an instance is created)"""

		instance = Callable(FixtureClassWInit)(1, init_kw=2)
		self.assertIsInstance(instance, FixtureClassWInit)
		self.assertEqual((1, 2), (instance.init_pos, instance.init_kw))

	def test_callable_instance(self):
		"""Test "Callable.__call__" with a callable instance"""

		self.assertEqual(('init', 'call'), Callable(FixtureClassWMethods('init'))('call'))

	def test_bound_method(self):
		"""Test "Callable.__call__" with a method bound to an instance"""

		expected_result = ('init', 'pos', (), 'kw', {})
		self.assertEqual(expected_result, Callable(FixtureClassWMethods('init').instance_method)('pos'))

	def test_class_method(self):
		"""Test "Callable.__call__" with a class method"""

		self.assertEqual(('FixtureClassWMethods', 'pos'), Callable(FixtureClassWMethods.class_method)('pos'))

	def test_static_method(self):
		"""Test "Callable.__call__" with a static method"""

		self.assertEqual('pos', Callable(FixtureClassWMethods.static_method)('pos'))

	def test_instance_method(self):
		"""Test "Callable.__call__" with an instance method (the parent class is instantiated first)"""

		expected_result = ('init', 'pos', ('extra',), 'k', {'x': 1})
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.instance_method)(('init',), {}, ('pos', 'extra'), {'kw_arg': 'k', 'x': 1}))

	def test_instance_method_w_keyword_arguments(self):
		"""Test "Callable.__call__" with an instance method, providing the arguments by keyword"""

		expected_result = ('init', 'pos', (), 'kw', {})
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.instance_method)((), {'init_arg': 'init'}, ('pos',), {}))

	def test_instance_method_w_parent(self):
		"""Test "Callable.__call__" with an instance method and an explicit parent (the parent is instantiated, not the class defining the method)"""

		self.assertEqual(('FixtureSubclassWMethods', 'arg'), Callable(FixtureClassWMethods.attached_method, parent=FixtureSubclassWMethods)((1,), {}, ('arg',), {}))

	def test_alias_instance_method(self):
		"""Test "Callable.__call__" with an alias of an instance method (the wrapped function is executed)"""

		expected_result = ('init', 'pos', (), 'kw', {})
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.alias_method)(('init',), {}, ('pos',), {}))

	def test_c_implemented_instance_method(self):
		"""Test "Callable.__call__" with a C implemented instance method"""

		self.assertEqual('ABC', Callable(str.upper)(('abc',), {}, (), {}))

	def test_instance_method_wrong_arguments(self):
		"""Test "Callable.__call__" with an instance method and arguments that don't follow the 4 items convention"""

		callable_ = Callable(FixtureClassWMethods.instance_method)
		self.assertRaises(TypeError, callable_, ('init',), {}, ('pos',))
		self.assertRaises(TypeError, callable_, ('init',), {}, ('pos',), {}, extra=1)
