#python
'''
Testing the introspection.object_metadata function
'''

from unittest import TestCase

from simplifiedapp.introspection import object_metadata

from fixtures import introspection as introspection_fixture

VERSION_REGEXP = r'\d+\.\d+\.\d+(?:\.(dev|post)\d+)?'

class TestObjectMetadataCallable(TestCase):
	'''
	Tests callable for the object_metadata function
	'''
	
	def setUp(self):
		self.metadata = object_metadata(introspection_fixture.test_callable)
	
	def test_name(self):
		'''
		Testing the correct detection of name
		'''
		
		expected_value = 'test_callable'
		self.assertEqual(expected_value, self.metadata['name'])
	
	def test_version(self):
		'''
		Testing the detection of the version number and its format
		'''
		
		self.assertRegex(self.metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
	def test_description(self):
		'''
		Testing the detection of description
		'''
		
		expected_value = 'Test fixture callable'
		self.assertEqual(expected_value, self.metadata['description'])
		
	def test_long_description(self):
		'''
		Testing the detection of long description
		'''
		
		expected_value = 'A callable test fixture for the object_metadata function.'
		self.assertEqual(expected_value, self.metadata['long_description'])
		
	def test_parameters(self):
		'''
		Testing the detection of parameters from docstring
		'''
		
		expected_value = {
			'kw1': {'description': 'First key word test parameter'},
			'kw2': {'description': 'Second key word test parameter'},
			'mult1': {'description': 'First pos/kw test parameter'},
			'mult2': {'description': 'Second pos/kw test parameter with default'},
			'pos1': {'description': 'First positional test parameter', 'is_optional': False, 'type_name': 'float'},
			'pos2': {'description': 'Second positional test parameter', 'is_optional': True, 'type_name': 'bool'},
		}
		self.assertDictEqual(expected_value, self.metadata['parameters'])
		
	def test_returns(self):
		'''
		Testing the detection of return value from docstring
		'''
		
		expected_value = {
			'description': 'nothing useful, really',
			'is_generator': False,
			'type_name': 'None'
		}
		self.assertDictEqual(expected_value, self.metadata['returns'])


class TestObjectMetadataClass(TestCase):
	'''
	Tests callable for the object_metadata function
	'''
	
	def setUp(self):
		self.metadata = object_metadata(introspection_fixture.TestClass)
	
	def test_name(self):
		'''
		Testing the correct detection of name
		'''
		
		expected_value = 'TestClass'
		self.assertEqual(expected_value, self.metadata['name'])
	
	def test_version(self):
		'''
		Testing the detection of the version number and its format
		'''
		
		self.assertRegex(self.metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
	def test_description(self):
		'''
		Testing the detection of description
		'''
		
		expected_value = 'Test fixture class'
		self.assertEqual(expected_value, self.metadata['description'])
		
	def test_long_description(self):
		'''
		Testing the detection of long description
		'''
		
		expected_value = 'A class test fixture for the object_metadata function.'
		self.assertEqual(expected_value, self.metadata['long_description'])
		
	def test_parameters(self):
		'''
		Testing the detection of parameters from docstring
		'''
		
		expected_value = {
			'param1': {'description': 'First positional test parameter'},
			'param2': {'description': 'Second positional test parameter'},
		}
		self.assertDictEqual(expected_value, self.metadata['parameters'])
		
	def test_returns(self):
		'''
		Testing the detection of return value from docstring
		'''
		
		expected_value = {
			'description': 'an initialized instance',
			'is_generator': False,
			'type_name': 'TestClass'
		}
		self.assertDictEqual(expected_value, self.metadata['returns'])


class TestObjectMetadataModule(TestCase):
	'''
	Tests module for the object_metadata function
	'''
	
	def setUp(self):
		self.metadata = object_metadata(introspection_fixture)
	
	def test_name(self):
		'''
		Testing the correct detection of name
		'''
		
		expected_value = 'fixtures.introspection'
		self.assertEqual(expected_value, self.metadata['name'])
	
	def test_version(self):
		'''
		Testing the detection of the version number and its format
		'''
		
		self.assertRegex(self.metadata['version'], '(?i:{})'.format(VERSION_REGEXP))
		
	def test_description(self):
		'''
		Testing the detection of description
		'''
		
		expected_value = 'Test fixture module'
		self.assertEqual(expected_value, self.metadata['description'])
		
	def test_long_description(self):
		'''
		Testing the detection of long description
		'''
		
		expected_value = 'Simple fixture module for object_metadata.'
		self.assertEqual(expected_value, self.metadata['long_description'])
		