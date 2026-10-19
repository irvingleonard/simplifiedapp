#! python
"""Testing the introspection_patched.enumerate_object_callables function"""

from heapq import heappush
from importlib import import_module
from pathlib import PurePath
from types import MethodType
from unittest import TestCase

from fixtures import enumeration_package, enumeration_public_names
from fixtures.enumeration_package import FixturePackageClass, FixtureSubmoduleClass, fixture_package_function, fixture_partial, fixture_submodule_function, fixture_unknown_module_function, submodule as enumeration_submodule
from fixtures.enumeration_package.sibling import fixture_sibling_function
from fixtures.introspection_patched import FixtureEnumerationClass, FixtureEnumerationDict, FixtureEnumerationSlots
from simplifiedapp.introspection_patched import enumerate_object_callables


class TestEnumerateObjectCallables(TestCase):
	"""Tests for the enumerate_object_callables function"""

	def members_by_name(self, members):
		"""Index the members by name

		:param list members: The members returned by "enumerate_object_callables"
		:returns dict: the members indexed by their name
		"""

		return {member.__name__: member for member in members}

	def test_class(self):
		"""Test "enumerate_object_callables" with a class (the members are retrieved like the class would)"""

		functions, classes = enumerate_object_callables(FixtureEnumerationClass)
		self.assertEqual([FixtureEnumerationClass.FixtureNestedClass], classes)

		functions = self.members_by_name(functions)
		self.assertIs(FixtureEnumerationClass.__dict__['instance_method'], functions['instance_method'])
		self.assertIs(FixtureEnumerationClass.__dict__['static_method'].__func__, functions['static_method'])
		self.assertIsInstance(functions['class_method'], MethodType)
		self.assertIs(FixtureEnumerationClass, functions['class_method'].__self__)
		self.assertIs(str.upper, functions['upper'])

	def test_class_special_members(self):
		"""Test "enumerate_object_callables" including the special ("__dunder__") members, even the C implemented ones"""

		functions = self.members_by_name(enumerate_object_callables(FixtureEnumerationClass)[0])
		self.assertIs(object.__init__, functions['__init__'])
		self.assertIs(FixtureEnumerationClass, functions['__init_subclass__'].__self__)

	def test_class_non_callables(self):
		"""Test "enumerate_object_callables" skipping members that aren't callable, without executing them (properties)"""

		functions = self.members_by_name(enumerate_object_callables(FixtureEnumerationClass)[0])
		for name in ('class_data', 'failing_property'):
			self.assertNotIn(name, functions)

	def test_sorted(self):
		"""Test "enumerate_object_callables" sorting the members by their name"""

		functions, classes = enumerate_object_callables(enumeration_package)
		self.assertEqual(sorted(member.__name__ for member in classes), [member.__name__ for member in classes])
		names = [name for name, member in sorted(vars(enumeration_package).items()) if member in functions]
		self.assertEqual([vars(enumeration_package)[name] for name in names], functions)

	def test_instance(self):
		"""Test "enumerate_object_callables" with an instance (the members are retrieved like the instance would, the properties aren't executed)"""

		instance = FixtureEnumerationClass()
		instance.instance_callable = fixture_package_function
		functions, classes = enumerate_object_callables(instance)
		self.assertEqual([FixtureEnumerationClass.FixtureNestedClass], classes)

		functions = self.members_by_name(functions)
		self.assertEqual('instance_method', functions['instance_method']())
		self.assertIs(instance, functions['instance_method'].__self__)
		self.assertEqual('FixtureEnumerationClass', functions['class_method']())
		self.assertEqual('static', functions['static_method']('static'))
		self.assertIs(fixture_package_function, functions['fixture_package_function'])
		self.assertIs(instance, functions['__repr__'].__self__)
		self.assertNotIn('failing_property', functions)

	def test_instance_unbindable_method(self):
		"""Test "enumerate_object_callables" with an instance holding a C implemented method of an unrelated class (it can't be bound, so it's kept as is)"""

		functions = self.members_by_name(enumerate_object_callables(FixtureEnumerationClass())[0])
		self.assertIs(str.upper, functions['upper'])

	def test_builtin_subclass(self):
		"""Test "enumerate_object_callables" with a subclass of a builtin class and one of its instances (C implemented methods get bound)"""

		self.assertIs(FixtureEnumerationDict, self.members_by_name(enumerate_object_callables(FixtureEnumerationDict)[0])['fromkeys'].__self__)

		instance = FixtureEnumerationDict(a=1)
		functions = self.members_by_name(enumerate_object_callables(instance)[0])
		self.assertIs(instance, functions['get'].__self__)
		self.assertEqual(1, functions['get']('a'))

	def test_unbindable_class_method(self):
		"""Test "enumerate_object_callables" with a C implemented class method of an unrelated class (it can't be bound, so it's kept as is)"""

		class_method = dict.__dict__['fromkeys']
		fixture_class = type('FixtureBorrowedClassMethod', (), {'borrowed': class_method})
		self.assertIs(class_method, self.members_by_name(enumerate_object_callables(fixture_class)[0])['fromkeys'])

	def test_slots(self):
		"""Test "enumerate_object_callables" with an instance using slots"""

		functions = enumerate_object_callables(FixtureEnumerationSlots())[0]
		self.assertIn(len, functions)

	def test_module(self):
		"""Test "enumerate_object_callables" with a package re-exporting a submodule (the names imported from unrelated modules are left out)"""

		expected_result = [fixture_package_function, fixture_partial, fixture_submodule_function, fixture_unknown_module_function], [FixturePackageClass, FixtureSubmoduleClass]
		self.assertEqual(expected_result, enumerate_object_callables(enumeration_package))

	def test_submodule(self):
		"""Test "enumerate_object_callables" with a submodule importing from a sibling (same root module) and from an unrelated module"""

		expected_result = [fixture_sibling_function, fixture_submodule_function], [FixtureSubmoduleClass]
		self.assertEqual(expected_result, enumerate_object_callables(enumeration_submodule))

	def test_module_public_names(self):
		"""Test "enumerate_object_callables" with a module declaring its public names in "__all__" (those are included regardless of where they were defined)"""

		expected_result = [enumeration_public_names.fixture_public_function, enumeration_public_names.fixture_unlisted_function, heappush], [PurePath]
		self.assertEqual(expected_result, enumerate_object_callables(enumeration_public_names))

	def test_c_accelerator(self):
		"""Test "enumerate_object_callables" with a standard library module whose functions come from a C accelerator module (listed in its "__all__")"""

		self.assertIn(heappush, enumerate_object_callables(import_module('heapq'))[0])
