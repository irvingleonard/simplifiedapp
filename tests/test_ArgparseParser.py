#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp


class DummyArgparseParser(set):
	def __init__(self, *args, defaults = None, **kwargs):
		super().__init__(args)
		self.options = simplifiedapp.ArgparseParser.DEFAULT_OPTIONS.copy()
		self.options.update(kwargs)
		self.defaults = {} if defaults is None else defaults


class TestArgparseParser(unittest.TestCase):
	'''
	Tests for the ArgparseParser class method
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.ArgparseParser
		self.maxDiff = None

		self.fixture_arguments = [
			simplifiedapp.ArgparseArgument('t'),
			simplifiedapp.ArgparseArgument('another'),
			simplifiedapp.ArgparseArgument('Test'),
			simplifiedapp.ArgparseArgument('THE_ONE'),
			simplifiedapp.ArgparseArgument('zlastone'),
		]
		self.fixture_defaults = {'a' : 13, 'ci' : 'txt'}
		self.fixture_options = {'prog' : 'test', 'description' : 'Test Description', 'epilog' : 'Test Epilog'}

		self.fixture_ne_arguments = [
			simplifiedapp.ArgparseArgument('s'),
			simplifiedapp.ArgparseArgument('one'),
			simplifiedapp.ArgparseArgument('Tist'),
			simplifiedapp.ArgparseArgument('THE_TWO'),
			simplifiedapp.ArgparseArgument('z_lastone'),
		]
		self.fixture_ne_defaults = {'a' : 14, 'cd' : 'exe'}
		self.fixture_ne_options = {'prog' : 'testit', 'description' : 'Test_Description', 'epilog' : 'Test_Epilog'}

	def test_init_empty(self):
		'''
		Test ArgparseParser.__init__ without parameters
		'''

		self.assertEqual(self.test_object(), DummyArgparseParser())

	def test_init_w_argument(self):
		'''
		Test ArgparseParser.__init__ with argument
		'''

		fixture_argument = simplifiedapp.ArgparseArgument('t')
		self.assertEqual(self.test_object(fixture_argument), DummyArgparseParser(fixture_argument))

	def test_init_w_arguments(self):
		'''
		Test ArgparseParser.__init__ with arguments
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_arguments))

	def test_init_w_defaults(self):
		'''
		Test ArgparseParser.__init__ with defaults
		'''

		self.assertEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_defaults))

	def test_init_w_details(self):
		'''
		Test ArgparseParser.__init__ with details
		'''

		self.assertEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_options))

	def test_contains_w_argument(self):
		'''
		Test ArgparseParser.__contains__ with an ArgparseArgument
		'''

		fixture_argument = simplifiedapp.ArgparseArgument('t')
		self.assertTrue(fixture_argument in self.test_object(fixture_argument))

	def test_contains_w_string(self):
		'''
		Test ArgparseParser.__contains__ with a string
		'''

		self.assertTrue('t' in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def test_contains_w_missing_argument(self):
		'''
		Test ArgparseParser.__contains__ with a missing ArgparseArgument
		'''

		self.assertFalse(simplifiedapp.ArgparseArgument('m') in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def test_contains_w_missing_string(self):
		'''
		Test ArgparseParser.__contains__ with a missing string
		'''

		self.assertFalse('m' in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def test_contains_w_string_complex(self):
		'''
		Test ArgparseParser.__contains__ with a string in a complex argument
		'''

		self.assertTrue('zlastone' in self.test_object(simplifiedapp.ArgparseArgument(('t', 'Test', 'zlastone'))))

	def test_contains_w_string_multiple(self):
		'''
		Test ArgparseParser.__contains__ with a string in multiple arguments
		'''

		self.assertTrue('zlastone' in self.test_object(*self.fixture_arguments))

	def test_eq_default(self):
		'''
		Test ArgparseParser.__eq__ with default instance
		'''

		self.assertEqual(self.test_object(), DummyArgparseParser())

	def test_eq_w_content(self):
		'''
		Test ArgparseParser.__eq__ with content
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_arguments))

	def test_eq_w_defaults(self):
		'''
		Test ArgparseParser.__eq__ with provided defaults
		'''

		self.assertEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_defaults))

	def test_eq_w_options(self):
		'''
		Test ArgparseParser.__eq__ with provided options
		'''

		self.assertEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_options))

	def test_eq_complex(self):
		'''
		Test ArgparseParser.__eq__ with everything (complex)
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options), DummyArgparseParser(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options))

	def test_ne_w_content(self):
		'''
		Test ArgparseParser.__ne__ with content
		'''

		self.assertNotEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_ne_arguments))

	def test_ne_w_defaults(self):
		'''
		Test ArgparseParser.__ne__ with provided defaults
		'''

		self.assertNotEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_ne_defaults))

	def test_ne_w_options(self):
		'''
		Test ArgparseParser.__ne__ with provided options
		'''

		self.assertNotEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_ne_options))

	def test_ne_complex(self):
		'''
		Test ArgparseParser.__ne__ with everything (complex)
		'''

		self.assertNotEqual(self.test_object(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options), DummyArgparseParser(*self.fixture_ne_arguments, defaults = self.fixture_ne_defaults, **self.fixture_ne_options))
