#! python
"""Testing the introspection_patched.object_metadata function"""

from types import ModuleType
from unittest import TestCase
from unittest.mock import patch

from fixtures import introspection_patched as fixtures_module
from fixtures.introspection_patched import FixtureClassWMethods, fixture_documented_function, fixture_short_documented_function
from simplifiedapp.introspection_patched import object_metadata


class TestObjectMetadata(TestCase):
	"""Tests for the object_metadata function"""

	maxDiff = None

	def test_documented_function(self):
		"""Test "object_metadata" with a function documented with every supported section"""

		expected_parameters = {
			'pos1': {'description': 'First positional parameter', 'is_optional': False, 'type_name': 'float'},
			'pos2': {'description': 'Second positional parameter'},
			'mult1': {'description': 'Positional or keyword parameter'},
			'args': {'description': 'Any other positional arguments'},
			'kw1': {'description': 'First keyword parameter'},
			'kw2': {'description': 'Second keyword parameter', 'is_optional': True, 'type_name': 'bool'},
			'kwargs': {'description': 'All other keyword arguments'},
		}
		expected_result = {
			'name': 'fixture_documented_function',
			'version': '0.1.3.dev1',
			'description': 'Documented function',
			'long_description': 'A function documented with every section supported by "object_metadata".',
			'parameters': expected_parameters,
			'returns': {'description': 'nothing useful, really', 'is_generator': False, 'type_name': 'None'},
		}
		self.assertDictEqual(expected_result, object_metadata(fixture_documented_function))

	def test_short_documented_function(self):
		"""Test "object_metadata" with a function documented with a short description only"""

		expected_result = {'name': 'fixture_short_documented_function', 'description': 'Short documented function'}
		self.assertDictEqual(expected_result, object_metadata(fixture_short_documented_function))

	def test_documented_class(self):
		"""Test "object_metadata" with a documented class"""

		expected_result = {
			'name': 'FixtureClassWMethods',
			'version': '4.5.6',
			'description': 'Class with every kind of method',
			'parameters': {'init_arg': {'description': 'The argument to initialize the instance'}},
		}
		self.assertDictEqual(expected_result, object_metadata(FixtureClassWMethods))

	def test_documented_module(self):
		"""Test "object_metadata" with a documented module"""

		expected_result = {
			'name': 'fixtures.introspection_patched',
			'version': '1.2.3',
			'description': 'Fixtures for the introspection_patched tests',
			'long_description': 'Functions and classes covering the different kinds of callables and signatures handled by the "simplifiedapp.introspection_patched" module.',
		}
		self.assertDictEqual(expected_result, object_metadata(fixtures_module))

	def test_main_module_w_file(self):
		"""Test "object_metadata" with a "__main__" module that has a file (the name of the file is used)"""

		main_module = ModuleType('__main__')
		main_module.__file__ = '/path/to/some_script.py'
		expected_result = {'name': 'some_script.py'}
		self.assertDictEqual(expected_result, object_metadata(main_module))

	def test_main_module_wo_file(self):
		"""Test "object_metadata" with a "__main__" module that has no file (like an interactive session)"""

		main_module = ModuleType('__main__')
		expected_result = {'name': '__main__'}
		self.assertDictEqual(expected_result, object_metadata(main_module))

	def test_undocumented_lambda(self):
		"""Test "object_metadata" with a lambda (no docstring)"""

		expected_result = {'name': '<lambda>'}
		self.assertDictEqual(expected_result, object_metadata(lambda x: x))

	def test_empty_docstring(self):
		"""Test "object_metadata" with an empty docstring"""

		def fixture_empty_docstring():
			""""""

			pass

		expected_result = {'name': 'fixture_empty_docstring'}
		self.assertDictEqual(expected_result, object_metadata(fixture_empty_docstring))

	def test_parameters_only_docstring(self):
		"""Test "object_metadata" with a docstring documenting the parameters only (no description)"""

		def fixture_parameters_only_docstring(a):
			""":param a: Only the parameter is documented"""

			pass

		expected_result = {'name': 'fixture_parameters_only_docstring', 'parameters': {'a': {'description': 'Only the parameter is documented'}}}
		self.assertDictEqual(expected_result, object_metadata(fixture_parameters_only_docstring))

	def test_custom_attributes(self):
		"""Test "object_metadata" with custom parameter and return attributes"""

		metadata = object_metadata(fixture_documented_function, param_attributes=('type_name',), return_attributes=('type_name',))
		expected_parameters = {'pos1': {'type_name': 'float'}, 'pos2': {}, 'mult1': {}, 'args': {}, 'kw1': {}, 'kw2': {'type_name': 'bool'}, 'kwargs': {}}
		self.assertDictEqual(expected_parameters, metadata['parameters'])
		self.assertDictEqual({'type_name': 'None'}, metadata['returns'])

	def test_wo_docstring_parser(self):
		"""Test "object_metadata" without the optional "docstring_parser" module (only the name and version are available)"""

		expected_result = {'name': 'fixture_documented_function', 'version': '0.1.3.dev1'}
		with patch('simplifiedapp.introspection_patched.docstring_parse', None):
			self.assertDictEqual(expected_result, object_metadata(fixture_documented_function))
