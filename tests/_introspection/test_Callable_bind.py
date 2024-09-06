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
		expected_result = (), {}
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

		expected_result = ('a', None, 'a_str', False, ['as', 1, True], {1: 'one', 'dct': 6, 'fer': False}, 2.3, 'ep1', 'ep2'), {'kw_req': 'here'}
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
		expected_kw = {
			'kw_def_bool': 'False',
			'kw_def_dict': {'i': 8, 'j': 98},
			'kw_def_list': [None, False, ''],
			'kw_def_none': 'bar',
			'kw_def_num': 3.14,
			'kw_def_str': 'carnage',
			'kw_req': 'there',
			'or not': 'to be',
			'to': 'be',
		}
		expected_result = ('b', 2, 'All', True, [True, False], {'g': 100, 'a': 0}, 7, 'epA', 'epB'), expected_kw
		self.assertEqual(expected_result, callable_.bind(**run_input))
	
	def test_class_w_new_and_init(self):
		'''
		Test "Callable.bind" with a class that implements __new__ and __init__
		'''
		
		args_w_keys = {
			'new_pos': 'r',
			'new_kw': 6,
			'init_pos': 's',
			'init_kw': 7,
		}
		expected_result = ('r', 's'), {'init_kw': 7, 'new_kw': 6}
		self.assertEqual(expected_result, Callable(FixtureClassWNewAndInit).bind(**args_w_keys))
	
	def test_deep_class(self):
		'''
		Test "Callable.bind" with a deep class
		'''
		
		args_w_keys = {
			'init_arg': 'spam',
		}
		expected_result = ('spam',), {}
		self.assertEqual(expected_result, Callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3).bind(**args_w_keys))
		
	def test_class_w_static_method(self):
		'''
		Test "Callable.bind" with a static method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_s',
		}
		expected_result = ('method_s',), {}
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.static_method).bind(**args_w_keys))
	
	def test_class_w_class_method(self):
		'''
		Test "Callable.bind" with a class method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_c',
		}
		expected_result = ('method_c',), {}
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.class_method).bind(**args_w_keys))
	
	def test_class_w_instance_method(self):
		'''
		Test "Callable.bind" with an instance method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_b',
		}
		expected_result = ('method_b',), {}
		self.assertEqual(expected_result, Callable(FixtureClassWMethods.bound_method).bind(**args_w_keys))
	
	def test_deep_class_w_instance_method(self):
		'''
		Test "Callable.bind" with an instance method on a deep class
		'''
		
		args_w_keys = {
			'pos_arg': 'deepos',
			'kw_arg': 'deepkw',
		}
		expected_result = ('deepos',), {'kw_arg': 'deepkw'}
		self.assertEqual(expected_result, Callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method).bind(**args_w_keys))
