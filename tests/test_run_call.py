#python
'''
Testing of argparse handling in simplifiedapp
'''

import unittest
import sys

import simplifiedapp


def fixture_callable(*args, **kwargs):
	return 'Ok from module root'


class TestRunCall(unittest.TestCase):
	'''
	Tests for the run_call function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.run_call
		self.maxDiff = None


	def test_error_tuple_not_5(self):
		'''
		Test error: call_ tuple length not 5
		'''

		self.assertRaises(ValueError, self.test_object, (1, 2, 3, 4), {})

	def test_error_callable_str_wo_parent(self):
		'''
		Test error: callable is str and no parent provided
		'''

		self.assertRaises(ValueError, self.test_object, ('a', None, None, (), ()), {})

	def test_callable_str_w_parent(self):
		'''
		Test callable is str and parent is current module
		'''

		self.assertEqual('Ok from module root', self.test_object(('fixture_callable', None, None, (), ()), {}, parent = sys.modules[__name__]))

	def test_args_list(self):
		'''
		Test complete_input with args list
		'''
		
		def fixture_args_list(*args):
			return args

		self.assertEqual(('1', 2), self.test_object((fixture_args_list, None, None, ('v1', 'v2'), ()), {'v1' : '1', 'v2' : 2}))

	def test_w_args_param(self):
		'''
		Test complete_input with a variable positional argument
		'''
		
		def fixture_function_w_args(*args):
			return args

		self.assertEqual(('v1', 2), self.test_object((fixture_function_w_args, 'args', None, (), ()), {'args' : ['v1', 2]}))



	def test_kwargs_list(self):
		'''
		Test callable_args with kwargs list
		'''
		
		def fixture_kwargs_list(**kwargs):
			return kwargs

		self.assertDictEqual({'v1' : '1', 'v2' : 2}, self.test_object((fixture_kwargs_list, None, None, (), ('v1', 'v2')), {'v1' : '1', 'v2' : 2}))


	def test_w_kwargs_param(self):
		'''
		Test complete_input with a variable keyword argument
		'''
		
		def fixture_function_w_kwargs(**kwargs):
			return kwargs

		self.assertDictEqual({'v1': 'a', 'v2': '2'}, self.test_object((fixture_function_w_kwargs, None, 'kwargs', (), ()), {'kwargs' : ['v1=a', 'v2=2']}))

