#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
from unittest import TestCase

from fixtures.classes import *
from simplifiedapp import IntrospectedArgumentParser, VarKWParameter

# params_from_class = IntrospectedArgumentParser.params_from_class
class TestIntrospectedArgumentParserParamsFromCallable(TestCase):
	'''
	Tests for the IntrospectedArgumentParser.params_from_class class method
	'''
	
	maxDiff = None

	def _test_empty_class(self):
		'''
		Test "IntrospectedArgumentParser.params_from_class" with an empty class
		'''
		
		expected_result = (
		[FixtureClassWMethods.bound_method, FixtureClassWMethods.class_method, FixtureClassWMethods.static_method], [])
		self.assertEqual(expected_result, params_from_class(FixtureEmptyClass))