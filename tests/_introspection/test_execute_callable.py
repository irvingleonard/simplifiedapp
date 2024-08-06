#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from simplifiedapp._introspection import execute_callable

class TestExecuteCallable(TestCase):
	'''
	Tests for the execute_callable function
	'''
	
	def setUp(self):
		self.test_object = execute_callable
	
	def test_empty_callable(self):
		'''
		Test "execute_callable" with a callable that doesn't have parameters
		'''

		def fixture_empty_callable():
			return True

		expected_result = True
		self.assertEqual(expected_result, self.test_object(fixture_empty_callable))

	def test_complex_callable(self):
		'''
		Test "execute_callable" with a callable that takes every possible parameter
		'''

		def fixture_complex_callable(pos, pos_def=1, /, mix=None, *args, kw_req, kw_opt='foo', **kwargs):
			return str(pos) + str(pos_def) + str(mix) + ''.join(args) + str(kw_req) + str(kw_opt) + str(kwargs)

		run_input = {
			'pos' : 'a',
			'args' : ['ep1', 'ep2'],
			'kw_req' : 'here',
		}
		expected_result = 'a1Noneep1ep2herefoo{}'
		self.assertEqual(expected_result, self.test_object(fixture_complex_callable, args_w_keys=run_input))

		run_input = {
			'pos': 'b',
			'pos_def': 2,
			'mix': 'All',
			'args': ['epA', 'epB'],
			'kw_req': 'there',
			'kw_opt': 'bar',
			'kwargs': {'to' : 'be', 'or not' : 'to be'},
		}
		expected_result = "b2AllepAepBtherebar{'to': 'be', 'or not': 'to be'}"
		self.assertEqual(expected_result, self.test_object(fixture_complex_callable, args_w_keys=run_input))
