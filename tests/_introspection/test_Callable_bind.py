#python
'''
Testing the introspection_patched.Callable.bind method
'''

from unittest import TestCase

from introspection import BoundArguments

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import Callable

class TestCallableBind(TestCase):
	'''
	Tests for the Callable.bind method
	'''

	def test_empty_function(self):
		'''
		Test "Callable.bind" with a function that doesn't have parameters
		'''
		
		callable_ = Callable(fixture_empty_function)
		expected_result = BoundArguments(callable_.signature, {})
		self.assertEqual(expected_result, callable_.bind())

	def test_function_w_all_parameter_combinations(self):
		'''
		Test "Callable.bind" with a function that takes every possible parameter
		'''
		
		callable_ = Callable(fixture_function_w_all_parameter_combinations)

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
		expected_result = BoundArguments(callable_.signature, expected_args)
		self.assertEqual(expected_result, callable_.bind(**run_input))

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
		expected_result = BoundArguments(callable_.signature, run_input)
		self.assertEqual(expected_result, callable_.bind(**run_input))
	
	def test_class_w_new_and_init(self):
		'''
		Test "Callable.bind" with a class that implements __new__ and __init__
		'''
		
		callable_ = Callable(FixtureClassWNewAndInit)
		args_w_keys = {
			'new_pos': 'r',
			'new_kw': 6,
			'init_pos': 's',
			'init_kw': 7,
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
	
	def test_deep_class(self):
		'''
		Test "Callable.bind" with a deep class
		'''
		
		callable_ = Callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3)
		args_w_keys = {
			'init_arg': 'spam',
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
		
	def test_class_w_static_method(self):
		'''
		Test "Callable.bind" with a static method
		'''
		
		callable_ = Callable(FixtureClassWMethods.static_method)
		args_w_keys = {
			'pos_arg': 'method_s',
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
	
	def test_class_w_class_method(self):
		'''
		Test "Callable.bind" with a class method
		'''
		
		callable_ = Callable(FixtureClassWMethods.class_method)
		args_w_keys = {
			'pos_arg': 'method_c',
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
	
	def test_class_w_instance_method(self):
		'''
		Test "Callable.bind" with an instance method
		'''
		
		callable_ = Callable(FixtureClassWMethods.bound_method)
		args_w_keys = {
			'pos_arg': 'method_b',
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
	
	def test_deep_class_w_instance_method(self):
		'''
		Test "Callable.bind" with an instance method on a deep class
		'''
		
		callable_ = Callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method)
		args_w_keys = {
			'pos_arg': 'deepos',
			'kw_arg': 'deepkw',
		}
		expected_result = BoundArguments(callable_.signature, args_w_keys)
		self.assertEqual(expected_result, callable_.bind(**args_w_keys))
