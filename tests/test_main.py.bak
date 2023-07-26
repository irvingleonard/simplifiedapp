#python
'''
Testing of argparse handling in simplifiedapp
'''

import io
import pathlib
import sys
import unittest
import unittest.mock

import simplifiedapp


def empty_callable():
	return 'Ok from test_main.'


class TestMain(unittest.TestCase):
	'''
	Tests for the main function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.main
		self.maxDiff = None
		sys.path.append(str(pathlib.Path( __file__ ).parent / 'fixtures'))

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_simple_function(self, mock_stdout):
		'''
		Test callable_args with simplest function signature
		'''
		
		def fixture_empty_function():
			pass

		self.test_object(fixture_empty_function, [])
		self.assertEqual('None\n', mock_stdout.getvalue())
	
	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_simple_class(self, mock_stdout):
		'''
		Test callable_args with a simple class
		'''
		
		class FixtureSimpleClass:
			def __init__(self, *args, **kwargs):
				pass
			def __repr__(self):
				return 'FixtureSimpleClass'
		
		self.test_object(FixtureSimpleClass, [])
		self.assertEqual('FixtureSimpleClass\n', mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_class_method(self, mock_stdout):
		'''
		Test a class with a simple method
		'''
		
		class FixtureClassWMethod:
			def test_method(self):
				return 'Ok from test_method.'
		
		self.test_object(FixtureClassWMethod, ['test_method'])
		self.assertEqual('Ok from test_method.', mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_error_empty_module(self, mock_stdout):
		'''
		Test error: empty module (no executable)
		'''
		
		import fixture_empty_module

		self.assertRaises(RuntimeError, self.test_object, fixture_empty_module, [])

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_target_none(self, mock_stdout):
		'''
		Test with a simple method as str
		'''
		
		self.test_object(None, ['empty_callable'])
		self.assertEqual('Ok from test_main.', mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_target_math(self, mock_stdout):
		'''
		Test with the builtin sys module
		'''
		
		self.test_object('sys', ['get_coroutine_origin_tracking_depth'])
		self.assertEqual('{}\n'.format(sys.get_coroutine_origin_tracking_depth()), mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_target_parent_str(self, mock_stdout):
		'''
		Test with a module's member as a str
		'''
		
		self.test_object('empty_callable', [])
		self.assertEqual('Ok from test_main.', mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_target_3rd_party_module(self, mock_stdout):
		'''
		Test with a 3rd party module (setuptools)
		'''
		
		self.test_object('setuptools', ['findall', '--dir', str(pathlib.Path( __file__ ).parent / 'fixtures' / 'module_dir_regular_file')])
		self.assertEqual(str([str(pathlib.Path( __file__ ).parent / 'fixtures' / 'module_dir_regular_file' / 'test_file')]) + '\n', mock_stdout.getvalue())

	def test_run_target_missing_3rd_party_module(self):
		'''
		Test with a missing (hopefully) 3rd party module
		'''
		
		self.assertRaises(ValueError, self.test_object, 'setuptool_please_dont_exist', [])

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_run_input_file(self, mock_stdout):
		'''
		Test with simple function and input_file
		'''
		
		def fixture_empty_function():
			return 'Ok from the input_file test.'

		self.test_object(fixture_empty_function, ['--input-file', str(pathlib.Path( __file__ ).parent / 'fixtures' / 'fixture_empty_config_file.ini'), 'ini'])
		self.assertEqual('Ok from the input_file test.', mock_stdout.getvalue())

	@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
	def test_syslog_logging(self, mock_stdout):
		'''
		Test logging to syslog
		'''
		
		def fixture_empty_function():
			pass

		result = self.test_object(fixture_empty_function, ['--log-to-syslog'])
		self.assertEqual('None\n', mock_stdout.getvalue())
		