#python
'''
Testing the _introspection.object_metadata function
'''

from unittest import TestCase

from fixtures import _introspection as fixtures_introspection
from simplifiedapp._introspection import object_metadata

VERSION_REGEXP = r'\d+\.\d+\.\d+(?:\.(dev|post)\d+)?'

class TestObjectMetadata(TestCase):
	'''
	Tests for the object_metadata function
	'''
	
	maxDiff = None
	
	def test_documented_function(self):
		'''
		Testing "object_metadata" with a documented function
		'''
		
		metadata = object_metadata(fixtures_introspection.fixture_documented_function)
		
		expected_value = 'fixture_documented_function'
		self.assertEqual(expected_value, metadata['name'])
		
		self.assertRegex(metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
		expected_value = 'Test fixture callable'
		self.assertEqual(expected_value, metadata['description'])
		
		expected_value = 'A callable test fixture for the object_metadata function.'
		self.assertEqual(expected_value, metadata['long_description'])
		
		expected_value = {
			'args': {'description': 'Any other positional arguments'},
			'kw1': {'description': 'First key word test parameter'},
			'kw2': {'description': 'Second key word test parameter', 'is_optional': True, 'type_name': 'bool'},
			'kwargs': {'description': 'All other keyword arguments'},
			'mult1': {'description': 'First pos/kw test parameter'},
			'mult2': {'description': 'Second pos/kw test parameter with default'},
			'pos1': {'description': 'First positional test parameter', 'is_optional': False, 'type_name': 'float'},
			'pos2': {'description': 'Second positional test parameter'},
		}
		self.assertDictEqual(expected_value, metadata['parameters'])
		
		expected_value = {
			'description': 'nothing useful, really',
			'is_generator': False,
			'type_name': 'None'
		}
		self.assertDictEqual(expected_value, metadata['returns'])
	
	def test_documented_class(self):
		'''
		Testing "object_metadata" with a documented class
		'''
		
		metadata = object_metadata(fixtures_introspection.FixtureDocumentedClass)
		
		expected_value = 'FixtureDocumentedClass'
		self.assertEqual(expected_value, metadata['name'])
		
		self.assertRegex(metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
		expected_value = 'Test fixture class'
		self.assertEqual(expected_value, metadata['description'])
		
		expected_value = 'A class test fixture for the object_metadata function.'
		self.assertEqual(expected_value, metadata['long_description'])
		
		expected_value = {
			'param1': {'description': 'First positional test parameter'},
			'param2': {'description': 'Second positional test parameter'},
		}
		self.assertDictEqual(expected_value, metadata['parameters'])
		
		expected_value = {
			'description': 'an initialized instance',
			'is_generator': False,
			'type_name': 'TestClass'
		}
		self.assertDictEqual(expected_value, metadata['returns'])
	
	def test_documented_module(self):
		'''
		Testing "object_metadata" with a documented module
		'''

		metadata = object_metadata(fixtures_introspection)
	
		expected_value = 'fixtures._introspection'
		self.assertEqual(expected_value, metadata['name'])
	
		self.assertRegex(metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
		expected_value = 'Test fixture module'
		self.assertEqual(expected_value, metadata['description'])
		
		expected_value = 'Simple fixture module for object_metadata.'
		self.assertEqual(expected_value, metadata['long_description'])
		
