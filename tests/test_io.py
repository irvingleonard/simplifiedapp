#python
'''Testing of I/O classes in simplifiedapp
These are the classes that convert from specific formats to python dict and back
'''

import pathlib
import unittest

import simplifiedapp

THIS_FILE = pathlib.Path(__file__).resolve(strict = True)

class TestBase(unittest.TestCase):

	content_fixture = {'something' : 'simple'}
	
	def setUp(self):
		self.values = simplifiedapp.BaseValues(self.content_fixture)
	
	def test_value(self):
		'''
		Test dict to value object casting
		'''
		
		self.assertEqual(self.values.content, self.content_fixture)
		
	def test_value_str(self):
		'''
		Test base value object string representation
		'''
		
		self.assertEqual(str(self.values), str(self.content_fixture))
		
	def test_value_repr(self):
		'''
		Test base value object internal representation
		'''
		
		self.assertEqual(repr(self.values), repr(self.content_fixture))


class TestIO:
	'''
	This is a base test class for all the specific format classes to inherit from.
	'''
	
	def __getattr__(self, name):
		if name == 'fixture_file_path':
			value = THIS_FILE.parent / 'fixtures' / self.fixture_file
			self.__setattr__(name, value)
			return value
		elif name == 'initialized_instance':
			value = self.io_class(str(self.fixture_file_path))
			self.__setattr__(name, value)
			return value
		else:
			raise AttributeError(name)
	
# 	def test_class_str(self):
# 		"""
# 		Test string casting
# 		"""
# 		
# 		self.assertEqual(str(self.initialized_instance), self.fixture_file)
	
	def test_class_repr(self):
		"""
		Test internal representation
		"""
		
		self.assertEqual(repr(self.initialized_instance), str(self.fixture_file_path))
	
	def test_file_load(self):
		"""
		Test the loading of a file
		"""
		
		self.assertEqual(self.initialized_instance.content, self.fixture_content)
		
	def test_wrong_attribute(self):
		'''
		Testing a wrong attribute
		'''
		
		with self.assertRaises(AttributeError):
			none = self.initialized_instance.contento


class TestConf(unittest.TestCase, TestIO):
	'''
	Tests for the class that handles the conf (ini) format
	'''
	
	io_class = simplifiedapp.ConfFile
	fixture_file = 'test.ini'
	fixture_content = {
		'this'			: 'is important',
		'SOME_SECTION'	: {
			'this'		: 'is important',
			'something' : 'else',
			'morrrr'	: 'settings here they go',
			'bored'		: 'of making stuff up',
			'sure'		: 'not',
		},
	}


class TestJSON(unittest.TestCase, TestIO):
	'''
	Tests for the class that handles the JSON format
	'''
	
	io_class = simplifiedapp.JSONFile
	fixture_file = 'test.json'
	fixture_content = {
		"ID": 5,
		"Name": "Edwy",
		"Country": "United Kingdom",
		"House": "House of Wessex",
		"Reign": "955-959"
	}
