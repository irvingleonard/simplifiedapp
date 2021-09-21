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

	def test_function_w_positional_args(self):
		'''
		Test callable_args with function having positional arguments
		'''
		
		def fixture_function_w_positional_args(a, b):
			pass

		expected_result = {
			None	: {},
			False	: {
				'__simplifiedapp_': (fixture_function_w_positional_args, ('a', 'b'), None, (), None),
			},
			'a'		: {},
			'b'		: {},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_positional_args))

	def test_function_w_default_positional_args(self):
		'''
		Test callable_args with function having positional arguments and default values
		'''
		
		def fixture_function_w_default_positional_args(a = 'a', bc = 'bc'):
			pass

		expected_result = {
			None	: {},
			False	: {
				'__simplifiedapp_': (fixture_function_w_default_positional_args, ('a', 'bc'), None, (), None),
			},
			'-a'		: {'default': 'a'},
			'--bc'		: {'default': 'bc'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_default_positional_args))

	def test_function_w_mixed_positional_args(self):
		'''
		Test callable_args with function having positional arguments and default values
		'''
		
		def fixture_function_w_mixed_positional_args(a, b, cd = 'cd', ef = 'ef'):
			pass

		expected_result = {
			None	: {},
			False	: {
				'__simplifiedapp_': (fixture_function_w_mixed_positional_args, ('a', 'b', 'cd', 'ef'), None, (), None),
			},
			'a'		: {},
			'b'		: {},
			'--cd'	: {'default': 'cd'},
			'--ef'	: {'default': 'ef'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_mixed_positional_args))

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
			'args': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '*'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_args))

	def test_function_w_keyword_args(self):
		'''
		Test callable_args with function having keyword arguments
		'''
		
		def fixture_function_w_keyword_args(*args, a = 'a', b = 1, cd = ('c', 'd')):
			pass

		expected_result = {
			'args'	: {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '*'},
			'-a'	: {'default': 'a'},
			'-b'	: {'default': 1, 'type': int},
			'--cd'	: {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '+'},
			None	: {},
			False	: {
				'__simplifiedapp_': (fixture_function_w_keyword_args, (), 'args', ('a', 'b', 'cd'), None),
			},
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_keyword_args))

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
			'--kwargs': {'action' : 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default' : [], 'nargs' : '+', 'help' : '(Use the key=value format for each entry)'},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_kwargs))

	def test_function_w_annotations(self):
		'''
		Test callable_args with function having annotated arguments
		'''
		
		def fixture_function_w_annotations(a_str : str, an_int : int, a_float : float, some_choices : ['a', 'b', 'c']):
			pass

		expected_result = {
			'a_str'			: {'type': str},
			'an_int'		: {'type': int},
			'a_float'		: {'type': float},
			'some_choices'	: {'choices': ['a', 'b', 'c']},
			None			: {},
			False			: {
				'__simplifiedapp_': (fixture_function_w_annotations, ('a_str', 'an_int', 'a_float', 'some_choices'), None, (), None),
			},

		}
		self.assertDictEqual(expected_result, self.test_object(fixture_function_w_annotations))

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
			'--kwargs'						: {'action' : 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
			'--parameter_w_default'			: {'default' : '3'},
			'--parameter_w_options'			: {'choices': ['first', 'second', 'third', 'nope'], 'default' : 'first'},
			'--supressable_parameter'		: {'default': argparse.SUPPRESS},
			'a_str'							: {'type': str},
			'an_int'						: {'type': int},
			'args'							: {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default' : [], 'nargs' : '*'},
			'simple_positional_parameter'	: {},
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_complex_function))
