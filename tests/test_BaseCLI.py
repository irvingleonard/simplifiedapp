#python
'''
Testing of argparse handling in simplifiedapp
'''

import pathlib
import unittest

import simplifiedapp
import tests.common

THIS_FILE = pathlib.Path(__file__).resolve(strict = True)

FIXTURE_BUILTIN_ARGPARSE_OPTIONS = {
	'json': False,
	'log_level': 'info',
	'log_to_syslog': False,
}

class BaseCLI(simplifiedapp.BaseCLI):
	pass

class TestBaseCLI(unittest.TestCase, tests.common.TestCase):
	'''
	Tests for the BaseCLI class
	'''
	
	def test_build_argparser_no_options(self):
		'''
		Testing basic argparser creation (without any options)
		'''
		
		fixture = {
			'_class': simplifiedapp.BaseCLI,
		}
		fixture.update(FIXTURE_BUILTIN_ARGPARSE_OPTIONS)
		result = simplifiedapp.BaseCLI._build_argparser()
		self.assertArgparseParse(result, fixture)