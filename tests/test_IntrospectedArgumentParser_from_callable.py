#python
'''
Testing of argparse handling in simplifiedapp
'''

from unittest import TestCase

from simplifiedapp import IntrospectedArgumentParser, LocalFormatterClass

class TestIntrospectedArgumentParserFromCallable(TestCase):
	'''
	Tests for the IntrospectedArgumentParser.from_callable class method
	'''
	
	def setUp(self):
		self.test_object = IntrospectedArgumentParser.from_callable

	def test_empty_callable(self):
		'''
		Test IntrospectedArgumentParser.from_callable with simplest function signature
		'''

		def fixture_empty_function():
			pass

		expected_result = IntrospectedArgumentParser(prog='fixture_empty_function', formatter_class=LocalFormatterClass)
		self.assertEqual(expected_result, self.test_object(fixture_empty_function))

	def test_w_versioned_callable(self):
		'''
		Test IntrospectedArgumentParser.from_callable with a versioned function
		'''

		def fixture_empty_function():
			pass
		fixture_empty_function.__version__ = '0.1'

		expected_result = IntrospectedArgumentParser(prog='fixture_empty_function', formatter_class=LocalFormatterClass)
		expected_result.add_argument('--fixture-empty-function-version', action='version', version='0.1')
		self.assertEqual(expected_result, self.test_object(fixture_empty_function))

	def _test_init_w_arguments(self):
		'''
		Test ArgparseParser.__init__ with arguments
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_arguments))

	def _test_init_w_defaults(self):
		'''
		Test ArgparseParser.__init__ with defaults
		'''

		self.assertEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_defaults))

	def _test_init_w_details(self):
		'''
		Test ArgparseParser.__init__ with details
		'''

		self.assertEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_options))

	def _test_contains_w_argument(self):
		'''
		Test ArgparseParser.__contains__ with an ArgparseArgument
		'''

		fixture_argument = simplifiedapp.ArgparseArgument('t')
		self.assertTrue(fixture_argument in self.test_object(fixture_argument))

	def _test_contains_w_string(self):
		'''
		Test ArgparseParser.__contains__ with a string
		'''

		self.assertTrue('t' in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def _test_contains_w_missing_argument(self):
		'''
		Test ArgparseParser.__contains__ with a missing ArgparseArgument
		'''

		self.assertFalse(simplifiedapp.ArgparseArgument('m') in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def _test_contains_w_missing_string(self):
		'''
		Test ArgparseParser.__contains__ with a missing string
		'''

		self.assertFalse('m' in self.test_object(simplifiedapp.ArgparseArgument('t')))

	def _test_contains_w_string_complex(self):
		'''
		Test ArgparseParser.__contains__ with a string in a complex argument
		'''

		self.assertTrue('zlastone' in self.test_object(simplifiedapp.ArgparseArgument(('t', 'Test', 'zlastone'))))

	def _test_contains_w_string_multiple(self):
		'''
		Test ArgparseParser.__contains__ with a string in multiple arguments
		'''

		self.assertTrue('zlastone' in self.test_object(*self.fixture_arguments))

	def _test_eq_default(self):
		'''
		Test ArgparseParser.__eq__ with default instance
		'''

		self.assertEqual(self.test_object(), DummyArgparseParser())

	def _test_eq_w_content(self):
		'''
		Test ArgparseParser.__eq__ with content
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_arguments))

	def _test_eq_w_defaults(self):
		'''
		Test ArgparseParser.__eq__ with provided defaults
		'''

		self.assertEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_defaults))

	def _test_eq_w_options(self):
		'''
		Test ArgparseParser.__eq__ with provided options
		'''

		self.assertEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_options))

	def _test_eq_complex(self):
		'''
		Test ArgparseParser.__eq__ with everything (complex)
		'''

		self.assertEqual(self.test_object(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options), DummyArgparseParser(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options))

	def _test_ne_w_content(self):
		'''
		Test ArgparseParser.__ne__ with content
		'''

		self.assertNotEqual(self.test_object(*self.fixture_arguments), DummyArgparseParser(*self.fixture_ne_arguments))

	def _test_ne_w_defaults(self):
		'''
		Test ArgparseParser.__ne__ with provided defaults
		'''

		self.assertNotEqual(self.test_object(defaults = self.fixture_defaults), DummyArgparseParser(defaults = self.fixture_ne_defaults))

	def _test_ne_w_options(self):
		'''
		Test ArgparseParser.__ne__ with provided options
		'''

		self.assertNotEqual(self.test_object(**self.fixture_options), DummyArgparseParser(**self.fixture_ne_options))

	def _test_ne_complex(self):
		'''
		Test ArgparseParser.__ne__ with everything (complex)
		'''

		self.assertNotEqual(self.test_object(*self.fixture_arguments, defaults = self.fixture_defaults, **self.fixture_options), DummyArgparseParser(*self.fixture_ne_arguments, defaults = self.fixture_ne_defaults, **self.fixture_ne_options))
