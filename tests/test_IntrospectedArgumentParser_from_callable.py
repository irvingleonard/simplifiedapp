#python
'''
Testing of argparse handling in simplifiedapp
'''

from unittest import TestCase

from fixtures.functions import *
from simplifiedapp import IntrospectedArgumentParser, LocalFormatterClass

from_callable = IntrospectedArgumentParser.from_callable
class TestIntrospectedArgumentParserFromCallable(TestCase):
	'''
	Tests for the IntrospectedArgumentParser.from_callable class method
	'''
	
	maxDiff = None

	def test_empty_function(self):
		'''
		Test IntrospectedArgumentParser.from_callable with simplest function signature
		'''
		
		kwargs = {
			'prog'				: 'fixture_empty_function',
			'formatter_class'	: LocalFormatterClass,
			'description'		: 'Empty function',
			'epilog'			: 'A function without parameters',
		}
		expected_result = IntrospectedArgumentParser(**kwargs)
		expected_result.set_defaults(callable=fixture_empty_function)
		self.assertEqual(expected_result, from_callable(fixture_empty_function))

	def test_function_w_version(self):
		'''
		Test IntrospectedArgumentParser.from_callable with a versioned function
		'''
		
		kwargs = {
			'prog'				: 'fixture_function_w_version',
			'formatter_class'	: LocalFormatterClass,
			'description'		: 'Versioned function',
			'epilog'			: 'Function with version attribute set',
		}
		expected_result = IntrospectedArgumentParser(**kwargs)
		expected_result.add_argument('--fixture-function-w-version-version', action='version', version='0.1')
		expected_result.set_defaults(callable=fixture_function_w_version)
		self.assertEqual(expected_result, from_callable(fixture_function_w_version))
