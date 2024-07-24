#python
'''
Testing of argparse handling in simplifiedapp
'''

from argparse import SUPPRESS
from unittest import TestCase

from simplifiedapp import IntrospectedArgumentParser, LocalFormatterClass, object_metadata, parameters_from_callable

class TestIntrospectedArgumentParserPrepareCallableParameter(TestCase):
	'''
	Tests for the IntrospectedArgumentParser._prepare_callable_parameter class method
	'''
	
	maxDiff = None
	
	def setUp(self):
		self.test_object = IntrospectedArgumentParser._prepare_callable_parameter
	
	def test_empty_parameter(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter without details
		'''

		expected_result = {}
		self.assertEqual(expected_result, self.test_object())
	
	def test_parameter_w_none_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a None default
		'''
		
		expected_result = {'default' : SUPPRESS}
		self.assertEqual(expected_result, self.test_object(default=None))
	
	def test_parameter_w_str_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a string default
		'''
		
		expected_result = {'default' : 'initial'}
		self.assertEqual(expected_result, self.test_object(default='initial'))
	
	def test_parameter_w_bool_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a boolean default
		'''
		
		expected_false_result = {'action': 'store_true'}
		self.assertEqual(expected_false_result, self.test_object(default=False))
		
		expected_true_result = {'action': 'store_false'}
		self.assertEqual(expected_true_result, self.test_object(default=True))
	
	def test_parameter_w_sequence_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a sequence default
		'''
		
		expected_frozenset_result = {'action': 'extend', 'default': frozenset({'frozen', 'set'}), 'nargs': '*'}
		self.assertEqual(expected_frozenset_result, self.test_object(default=frozenset(('frozen', 'set'))))
		
		expected_set_result = {'action': 'extend', 'default': {'e', 't', 's'}, 'nargs': '*'}
		self.assertEqual(expected_set_result, self.test_object(default={'s', 'e', 't'}))
		
		expected_tuple_result = {'action': 'extend', 'default': ('tu', 'ple'), 'nargs': '*'}
		self.assertEqual(expected_tuple_result, self.test_object(default=('tu', 'ple')))
		
		expected_list_result = {'action': 'extend', 'default': ['li', 'st'], 'nargs': '*'}
		self.assertEqual(expected_list_result, self.test_object(default=['li', 'st']))
	
	def test_parameter_w_mapping_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a mapping default
		'''
		
		expected_result = {
			'action': 'extend',
			'default': ['a=map', 'test=True'],
			'help': '(Use the key=value format for each entry)',
			'nargs': '*'
		}
		self.assertEqual(expected_result, self.test_object(default={'a' : 'map', 'test' : True}))

	def test_parameter_w_numeric_default(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with a numeric default
		'''
		
		expected_int_result = {'default': 14, 'type': int}
		self.assertEqual(expected_int_result, self.test_object(default=14))
		
		expected_float_result = {'default': 3.14, 'type': float}
		self.assertEqual(expected_float_result, self.test_object(default=3.14))
		
		expected_complex_result = {'default': (6+12j), 'type': complex}
		self.assertEqual(expected_complex_result, self.test_object(default=(6+12j)))

	def test_parameter_w_annotations(self):
		'''
		Test IntrospectedArgumentParser._prepare_callable_parameter with annotations
		'''

		from fixtures import _introspection as introspection_fixture
		tst = parameters_from_callable(introspection_fixture.test_callable, callable_metadata=object_metadata(introspection_fixture.test_callable))
		expected_result = {}
		self.assertEqual(expected_result, tst['pos2'])
		#self.assertEqual(expected_result, self.test_object(tst['kw2']['annotations']))

	def _test_function_w_annotations(self):
		'''
		Test ArgparseParser.from_callable with function having annotated arguments
		'''
		
		def fixture_function_w_annotations(a_str : str, an_int : int, a_float : float, some_choices : ['a', 'b', 'c']):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('a_str', type = str),
				ARGUMENT_CLASS('an_int', type = int),
				ARGUMENT_CLASS('a_float', type = float),
				ARGUMENT_CLASS('some_choices', choices = ['a', 'b', 'c']),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_function_w_annotations, ('a_str', 'an_int', 'a_float', 'some_choices'), None, (), None)})

		self.assertEqual(self.test_object(fixture_function_w_annotations), expected_result)

	def _test_version(self):
		'''
		Test ArgparseParser.from_callable with versioned function (because "reasons")
		'''
		
		def fixture_versioned_function():
			pass
		fixture_versioned_function.__version__ = '0.1'

		expected_arguments = (
				ARGUMENT_CLASS('version', action = 'version', version = '0.1'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_versioned_function, (), None, (), None)})
		self.assertEqual(self.test_object(fixture_versioned_function), expected_result)

	def _test_complex_function(self):
		'''
		Test ArgparseParser.from_callable with the most "complex" function possible
		'''
		
		def fixture_complex_function(simple_positional_parameter, a_str: str, an_int: int, parameter_w_default = "3", parameter_w_options: ['first', 'second', 'third', 'nope'] = 'first', a_bool = True, *args, keyword_parameter = 'some value', __ = 'weird parameter name', supressable_parameter = None, **kwargs):
			pass

		expected_arguments = (
				ARGUMENT_CLASS('simple_positional_parameter'),
				ARGUMENT_CLASS('a_str', type = str),
				ARGUMENT_CLASS('an_int', type = int),
				ARGUMENT_CLASS('parameter_w_default', default = '3'),
				ARGUMENT_CLASS('parameter_w_options', choices = ['first', 'second', 'third', 'nope'], default = 'first'),
				ARGUMENT_CLASS('a_bool', action = 'store_false', default = True),
				ARGUMENT_CLASS('args', action = 'extend', default = [], nargs = '*'),
				ARGUMENT_CLASS('keyword_parameter', default = 'some value'),
				ARGUMENT_CLASS('__', default = 'weird parameter name'),
				ARGUMENT_CLASS('supressable_parameter', default = argparse.SUPPRESS),
				ARGUMENT_CLASS('kwargs', action = 'extend', default = [], nargs = '+', help = '(Use the key=value format for each entry)'),
		)
		expected_result = PARSER_CLASS(*expected_arguments, defaults = {'__simplifiedapp_' : (fixture_complex_function, ('simple_positional_parameter', 'a_str', 'an_int', 'parameter_w_default', 'parameter_w_options', 'a_bool'), 'args', ('keyword_parameter', '__', 'supressable_parameter'), 'kwargs')})

		self.assertEqual(self.test_object(fixture_complex_function), expected_result)

