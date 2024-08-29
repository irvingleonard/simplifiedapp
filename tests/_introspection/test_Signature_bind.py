#python
'''
Testing the introspection_patched.EnhancedSignature.bind method
'''

from unittest import TestCase

from introspection import BoundArguments

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import Signature

class TestEnhancedSignature(TestCase):
	'''
	Tests for the EnhancedSignature.bind method
	'''

	def test_empty_function(self):
		'''
		Test "EnhancedSignature.bind" with a function that doesn't have parameters
		'''
		
		signature_ = Signature.from_callable(fixture_empty_function)
		expected_result = BoundArguments(signature_, {})
		self.assertEqual(expected_result, signature_.bind())

	def test_function_w_all_parameter_combinations(self):
		'''
		Test "EnhancedSignature.bind" with a function that takes every possible parameter
		'''
		
		signature_ = Signature.from_callable(fixture_function_w_all_parameter_combinations)

		run_input = {
			'pos_req' : 'a',
			'more_pos' : ('ep1', 'ep2'),
			'kw_req' : 'here',
		}
		expected_args = {
			'pos_req': 'a',
			'pos_def_none': None,
			'pos_def_str': 'a_str',
			'pos_def_bool': False,
			'pos_def_list': ['as', 1, True],
			'pos_def_dict': {'dct': 6, 'fer': False, 1: 'one'},
			'pos_def_num': 2.3,
			'more_pos': ('ep1', 'ep2'),
			'kw_req': 'here',
		}
		expected_result = BoundArguments(signature_, expected_args)
		self.assertEqual(expected_result, signature_.bind(**run_input))

		run_input = {
			'pos_req': 'b',
			'pos_def_none': 2,
			'pos_def_str': 'All',
			'pos_def_bool': True,
			'pos_def_list': [True, False],
			'pos_def_dict': {'g' : 100, 'a' : 0},
			'pos_def_num': 7,
			'more_pos': ('epA', 'epB'),
			'kw_req': 'there',
			'kw_def_none': 'bar',
			'kw_def_str': 'carnage',
			'kw_def_bool': 'False',
			'kw_def_list': [None, False, ''],
			'kw_def_dict': {'i' : 8, 'j' : 98},
			'kw_def_num': 3.14,
			'more_kw': {'to' : 'be', 'or not' : 'to be'},
		}
		expected_result = BoundArguments(signature_, run_input)
		self.assertEqual(expected_result, signature_.bind(**run_input))
	
	def test_class_w_new_and_init(self):
		'''
		Test "EnhancedSignature.bind" with a class that implements __new__ and __init__
		'''
		
		signature_ = Signature.from_callable(FixtureClassWNewAndInit)
		# signature_ = signature_.without_parameters(0)
		print('Signature is: ', signature_.parameters)
		args_w_keys = {
			'new_pos': 'r',
			'new_kw': 6,
			'init_pos': 's',
			'init_kw': 7,
		}
		# expected_result = BoundArguments(signature_, args_w_keys)
		result = signature_.bind(**args_w_keys)
		print('Args: ', result.signature)
		self.assertEqual(expected_result, signature_.bind(**args_w_keys))
	
	def _test_deep_class(self):
		'''
		Test "execute_callable" with a class that implements __new__ and __init__
		'''
		
		args_w_keys = {
			'init_arg': 'spam',
		}
		expected_result = FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3(args_w_keys['init_arg'])
		self.assertEqual(expected_result, execute_callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3, args_w_keys=args_w_keys))
		
	def _test_class_w_static_method(self):
		'''
		Test "execute_callable" with a static method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_s',
		}
		expected_result = 'static-method_s'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.static_method, args_w_keys=args_w_keys))
	
	def _test_class_w_class_method(self):
		'''
		Test "execute_callable" with a class method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_c',
		}
		expected_result = 'ultra-class-method_c'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.class_method, args_w_keys=args_w_keys))
	
	def _test_class_w_bound_method(self):
		'''
		Test "execute_callable" with a bound method
		'''
		
		args_w_keys = {
			'init_arg': 'pre',
			'pos_arg': 'method_b',
		}
		expected_result = 'ultra-pre-bound-method_b'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.bound_method, args_w_keys=args_w_keys))
	
	def _test_deep_class_w_bound_method(self):
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
