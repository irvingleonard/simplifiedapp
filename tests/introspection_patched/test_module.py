#! python
"""Testing the execution of the introspection_patched module itself (the patches applied when it's executed)"""

from importlib.util import module_from_spec, spec_from_file_location
from sys import modules
from unittest import TestCase
from unittest.mock import patch

from introspection import mark as introspection_mark

from fixtures.introspection_patched import fixture_documented_function
from simplifiedapp import introspection_patched
from simplifiedapp.introspection_patched import Signature


class TestModuleExecution(TestCase):
	"""Tests for executing the module again (like a reload would do)"""

	PATCHED_SIGNATURE_ATTRIBUTES = ('variable_positional_parameter', 'variable_keyword_parameter', 'from_callable', 'supplying_method', '_from_class_default', 'from_class')

	def setUp(self):
		"""Save the patched upstream attributes, since executing the module again replaces them"""

		self.signature_attributes = {name: vars(Signature)[name] for name in self.PATCHED_SIGNATURE_ATTRIBUTES}
		self.has_mark = introspection_mark.has_mark

	def tearDown(self):
		"""Restore the patched upstream attributes from the original execution of the module"""

		for name, value in self.signature_attributes.items():
			setattr(Signature, name, value)
		introspection_mark.has_mark = self.has_mark

	def execute_module(self):
		"""Execute the module from its file, as a new module

		:returns module: the new module
		"""

		spec = spec_from_file_location('simplifiedapp.introspection_patched_executed_again', introspection_patched.__file__)
		module = module_from_spec(spec)
		spec.loader.exec_module(module)
		return module

	def test_wo_docstring_parser(self):
		"""Test executing the module without the optional "docstring_parser" module"""

		with patch.dict(modules, {'docstring_parser': None}):
			module = self.execute_module()
		self.assertIsNone(module.docstring_parse)
		expected_result = {'name': 'fixture_documented_function', 'version': '0.1.3.dev1'}
		self.assertDictEqual(expected_result, module.object_metadata(fixture_documented_function))

	def test_upstream_from_callable_kept(self):
		"""Test executing the module again keeps the upstream "from_callable" (instead of the patched one, which would then call itself)"""

		upstream_from_callable = Signature._from_callable_original
		self.execute_module()
		self.assertIs(upstream_from_callable, Signature._from_callable_original)
		self.assertEqual('(self, /, *args, **kwargs)', str(Signature.from_callable(object.__init__)))
		self.assertEqual('(a, b=1)', str(Signature.from_callable(lambda a, b=1: None)))
