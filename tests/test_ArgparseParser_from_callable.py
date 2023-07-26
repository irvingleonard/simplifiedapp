#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp

ARGUMENT_CLASS = simplifiedapp.ArgparseArgument
PARSER_CLASS = simplifiedapp.ArgparseParser

class TestArgparseParserFromCallable(unittest.TestCase):
	'''
	Tests for the ArgparseParser.from_callable class method
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.ArgparseParser.from_callable
		self.maxDiff = None

	def test_empty_function(self):
		'''
		Test ArgparseParser.from_callable with simplest function signature
		'''

		def fixture_empty_function():
			pass

		expected_result = PARSER_CLASS(defaults = {'__simplifiedapp_' : (fixture_empty_function, (), None, (), None)})
		self.assertEqual(self.test_object(fixture_empty_function), expected_result)

	def test_function_w_positional_args(self):
		'''
		Test ArgparseParser.from_callable with function having positional arguments
		'''
		
		def fixture_function_w_positional_args(a, b):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('a'),
				ARGUMENT_CLASS('b'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_positional_args, ('a', 'b'), None, (), None)})
		self.assertEqual(self.test_object(fixture_function_w_positional_args), expected_result)

	def test_function_w_default_positional_args(self):
		'''
		Test ArgparseParser.from_callable with function having positional arguments and default values
		'''
		
		def fixture_function_w_default_positional_args(a = 'a', bc = 'bc'):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('a', default = 'a'),
				ARGUMENT_CLASS('bc', default = 'bc'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_default_positional_args, ('a', 'bc'), None, (), None)})
		self.assertEqual(self.test_object(fixture_function_w_default_positional_args), expected_result)

	def test_function_w_mixed_positional_args(self):
		'''
		Test ArgparseParser.from_callable with function having positional arguments and default values
		'''
		
		def fixture_function_w_mixed_positional_args(a, b, cd = 'cd', ef = 'ef'):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('a'),
				ARGUMENT_CLASS('b'),
				ARGUMENT_CLASS('cd', default = 'cd'),
				ARGUMENT_CLASS('ef', default = 'ef'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_mixed_positional_args, ('a', 'b', 'cd', 'ef'), None, (), None)})
		self.assertEqual(self.test_object(fixture_function_w_mixed_positional_args), expected_result)

	def test_function_w_args(self):
		'''
		Test ArgparseParser.from_callable with function containing a variable arguments parameter (*args)
		'''
		
		def fixture_function_w_args(*args):
			pass

		expected_result = PARSER_CLASS(ARGUMENT_CLASS('args', action = 'extend', default = [], nargs = '*'), defaults = {'__simplifiedapp_' : (fixture_function_w_args, (), 'args', (), None)})
		self.assertEqual(self.test_object(fixture_function_w_args), expected_result)

	def test_function_w_keyword_args(self):
		'''
		Test ArgparseParser.from_callable with function having keyword arguments
		'''
		
		def fixture_function_w_keyword_args(*args, a = 'a', b = 1, cd = ('c', 'd')):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('args', action = 'extend', default = [], nargs = '*'),
				ARGUMENT_CLASS('a', default = 'a'),
				ARGUMENT_CLASS('b', default = 1, type = int),
				ARGUMENT_CLASS('cd', action = 'extend', default = ['c', 'd'], nargs = '+'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_keyword_args, (), 'args', ('a', 'b', 'cd'), None)})

		self.assertEqual(self.test_object(fixture_function_w_keyword_args), expected_result)

	def test_function_w_kwargs(self):
		'''
		Test ArgparseParser.from_callable with function containing a variable keyword arguments parameter (*kwargs)
		'''
		
		def fixture_function_w_kwargs(**kwargs):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('kwargs', action = 'extend', default = [], nargs = '+', help = '(Use the key=value format for each entry)'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_kwargs, (), None, (), 'kwargs')})

		self.assertEqual(self.test_object(fixture_function_w_kwargs), expected_result)

	def test_function_w_annotations(self):
		'''
		Test ArgparseParser.from_callable with function having annotated arguments
		'''
		
		def fixture_function_w_annotations(a_str : str, an_int : int, a_float : float, some_choices : ['a', 'b', 'c']):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('a_str', type = str),
				ARGUMENT_CLASS('an_int', type = int),
				ARGUMENT_CLASS('a_float', type = float),
				ARGUMENT_CLASS('some_choices', choices = ['a', 'b', 'c']),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_annotations, ('a_str', 'an_int', 'a_float', 'some_choices'), None, (), None)})

		self.assertEqual(self.test_object(fixture_function_w_annotations), expected_result)

	def test_version(self):
		'''
		Test ArgparseParser.from_callable with versioned function (because "reasons")
		'''
		
		def fixture_versioned_function():
			pass
		fixture_versioned_function.__version__ = '0.1'

		expected_arguments = (
				ARGUMENT_CLASS('version', action = 'version', version = '0.1'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_versioned_function, (), None, (), None)})
		self.assertEqual(self.test_object(fixture_versioned_function), expected_result)

	def test_complex_function(self):
		'''
		Test ArgparseParser.from_callable with the most "complex" function possible
		'''
		
		def fixture_complex_function(simple_positional_parameter, a_str: str, an_int: int, parameter_w_default = "3", parameter_w_options: ['first', 'second', 'third', 'nope'] = 'first', a_bool = True, *args, keyword_parameter = 'some value', __ = 'weird parameter name', supressable_parameter = None, **kwargs):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('simple_positional_parameter'),
				ARGUMENT_CLASS('a_str', type = str),
				ARGUMENT_CLASS('an_int', type = int),
				ARGUMENT_CLASS('parameter_w_default', default = '3'),
				ARGUMENT_CLASS('parameter_w_options', choices = ['first', 'second', 'third', 'nope'], default = 'first'),
				ARGUMENT_CLASS('a_bool', action = 'store_false', default = True),
				ARGUMENT_CLASS('args', action = 'extend', default = [], nargs = '*'),
				ARGUMENT_CLASS('keyword_parameter', default = 'some value'),
				ARGUMENT_CLASS('__', default = 'weird parameter name'),
				ARGUMENT_CLASS('supressable_parameter', default = argparse.SUPPRESS),
				ARGUMENT_CLASS('kwargs', action = 'extend', default = [], nargs = '+', help = '(Use the key=value format for each entry)'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_complex_function, ('simple_positional_parameter', 'a_str', 'an_int', 'parameter_w_default', 'parameter_w_options', 'a_bool'), 'args', ('keyword_parameter', '__', 'supressable_parameter'), 'kwargs')})

		self.assertEqual(self.test_object(fixture_complex_function), expected_result)
