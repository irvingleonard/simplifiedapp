#python
"""
Testing the introspection_patched.Signature.from_class method
"""

from unittest import TestCase

from fixtures.classes import *
from simplifiedapp.introspection_patched import Signature

class TestCallableSignatureForClass(TestCase):
	"""
	Tests for the Signature.from_class method
	"""

	def test_w_empty_class(self):
		"""
		Testing "Signature.from_class" with an empty class
		"""
		
		expected_result = Signature(parameters=[], forward_ref_context=FixtureEmptyClass.__module__)
		self.assertEqual(expected_result, Signature.from_class(FixtureEmptyClass))

	def test_class_w_new(self):
		"""
		Testing "Signature.from_class" with a class having a __new__ method
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNew.__new__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNew))
	
	def test_class_w_new_varargs(self):
		"""
		Testing "Signature.from_class" with a class having a __new__ method that accepts varargs parameter
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewVarargs.__new__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewVarargs))
	
	def test_class_w_new_varkw(self):
		"""
		Testing "Signature.from_class" with a class having a __new__ method that accepts varkw parameter
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewVarkw.__new__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewVarkw))
		
	def test_class_w_init(self):
		"""
		Testing "Signature.from_class" with a class having a __init__ method
		"""
		
		expected_result = Signature.from_callable(FixtureClassWInit.__init__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWInit))
	
	def test_class_w_init_varargs(self):
		"""
		Testing "Signature.from_class" with a class having a __init__ method that accepts varargs parameter
		"""
		
		expected_result = Signature.from_callable(FixtureClassWInitVarargs.__init__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWInitVarargs))
	
	def test_class_w_init_varkw(self):
		"""
		Testing "Signature.from_class" with a class having a __init__ method that accepts varkw parameter
		"""
		
		expected_result = Signature.from_callable(FixtureClassWInitVarkw.__init__).without_first_parameter()
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWInitVarkw))

	def test_class_w_new_n_init_complex(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with a complex combination of parameters
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitComplex.expected_signature)
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewAndInitComplex))

	def test_class_w_new_n_init_matching(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods that accepts exactly the same parameters
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitMatching.expected_signature)
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewAndInitMatching))

	def test_class_w_new_n_init_mismatch_positional(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with a mismatching combination of positional parameters
		"""

		expected_result = Signature.from_callable(FixtureClassWNewAndInitMismatchPositional.expected_signature)
		with self.assertWarns(SyntaxWarning):
			result = Signature.from_class(FixtureClassWNewAndInitMismatchPositional)
		self.assertEqual(expected_result, result)

	def test_class_w_new_n_init_mismatch_positional_or_keyword(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with a mismatching combination of positional-or-keyword parameters
		"""

		expected_result = Signature.from_callable(FixtureClassWNewAndInitMismatchPositionalOrKeyword.expected_signature)
		with self.assertWarns(SyntaxWarning):
			result = Signature.from_class(FixtureClassWNewAndInitMismatchPositionalOrKeyword)
		self.assertEqual(expected_result, result)

	def test_class_w_new_n_init_n_flexible_new(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with __new__ accepting varargs and varkw parameters
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitFNew.expected_signature)
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewAndInitFNew))
	
	def test_class_w_new_n_init_n_flexible_init(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with __init__ accepting varargs and varkw parameters
		"""
		
		expected_result = Signature.from_callable(FixtureClassWNewAndInitFInit.expected_signature)
		self.assertEqual(expected_result, Signature.from_class(FixtureClassWNewAndInitFInit))

	def test_class_w_new_n_init_invalid_positional(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with an invalid combination of positional parameters
		"""

		self.assertRaises(ValueError, Signature.from_class, FixtureClassWNewAndInitInvalidPositional)

	def test_class_w_new_n_init_invalid_positional_or_keyword(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with an invalid combination of positional or keyword parameters
		"""

		self.assertRaises(ValueError, Signature.from_class, FixtureClassWNewAndInitInvalidPositionalOrKeyword)

	def test_class_w_new_n_init_invalid_keyword(self):
		"""
		Testing "Signature.from_class" with a class having __new__ and __init__ methods with an invalid combination of keyword parameters
		"""

		self.assertRaises(ValueError, Signature.from_class, FixtureClassWNewAndInitInvalidKeyword)
