#python
'''
Testing of metadata handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp


class DummyArgparseArgument(set):
	def __init__(self, arg, **kwargs):
		if isinstance(arg, str):
			arg = (arg,)
		super().__init__([arg_.lstrip('-') for arg_ in arg])
		self._options = kwargs


class TestArgparseArgument(unittest.TestCase):
	'''
	Tests for the ArgparseArgument.from_inspect class method
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.ArgparseArgument.from_inspect
		self.maxDiff = None
	
	def test_annotations_class_str(self):
		'''
		Testing ArgparseArgument.from_inspect with annotation for type str
		'''
		
		self.assertEqual(self.test_object('test', {}, {'test' : str}, ''), DummyArgparseArgument('test', type = str))

	def test_annotations_choices(self):
		'''
		Testing ArgparseArgument.from_inspect with annotation for choices
		'''
		
		self.assertEqual(self.test_object('test', {}, {'test' : ('b', 3, False)}, ''), DummyArgparseArgument('test', choices = ('b', 3, False)))

	def test_default_none(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: None
		'''
		
		self.assertEqual(self.test_object('test', {'default' : None}, {}, ''), DummyArgparseArgument('test', default = argparse.SUPPRESS))

	def test_default_int(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: int
		'''

		self.assertEqual(self.test_object('test', {'default' : 3}, {}, ''), DummyArgparseArgument('test', default = 3, type = int))

	def test_default_float(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: float
		'''

		self.assertEqual(self.test_object('test', {'default' : 2.5}, {}, ''), DummyArgparseArgument('test', default = 2.5, type = float))

	def test_default_str(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: str
		'''
		
		self.assertEqual(self.test_object('test', {'default' : 'd'}, {}, ''), DummyArgparseArgument('test', default = 'd'))
	
	def test_default_false(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: False
		'''
		
		self.assertEqual(self.test_object('test', {'default' : False}, {}, ''), DummyArgparseArgument('test', default = False, action = 'store_true'))
	
	def test_default_true(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: True
		'''
		
		self.assertEqual(self.test_object('test', {'default' : True}, {}, ''), DummyArgparseArgument('test', default = True, action = 'store_false'))

	def test_default_tuple(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: tuple
		'''
		
		self.assertEqual(self.test_object('test', {'default' : ('v1', 2)}, {}, ''), DummyArgparseArgument('test', default = ['v1', 2], action = 'extend', nargs = '+'))

	def test_default_tuple_w_nargs(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: tuple with nargs
		'''
		
		self.assertEqual(self.test_object('test', {'default' : ('v1', 2), 'nargs' : '*'}, {}, ''), DummyArgparseArgument('test', default = ['v1', 2], action = 'extend', nargs = '*'))

	def test_default_dict(self):
		'''
		Testing ArgparseArgument.from_inspect with defaults: dict
		'''
		
		self.assertEqual(self.test_object('test', {'default' : {'v1' : 1, 2 : 'V2'}}, {}, ''), DummyArgparseArgument('test', default = [], action = 'extend', nargs = '+', help = '(Use the key=value format for each entry)'))
