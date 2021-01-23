#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import unittest

import simplifiedapp
import tests.common

class TestPopulation(unittest.TestCase, tests.common.TestCase):
	'''
	Tests for the _populate_argparse_parser function
	'''
	
	def test_set_defaults(self):
		'''
		Test argparser set_defaults
		'''
		
		fixture = {'something' : 'useless'}
		result = simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(), {False: fixture})
		self.assertArgparseParse(result, fixture)
	
	def test_simple_argument(self):
		'''
		Test argparser simple argument
		'''
		
		fixture = {'foo' : {'default' : 'initial value', 'help' : 'this will foo'}}
		result = simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter), fixture)
		result_pattern  = '.*^\s*positional arguments:\s*^\s*foo\s+this\s+will\s+foo\s*$.*'
		self.assertArgparseHelpRegex(result, result_pattern)
	
	def test_empty_subparser(self):
		'''
		Test argparser with empty subparser
		'''
		
		fixture = {True : ({'help' : 'Possible actions'}, {})}
		result = simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter), fixture)
		result_pattern  = '.*^\s*positional arguments:\s*^\s*\{}\s+Possible\s+actions\s*$.*'
		self.assertArgparseHelpRegex(result, result_pattern)
	
	def test_a_subparser(self):
		'''
		Test argparser with a subparser
		'''
		
		fixture = {True : ({'help' : 'Possible actions'}, {'foo' : ({'help' : 'fooing this!'}, {})})}
		result = simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter), fixture)
		result_pattern  = '.*^\s*positional arguments:\s*^\s*\{foo}\s+Possible\s+actions\s*^\s*foo\s+fooing\s+this!\s*$.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		
	def test_wrong_dict_key(self):
		'''
		Testing argparser with a wrong dict key
		'''
		
		with self.assertRaises(ValueError):
			simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(), {4 : 'wrong', 5 : {'key' : 'still wrong'}})
			
	def test_wrong_dict_value(self):
		'''
		Testing argparser argument with wrong value
		'''
		
		with self.assertRaises(ValueError):
			simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(), { 'wrong' : 'very'})
			
	def test_wrong_subparser_structure(self):
		'''
		Testing argparser subparser with wrong structure
		'''
		
		with self.assertRaises(ValueError):
			simplifiedapp._populate_argparse_parser(argparse.ArgumentParser(), {True : 'wrong, very'})


class TestBuild(unittest.TestCase, tests.common.TestCase):
	'''
	Tests for the build_argparse_parser function
	'''
	
	maxDiff = None
	
	def setUp(self):
		self.metadata = simplifiedapp.setuptools_get_metadata(simplifiedapp)
	
	def test_description(self):
		'''
		Testing the addition of the description to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*{description}\s*$.*'.format(description = self.metadata['description'])
		self.assertArgparseHelpRegex(result, result_pattern)
		
	def test_epilog(self):
		'''
		Testing the addition of the epilog to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*{epilog}\s*$.*'.format(epilog = self.metadata['long_description'])
		self.assertArgparseHelpRegex(result, result_pattern)
	
	def test_version_switch_addition(self):
		'''
		Testing the addition of the --version switch to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*--version\s+.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		
# 	def test_version_switch(self):
# 		'''
# 		Testing the --version switch
# 		'''
# 		
# 		#This won't work. The --version switch/action is hardcoded to output directly to stdout
# 		result = simplifiedapp.build_argparse_parser(simplifiedapp).parse_args(['--version'])
# 		self.assertEqual(result['version'], self.metadata['version'])
		
	def test_default_options_log_level(self):
		'''
		Testing the addition of the log-level (a default option) switch to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*--log-level\s+\{notset,debug,info,warning,error,critical}\s+.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		
	def test_default_options_log_to_syslog(self):
		'''
		Testing the addition of the log-to-syslog (a default option) switch to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*--log-to-syslog\s+.*'
		self.assertArgparseHelpRegex(result, result_pattern)
	
	def test_default_options_input_file(self):
		'''
		Testing the addition of the input_file (a default option) switch to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*--input-file\s+.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		
	def test_default_options_json(self):
		'''
		Testing the addition of the json (a default option) switch to the parser
		'''
		
		result = simplifiedapp.build_argparse_parser(simplifiedapp)
		result_pattern  = '.*^\s*--json\s+.*'
		self.assertArgparseHelpRegex(result, result_pattern)
	
	def test_as_subparser(self):
		'''
		Testing the build as a subparser
		'''
		
		result = argparse.ArgumentParser()
		simplifiedapp.build_argparse_parser(simplifiedapp, parent_parser = result.add_subparsers(help='possible subparsers').add_parser('test-subparser'))
		result_pattern  = '.*^\s*positional\s+arguments:\s+^\s*\{test-subparser}\s+possible\s+subparsers\s*$.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		
	def test_providing_content(self):
		'''
		Testing the build by feeding it content (not just the defaults)
		'''
		
		fixture = {
			'test-param'			: {'help' : 'positional test parameter'},
			'--test-optional-param'	: {'help' : 'optional test parameter'},
		}
		result = simplifiedapp.build_argparse_parser(simplifiedapp, parser_content= fixture)
		result_pattern  = '.*^\s*positional arguments:\s*^\s*test-param\s+positional\s+test\s+parameter\s*$.*^\s*--test-optional-param\s+TEST_OPTIONAL_PARAM\s*^\s*optional\s+test\s+parameter\s+\(default:\s+None\)\s*$.*'
		self.assertArgparseHelpRegex(result, result_pattern)
		