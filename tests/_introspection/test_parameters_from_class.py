#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from fixtures.classes import *
from simplifiedapp._introspection import parameters_from_class

class TestParametersFromClass(TestCase):
	'''
	Tests for the parameters_from_class function
	'''
	
	def test_empty_class(self):
		'''
		Test "parameters_from_class" with an empty class
		'''

		expected_result = {}
		self.assertEqual(expected_result, parameters_from_class(FixtureEmptyClass))

	def test_class_w_new(self):
		'''
		Test "parameters_from_class" with a class that implements __new__
		'''

		expected_result = {'new_pos': {'positional': True}, 'new_kw': {'positional': False}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNew))
	
	def test_class_w_new_varargs(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ with varargs
		'''

		expected_result = {'new_pos': {'positional': True}, 'args': {'default': [], 'positional': True, 'special': 'varargs'}, 'new_kw': {'positional': False}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewVarargs))
		
	def test_class_w_new_varkw(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ with varkw
		'''

		expected_result = {'new_pos': {'positional': True}, 'new_kw': {'positional': False}, 'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewVarkw))
	
	def test_class_w_init(self):
		'''
		Test "parameters_from_class" with a class that implements __init__
		'''

		expected_result = {'init_pos': {'positional': True}, 'init_kw': {'positional': False}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWInit))
	
	def test_class_w_init_varargs(self):
		'''
		Test "parameters_from_class" with a class that implements __init__ with varargs
		'''

		expected_result = {'init_pos': {'positional': True}, 'args': {'default': [], 'positional': True, 'special': 'varargs'}, 'init_kw': {'positional': False}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWInitVarargs))
		
	def test_class_w_init_varkw(self):
		'''
		Test "parameters_from_class" with a class that implements __init__ with varkw
		'''

		expected_result = {'init_pos': {'positional': True}, 'init_kw': {'positional': False}, 'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWInitVarkw))
		
	def test_class_w_new_and_init(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ and __init__
		'''

		expected_result = {
			'new_pos': {'positional': True},
			'init_pos': {'positional': True},
			'args': {'default': [], 'positional': True, 'special': 'varargs'},
			'new_kw': {'positional': False},
			'init_kw': {'positional': False},
			'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'},
		}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewAndInit))
		
	def test_class_w_new_and_init_n_var(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ and __init__ and no varargs or varkw
		'''

		expected_result = {'foo': {'positional': True}, 'bar': {'positional': False}}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewAndInitNVar))
		
	def test_class_w_new_and_init_var_new(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ (with varargs or varkw) and __init__
		'''

		expected_result = {
			'foo': {'positional': True},
			'args': {'default': [], 'positional': True, 'special': 'varargs'},
			'bar': {'positional': False},
			'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'},
		}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewAndInitVarNew))
	
	def test_class_w_new_and_init_var_init(self):
		'''
		Test "parameters_from_class" with a class that implements __new__ and __init__ (with varargs or varkw)
		'''

		expected_result = {
			'foo': {'positional': True},
			'args': {'default': [], 'positional': True, 'special': 'varargs'},
			'bar': {'positional': False},
			'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'},
		}
		self.assertEqual(expected_result, parameters_from_class(FixtureClassWNewAndInitVarNew))
	