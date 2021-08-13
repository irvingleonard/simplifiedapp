#python
'''
Testing of metadata handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp

class TestParamMetadata(unittest.TestCase):
	'''
	Tests for the param_metadata function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.param_metadata
		self.maxDiff = None
	
	def test_annotations_class_str(self):
		'''
		Testing annotation for type str
		'''
		
		expected_result = {'type' : str}
		self.assertDictEqual(expected_result, self.test_object('a', {}, {'a' : str}, ''))

	def test_annotations_choices(self):
		'''
		Testing annotation for choices
		'''
		
		expected_result = {'choices' : ('b', 3, False)}
		self.assertDictEqual(expected_result, self.test_object('a', {}, {'a' : ('b', 3, False)}, ''))

	def test_default_none(self):
		'''
		Testing defaults: None
		'''
		
		expected_result = {'default' : argparse.SUPPRESS}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : None}, {}, ''))

	def test_default_str(self):
		'''
		Testing defaults: str
		'''
		
		expected_result = {'default' : 'v'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 'v'}, {}, ''))
	
	def test_default_false(self):
		'''
		Testing defaults: False
		'''
		
		expected_result = {'default' : False, 'action' : 'store_true'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : False}, {}, ''))
	
	def test_default_true(self):
		'''
		Testing defaults: True
		'''
		
		expected_result = {'default' : True, 'action' : 'store_false'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : True}, {}, ''))

	def test_default_tuple(self):
		'''
		Testing defaults: tuple
		'''
		
		expected_result = {'default' : [], 'action' : 'extend', 'nargs' : '+'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : ('v1', 2)}, {}, ''))

	def test_default_tuple_w_nargs(self):
		'''
		Testing defaults: tuple with nargs
		'''
		
		expected_result = {'default' : [], 'action' : 'extend', 'nargs' : '*'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : ('v1', 2), 'nargs' : '*'}, {}, ''))

	def test_default_dict(self):
		'''
		Testing defaults: dict
		'''
		
		expected_result = {'default' : [], 'action' : 'extend', 'nargs' : '+', 'help': '(Use the key=value format for each entry)'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : {'v1' : 1, 2 : 'V2'}}, {}, ''))

	def test_default_int(self):
		'''
		Testing defaults: int
		'''
		
		expected_result = {'default' : 3, 'type' : int}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 3}, {}, ''))

	def test_default_float(self):
		'''
		Testing defaults: float
		'''
		
		expected_result = {'default' : 2.5, 'type' : float}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 2.5}, {}, ''))