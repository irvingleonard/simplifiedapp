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
				'__simplifiedapp_': (FixtureEmpty, None, None, (), ()),
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
				'__simplifiedapp_': (FixtureEmptyInit, None, None, (), ()),
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
			False	: {'__simplifiedapp_': (FixtureEmptyCall, None, None, (), ())},
			True	: ({'title': 'FixtureEmptyCall methods'}, {
				'__call__': (([], {}), {
					None	: {},
					False	: {'__simplifiedapp_': ((FixtureEmptyCall, None, None, (), ()), ('__call__', None, None, (), ()))}
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyCall))
	
	def test_version(self):
		'''
		Test class_args with versioned class (because "reasons")
		'''
		
		class FixtureEmptyCall:
			__version__ = '0.1'

		expected_result = {
			None		: {},
			False		: {'__simplifiedapp_': (FixtureEmptyCall, None, None, (), ())},
			'--version'	: {'action': 'version', 'version': '0.1'},
		}
		self.assertDictEqual(expected_result, self.test_object(FixtureEmptyCall))
