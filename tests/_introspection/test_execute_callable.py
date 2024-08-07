#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from fixtures.functions import *
from simplifiedapp._introspection import execute_callable

class TestExecuteCallable(TestCase):
	'''
	Tests for the execute_callable function
	'''
	
	def test_empty_function(self):
		'''
		Test "execute_callable" with a function that doesn't have parameters
		'''

		expected_result = True
		self.assertEqual(expected_result, execute_callable(fixture_empty_function))

	def test_function_w_all_parameter_combinations(self):
		'''
		Test "execute_callable" with a function that takes every possible parameter
		'''

		run_input = {
			'pos_req' : 'a',
			'more_pos' : ['ep1', 'ep2'],
			'kw_req' : 'here',
		}
		expected_result = "aNonea_strFalse['as', 1, True]{'dct': 6, 'fer': False, 1: 'one'}2.3('ep1', 'ep2')hereNoneanother_strTrue[1, 'tre', 6.7]{1: 'dfe', 'yufgb': 'sdqwda'}(8+98j){}"
		self.assertEqual(expected_result, execute_callable(fixture_function_w_all_parameter_combinations, args_w_keys=run_input))

		run_input = {
			'pos_req': 'b',
			'pos_def_none': 2,
			'pos_def_str': 'All',
			'pos_def_bool': True,
			'pos_def_list': [True, False],
			'pos_def_dict': {'g' : 100, 'a' : 0},
			'pos_def_num': 7,
			'more_pos': ['epA', 'epB'],
			'kw_req': 'there',
			'kw_def_none': 'bar',
			'kw_def_str': 'carnage',
			'kw_def_bool': 'False',
			'kw_def_list': [None, False, ''],
			'kw_def_dict': {'i' : 8, 'j' : 98},
			'kw_def_num': 3.14,
			'more_kw': {'to' : 'be', 'or not' : 'to be'},
		}
		
		expected_result = "b2AllTrue[True, False]{'g': 100, 'a': 0}7('epA', 'epB')therebarcarnageFalse[None, False, '']{'i': 8, 'j': 98}3.14{'to': 'be', 'or not': 'to be'}"
		self.assertEqual(expected_result, execute_callable(fixture_function_w_all_parameter_combinations, args_w_keys=run_input))
	