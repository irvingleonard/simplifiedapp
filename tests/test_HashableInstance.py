#python
'''
Testing of metadata handling in simplifiedapp
'''

import unittest

import simplifiedapp

class TestForcedHash(unittest.TestCase):
	'''
	Tests for the HashableInstance class
	'''
	
	def setUp(self):
		self.test_object = lambda item: hash(simplifiedapp.HashableInstance(item))
	
	def test_none(self):
		'''
		Testing HashableInstance with input None
		'''
		
		self.assertEqual(self.test_object(None), hash(None))

	def test_false(self):
		'''
		Testing HashableInstance with input False
		'''

		self.assertEqual(self.test_object(False), 0)

	def test_true(self):
		'''
		Testing HashableInstance with input True
		'''

		self.assertEqual(self.test_object(True), 1)
	
	def test_int(self):
		'''
		Testing HashableInstance with input integer
		'''
		
		self.assertEqual(self.test_object(127), 127)
		
	def test_float(self):
		'''
		Testing HashableInstance with input float
		'''
		
		self.assertEqual(self.test_object(22.56), hash(22.56))

	def test_complex(self):
		'''
		Testing HashableInstance with input complex
		'''

		self.assertEqual(self.test_object(complex('1+2j')), hash(complex('1+2j')))
		
	def test_list(self):
		'''
		Testing HashableInstance with input list
		'''

		self.assertEqual(self.test_object([1, 't', False]), hash((1, 't', False)))

	def test_tuple(self):
		'''
		Testing HashableInstance with input tuple
		'''

		self.assertEqual(self.test_object((1, 't', False)), hash((1, 't', False)))

	def test_range(self):
		'''
		Testing HashableInstance with input range
		'''

		self.assertEqual(self.test_object(range(5)), hash(range(5)))

	def test_string(self):
		'''
		Testing HashableInstance with input string
		'''
		
		self.assertEqual(self.test_object('test'), hash('test'))

	def test_set(self):
		'''
		Testing HashableInstance with input set
		'''

		self.assertEqual(self.test_object({1, 't', False}), hash(frozenset({1, 't', False})))

	def test_frozenset(self):
		'''
		Testing HashableInstance with input frozenset
		'''

		self.assertEqual(self.test_object(frozenset((1, 't', False))), hash(frozenset((1, 't', False))))

	def test_dict(self):
		'''
		Testing HashableInstance with input dict
		'''

		fixture = {'number' : 1, 0 : 't', None : False}
		self.assertEqual(self.test_object(fixture), hash(tuple([(key, value) for key, value in fixture.items()])))
