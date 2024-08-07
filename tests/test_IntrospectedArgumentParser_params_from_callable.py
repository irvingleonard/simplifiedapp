#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
from unittest import TestCase

from fixtures.functions import *
from simplifiedapp import IntrospectedArgumentParser, VarKWParameter

params_from_callable = IntrospectedArgumentParser.params_from_callable
class TestIntrospectedArgumentParserParamsFromCallable(TestCase):
	'''
	Tests for the IntrospectedArgumentParser.params_from_callable class method
	'''
	
	maxDiff = None

	def test_empty_function(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with simplest function signature
		'''

		expected_result = {}
		self.assertEqual(expected_result, params_from_callable(fixture_empty_function))

	def test_function_w_positional_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having positional arguments
		'''

		expected_result = {
			'fixture-function-w-positional-args-a' : {},
			'fixture-function-w-positional-args-b' : {},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_positional_args))
	
	def test_function_w_mixed_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having mixed arguments
		'''

		expected_result = {
			'fixture-function-w-mixed-args-a' : {},
			'fixture-function-w-mixed-args-b' : {},
			'fixture-function-w-mixed-args-c' : {},
			'fixture-function-w-mixed-args-d' : {},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_mixed_args))
	
	def test_function_w_varargs(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having variable positional arguments
		'''

		expected_result = {
			'fixture-function-w-varargs-args': {'action': 'extend', 'default': [], 'nargs': '*'},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_varargs))

	def test_function_w_keyword_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having keyword arguments
		'''

		def fixture_function_w_keyword_args(*, c, d):
			pass

		expected_result = {
			'--fixture-function-w-keyword-args-c': {'required': True},
			'--fixture-function-w-keyword-args-d': {'required': True},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_keyword_args))
		
	def test_function_w_varkw(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having variable keyword arguments
		'''

		expected_result = {
			'--fixture-function-w-varkw-kwargs': {'action': 'extend', 'default': [], 'nargs': '*',  'type': VarKWParameter, 'help': '(Use the key=value format for each entry)'},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_varkw))

	def test_function_w_default_positional_args(self):
		'''
		Test ArgparseParser.params_from_callable with function having positional arguments and default values
		'''

		expected_result = {
			'fixture-function-w-default-positional-args-a': {},
			'fixture-function-w-default-positional-args-b': {'default': 2, 'nargs': '?', 'type': int},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_default_positional_args))

	def test_function_w_default_mixed_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having mixed arguments and default values
		'''

		expected_result = {
			'fixture-function-w-default-mixed-args-a': {},
			'fixture-function-w-default-mixed-args-b': {},
			'fixture-function-w-default-mixed-args-c': {'action': 'store_true', 'nargs': '?'},
			'fixture-function-w-default-mixed-args-d': {'default': 4, 'nargs': '?', 'type': int},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_default_mixed_args))

	def test_function_w_default_keyword_args(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having keyword arguments
		'''

		expected_result = {
			'--fixture-function-w-default-keyword-args-c': {'required': True},
			'--fixture-function-w-default-keyword-args-d': {'action': 'store_false'},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_default_keyword_args))

	def test_function_w_version(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having keyword arguments
		'''

		expected_result = {'--fixture-function-w-version-version': {'action': 'version', 'version': '0.1'}}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_version))


	def test_function_w_all_parameter_combinations(self):
		'''
		Test IntrospectedArgumentParser.params_from_callable with function having all possible parameter combinations
		'''

		expected_result = {
			'--fixture-function-w-all-parameter-combinations-kw-def-bool': {'action': 'store_false'},
			'--fixture-function-w-all-parameter-combinations-kw-def-dict': {'action': 'extend', 'default': ['1=dfe', 'yufgb=sdqwda'], 'nargs': '*'},
			'--fixture-function-w-all-parameter-combinations-kw-def-list': {'action': 'extend', 'default': [1, 'tre', 6.7], 'nargs': '*'},
			'--fixture-function-w-all-parameter-combinations-kw-def-none': {'default': '==SUPPRESS=='},
			'--fixture-function-w-all-parameter-combinations-kw-def-num': {'default': (8+98j), 'type': complex},
			'--fixture-function-w-all-parameter-combinations-kw-def-str': {'default': 'another_str'},
			'--fixture-function-w-all-parameter-combinations-kw-req': {'required': True},
			'--fixture-function-w-all-parameter-combinations-more-kw': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '*', 'type': VarKWParameter},
			'fixture-function-w-all-parameter-combinations-more-pos': {'action': 'extend', 'default': [], 'nargs': '*'},
			'fixture-function-w-all-parameter-combinations-pos-def-bool': {'action': 'store_true', 'nargs': '?'},
			'fixture-function-w-all-parameter-combinations-pos-def-dict': {'action': 'extend', 'default': ['dct=6', 'fer=False', '1=one'], 'nargs': '*'},
			'fixture-function-w-all-parameter-combinations-pos-def-list': {'action': 'extend', 'default': ['as', 1, True], 'nargs': '*'},
			'fixture-function-w-all-parameter-combinations-pos-def-none': {'default': '==SUPPRESS==', 'nargs': '?'},
			'fixture-function-w-all-parameter-combinations-pos-def-num': {'default': 2.3, 'nargs': '?', 'type': float},
			'fixture-function-w-all-parameter-combinations-pos-def-str': {'default': 'a_str', 'nargs': '?'},
			'fixture-function-w-all-parameter-combinations-pos-req': {},
		}
		self.assertEqual(expected_result, params_from_callable(fixture_function_w_all_parameter_combinations))
