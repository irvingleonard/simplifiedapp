#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from fixtures.classes import *
from simplifiedapp._introspection import instantiate_class

class TestInstantiateClass(TestCase):
	'''
	Tests for the instantiate_class function
	'''
	
	def test_empty_class(self):
		'''
		Test "instantiate_class" with an empty class
		'''

		expected_result = FixtureEmptyClass()
		self.assertEqual(expected_result, instantiate_class(FixtureEmptyClass))

	def test_class_w_new(self):
		'''
		Test "instantiate_class" with a class that implements __new__
		'''

		args_w_keys = {
			'new_pos'	: '1',
			'new_kw'	: 'k',
		}

		expected_result = FixtureClassWNew(args_w_keys['new_pos'], new_kw=args_w_keys['new_kw'])
		self.assertEqual(expected_result, instantiate_class(FixtureClassWNew, args_w_keys=args_w_keys))
	
	def test_class_w_init(self):
		'''
		Test "instantiate_class" with a class that implements __init__
		'''

		args_w_keys = {
			'init_pos'	: '2',
			'init_kw'	: 'l',
		}

		expected_result = FixtureClassWInit(args_w_keys['init_pos'], init_kw=args_w_keys['init_kw'])
		self.assertEqual(expected_result, instantiate_class(FixtureClassWInit, args_w_keys=args_w_keys))
		
	def test_class_w_new_and_init(self):
		'''
		Test "instantiate_class" with a class that implements __new__ and __init__
		'''

		args_w_keys = {
			'new_pos'	: '1',
			'new_kw'	: 'k',
			'init_pos'	: '2',
			'init_kw'	: 'l',
		}
		expected_result = FixtureClassWNewAndInit(args_w_keys['new_pos'], args_w_keys['init_pos'], new_kw=args_w_keys['new_kw'], init_kw=args_w_keys['init_kw'])
		self.assertEqual(expected_result, instantiate_class(FixtureClassWNewAndInit, args_w_keys=args_w_keys))