#python
'''
Testing the introspection_patched.Callable._get_signature_detect_type method
'''

from unittest import TestCase

from fixtures.functions import *
from fixtures.classes import *
from simplifiedapp.introspection_patched import CallableType, Callable, Signature


class TestCallableGetSignatureDetectType(TestCase):
	'''
	Tests for the Callable._get_signature_detect_type method
	'''

	def test_w_function(self):
		'''
		Test "Callable._get_signature_detect_type" with a function
		'''
		
		callable_ = Callable(fixture_function_w_all_parameter_combinations)
		expected_result = Signature.from_callable(fixture_function_w_all_parameter_combinations), CallableType['FUNCTION']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_w_inner_function(self):
		'''
		Test "Callable._get_signature_detect_type" with a nested function
		'''
		
		callable_ = Callable(fixture_nested_functions_outer())
		expected_result = Signature.from_callable(fixture_nested_functions_outer()), CallableType['FUNCTION']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def _test_w_class(self):
		'''
		Test "Callable._get_signature_detect_type" with a class
		'''
		
		callable_ = Callable(FixtureClassWNewAndInit)
		expected_result = Signature.from_callable(FixtureClassWNewAndInit), CallableType['CLASS']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_w_static_method_from_class(self):
		'''
		Test "Callable._get_signature_detect_type" with a static method from a class
		'''
		
		callable_ = Callable(FixtureClassWMethods.static_method)
		expected_result = Signature.for_method(FixtureClassWMethods, 'static_method'), CallableType['STATIC_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_w_class_method_from_class(self):
		'''
		Test "Callable._get_signature_detect_type" with a class method from a class
		'''
		
		callable_ = Callable(FixtureClassWMethods.class_method)
		expected_result = Signature.for_method(FixtureClassWMethods, 'class_method').without_first_parameter(), CallableType['CLASS_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_class_w_instance_method_from_class(self):
		'''
		Test "Callable._get_signature_detect_type" with an instance method from a class
		'''
		
		callable_ = Callable(FixtureClassWMethods.bound_method)
		expected_result = Signature.for_method(FixtureClassWMethods, 'bound_method').without_first_parameter(), CallableType['INSTANCE_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_w_class_instance(self):
		'''
		Test "Callable._get_signature_detect_type" with a class instance
		'''
		
		callable_ = Callable(FixtureClassWMethods(None))
		expected_result = Signature.from_callable(FixtureClassWMethods(None).__call__), CallableType['INSTANCE']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def test_w_static_method_from_class_instance(self):
		'''
		Test "Callable._get_signature_detect_type" with a static method from a class instance
		'''
		
		instance_ = FixtureClassWMethods(None)
		callable_ = Callable(instance_.static_method)
		expected_signature = Signature.from_callable(instance_.static_method)
		print('Expected signature: ', expected_signature.parameters)
		expected_result = expected_signature, CallableType['STATIC_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def _test_w_class_method_from_class(self):
		'''
		Test "Callable._get_signature_detect_type" with a class method from a class
		'''
		
		callable_ = Callable(FixtureClassWMethods.class_method)
		expected_result = Signature.for_method(FixtureClassWMethods, 'class_method').without_first_parameter(), \
		CallableType['CLASS_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
	
	def _test_class_w_instance_method_from_instance(self):
		'''
		Test "Callable._get_signature_detect_type" with an instance method from an instance
		'''
		
		instance_ = FixtureClassWMethods(None)
		callable_ = Callable(instance_.bound_method)
		expected_result = Signature.for_method(instance_, 'bound_method').without_first_parameter(), CallableType['INSTANCE_METHOD']
		self.assertEqual(expected_result, callable_._get_signature_detect_type())
