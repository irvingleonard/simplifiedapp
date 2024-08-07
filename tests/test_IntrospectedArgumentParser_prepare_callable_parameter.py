#python
'''
Testing of argparse handling in simplifiedapp
'''

from argparse import SUPPRESS
from unittest import TestCase

from simplifiedapp import IntrospectedArgumentParser

prepare_callable_parameter = IntrospectedArgumentParser._prepare_callable_parameter
class TestIntrospectedArgumentParserPrepareCallableParameter(TestCase):
	'''
	Tests for the IntrospectedArgumentParser._prepare_callable_parameter class method
	'''
	
	maxDiff = None
	
	def test_empty_parameter(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter without details
		'''

		expected_result = ({}, [], [])
		self.assertEqual(expected_result, prepare_callable_parameter())
	
	def test_parameter_w_none_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a None default
		'''
		
		expected_result = ({'default' : SUPPRESS}, [], [])
		self.assertEqual(expected_result, prepare_callable_parameter(default=None))
	
	def test_parameter_w_str_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a string default
		'''
		
		expected_result = ({'default' : 'initial'}, [], [])
		self.assertEqual(expected_result, prepare_callable_parameter(default='initial'))
	
	def test_parameter_w_bool_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a boolean default
		'''
		
		expected_false_result = ({'action': 'store_true'}, [], [])
		self.assertEqual(expected_false_result, prepare_callable_parameter(default=False))
		
		expected_true_result = ({'action': 'store_false'}, [], [])
		self.assertEqual(expected_true_result, prepare_callable_parameter(default=True))
	
	def test_parameter_w_sequence_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a sequence default
		'''
		
		expected_frozenset_result = ({'action': 'extend', 'default': frozenset({'frozen', 'set'}), 'nargs': '*'}, [], [])
		self.assertEqual(expected_frozenset_result, prepare_callable_parameter(default=frozenset(('frozen', 'set'))))
		
		expected_set_result = ({'action': 'extend', 'default': {'e', 't', 's'}, 'nargs': '*'}, [], [])
		self.assertEqual(expected_set_result, prepare_callable_parameter(default={'s', 'e', 't'}))
		
		expected_tuple_result = ({'action': 'extend', 'default': ('tu', 'ple'), 'nargs': '*'}, [], [])
		self.assertEqual(expected_tuple_result, prepare_callable_parameter(default=('tu', 'ple')))
		
		expected_list_result = ({'action': 'extend', 'default': ['li', 'st'], 'nargs': '*'}, [], [])
		self.assertEqual(expected_list_result, prepare_callable_parameter(default=['li', 'st']))
	
	def test_parameter_w_mapping_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a mapping default
		'''
		
		expected_result = ({
			'action': 'extend',
			'default': ['a=map', 'test=True'],
			'nargs': '*'
		}, [], [])
		self.assertEqual(expected_result, prepare_callable_parameter(default={'a' : 'map', 'test' : True}))

	def test_parameter_w_numeric_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a numeric default
		'''
		
		expected_int_result = ({'default': 14, 'type': int}, [], [])
		self.assertEqual(expected_int_result, prepare_callable_parameter(default=14))
		
		expected_float_result = ({'default': 3.14, 'type': float}, [], [])
		self.assertEqual(expected_float_result, prepare_callable_parameter(default=3.14))
		
		expected_complex_result = ({'default': (6+12j), 'type': complex}, [], [])
		self.assertEqual(expected_complex_result, prepare_callable_parameter(default=(6+12j)))

	# def test_parameter_w_annotations(self):
	# 	'''
	# 	Test IntrospectedArgumentParser._prepare_callable_parameter with annotations
	# 	'''
	#
	# 	from fixtures import _introspection as introspection_fixture
	# 	tst = parameters_from_callable(introspection_fixture.test_callable, callable_metadata=object_metadata(introspection_fixture.test_callable))
	# 	expected_result = {}
	# 	self.assertEqual(expected_result, tst['pos2']['annotation'])
	# 	self.assertEqual(expected_result, self.test_object(tst['kw2']['annotations']))

	def test_parameter_w_docstring(self):
		'''
		Test ArgparseParser.from_callable with function having docstring documented parameters
		'''

		expected_result_matching = ({'help': 'Second key word test parameter'},[],[])
		docstring_matching = {'description': 'Second key word test parameter', 'is_optional': False}
		self.assertEqual(expected_result_matching, prepare_callable_parameter(docstring=docstring_matching))

		expected_result_required_bad = ({
			'help': 'Second key word test parameter'
		}, [
			'''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's optional but doesn't match "{parent_description}"'s signature'''
		], [])
		docstring_required_bad = {'description': 'Second key word test parameter', 'is_optional': True}
		self.assertEqual(expected_result_required_bad, prepare_callable_parameter(docstring=docstring_required_bad))

		expected_result_optional_bad = ({
			'action': 'store_false',
			'help': 'Second key word test parameter'
		}, [], [
			'''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's required but doesn't match "{parent_description}"'s signature'''
		])
		docstring_optional_bad = {'description': 'Second key word test parameter', 'is_optional': False}
		self.assertEqual(expected_result_optional_bad, prepare_callable_parameter(docstring=docstring_optional_bad, default=True))
