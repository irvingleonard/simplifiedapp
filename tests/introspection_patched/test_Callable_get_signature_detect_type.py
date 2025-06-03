#python
"""
Testing the introspection_patched.Callable._get_signature_detect_type method
"""

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import Callable, CallableType, Parameter, ParameterKind, Signature


class TestCallableGetSignatureDetectType(TestCase):
	"""
	Tests for the Callable._get_signature_detect_type method
	"""

	def test_w_function(self):
		"""
		Testing "Callable._get_signature_detect_type" with a function
		"""

		expected_parameters = [
			Parameter('pos_req', ParameterKind.POSITIONAL_ONLY),
			Parameter('pos_def_none', ParameterKind.POSITIONAL_ONLY, default=None),
			Parameter('pos_def_str', ParameterKind.POSITIONAL_ONLY, default='a_str'),
			Parameter('pos_def_bool', ParameterKind.POSITIONAL_ONLY, default=False),
			Parameter('pos_def_list', ParameterKind.POSITIONAL_OR_KEYWORD, default=['as', 1, True]),
			Parameter('pos_def_dict', ParameterKind.POSITIONAL_OR_KEYWORD, default={1: 'one', 'dct': 6, 'fer': False}),
			Parameter('pos_def_num', ParameterKind.POSITIONAL_OR_KEYWORD, default=2.3),
			Parameter('more_pos', ParameterKind.VAR_POSITIONAL),
			Parameter('kw_req', ParameterKind.KEYWORD_ONLY),
			Parameter('kw_def_none', ParameterKind.KEYWORD_ONLY, default=None),
			Parameter('kw_def_str', ParameterKind.KEYWORD_ONLY, default='another_str'),
			Parameter('kw_def_bool', ParameterKind.KEYWORD_ONLY, default=True),
			Parameter('kw_def_list', ParameterKind.KEYWORD_ONLY, default=[1, 'tre', 6.7]),
			Parameter('kw_def_dict', ParameterKind.KEYWORD_ONLY, default={1: 'dfe', 'yufgb': 'sdqwda'}),
			Parameter('kw_def_num', ParameterKind.KEYWORD_ONLY, default=(8 + 98j)),
			Parameter('more_kw', ParameterKind.VAR_KEYWORD),
		]
		expected_result = Signature(parameters=expected_parameters, forward_ref_context='fixtures.functions'), CallableType['FUNCTION']
		result = Callable(fixture_function_w_all_parameter_combinations)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])

	def test_w_inner_function(self):
		"""
		Testing "Callable._get_signature_detect_type" with a nested function
		"""

		expected_parameters = [
			Parameter('pos_req', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters, forward_ref_context='fixtures.functions'), CallableType['FUNCTION']
		result = Callable(fixture_nested_functions_outer())._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])
	
	def test_w_class(self):
		"""
		Testing "Callable._get_signature_detect_type" with a class
		"""

		expected_parameters = [
			Parameter('new_pos', ParameterKind.POSITIONAL_ONLY),
			Parameter('init_pos', ParameterKind.POSITIONAL_ONLY),
			Parameter('args', ParameterKind.VAR_POSITIONAL),
			Parameter('new_kw', ParameterKind.KEYWORD_ONLY),
			Parameter('init_kw', ParameterKind.KEYWORD_ONLY),
			Parameter('kwargs', ParameterKind.VAR_KEYWORD),
		]
		expected_result = Signature(parameters=expected_parameters, forward_ref_context='fixtures.classes'), CallableType['CLASS']
		result = Callable(FixtureClassWNewAndInitComplex)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])
	
	def test_w_static_method_from_class(self):
		"""
		Testing "Callable._get_signature_detect_type" with a static method from a class
		"""

		expected_parameters = [
			Parameter('pos_arg', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters), CallableType['STATIC_METHOD']
		result = Callable(FixtureClassWMethods.static_method)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])

	def test_w_class_method_from_class(self):
		"""
		Testing "Callable._get_signature_detect_type" with a class method from a class
		"""

		expected_parameters = [
			Parameter('pos_arg', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters), CallableType['CLASS_METHOD']
		result = Callable(FixtureClassWMethods.class_method)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])
	
	def test_class_w_instance_method_from_class(self):
		"""
		Testing "Callable._get_signature_detect_type" with an instance method from a class
		"""

		expected_parameters = [
			Parameter('pos_arg', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters), CallableType['INSTANCE_METHOD']
		result = Callable(FixtureClassWMethods.regular_method)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])
	
	def test_w_class_instance(self):
		"""
		Testing "Callable._get_signature_detect_type" with a class instance
		"""

		expected_parameters = [
			Parameter('args', ParameterKind.VAR_POSITIONAL),
			Parameter('kwargs', ParameterKind.VAR_KEYWORD),
		]
		expected_result = Signature(parameters=expected_parameters, forward_ref_context='fixtures.classes'), CallableType['INSTANCE']
		result = Callable(FixtureClassWMethods())._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])
	
	def test_class_w_bound_method_from_class_instance(self):
		"""
		Testing "Callable._get_signature_detect_type" with an bound method from a class instance
		"""

		expected_parameters = [
			Parameter('pos_arg', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters, forward_ref_context='fixtures.classes'), CallableType['BOUND_METHOD']
		result = Callable(FixtureClassWMethods().regular_method)._get_signature_detect_type()
		self.assertEqual(expected_parameters, result[0].parameter_list)
		self.assertEqual(expected_result[0], result[0])
		self.assertEqual(expected_result[1], result[1])

	def test_class_w_static_method_w_problematic_param(self):
		"""Testing "Callable._get_signature_detect_type" with a static method whose first parameter is called "self".
		The current code would misidentify it as a bound method, hence the "not equal" check. This is a test that proves that the current logic is faulty.
		"""

		expected_parameters = [
			Parameter('self', ParameterKind.POSITIONAL_ONLY),
			Parameter('second_argument', ParameterKind.POSITIONAL_ONLY),
		]
		expected_result = Signature(parameters=expected_parameters), CallableType['STATIC_METHOD']
		result = Callable(FixtureClassWMethods.problematic_static_method)._get_signature_detect_type()
		self.assertNotEqual(expected_parameters, result[0].parameter_list)
		self.assertNotEqual(expected_result[0], result[0])
		self.assertNotEqual(expected_result[1], result[1])