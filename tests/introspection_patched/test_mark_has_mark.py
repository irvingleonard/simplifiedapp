#! python
"""Testing the introspection_patched has_mark patch"""

from functools import wraps
from unittest import TestCase

from introspection import mark as introspection_mark
from introspection.mark import does_not_alter_signature, forwards_arguments

from fixtures.introspection_patched import FixtureSubclassWMarkedInit, fixture_function
from simplifiedapp.introspection_patched import mark_has_mark


class TestMarkHasMark(TestCase):
	"""Tests for the patched introspection.mark.has_mark function"""

	def test_patch_applied(self):
		"""Test that the upstream function was replaced"""

		self.assertIs(mark_has_mark, introspection_mark.has_mark)

	def test_marked(self):
		"""Test "has_mark" with a marked function"""

		self.assertTrue(mark_has_mark(FixtureSubclassWMarkedInit.__init__, does_not_alter_signature))

	def test_different_mark(self):
		"""Test "has_mark" with a function marked with a different mark"""

		self.assertFalse(mark_has_mark(FixtureSubclassWMarkedInit.__init__, forwards_arguments))

	def test_unmarked(self):
		"""Test "has_mark" with a function that isn't marked"""

		self.assertFalse(mark_has_mark(fixture_function, does_not_alter_signature))

	def test_wrapped_marked(self):
		"""Test "has_mark" with a wrapper of a marked function (the wrapped function is checked too)"""

		@wraps(FixtureSubclassWMarkedInit.__init__)
		def wrapper(*args, **kwargs):
			"""Wrapper around the marked function

			:param args: Forwarded positional arguments
			:param kwargs: Forwarded keyword arguments
			:returns None: nothing
			"""

			return FixtureSubclassWMarkedInit.__init__(*args, **kwargs)

		self.assertTrue(mark_has_mark(wrapper, does_not_alter_signature))

	def test_not_weak_referenceable(self):
		"""Test "has_mark" with a C implemented method, which can't be weakly referenced (upstream fails with a TypeError)"""

		self.assertFalse(mark_has_mark(object.__init__, does_not_alter_signature))
		self.assertFalse(mark_has_mark(type.__dict__['__call__'], does_not_alter_signature))
