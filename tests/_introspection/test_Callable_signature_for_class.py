#python
'''
Testing the introspection_patched.Callable._signature_for_class method
'''

from unittest import TestCase

from fixtures.classes import *
from simplifiedapp.introspection_patched import Callable, Signature

class TestCallableSignatureForClass(TestCase):
	'''
	Tests for the Callable._signature_for_class method
	'''

	def test_w_empty_class(self):
		'''
		Test "Callable._signature_for_class" with an empty class
		'''
		
		expected_result = Signature(parameters=[], forward_ref_context=FixtureEmptyClass.__module__)
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureEmptyClass))

	def test_class_w_new(self):
		'''
		Test "Callable._signature_for_class" with a class having a __new__ method
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNew.__new__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNew))
	
	def test_class_w_new_varargs(self):
		'''
		Test "Callable._signature_for_class" with a class having a __new__ method that accepts varargs parameter
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewVarargs.__new__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewVarargs))
	
	def test_class_w_new_varkw(self):
		'''
		Test "Callable._signature_for_class" with a class having a __new__ method that accepts varkw parameter
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewVarkw.__new__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewVarkw))
		
	def test_class_w_init(self):
		'''
		Test "Callable._signature_for_class" with a class having a __init__ method
		'''
		
		expected_result = Signature.from_callable(FixtureClassWInit.__init__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWInit))
	
	def test_class_w_init_varargs(self):
		'''
		Test "Callable._signature_for_class" with a class having a __init__ method that accepts varargs parameter
		'''
		
		expected_result = Signature.from_callable(FixtureClassWInitVarargs.__init__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWInitVarargs))
	
	def test_class_w_init_varkw(self):
		'''
		Test "Callable._signature_for_class" with a class having a __init__ method that accepts varkw parameter
		'''
		
		expected_result = Signature.from_callable(FixtureClassWInitVarkw.__init__).without_first_parameter()
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWInitVarkw))
	
	def test_class_w_new_n_init_flexible(self):
		'''
		Test "Callable._signature_for_class" with a class having __new__ and __init__ methods that accepts varargs and varkw parameters
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInit.expected_signature)
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewAndInit))
	
	def test_class_w_new_n_init_strict(self):
		'''
		Test "Callable._signature_for_class" with a class having __new__ and __init__ methods that accepts exactly the same parameters
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitNVar.expected_signature)
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewAndInitNVar))
	
	def test_class_w_new_n_init_n_variable_new(self):
		'''
		Test "Callable._signature_for_class" with a class having __new__ and __init__ methods with __new__ accepting varargs and varkw parameters
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitVarNew.expected_signature)
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewAndInitVarNew))
	
	def test_class_w_new_n_init_n_variable_init(self):
		'''
		Test "Callable._signature_for_class" with a class having __new__ and __init__ methods with __init__ accepting varargs and varkw parameters
		'''
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitVarInit.expected_signature)
		self.assertEqual(expected_result, Callable._signature_for_class(FixtureClassWNewAndInitVarInit))
	