#python
'''
Testing of metadata handling in simplifiedapp
'''

import unittest

import simplifiedapp

class TestDetection(unittest.TestCase):
	'''
	Tests for the setuptools_get_metadata function
	'''
	
	def setUp(self):
		self.metadata = simplifiedapp.setuptools_get_metadata(simplifiedapp)
	
	def test_name(self):
		'''
		Testing the correct detection of name
		'''
		
		self.assertEqual(self.metadata['name'], 'simplifiedapp')
	
	def test_version(self):
		'''
		Testing the detection of the version number and its format
		'''
		
		result_pattern  = '\d+\.\d+\.\d+(?:-\w{3,4}\d+)?'
		self.assertRegex(self.metadata['version'], '(?i:{})'.format(result_pattern))
		
	def test_description(self):
		'''
		Testing the detection of description
		'''
		
		self.assertIn('description', self.metadata)
		
	def test_long_description(self):
		'''
		Testing the detection of long description
		'''
		
		self.assertIn('long_description', self.metadata)

