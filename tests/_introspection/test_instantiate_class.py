#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from simplifiedapp._introspection import instantiate_class

class TestInstantiateClass(TestCase):
	'''
	Tests for the execute_callable function
	'''
	
	def setUp(self):
		self.test_object = instantiate_class
	
	def test_empty_class(self):
		'''
		Test "execute_callable" with a callable that doesn't have parameters
		'''

		class FixtureEmptyClass:
			pass

		expected_result = {}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyClass))

	def _test_complex_callable(self):
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
