# python
'''
Testing the introspection.enumerate_object_callables function
'''

from unittest import TestCase

from fixtures.classes import *
from simplifiedapp._introspection import enumerate_object_callables


class TestEnumerateClassCallables(TestCase):
	'''
	Tests for the enumerate_object_callables function
	'''
	
	maxDiff = None
	
	def test_class_w_methods(self):
		'''
		Test "enumerate_object_callables" with a class that implements different kind of methods
		'''
		
		expected_result = ([FixtureClassWMethods.__call__, FixtureClassWMethods.bound_method, FixtureClassWMethods.class_method, FixtureClassWMethods.problematic_static_method, FixtureClassWMethods.static_method], [])
		self.assertEqual(expected_result, enumerate_object_callables(FixtureClassWMethods))
	
	def test_deep_class(self):
		'''
		Test "enumerate_object_callables" with a deep class
		'''
		
		expected_result = ([], [FixtureDeepClassL1.FixtureDeepClassL2])
		self.assertEqual(expected_result, enumerate_object_callables(FixtureDeepClassL1))