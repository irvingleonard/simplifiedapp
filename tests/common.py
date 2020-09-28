#python
'''Testing of I/O classes in simplifiedapp
These are the classes that convert from specific formats to python dict and back
'''

import pathlib

import simplifiedapp

THIS_FILE = pathlib.Path(__file__).resolve(strict = True)

class TestCase():
	'''Enhanced unittest.TestCase
	This class adds specific modules functionality to the standard unittest.TestCase class.
	'''
	
	def assertExplore(self, result):
		self.maxDiff = None
		self.assertEqual(result, '', msg = 'Exploratory error')
	
	def assertArgparseParse(self, parser, fixture, args = None, msg = None):
		self.assertEqual(vars(parser.parse_args({} if args is None else args)), fixture, msg = msg)
		
	def assertArgparseHelpRegex(self, parser, regex, msg = None):
		self.assertRegex(parser.format_help(), '(?msi:{regex})'.format(regex = regex), msg = msg)

