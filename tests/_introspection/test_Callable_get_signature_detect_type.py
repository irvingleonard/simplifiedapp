#python
'''
Testing the introspection_patched.Callable._get_signature_detect_type method
'''

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import IS_FUNCTION, IS_STATIC_METHOD, Callable, Signature

class TestCallableGetSignatureDetectType(TestCase):
	'''
	Tests for the Callable._get_signature_detect_type method
	'''

	def test_w_function(self):
		'''
		Test "Callable._get_signature_detect_type" with a function
		'''
		
		callable_ = Callable(fixture_function_w_all_parameter_combinations)
		expected_result = Signature.from_callable(fixture_function_w_all_parameter_combinations), IS_FUNCTION
		self.assertEqual(expected_result, callable_._get_signature_detect_type())

	
	def _test_w_class(self):
		'''
		Test "Callable._get_signature_detect_type" with a class
		'''
		
		signature_ = Signature.from_callable(FixtureClassWNewAndInit)
		# signature_ = signature_.without_parameters(0)
		print('Signature is: ', signature_.parameters)
		args_w_keys = {
			'new_pos': 'r',
			'new_kw': 6,
			'init_pos': 's',
			'init_kw': 7,
		}
		# expected_result = BoundArguments(signature_, args_w_keys)
		result = signature_.bind(**args_w_keys)
		print('Args: ', result.signature)
		self.assertEqual(expected_result, signature_.bind(**args_w_keys))
	
	def test_w_static_method(self):
		'''
		Test "Callable._get_signature_detect_type" with a static method
		'''
		
		callable_ = Callable(FixtureClassWMethods.static_method)
		expected_result = Signature.for_method(FixtureClassWMethods, 'static_method'), IS_STATIC_METHOD
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def _test_class_w_class_method(self):
		'''
		Test "execute_callable" with a class method
		'''
		
		args_w_keys = {
			'pos_arg': 'method_c',
		}
		expected_result = 'ultra-class-method_c'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.class_method, args_w_keys=args_w_keys))
	
	def _test_class_w_bound_method(self):
		'''
		Test "execute_callable" with a bound method
		'''
		
		args_w_keys = {
			'init_arg': 'pre',
			'pos_arg': 'method_b',
		}
		expected_result = 'ultra-pre-bound-method_b'
		self.assertEqual(expected_result, execute_callable(FixtureClassWMethods.bound_method, args_w_keys=args_w_keys))
	
	def _test_deep_class_w_bound_method(self):
		'''
		Test "execute_callable" with a bound method on a deep class
		'''
		
		args_w_keys = {
			'init_arg': 'pre',
			'pos_arg': 'deepos',
			'kw_arg': 'deepkw',
		}
		expected_result = 'pre-deepos-deepkw'
		self.assertEqual(expected_result, execute_callable(FixtureDeepClassL1.FixtureDeepClassL2.FixtureDeepClassL3.deep_method, args_w_keys=args_w_keys))
