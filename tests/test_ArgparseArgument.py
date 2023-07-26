#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp


class DummyArgparseArgument(frozenset):
	def __new__(cls, arg, **kwargs):
		if isinstance(arg, str):
			arg = (arg,)
		return frozenset.__new__(cls, [arg_.lstrip('-') for arg_ in arg])
	def __init__(self, arg, **kwargs):
		self._options = kwargs


class TestArgparseArgument(unittest.TestCase):
	'''
	Tests for the ArgparseArgument class method
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.ArgparseArgument
		self.maxDiff = None

	def test_init_w_names_string(self):
		'''
		Test ArgparseArgument.__init__ with names as a string
		'''

		self.assertEqual(frozenset(self.test_object('test')), {'test'})

	def test_init_w_names_iterable(self):
		'''
		Test ArgparseArgument.__init__ with names as an iterable
		'''

		self.assertEqual(frozenset(self.test_object(('test', 'another', 'one'))), {'test', 'another', 'one'})

	def test_eq_w_simple_name(self):
		'''
		Test ArgparseArgument.__eq__ with simple name
		'''

		self.assertEqual(self.test_object('test'), DummyArgparseArgument('test'))

	def test_eq_w_multiple_names(self):
		'''
		Test ArgparseArgument.__eq__ with multiple names
		'''

		self.assertEqual(self.test_object(('test', 'another', 'one')), DummyArgparseArgument(('test', 'another', 'one')))

	def test_eq_w_different_simple_names(self):
		'''
		Test ArgparseArgument.__eq__ with different simple names
		'''

		self.assertFalse(self.test_object('test').__eq__(DummyArgparseArgument('no_test')))

	def test_eq_w_different_multiple_names(self):
		'''
		Test ArgparseArgument.__eq__ with different multiple names
		'''

		self.assertFalse(self.test_object(('test', 'another', 'one')).__eq__(DummyArgparseArgument(('test', 'one', 'two'))))

	def test_ne__w_simple_name(self):
		'''
		Test ArgparseArgument.__ne__ with simple name
		'''

		self.assertFalse(self.test_object('test').__ne__(DummyArgparseArgument('test')))

	def test_ne_w_multiple_names(self):
		'''
		Test ArgparseArgument.__ne__ with multiple names
		'''

		self.assertFalse(self.test_object(('test', 'another', 'one')).__ne__(DummyArgparseArgument(('test', 'another', 'one'))))

	def test_ne_w_different_simple_names(self):
		'''
		Test ArgparseArgument.__ne__ with different simple names
		'''

		self.assertNotEqual(self.test_object('test'), DummyArgparseArgument('no_test'))

	def test_ne_w_different_multiple_names(self):
		'''
		Test ArgparseArgument.__ne__ with different multiple names
		'''

		self.assertNotEqual(self.test_object(('test', 'another', 'one')), DummyArgparseArgument(('test', 'one', 'two')))

	def test_names_short(self):
		'''
		Test ArgparseArgument.names with short name
		'''

		self.assertEqual(frozenset(self.test_object('T').names()), {'-T'})

	def test_names_long(self):
		'''
		Test ArgparseArgument.names with long name
		'''

		self.assertEqual(frozenset(self.test_object(('test')).names()), {'--test'})

	def test_names_multiple(self):
		'''
		Test ArgparseArgument.names with multiple names
		'''

		self.assertEqual(frozenset(self.test_object(('t', 'test', 'O', 'Original', 'FINAL')).names()), {'-t', '--test', '-O', '--Original', '--FINAL'})

	def test_length_default(self):
		'''
		Test ArgparseArgument.length with default value
		'''

		self.assertEqual(self.test_object('test').length(), 2)

	def test_length_integer(self):
		'''
		Test ArgparseArgument.length with integer value
		'''

		self.assertEqual(self.test_object('test', nargs = 3).length(), 4)

	def test_length_variable(self):
		'''
		Test ArgparseArgument.length with variable value
		'''

		self.assertRaises(ValueError, self.test_object('test', nargs = '*').length)

	def test_length_action_store_const(self):
		'''
		Test ArgparseArgument.length with action = store_const
		'''

		self.assertEqual(self.test_object('test', action = 'store_const').length(), 1)

	def test_length_action_store_true(self):
		'''
		Test ArgparseArgument.length with action = store_true
		'''

		self.assertEqual(self.test_object('test', action = 'store_true').length(), 1)

	def test_length_action_append_const(self):
		'''
		Test ArgparseArgument.length with action = append_const
		'''

		self.assertEqual(self.test_object('test', action = 'append_const').length(), 1)

	def test_length_action_count(self):
		'''
		Test ArgparseArgument.length with action = count
		'''

		self.assertEqual(self.test_object('test', action = 'count').length(), 1)

	def test_length_action_count(self):
		'''
		Test ArgparseArgument.length with action = count
		'''

		self.assertEqual(self.test_object('test', action = 'count').length(), 1)

	def test_length_action_help(self):
		'''
		Test ArgparseArgument.length with action = help
		'''

		self.assertEqual(self.test_object('test', action = 'help').length(), 1)

	def test_length_action_version(self):
		'''
		Test ArgparseArgument.length with action = version
		'''

		self.assertEqual(self.test_object('test', action = 'version').length(), 1)
