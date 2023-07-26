#python
'''
Testing of metadata handling in simplifiedapp
'''

import pathlib
import unittest

import simplifiedapp

PARENT_DIR = pathlib.Path( __file__ ).parent

class TestFilesInModuleDir(unittest.TestCase):
	'''
	Tests for the files_in_module_dir function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.files_in_module_dir
		self.module_dir = PARENT_DIR / 'fixtures'
		self.maxDiff = None
	
	def test_error_invalid_module_dir(self):
		'''
		Test error: invalid module dir
		'''

		self.assertRaises(ValueError, self.test_object, self.module_dir / 'fixture_invalid_module_dir', '')

	def test_error_invalid_dir_name(self):
		'''
		Test error: invalid dir name
		'''

		self.assertRaises(Exception, self.test_object, self.module_dir, 'fixture_invalid_module_dir')
	
	def test_regular_file(self):
		'''
		Testing with a regular file
		'''
		
		self.assertEqual(['module_dir_regular_file/test_file'], self.test_object(self.module_dir, 'module_dir_regular_file'))

	def test_subdir(self):
		'''
		Testing with a subdir
		'''
		
		self.assertEqual(['module_dir_subdir/subdir/test_file'], self.test_object(self.module_dir, 'module_dir_subdir'))
	def test_exclusions(self):
		'''
		Testing with an excluded file
		'''
		
		self.assertEqual([], self.test_object(self.module_dir, 'module_dir_exclusions'))
