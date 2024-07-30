#python
'''
Testing the introspection.param_metadata function
'''

from importlib import import_module
from unittest import TestCase

from simplifiedapp._introspection import IS_CALLABLE, IS_CLASS, IS_MODULE, get_target

from fixtures import _introspection as introspection_fixture

class TestGetTarget(TestCase):
	'''
	Tests for the get_target function
	'''
	
	def setUp(self):
		self.test_object = get_target
	
	def test_callable_target(self):
		'''
		Test "get_target" with a callable provided as target
		'''

		def fixture_empty_callable():
			pass

		expected_result = (fixture_empty_callable, IS_CALLABLE)
		self.assertEqual(expected_result, self.test_object(target=fixture_empty_callable))

	def test_class_target(self):
		'''
		Test "get_target" with a class provided as target
		'''

		class FixtureEmptyClass:
			pass

		expected_result = (FixtureEmptyClass, IS_CLASS)
		self.assertEqual(expected_result, self.test_object(target=FixtureEmptyClass))

	def test_module_target(self):
		'''
		Test "get_target" with a module provided as target
		'''

		expected_result = (introspection_fixture, IS_MODULE)
		self.assertEqual(expected_result, self.test_object(target=introspection_fixture))

	def test_module_autodetection(self):
		'''
		Test "get_target" without a target to trigger module detection
		'''

		import unittest.case
		expected_result = (unittest.case, IS_MODULE)
		self.assertEqual(expected_result, self.test_object())

	def test_module_as_string(self):
		'''
		Test "get_target" with an imported module name as a string
		'''

		import fixtures.fixture_empty_module
		expected_result = (fixtures.fixture_empty_module, IS_MODULE)
		self.assertEqual(expected_result, self.test_object('fixtures.fixture_empty_module'))

	def test_module_callable_as_string(self):
		'''
		Test "get_target" with a callable name as a string (member of calling module)
		'''

		from unittest.case import addModuleCleanup
		expected_result = (addModuleCleanup, IS_CALLABLE)
		self.assertEqual(expected_result, self.test_object('addModuleCleanup'))

	def test_module_importable_as_string(self):
		'''
		Test "get_target" with an importable module name as a string
		'''

		test_result = self.test_object('fixtures.fixture_versioned_module')
		expected_result = (import_module('fixtures.fixture_versioned_module'), IS_MODULE)
		self.assertEqual(expected_result, test_result)

	def test_module_non_importable_as_string(self):
		'''
		Test "get_target" with a non-importable module name as a string
		'''

		self.assertRaises(ValueError, self.test_object, 'fixtures.fixture_invalid_module_dir')
