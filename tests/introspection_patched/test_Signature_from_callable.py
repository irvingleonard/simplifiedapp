#! python
"""Testing the introspection_patched Signature.from_callable patch"""

from functools import wraps
from unittest import TestCase

from fixtures.introspection_patched import fixture_function
from simplifiedapp.introspection_patched import Signature


class TestSignatureFromCallable(TestCase):
	"""Tests for the patched Signature.from_callable method"""

	def test_c_implemented_init(self):
		"""Test "Signature.from_callable" with a C implemented "__init__" (a slot wrapper, which upstream can't handle)"""

		signature = Signature.from_callable(object.__init__)
		self.assertIsInstance(signature, Signature)
		self.assertEqual('(self, /, *args, **kwargs)', str(signature))

	def test_bound_c_implemented_init(self):
		"""Test "Signature.from_callable" with a bound C implemented "__init__" (a method wrapper, which upstream can't handle)"""

		self.assertEqual('(*args, **kwargs)', str(Signature.from_callable({}.__init__)))

	def test_other_c_implemented_method(self):
		"""Test "Signature.from_callable" with a C implemented method other than "__init__" (handled by upstream)"""

		self.assertEqual('(self, /)', str(Signature.from_callable(object.__repr__)))

	def test_function(self):
		"""Test "Signature.from_callable" with a regular function (handled by upstream)"""

		signature = Signature.from_callable(fixture_function)
		self.assertEqual('(pos_only, /, pos_or_kw, *args, kw_only, **kwargs)', str(signature))
		self.assertEqual('fixtures.introspection_patched', signature.forward_ref_context)

	def test_follow_wrapped(self):
		"""Test "Signature.from_callable" forwarding "follow_wrapped" to upstream
		Upstream caches the signature in the callable (and "functools.wraps" copies it to the wrapper), so each call gets a new wrapped function and a new wrapper.
		"""

		def wrapper_factory():
			"""Create a new function and a wrapper around it

			:returns function: the wrapper
			"""

			def wrapped(a, b=1):
				"""Function to be wrapped

				:param a: A positional or keyword parameter
				:param b: A positional or keyword parameter with a default value
				:returns tuple: the arguments received
				"""

				return a, b

			@wraps(wrapped)
			def wrapper(*args, **kwargs):
				"""Wrapper around the function

				:param args: Forwarded positional arguments
				:param kwargs: Forwarded keyword arguments
				:returns tuple: whatever the wrapped function returns
				"""

				return wrapped(*args, **kwargs)

			return wrapper

		self.assertEqual('(a, b=1)', str(Signature.from_callable(wrapper_factory())))
		self.assertEqual('(*args, **kwargs)', str(Signature.from_callable(wrapper_factory(), follow_wrapped=False)))

	def test_use_signature_db(self):
		"""Test "Signature.from_callable" forwarding "use_signature_db" to upstream"""

		self.assertEqual('(s: Sized, /) -> int', str(Signature.from_callable(len)))
		self.assertEqual('(obj, /)', str(Signature.from_callable(len, use_signature_db=False)))
