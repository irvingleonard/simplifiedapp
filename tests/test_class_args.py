#python
'''
Testing of argparse handling in simplifiedapp
'''

import unittest

import simplifiedapp

class TestClassArgs(unittest.TestCase):
	'''
	Tests for the class_args function using simplifiedapp content
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.class_args
		self.maxDiff = None


	def test_empty_class(self):
		'''
		Test class_args with an empty class
		'''
		
		class FixtureEmpty:
			pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (FixtureEmpty, (), None, (), None),
			},

		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmpty))

	def test_empty_init(self):
		'''
		Test class_args with simplest __init__ signature
		'''
		
		class FixtureEmptyInit:
			def __init__(self):
				pass

		expected_result = {
			None	: {},
			False: {
				'__simplifiedapp_': (FixtureEmptyInit, (), None, (), None),
			},

		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyInit))

	def test_call(self):
		'''
		Test class_args with simplest __call__ signature
		'''
		
		class FixtureEmptyCall:
			def __call__(self):
				pass

		expected_result = {
			None	: {},
			False	: {'__simplifiedapp_': (FixtureEmptyCall, (), None, (), None)},
			True	: ({'title': 'FixtureEmptyCall methods'}, {
				'__call__': (([], {}), {
					None	: {},
					False	: {'__simplifiedapp_': ((FixtureEmptyCall, (), None, (), None), ('__call__', (), None, (), None))}
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyCall))
	
	def test_positionals_method(self):
		'''
		Test class_args with a method accepting positional arguments
		'''
		
		class FixturePositionalMethod:
			def a_method(self, a, b, c):
				pass

		expected_result = {
			None	: {},
			False	: {'__simplifiedapp_': (FixturePositionalMethod, (), None, (), None)},
			True	: ({'title': 'FixturePositionalMethod methods'}, {
				'a_method': (([], {}), {
					None	: {},
					False	: {'__simplifiedapp_': ((FixturePositionalMethod, (), None, (), None), ('a_method', ('a', 'b', 'c'), None, (), None))},
					'a'		: {},
					'b'		: {},
					'c'		: {},
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(FixturePositionalMethod))

	def test_positionals_method_w_defaults(self):
		'''
		Test class_args with a method accepting positional arguments with default values
		'''
		
		class FixturePositionalMethodwDefaults:
			def a_method(self, a = 'a', number = 2, list_ = ['c']):
				pass

		expected_result = {
			None	: {},
			False	: {'__simplifiedapp_': (FixturePositionalMethodwDefaults, (), None, (), None)},
			True	: ({'title': 'FixturePositionalMethodwDefaults methods'}, {
				'a_method': (([], {}), {
					None		: {},
					False		: {'__simplifiedapp_': ((FixturePositionalMethodwDefaults, (), None, (), None), ('a_method', ('a', 'number', 'list_'), None, (), None))},
					'-a'		: {'default': 'a'},
					'--number'	: {'default': 2, 'type': int},
					'--list_'	: {'action': 'extend', 'default': [], 'nargs': '+'},
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(FixturePositionalMethodwDefaults))

	def test_keywords_method(self):
		'''
		Test class_args with a method accepting keyword arguments
		'''
		
		class FixtureKeywordsMethod:
			def a_method(self, *args, a = 'a', number = 2, list_ = ['c']):
				pass

		expected_result = {
			None	: {},
			False	: {'__simplifiedapp_': (FixtureKeywordsMethod, (), None, (), None)},
			True	: ({'title': 'FixtureKeywordsMethod methods'}, {
				'a_method': (([], {}), {
					None		: {},
					False		: {'__simplifiedapp_': ((FixtureKeywordsMethod, (), None, (), None), ('a_method', (), 'args', ('a', 'number', 'list_'), None))},
					'args'		: {'action': 'extend', 'default': [], 'nargs': '*'},
					'-a'		: {'default': 'a'},
					'--number'	: {'default': 2, 'type': int},
					'--list_'	: {'action': 'extend', 'default': [], 'nargs': '+'},
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(FixtureKeywordsMethod))

	def test_version(self):
		'''
		Test class_args with versioned class (because "reasons")
		'''
		
		class FixtureEmptyCall:
			__version__ = '0.1'

		expected_result = {
			None		: {},
			False		: {'__simplifiedapp_': (FixtureEmptyCall, (), None, (), None)},
			'--version'	: {'action': 'version', 'version': '0.1'},
		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyCall))
