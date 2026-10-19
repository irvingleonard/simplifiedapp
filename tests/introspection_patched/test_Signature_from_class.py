#! python
"""Testing the introspection_patched Signature.from_class and Signature._from_class_default class methods"""

from unittest import TestCase
from warnings import catch_warnings, simplefilter

from fixtures.introspection_patched import FixtureClassWIncompatibleInit, FixtureClassWIncompatibleKeyword, FixtureClassWIncompatibleMetaclass, FixtureClassWIncompatibleNew, FixtureClassWIncompatiblePositional, FixtureClassWInit, FixtureClassWInitVarargs, FixtureClassWInitVarkw, FixtureClassWKeywordOnlyInit, FixtureClassWMarkedMetaclass, FixtureClassWMetaclassCall, FixtureClassWNew, FixtureClassWNewAndInit, FixtureClassWNewVarargs, FixtureClassWNewVarkw, FixtureClassWSharedParameters, FixtureClassWVarargsInit, FixtureClassWVarargsMetaclass, FixtureClassWVarargsNew, FixtureDict, FixtureEmptyClass, FixtureSubclassWMarkedInit, fixture_function
from simplifiedapp.introspection_patched import Signature


class TestSignatureFromClassDefault(TestCase):
	"""Tests for the Signature._from_class_default class method (classes instantiated by "type.__call__")"""

	EXPECTED_SIGNATURES = {
		FixtureEmptyClass: '()',
		FixtureClassWNew: '(new_pos, /, *, new_kw)',
		FixtureClassWNewVarargs: '(new_pos, /, *args, new_kw)',
		FixtureClassWNewVarkw: '(new_pos, /, *, new_kw, **kwargs)',
		FixtureClassWInit: '(init_pos, /, *, init_kw)',
		FixtureClassWInitVarargs: '(init_pos, /, *args, init_kw)',
		FixtureClassWInitVarkw: '(init_pos, /, *, init_kw, **kwargs)',
		FixtureClassWSharedParameters: '(shared, /, extra, *, shared_kw=1)',
		FixtureClassWKeywordOnlyInit: '(a, *, b)',
		FixtureClassWVarargsNew: '(a)',
		FixtureClassWVarargsInit: '(*args, kw=None)',
		FixtureDict: '(*args, **kwargs)',
		FixtureSubclassWMarkedInit: '(a, *, b=1)',
	}

	def test_signatures(self):
		"""Test "Signature._from_class_default" with every combination of "__new__" and "__init__" in the fixtures"""

		for class_, expected_result in self.EXPECTED_SIGNATURES.items():
			with self.subTest(class_=class_.__name__):
				with catch_warnings():
					simplefilter('error')
					self.assertEqual(expected_result, str(Signature._from_class_default(class_)))

	def test_mismatching_positional_names(self):
		"""Test "Signature._from_class_default" with "__new__" and "__init__" receiving the same positional argument under different names"""

		with self.assertWarns(SyntaxWarning):
			signature = Signature._from_class_default(FixtureClassWNewAndInit)
		self.assertEqual('(new_pos, /, *args, new_kw, init_kw, **kwargs)', str(signature))

	def test_forward_ref_context(self):
		"""Test "Signature._from_class_default" setting the forward reference context to the module of the class"""

		self.assertEqual('fixtures.introspection_patched', Signature._from_class_default(FixtureClassWInit).forward_ref_context)

	def test_incompatible_classes(self):
		"""Test "Signature._from_class_default" with classes that can't be instantiated with any combination of arguments"""

		for class_ in (FixtureClassWIncompatibleNew, FixtureClassWIncompatibleInit, FixtureClassWIncompatiblePositional, FixtureClassWIncompatibleKeyword):
			with self.subTest(class_=class_.__name__):
				self.assertRaises(ValueError, Signature._from_class_default, class_)

	def test_not_a_class(self):
		"""Test "Signature._from_class_default" with something that isn't a class"""

		self.assertRaises(ValueError, Signature._from_class_default, fixture_function)


class TestSignatureFromClass(TestCase):
	"""Tests for the Signature.from_class class method"""

	def test_default_call(self):
		"""Test "Signature.from_class" with a class whose metaclass doesn't override "__call__" (the default implementation is used)"""

		self.assertEqual(Signature._from_class_default(FixtureClassWInit), Signature.from_class(FixtureClassWInit))

	def test_metaclass_call(self):
		"""Test "Signature.from_class" with a class whose metaclass overrides "__call__" """

		self.assertEqual('(key)', str(Signature.from_class(FixtureClassWMetaclassCall)))

	def test_marked_metaclass_call(self):
		"""Test "Signature.from_class" with a class whose metaclass "__call__" is marked with "does_not_alter_signature" (the default implementation is used)"""

		self.assertEqual('(x)', str(Signature.from_class(FixtureClassWMarkedMetaclass)))

	def test_varargs_metaclass_call(self):
		"""Test "Signature.from_class" with a class whose metaclass "__call__" receives the class in its variable positional parameter"""

		self.assertEqual('(*args)', str(Signature.from_class(FixtureClassWVarargsMetaclass)))

	def test_incompatible_metaclass_call(self):
		"""Test "Signature.from_class" with a class whose metaclass "__call__" can't receive the class"""

		self.assertRaises(ValueError, Signature.from_class, FixtureClassWIncompatibleMetaclass)

	def test_not_a_class(self):
		"""Test "Signature.from_class" with something that isn't a class"""

		self.assertRaises(ValueError, Signature.from_class, fixture_function)
