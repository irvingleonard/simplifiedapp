#python
"""
Testing the introspection.Callable.callable_children method
"""

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import Callable

class TestExecuteCallableCallableChildren(TestCase):
	"""
	Tests for the Callable.callable_children method
	"""

	def test_lambda_function(self):
		"""
		Testing "Callable.callable_children" with a lambda function
		"""

		lambda_ = lambda: True
		expected_result = [lambda_.__call__], []
		self.assertEqual(expected_result, Callable(lambda_).callable_children())

	def test_regular_function(self):
		"""
		Testing "Callable.callable_children" with a regular function
		"""

		expected_result = [fixture_empty_function.__call__], []
		self.assertEqual(expected_result, Callable(fixture_empty_function).callable_children())

	def test_nested_function(self):
		"""
		Testing "Callable.callable_children" with a nested function
		"""

		expected_result = [fixture_nested_functions_outer.__call__], []
		self.assertEqual(expected_result, Callable(fixture_nested_functions_outer).callable_children())
	
	def test_class(self):
		"""
		Testing "Callable.callable_children" with a class
		"""

		expected_result = [
			FixtureClassWMethods.__call__,
			FixtureClassWMethods.class_method,
			FixtureClassWMethods.problematic_static_method,
			FixtureClassWMethods.regular_method,
			FixtureClassWMethods.static_method,
		], []
		self.assertEqual(expected_result, Callable(FixtureClassWMethods).callable_children())
	
	def test_deep_class(self):
		"""
		Test "Callable.callable_children" with a deep class
		"""

		expected_result = [], [FixtureDeepClassL1.FixtureDeepClassL2]
		self.assertEqual(expected_result, Callable(FixtureDeepClassL1).callable_children())
		expected_result = [], [FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3]
		self.assertEqual(expected_result, Callable(FixtureDeepClassL1.FixtureDeepClassL2).callable_children())
		
	def test_static_method(self):
		"""
		Test "Callable.callable_children" with a static method
		"""

		expected_result = [FixtureClassWMethods.static_method.__call__], []
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.static_method).callable_children())
	
	def test_class_method(self):
		"""
		Test "Callable.callable_children" with a class method
		"""

		class_method_ = FixtureClassWMethods.class_method
		expected_result = [class_method_.__call__], []
		self.assertEqual(expected_result, Callable(class_method_).callable_children())

	def test_bound_method(self):
		"""
		Test "Callable.callable_children" with a bound method of an instance
		"""

		bound_method = FixtureClassWMethods(init_arg='pre').regular_method
		expected_result = [bound_method.__call__], []
		self.assertEqual(expected_result, Callable(bound_method).callable_children())

	def test_instance_method(self):
		"""
		Test "Callable.callable_children" with an instance method of a class
		"""

		expected_result = [FixtureClassWMethods.regular_method.__call__], []
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.regular_method).callable_children())

	def test_bound_method_from_deep_class_instance(self):
		"""
		Test "Callable.callable_children" with a bound method of an instance from a deep class
		"""

		bound_method = FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3(init_arg='INIT-PRE').deep_method
		expected_result = [bound_method.__call__], []
		self.assertEqual(expected_result, Callable(bound_method).callable_children())

	def test_instance_method_from_deep_class(self):
		"""
		Test "Callable.callable_children" with an instance method from a deep class
		"""

		expected_result = [FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method.__call__], []
		self.assertEqual(expected_result, Callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method).callable_children())
