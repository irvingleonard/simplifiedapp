#python
"""
Testing the introspection.list_callable_children function
"""

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from fixtures import fixture_empty_module, fixture_module_w_callable, fixture_module_w_class, fixture_module_w_private_callable
from simplifiedapp._introspection import list_callable_children

class TestExecuteCallableCallableChildren(TestCase):
	"""
	Tests for the list_callable_children function
	"""

	def test_lambda_function(self):
		"""
		Testing "list_callable_children" with a lambda function
		"""

		lambda_ = lambda: True
		expected_result = [lambda_.__call__], []
		self.assertEqual(expected_result, list_callable_children(lambda_))

	def test_regular_function(self):
		"""
		Testing "list_callable_children" with a regular function
		"""

		expected_result = [fixture_empty_function.__call__], []
		self.assertEqual(expected_result, list_callable_children(fixture_empty_function))

	def test_nested_function(self):
		"""
		Testing "list_callable_children" with a nested function
		"""

		expected_result = [fixture_nested_functions_outer.__call__], []
		self.assertEqual(expected_result, list_callable_children(fixture_nested_functions_outer))
	
	def test_class(self):
		"""
		Testing "list_callable_children" with a class
		"""

		expected_result = [
			FixtureClassWMethods.__call__,
			FixtureClassWMethods.class_method,
			FixtureClassWMethods.problematic_static_method,
			FixtureClassWMethods.regular_method,
			FixtureClassWMethods.static_method,
		], []
		self.assertEqual(expected_result, list_callable_children(FixtureClassWMethods))
	
	def test_deep_class(self):
		"""
		Testing "list_callable_children" with a deep class
		"""

		expected_result = [], [FixtureDeepClassL1.FixtureDeepClassL2]
		self.assertEqual(expected_result, list_callable_children(FixtureDeepClassL1))
		expected_result = [], [FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3]
		self.assertEqual(expected_result, list_callable_children(FixtureDeepClassL1.FixtureDeepClassL2))
		
	def test_static_method(self):
		"""
		Testing "list_callable_children" with a static method
		"""

		expected_result = [FixtureClassWMethods.static_method.__call__], []
		self.assertEqual(expected_result, list_callable_children(FixtureClassWMethods.static_method))
	
	def test_class_method(self):
		"""
		Testing "list_callable_children" with a class method
		"""

		class_method_ = FixtureClassWMethods.class_method
		expected_result = [class_method_.__call__], []
		self.assertEqual(expected_result, list_callable_children(class_method_))

	def test_bound_method(self):
		"""
		Testing "list_callable_children" with a bound method of an instance
		"""

		bound_method = FixtureClassWMethods(init_arg='pre').regular_method
		expected_result = [bound_method.__call__], []
		self.assertEqual(expected_result, list_callable_children(bound_method))

	def test_instance_method(self):
		"""
		Testing "list_callable_children" with an instance method of a class
		"""

		expected_result = [FixtureClassWMethods.regular_method.__call__], []
		self.assertEqual(expected_result, list_callable_children(FixtureClassWMethods.regular_method))

	def test_bound_method_from_deep_class_instance(self):
		"""
		Testing "list_callable_children" with a bound method of an instance from a deep class
		"""

		bound_method = FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3(init_arg='INIT-PRE').deep_method
		expected_result = [bound_method.__call__], []
		self.assertEqual(expected_result, list_callable_children(bound_method))

	def test_instance_method_from_deep_class(self):
		"""
		Testing "list_callable_children" with an instance method from a deep class
		"""

		expected_result = [FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method.__call__], []
		self.assertEqual(expected_result, list_callable_children(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method))

	def test_empty_module(self):
		"""
		Testing "list_callable_children" with an empty module
		"""

		expected_result = [], []
		self.assertEqual(expected_result, list_callable_children(fixture_empty_module))

	def test_module_w_callable(self):
		"""
		Testing "list_callable_children" with a module containing a callable
		"""

		expected_result = [fixture_module_w_callable.test_callable], []
		self.assertEqual(expected_result, list_callable_children(fixture_module_w_callable))

	def test_module_w_class(self):
		"""
		Testing "list_callable_children" with a module containing a class
		"""

		expected_result = [], [fixture_module_w_class.TestClass]
		self.assertEqual(expected_result, list_callable_children(fixture_module_w_class))

	def test_module_w_private_callable(self):
		"""
		Testing "list_callable_children" with a module containing a private callable
		"""

		expected_result = [fixture_module_w_private_callable._test_callable], []
		self.assertEqual(expected_result, list_callable_children(fixture_module_w_private_callable))
