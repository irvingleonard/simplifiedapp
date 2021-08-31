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
					'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
					'args': {'action': 'extend', 'default': [], 'nargs': '*'},
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
							'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
							'args': {'action': 'extend', 'default': [], 'nargs': '*'},
							}),
						}),
					'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
					'args': {'action': 'extend', 'default': [], 'nargs': '*'}
					}),
				}),
		}
		self.assertDictEqual(expected_result, self.test_object(fixture_module_w_class))

	def test_module_w_builtin(self):
		'''
		Test with builtin module (venv)
		'''
		
		import venv

		expected_result = {
			None	: {
				'description'	: '\nVirtual environment (venv) package for Python. Based on PEP 405.',
				'epilog'		: '\nopyright (C) 2011-2014 Vinay Sajip.\nicensed to the PSF under a contributor agreement.'
				},
			True: ({'title': 'venv callables'}, {
				'create': (([], {}), {
					None						: {'description' : 'Create a virtual environment in a directory.', 'epilog' : None},
					False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
					'--clear'					: {'action' : 'store_true', 'default' : False},
					'--prompt'					: {'default' : argparse.SUPPRESS},
					'--symlinks'				: {'action' : 'store_true', 'default' : False},
					'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
					'--upgrade_deps'			: {'action' : 'store_true', 'default' : False},
					'--with_pip'				: {'action' : 'store_true', 'default' : False},
					'env_dir'					: {}
				}),
				'main': (([], {}), {
					None		: {},
					False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
					'--args'	: {'default': argparse.SUPPRESS}
				})
			})
		}

		self.assertDictEqual(expected_result, self.test_object(venv))

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
