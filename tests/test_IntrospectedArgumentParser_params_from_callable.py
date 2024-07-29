#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
from unittest import TestCase

from fixtures import test_callable_all_parameter_combinations
from simplifiedapp import IntrospectedArgumentParser, LocalFormatterClass, object_metadata

class TestIntrospectedArgumentParserParamsFromCallable(TestCase):
	'''
	Tests for the IntrospectedArgumentParser.params_from_callable class method
	'''
	
	maxDiff = None
	
	def setUp(self):
		self.test_object = IntrospectedArgumentParser.params_from_callable
	
	def test_empty_function(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with simplest function signature
		'''

		def fixture_empty_function():
			pass

		expected_result = {}
		self.assertEqual(expected_result, self.test_object(fixture_empty_function))

	def test_function_w_positional_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having positional arguments
		'''

		def fixture_function_w_positional_args(a, b, /):
			pass

		expected_result = {
			'fixture-function-w-positional-args-a' : {},
			'fixture-function-w-positional-args-b' : {},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_positional_args, callable_metadata=object_metadata(fixture_function_w_positional_args)))
	
	def test_function_w_mixed_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having mixed arguments
		'''

		def fixture_function_w_mixed_args(a, b, c, d):
			pass

		expected_result = {
			'fixture-function-w-mixed-args-a' : {},
			'fixture-function-w-mixed-args-b' : {},
			'fixture-function-w-mixed-args-c' : {},
			'fixture-function-w-mixed-args-d' : {},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_mixed_args, callable_metadata=object_metadata(fixture_function_w_mixed_args)))
	
	def test_function_w_keyword_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having keyword arguments
		'''

		def fixture_function_w_keyword_args(*, c, d):
			pass

		expected_result = {
			'fixture-function-w-keyword-args-c': {'required': True},
			'fixture-function-w-keyword-args-d': {'required': True},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_keyword_args, callable_metadata=object_metadata(fixture_function_w_keyword_args)))

	def test_function_w_default_positional_args(self):
		'''
		Test ArgparseParser.params_from_callable with function having positional arguments and default values
		'''
		
		def fixture_function_w_default_positional_args(a, b=2, /):
			pass

		expected_result = {
			'fixture-function-w-default-positional-args-a': {},
			'fixture-function-w-default-positional-args-b': {'default': 2, 'type': int},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_default_positional_args, callable_metadata=object_metadata(fixture_function_w_default_positional_args)))

	def test_function_w_default_mixed_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having mixed arguments and default values
		'''

		def fixture_function_w_default_mixed_args(a, b, c=False, d=4):
			pass

		expected_result = {
			'fixture-function-w-default-mixed-args-a': {},
			'fixture-function-w-default-mixed-args-b': {},
			'fixture-function-w-default-mixed-args-c': {'action': 'store_true'},
			'fixture-function-w-default-mixed-args-d': {'default': 4, 'type': int},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_default_mixed_args, callable_metadata=object_metadata(fixture_function_w_default_mixed_args)))

	def test_function_w_default_keyword_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having keyword arguments
		'''

		def fixture_function_w_default_keyword_args(*, c, d=True):
			pass

		expected_result = {
			'fixture-function-w-default-keyword-args-c': {'required': True},
			'fixture-function-w-default-keyword-args-d': {'action': 'store_false'},
		}
		self.assertEqual(expected_result, self.test_object(fixture_function_w_default_keyword_args, callable_metadata=object_metadata(fixture_function_w_default_keyword_args)))

	def test_all_parameter_combinations(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with all possible parameter variations
		'''

		expected_result = {
			'test-callable-all-parameter-combinations-kw-def-bool': {'action': 'store_false'},
			'test-callable-all-parameter-combinations-kw-def-dict': {'action': 'extend', 'default': ['1=dfe', 'yufgb=sdqwda'], 'help': '(Use the key=value format for each entry)', 'nargs': '*'},
			'test-callable-all-parameter-combinations-kw-def-list': {'action': 'extend', 'default': [1, 'tre', 6.7], 'nargs': '*'},
			'test-callable-all-parameter-combinations-kw-def-none': {'default': '==SUPPRESS=='},
			'test-callable-all-parameter-combinations-kw-def-num': {'default': (8+98j), 'type': complex},
			'test-callable-all-parameter-combinations-kw-def-str': {'default': 'another_str'},
			'test-callable-all-parameter-combinations-kw-req': {'required': True},
			'test-callable-all-parameter-combinations-more-kw': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '*'},
			'test-callable-all-parameter-combinations-more-pos': {'action': 'extend', 'default': (), 'nargs': '*'},
			'test-callable-all-parameter-combinations-pos-def-bool': {'action': 'store_true'},
			'test-callable-all-parameter-combinations-pos-def-dict': {'action': 'extend', 'default': ['dct=6', 'fer=False', '1=one'], 'help': '(Use the key=value format for each entry)', 'nargs': '*'},
			'test-callable-all-parameter-combinations-pos-def-list': {'action': 'extend', 'default': ['as', 1, True], 'nargs': '*'},
			'test-callable-all-parameter-combinations-pos-def-none': {'default': '==SUPPRESS=='},
			'test-callable-all-parameter-combinations-pos-def-num': {'default': 2.3, 'type': float},
			'test-callable-all-parameter-combinations-pos-def-str': {'default': 'a_str'},
			'test-callable-all-parameter-combinations-pos-req': {},
		}
		self.assertEqual(expected_result, self.test_object(test_callable_all_parameter_combinations, callable_metadata=object_metadata(test_callable_all_parameter_combinations)))
