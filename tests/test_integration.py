#! python
'''Integration testing for simplifiedapp
Run some integration tests.
'''

import pathlib
import unittest

import simplifiedapp
import tests.common

THIS_FILE = pathlib.Path(__file__).resolve(strict = True)

class TestTests(unittest.TestCase, tests.common.TestCase):
	
	def test_assertExplore(self):
		'''
		Testing for the availability of assert explore
		'''
		
		#This is a tool for test development. This have 0 impact in the module code
		self.assertExplore('')

class TestInput(unittest.TestCase):
	
	def __getattr__(self, name):
		if name == 'fixtures_path':
			value = THIS_FILE.parent / 'fixtures'
			self.__setattr__(name, value)
			return value
		else:
			raise AttributeError(name)
	
	def setUp(self):
	
		self._conf_input = simplifiedapp.ConfFile(self.fixtures_path / 'test.ini')
		self._json_input = simplifiedapp.JSONFile(self.fixtures_path / 'test.json')
		
	def test_input_merging(self):
		'''
		Test the | operator on inputs
		'''
		
		merge_result = {
			'also here' : 'from a regular dict',
			'Country': 'United Kingdom',
			'House': 'House of Wessex',
			'ID': 5,
			'Name': 'Edwy',
			'Reign': '955-959',
			'SOME_SECTION': {
				'bored': 'of making stuff up',
				'morrrr': 'settings here they go',
				'something': 'else',
				'sure': 'not',
				'this': 'is important',
			},
			'this': 'is important',
		}
		
		self.assertEqual({'also here' : 'from a regular dict'} | self._conf_input | self._json_input, merge_result)
		
# 	def test

# def main(*args, i_need_this = None, a_boolean_switch = False, **kwargs): #The i_need_this parameter (or any parameter for that matter) can't be a positional argument or else it won't work. Your function MUST accept **kwargs (and it's a good idea to accept *args too)
# 	return kwargs
# 
# _ARGPARSE_OPTIONS = { #There's a documentation subsection for this data structure.
# 		'i-need-this'			: {'help' : 'This piece of information is required'},
# 		'--this-would-be-nice'	: {'default' : argparse.SUPPRESS, 'help' : 'It would be nice to have this. If not provided, there will be no attribute for it in the resulting argparser (because of the default)'},
# 		'--a-boolean-switch'	: {'action' : 'store_true', 'default' : False, 'help' : 'To be or not to be.'},
# 		False	: {'_func' : main} #This references your main function
# 	}
