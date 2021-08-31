#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp

class TestCallableArgs(unittest.TestCase):
	'''
	Tests for the callable_args function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.callable_args
		self.maxDiff = None


	def test_empty_function(self):
		'''
		Test callable_args with simplest function signature
		'''
		
		def fixture_empty_function():
			pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (fixture_empty_function, (), None, (), None),
			},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_empty_function))

	def test_function_w_args(self):
		'''
		Test callable_args with function containing a variable arguments parameter (*args)
		'''
		
		def fixture_function_w_args(*args):
			pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (fixture_function_w_args, (), 'args', (), None),
			},
			'args': {'action': 'extend', 'default': [], 'nargs': '*'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_args))

	def test_function_w_kwargs(self):
		'''
		Test callable_args with function containing a variable keyword arguments parameter (*kwargs)
		'''
		
		def fixture_function_w_kwargs(**kwargs):
			pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (fixture_function_w_kwargs, (), None, (), 'kwargs'),
			},
			'--kwargs': {'action' : 'extend', 'default' : [], 'nargs' : '+', 'help' : '(Use the key=value format for each entry)'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_kwargs))

	def test_version(self):
		'''
		Test callable_args with versioned function (because "reasons")
		'''
		
		def fixture_versioned_function():
			pass
		fixture_versioned_function.__version__ = '0.1'

		expected_result = {
			None		: {},
			False		: {'__simplifiedapp_': (fixture_versioned_function, (), None, (), None)},
			'--version'	: {'action': 'version', 'version': '0.1'},
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_versioned_function))

	def test_complex_function(self):
		'''
		Test callable_args with the most "complex" function possible
		'''
		
		def fixture_complex_function(simple_positional_parameter, a_str: str, an_int: int, parameter_w_default = "3", parameter_w_options: ['first', 'second', 'third', 'nope'] = 'first', a_bool = True, *args, keyword_parameter = 'some value', __ = 'weird parameter name', supressable_parameter = None, **kwargs):
			pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (fixture_complex_function, ('simple_positional_parameter', 'a_str', 'an_int', 'parameter_w_default', 'parameter_w_options', 'a_bool'), 'args', ('keyword_parameter', '__', 'supressable_parameter'), 'kwargs'),
			},
			'--__': {'default': 'weird parameter name'},
			'--a_bool'						: {'action': 'store_false', 'default' : True},
			'--keyword_parameter'			: {'default': 'some value'},
			'--kwargs'						: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
			'--parameter_w_default'			: {'default' : '3'},
			'--parameter_w_options'			: {'choices': ['first', 'second', 'third', 'nope'], 'default' : 'first'},
			'--supressable_parameter'		: {'default': argparse.SUPPRESS},
			'a_str'							: {'type': str},
			'an_int'						: {'type': int},
			'args'							: {'action': 'extend', 'default' : [], 'nargs' : '*'},
			'simple_positional_parameter'	: {},
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_complex_function))
