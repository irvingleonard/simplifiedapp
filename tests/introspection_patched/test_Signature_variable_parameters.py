#! python
"""Testing the introspection_patched Signature.variable_positional_parameter and Signature.variable_keyword_parameter properties"""

from unittest import TestCase

from introspection.parameter import ParameterKind

from fixtures.introspection_patched import fixture_function, fixture_function_wo_variable_parameters
from simplifiedapp.introspection_patched import Signature


class TestSignatureVariablePositionalParameter(TestCase):
	"""Tests for the Signature.variable_positional_parameter property"""

	def test_w_variable_positional_parameter(self):
		"""Test "Signature.variable_positional_parameter" with a signature that has one"""

		parameter = Signature.from_callable(fixture_function).variable_positional_parameter
		self.assertEqual(('args', ParameterKind.VAR_POSITIONAL), (parameter.name, parameter.kind))

	def test_wo_variable_positional_parameter(self):
		"""Test "Signature.variable_positional_parameter" with a signature that doesn't have one"""

		self.assertIsNone(Signature.from_callable(fixture_function_wo_variable_parameters).variable_positional_parameter)


class TestSignatureVariableKeywordParameter(TestCase):
	"""Tests for the Signature.variable_keyword_parameter property"""

	def test_w_variable_keyword_parameter(self):
		"""Test "Signature.variable_keyword_parameter" with a signature that has one"""

		parameter = Signature.from_callable(fixture_function).variable_keyword_parameter
		self.assertEqual(('kwargs', ParameterKind.VAR_KEYWORD), (parameter.name, parameter.kind))

	def test_wo_variable_keyword_parameter(self):
		"""Test "Signature.variable_keyword_parameter" with a signature that doesn't have one"""

		self.assertIsNone(Signature.from_callable(fixture_function_wo_variable_parameters).variable_keyword_parameter)
