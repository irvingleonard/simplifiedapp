#python
'''
Testing of argparse handling in simplifiedapp
'''

from unittest import TestCase

from fixtures.raw_parameters import *
from simplifiedapp import IntrospectedArgumentParser, VarKWParameter

prepare_parameters = IntrospectedArgumentParser._prepare_parameters
class TestIntrospectedArgumentParserPrepareParameters(TestCase):
	'''
	Tests for the IntrospectedArgumentParser._prepare_parameters class method
	'''
	
	maxDiff = None
	
	def setUp(self):
		self.container_name = 'prepare_parameters_tests'
	
	def test_empty_parameters(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" without any parameters
		'''

		expected_result = {}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_EMPTY_PARAMETERS, container_name=self.container_name))

	def test_positional_args(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with positional arguments
		'''

		expected_result = {
			'prepare-parameters-tests-a' : {},
			'prepare-parameters-tests-b' : {},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_POSITIONAL_ARGS, container_name=self.container_name))
	
	
	def test_varargs(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with variable positional arguments
		'''

		expected_result = {
			'prepare-parameters-tests-args': {'action': 'extend', 'default': [], 'nargs': '*'},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_VARARGS, container_name=self.container_name))

	def test_keyword_args(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with keyword arguments
		'''

		expected_result = {
			'--prepare-parameters-tests-c': {'required': True},
			'--prepare-parameters-tests-d': {'required': True},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_KEYWORD_ARGS, container_name=self.container_name))
		
	def test_varkw(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with variable keyword arguments
		'''

		expected_result = {
			'--prepare-parameters-tests-kwargs': {'action': 'extend', 'default': [], 'nargs': '*',  'type': VarKWParameter, 'help': '(Use the key=value format for each entry)'},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_VARKW, container_name=self.container_name))

	def test_default_positional_args(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with positional arguments and default values
		'''

		expected_result = {
			'prepare-parameters-tests-a': {},
			'prepare-parameters-tests-b': {'default': 2, 'nargs': '?', 'type': int},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_DEFAULT_POSITIONAL_ARGS, container_name=self.container_name))

	def test_default_keyword_args(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with keyword arguments and default values
		'''

		expected_result = {
			'--prepare-parameters-tests-c': {'required': True},
			'--prepare-parameters-tests-d': {'action': 'store_false'},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_DEFAULT_KEYWORD_ARGS, container_name=self.container_name))

	def test_version(self):
		'''
		Test "IntrospectedArgumentParser._prepare_parameters" with version
		'''

		expected_result = {'--prepare-parameters-tests-version': {'action': 'version', 'version': '0.1'}}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_VERSION, container_name=self.container_name))


	def test_function_w_all_parameter_combinations(self):
		'''
		Test IntrospectedArgumentParser._prepare_parameters with function having all possible parameter combinations
		'''

		expected_result = {
			'--prepare-parameters-tests-kw-def-bool': {'action': 'store_false'},
			'--prepare-parameters-tests-kw-def-dict': {'action': 'extend', 'default': ['1=dfe', 'yufgb=sdqwda'], 'nargs': '*'},
			'--prepare-parameters-tests-kw-def-list': {'action': 'extend', 'default': [1, 'tre', 6.7], 'nargs': '*'},
			'--prepare-parameters-tests-kw-def-none': {'default': '==SUPPRESS=='},
			'--prepare-parameters-tests-kw-def-num': {'default': (8+98j), 'type': complex},
			'--prepare-parameters-tests-kw-def-str': {'default': 'another_str'},
			'--prepare-parameters-tests-kw-req': {'required': True},
			'--prepare-parameters-tests-more-kw': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '*', 'type': VarKWParameter},
			'prepare-parameters-tests-more-pos': {'action': 'extend', 'default': [], 'nargs': '*'},
			'prepare-parameters-tests-pos-def-bool': {'action': 'store_true', 'nargs': '?'},
			'prepare-parameters-tests-pos-def-dict': {'action': 'extend', 'default': ['1=one', 'dct=6', 'fer=False'], 'nargs': '*'},
			'prepare-parameters-tests-pos-def-list': {'action': 'extend', 'default': ['as', 1, True], 'nargs': '*'},
			'prepare-parameters-tests-pos-def-none': {'default': '==SUPPRESS==', 'nargs': '?'},
			'prepare-parameters-tests-pos-def-num': {'default': 2.3, 'nargs': '?', 'type': float},
			'prepare-parameters-tests-pos-def-str': {'default': 'a_str', 'nargs': '?'},
			'prepare-parameters-tests-pos-req': {},
		}
		self.assertEqual(expected_result, prepare_parameters(FIXTURE_ALL_PARAMETER_COMBINATIONS, container_name=self.container_name))
