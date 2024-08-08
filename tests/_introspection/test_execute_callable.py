#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp._introspection import execute_callable

class TestExecuteCallable(TestCase):
	'''
	Tests for the execute_callable function
	'''
	
	def test_not_callable(self):
		'''
		Test "execute_callable" with a non-callable value
		'''

		self.assertRaises(ValueError, execute_callable, None)

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
	
	def test_class_w_new_and_init(self):
		'''
		Test "execute_callable" with a class that implements __new__ and __init__
		'''
		
		args_w_keys = {
			'new_pos': 'r',
			'new_kw': 6,
			'init_pos': 's',
			'init_kw': 7,
		}
		expected_result = FixtureClassWNewAndInit(args_w_keys['new_pos'], args_w_keys['init_pos'], new_kw=args_w_keys['new_kw'], init_kw=args_w_keys['init_kw'])
		self.assertEqual(expected_result, execute_callable(FixtureClassWNewAndInit, args_w_keys=args_w_keys))
	
	def test_deep_class(self):
		'''
		Test "execute_callable" with a class that implements __new__ and __init__
		'''
		
		args_w_keys = {
			'init_arg': 'spam',
		}
		expected_result = FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3(args_w_keys['init_arg'])
		self.assertEqual(expected_result, execute_callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3, args_w_keys=args_w_keys))
		
	def test_class_w_static_method(self):
		'''
		Test "execute_callable" with a static method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_s',
		}
		expected_result = 'static-method_s'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.static_method, args_w_keys=args_w_keys))
	
	def test_class_w_class_method(self):
		'''
		Test "execute_callable" with a class method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_c',
		}
		expected_result = 'ultra-class-method_c'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.class_method, args_w_keys=args_w_keys))
	
	def test_class_w_bound_method(self):
		'''
		Test "execute_callable" with a bound method
		'''
		
		args_w_keys = {
			'init_arg': 'pre',
			'pos_arg': 'method_b',
		}
		expected_result = 'ultra-pre-bound-method_b'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.bound_method, args_w_keys=args_w_keys))
	
	def test_deep_class_w_bound_method(self):
		'''
		Test "execute_callable" with a bound method on a deep class
		'''
		
		args_w_keys = {
			'init_arg': 'pre',
			'pos_arg': 'deepos',
			'kw_arg': 'deepkw',
		}
		expected_result = 'pre-deepos-deepkw'
		self.assertEqual(expected_result, execute_callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method, args_w_keys=args_w_keys))
