#python
'''
Testing of argparse handling in simplifiedapp
'''

import argparse
import pathlib
import sys
import unittest

import simplifiedapp


class TestModuleArgs(unittest.TestCase):
	'''
	Tests for the module_args function
	'''
	
	def setUp(self):
		self.test_object = simplifiedapp.module_args
		self.maxDiff = None
		sys.path.append(str(pathlib.Path( __file__ ).parent / 'fixtures'))

	def test_empty_module(self):
		'''
		Test empty module
		'''
		
		import fixture_empty_module

		expected_result = {None : {}}
		self.assertDictEqual(expected_result, self.test_object(fixture_empty_module))

	def test_module_w_callable(self):
		'''
		Test module including a callable
		'''
		
		import fixture_module_w_callable

		expected_result = {
			None	: {},
			True	: ({'title': 'fixture_module_w_callable callables'}, {
				'test_callable': (([], {}), {
					None: {},
					False: {'__simplifiedapp_': (fixture_module_w_callable.test_callable, (), 'args', (), 'kwargs')},
					'--kwargs': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
					'args': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '*'},
				}),
			}),
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_module_w_callable))

	def test_module_w_private_callable(self):
		'''
		Test module including a private callable
		'''
		
		import fixture_module_w_private_callable

		
		self.assertDictEqual({None : {}}, self.test_object(fixture_module_w_private_callable))

	def test_module_w_class(self):
		'''
		Test module including a class
		'''
		
		import fixture_module_w_class

		expected_result = {
			None	: {},
			True	: ({'title': 'fixture_module_w_class callables'}, {
				'TestClass': (([], {}), {
					None	: {},
					False	: {'__simplifiedapp_': (fixture_module_w_class.TestClass, (), 'args', (), 'kwargs')},
					True: ({'title': 'TestClass methods'}, {
						'test_method': (([], {}), {
							None	: {},
							False: {'__simplifiedapp_': ((fixture_module_w_class.TestClass, (), 'args', (), 'kwargs'), ('test_method', (), 'args', (), 'kwargs'))},
							'--kwargs': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
							'args': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '*'},
							}),
						}),
					'--kwargs': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
					'args': {'action': 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'default': [], 'nargs': '*'}
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_module_w_class))

	def test_module_w_builtin(self):
		'''
		Test with builtin module (venv)
		'''

		import fixture_builtins
		import venv

		self.assertDictEqual(fixture_builtins.module_args_venv(), self.test_object(venv))

	def test_version(self):
		'''
		Test with versioned module
		'''
		
		import fixture_versioned_module

		expected_result = {
			None	: {},
			'--version'	: {'action'	: 'version', 'version'	: '0.1'}
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_versioned_module))
