#! python
"""Testing the introspection_patched.Callable._get_signature_detect_type method"""

from functools import partial
from unittest import TestCase

from fixtures.introspection_patched import FixtureClassWInit, FixtureClassWMethods, FixtureSubclassWMarkedMethod, fixture_function, fixture_function_wo_variable_parameters, fixture_local_class_factory, fixture_nested_function_factory
from simplifiedapp.introspection_patched import Callable, CallableType, Signature


class TestCallableGetSignatureDetectType(TestCase):
	"""Tests for the Callable._get_signature_detect_type method"""

	def assert_signature_type(self, expected_signature, expected_type, callable_):
		"""Check the signature (as a string) and the type detected for a callable

		:param str expected_signature: The expected signature
		:param str expected_type: The name of the expected "CallableType"
		:param Callable callable_: The callable to check
		:returns None: it fails the test if there's any mismatch
		"""

		signature, type_ = callable_._get_signature_detect_type()
		self.assertEqual((expected_signature, CallableType[expected_type]), (str(signature), type_))

	def test_class(self):
		"""Test "Callable._get_signature_detect_type" with a class"""

		signature, type_ = Callable(FixtureClassWInit)._get_signature_detect_type()
		self.assertEqual((Signature.from_class(FixtureClassWInit), CallableType['CLASS']), (signature, type_))

	def test_bound_method(self):
		"""Test "Callable._get_signature_detect_type" with a method bound to an instance"""

		self.assert_signature_type("(pos_arg, /, *args, kw_arg='kw', **kwargs)", 'BOUND_METHOD', Callable(FixtureClassWMethods(1).instance_method))

	def test_builtin_bound_method(self):
		"""Test "Callable._get_signature_detect_type" with a C implemented method bound to an instance"""

		self.assert_signature_type('(object, /)', 'BOUND_METHOD', Callable([].append))

	def test_class_method(self):
		"""Test "Callable._get_signature_detect_type" with a class method, retrieved from the class and from an instance"""

		self.assert_signature_type('(pos_arg)', 'CLASS_METHOD', Callable(FixtureClassWMethods.class_method))
		self.assert_signature_type('(pos_arg)', 'CLASS_METHOD', Callable(FixtureClassWMethods(1).class_method))

	def test_static_method(self):
		"""Test "Callable._get_signature_detect_type" with a static method, retrieved from the class and from an instance"""

		self.assert_signature_type('(pos_arg)', 'STATIC_METHOD', Callable(FixtureClassWMethods.static_method))
		self.assert_signature_type('(pos_arg)', 'STATIC_METHOD', Callable(FixtureClassWMethods(1).static_method))

	def test_static_method_w_self(self):
		"""Test "Callable._get_signature_detect_type" with a static method whose first parameter is called "self" """

		self.assert_signature_type('(self, pos_arg)', 'STATIC_METHOD', Callable(FixtureClassWMethods.static_method_w_self))

	def test_instance_method(self):
		"""Test "Callable._get_signature_detect_type" with an instance method (without the parameter receiving the instance)"""

		self.assert_signature_type("(pos_arg, /, *args, kw_arg='kw', **kwargs)", 'INSTANCE_METHOD', Callable(FixtureClassWMethods.instance_method))

	def test_varargs_instance_method(self):
		"""Test "Callable._get_signature_detect_type" with an instance method receiving the instance in its variable positional parameter"""

		self.assert_signature_type('(*args)', 'INSTANCE_METHOD', Callable(FixtureClassWMethods.varargs_method))

	def test_incompatible_instance_method(self):
		"""Test "Callable._get_signature_detect_type" with an instance method that can't receive the instance"""

		self.assertRaises(ValueError, Callable(FixtureClassWMethods.incompatible_method)._get_signature_detect_type)

	def test_marked_instance_method(self):
		"""Test "Callable._get_signature_detect_type" with an instance method marked with "does_not_alter_signature" (the signature comes from the supplying implementation)"""

		self.assert_signature_type("(pos_arg, /, *args, kw_arg='kw', **kwargs)", 'INSTANCE_METHOD', Callable(FixtureSubclassWMarkedMethod.instance_method))

	def test_local_class_instance_method(self):
		"""Test "Callable._get_signature_detect_type" with an instance method of a class defined inside a function, with an explicit parent"""

		local_class = fixture_local_class_factory()
		self.assert_signature_type('(arg)', 'INSTANCE_METHOD', Callable(local_class.method_wo_super, parent=local_class))

	def test_method_descriptor(self):
		"""Test "Callable._get_signature_detect_type" with C implemented instance methods"""

		self.assert_signature_type('()', 'INSTANCE_METHOD', Callable(str.upper))
		self.assert_signature_type('()', 'INSTANCE_METHOD', Callable(object.__repr__))

	def test_function(self):
		"""Test "Callable._get_signature_detect_type" with functions"""

		self.assert_signature_type('(pos_only, /, pos_or_kw, *args, kw_only, **kwargs)', 'FUNCTION', Callable(fixture_function))
		self.assert_signature_type('(nested_arg)', 'FUNCTION', Callable(fixture_nested_function_factory()))

	def test_builtin_function(self):
		"""Test "Callable._get_signature_detect_type" with a builtin function"""

		self.assert_signature_type('(s: Sized, /) -> int', 'FUNCTION', Callable(len))

	def test_callable_instance(self):
		"""Test "Callable._get_signature_detect_type" with a callable instance"""

		self.assert_signature_type('(call_arg)', 'INSTANCE', Callable(FixtureClassWMethods(1)))

	def test_partial(self):
		"""Test "Callable._get_signature_detect_type" with a "functools.partial" object"""

		self.assert_signature_type('(b=1)', 'INSTANCE', Callable(partial(fixture_function_wo_variable_parameters, 1)))
