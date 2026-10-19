#! python
"""Fixtures for the introspection_patched tests
Functions and classes covering the different kinds of callables and signatures handled by the "simplifiedapp.introspection_patched" module.
"""

from introspection.mark import does_not_alter_signature

__version__ = '1.2.3'


def fixture_function(pos_only, /, pos_or_kw, *args, kw_only, **kwargs):
	"""Function with every kind of parameter
	It returns its arguments, so the call can be checked.

	:param pos_only: A positional only parameter
	:param pos_or_kw: A positional or keyword parameter
	:param args: The variable positional parameter
	:param kw_only: A keyword only parameter
	:param kwargs: The variable keyword parameter
	:returns tuple: all the arguments received
	"""

	return pos_only, pos_or_kw, args, kw_only, kwargs
fixture_function.fixture_attribute = 'fixture value'


def fixture_function_wo_variable_parameters(a, b=1):
	"""Function without variable parameters
	It returns its arguments, so the call can be checked.

	:param a: A positional or keyword parameter
	:param b: A positional or keyword parameter with a default value
	:returns tuple: all the arguments received
	"""

	return a, b


def fixture_documented_function(pos1, pos2, /, mult1='mult1', *args, kw1, kw2=False, **kwargs):
	"""Documented function
	A function documented with every section supported by "object_metadata".

	:param float pos1: First positional parameter
	:param pos2: Second positional parameter
	:param mult1: Positional or keyword parameter
	:param args: Any other positional arguments
	:param kw1: First keyword parameter
	:param bool? kw2: Second keyword parameter
	:param kwargs: All other keyword arguments
	:returns None: nothing useful, really
	"""

	pass
fixture_documented_function.__version__ = '0.1.3.dev1'


def fixture_short_documented_function():
	"""Short documented function"""

	pass


def fixture_nested_function_factory():
	"""Create a nested function
	The returned function was defined inside this one (not in a class).

	:returns function: the nested function
	"""

	def fixture_nested_function(nested_arg):
		"""Nested function

		:param nested_arg: Any argument
		:returns Any: the argument received
		"""

		return nested_arg

	return fixture_nested_function


def fixture_local_class_factory():
	"""Create a class inside a function
	The class can't be reached from the module; one of its methods uses "super()", the other one doesn't.

	:returns type: the local class
	"""

	class FixtureLocalClass:
		"""Class defined inside a function"""

		def __init__(self):
			"""Initialize the instance"""

			super().__init__()

		def method_w_super(self, arg):
			"""Method using "super()", which gets a "__class__" closure cell

			:param arg: Any argument
			:returns Any: the argument received
			"""

			super().__init__()
			return arg

		def method_wo_super(self, arg):
			"""Method that doesn't use "super()"

			:param arg: Any argument
			:returns Any: the argument received
			"""

			return arg

	return FixtureLocalClass


def fixture_attached_function(self, arg):
	"""Function that gets attached to a class under a different name

	:param self: The instance
	:param arg: Any argument
	:returns tuple: the class name of the instance and the argument received
	"""

	return type(self).__name__, arg


class FixtureEmptyClass:
	"""Class without "__new__" nor "__init__" """

	pass


class FixtureClassWNew:
	"""Class with "__new__" only"""

	def __new__(cls, new_pos, /, *, new_kw):
		"""Create the instance

		:param new_pos: Positional parameter
		:param new_kw: Keyword parameter
		:returns FixtureClassWNew: the instance
		"""

		return super().__new__(cls)


class FixtureClassWNewVarargs:
	"""Class with "__new__" only, taking variable positional arguments"""

	def __new__(cls, new_pos, /, *args, new_kw):
		"""Create the instance

		:param new_pos: Positional parameter
		:param args: Variable positional parameter
		:param new_kw: Keyword parameter
		:returns FixtureClassWNewVarargs: the instance
		"""

		return super().__new__(cls)


class FixtureClassWNewVarkw:
	"""Class with "__new__" only, taking variable keyword arguments"""

	def __new__(cls, new_pos, /, *, new_kw, **kwargs):
		"""Create the instance

		:param new_pos: Positional parameter
		:param new_kw: Keyword parameter
		:param kwargs: Variable keyword parameter
		:returns FixtureClassWNewVarkw: the instance
		"""

		return super().__new__(cls)


class FixtureClassWInit:
	"""Class with "__init__" only"""

	def __init__(self, init_pos, /, *, init_kw):
		"""Initialize the instance

		:param init_pos: Positional parameter
		:param init_kw: Keyword parameter
		"""

		self.init_pos, self.init_kw = init_pos, init_kw


class FixtureClassWInitVarargs:
	"""Class with "__init__" only, taking variable positional arguments"""

	def __init__(self, init_pos, /, *args, init_kw):
		"""Initialize the instance

		:param init_pos: Positional parameter
		:param args: Variable positional parameter
		:param init_kw: Keyword parameter
		"""

		pass


class FixtureClassWInitVarkw:
	"""Class with "__init__" only, taking variable keyword arguments"""

	def __init__(self, init_pos, /, *, init_kw, **kwargs):
		"""Initialize the instance

		:param init_pos: Positional parameter
		:param init_kw: Keyword parameter
		:param kwargs: Variable keyword parameter
		"""

		pass


class FixtureClassWNewAndInit:
	"""Class with both "__new__" and "__init__", taking every kind of parameter (with mismatching names)"""

	def __new__(cls, new_pos, /, *args, new_kw, **kwargs):
		"""Create the instance

		:param new_pos: Positional parameter
		:param args: Variable positional parameter
		:param new_kw: Keyword parameter
		:param kwargs: Variable keyword parameter
		:returns FixtureClassWNewAndInit: the instance
		"""

		return super().__new__(cls)

	def __init__(self, init_pos, /, *args, init_kw, **kwargs):
		"""Initialize the instance

		:param init_pos: Positional parameter (receives the same value as "new_pos")
		:param args: Variable positional parameter
		:param init_kw: Keyword parameter
		:param kwargs: Variable keyword parameter
		"""

		pass


class FixtureClassWSharedParameters:
	"""Class with both "__new__" and "__init__", sharing some parameters"""

	def __new__(cls, shared, /, *args, shared_kw=1, **kwargs):
		"""Create the instance

		:param shared: Positional parameter shared with "__init__"
		:param args: Variable positional parameter
		:param shared_kw: Keyword parameter shared with "__init__"
		:param kwargs: Variable keyword parameter
		:returns FixtureClassWSharedParameters: the instance
		"""

		return super().__new__(cls)

	def __init__(self, shared, /, extra, *, shared_kw=2):
		"""Initialize the instance

		:param shared: Positional parameter shared with "__new__"
		:param extra: Positional parameter only taken by "__init__"
		:param shared_kw: Keyword parameter shared with "__new__"
		"""

		pass


class FixtureClassWKeywordOnlyInit:
	"""Class whose "__init__" parameter can only be passed as a keyword (since "__new__" has no variable positional parameter)"""

	def __new__(cls, a, **kwargs):
		"""Create the instance

		:param a: Positional parameter
		:param kwargs: Variable keyword parameter
		:returns FixtureClassWKeywordOnlyInit: the instance
		"""

		return super().__new__(cls)

	def __init__(self, a, b):
		"""Initialize the instance

		:param a: Positional parameter
		:param b: Positional or keyword parameter
		"""

		pass


class FixtureClassWVarargsNew:
	"""Class whose "__new__" receives the class in its variable positional parameter"""

	def __new__(*args, **kwargs):
		"""Create the instance

		:param args: Variable positional parameter (the class comes first)
		:param kwargs: Variable keyword parameter
		:returns FixtureClassWVarargsNew: the instance
		"""

		return object.__new__(args[0])

	def __init__(self, a):
		"""Initialize the instance

		:param a: Positional parameter
		"""

		pass


class FixtureClassWVarargsInit:
	"""Class whose "__init__" receives the instance in its variable positional parameter"""

	def __init__(*args, kw=None):
		"""Initialize the instance

		:param args: Variable positional parameter (the instance comes first)
		:param kw: Keyword parameter
		"""

		pass


class FixtureClassWIncompatiblePositional:
	"""Class whose "__init__" requires a positional parameter that "__new__" doesn't accept"""

	def __new__(cls, a):
		"""Create the instance

		:param a: Positional parameter
		:returns FixtureClassWIncompatiblePositional: the instance
		"""

		return super().__new__(cls)

	def __init__(self, a, b):
		"""Initialize the instance

		:param a: Positional parameter
		:param b: Positional parameter not accepted by "__new__"
		"""

		pass


class FixtureClassWIncompatibleKeyword:
	"""Class whose "__init__" requires a keyword parameter that "__new__" doesn't accept"""

	def __new__(cls, a):
		"""Create the instance

		:param a: Positional parameter
		:returns FixtureClassWIncompatibleKeyword: the instance
		"""

		return super().__new__(cls)

	def __init__(self, a, *, k):
		"""Initialize the instance

		:param a: Positional parameter
		:param k: Keyword parameter not accepted by "__new__"
		"""

		pass


class FixtureClassWIncompatibleNew:
	"""Class whose "__new__" can't receive the class"""

	def __new__(**kwargs):
		"""Create the instance

		:param kwargs: Variable keyword parameter
		:returns None: it can't actually work
		"""

		pass


class FixtureClassWIncompatibleInit:
	"""Class whose "__init__" can't receive the instance"""

	def __init__(**kwargs):
		"""Initialize the instance

		:param kwargs: Variable keyword parameter
		"""

		pass


class FixtureDict(dict):
	"""Subclass of a builtin class, inheriting its C implemented "__new__" and "__init__" """

	pass


class FixtureBaseWInit:
	"""Base class with a regular "__init__" """

	def __init__(self, a, *, b=1):
		"""Initialize the instance

		:param a: Positional parameter
		:param b: Keyword parameter
		"""

		self.a, self.b = a, b


class FixtureSubclassWMarkedInit(FixtureBaseWInit):
	"""Subclass whose "__init__" just forwards its arguments (marked with "does_not_alter_signature")"""

	@does_not_alter_signature
	def __init__(self, *args, **kwargs):
		"""Initialize the instance

		:param args: Forwarded positional arguments
		:param kwargs: Forwarded keyword arguments
		"""

		super().__init__(*args, **kwargs)


class FixtureMetaclassWCall(type):
	"""Metaclass overriding "__call__" """

	def __call__(cls, key):
		"""Return a value instead of an instance

		:param key: The only argument accepted when calling the class
		:returns str: a value built from the key
		"""

		return f'cached-{key}'


class FixtureClassWMetaclassCall(metaclass=FixtureMetaclassWCall):
	"""Class whose metaclass overrides "__call__" """

	def __init__(self, a, b):
		"""Initialize the instance (never actually called)

		:param a: Positional parameter
		:param b: Positional parameter
		"""

		pass


class FixtureMarkedMetaclass(type):
	"""Metaclass whose "__call__" just forwards its arguments (marked with "does_not_alter_signature")"""

	@does_not_alter_signature
	def __call__(cls, *args, **kwargs):
		"""Forward the call to "type.__call__"

		:param args: Forwarded positional arguments
		:param kwargs: Forwarded keyword arguments
		:returns Any: the instance
		"""

		return super().__call__(*args, **kwargs)


class FixtureClassWMarkedMetaclass(metaclass=FixtureMarkedMetaclass):
	"""Class whose metaclass "__call__" doesn't alter the signature"""

	def __init__(self, x):
		"""Initialize the instance

		:param x: Positional parameter
		"""

		pass


class FixtureVarargsMetaclass(type):
	"""Metaclass whose "__call__" receives the class in its variable positional parameter"""

	def __call__(*args):
		"""Return the arguments received

		:param args: Variable positional parameter (the class comes first)
		:returns tuple: the arguments received
		"""

		return args


class FixtureClassWVarargsMetaclass(metaclass=FixtureVarargsMetaclass):
	"""Class whose metaclass "__call__" has a leading variable positional parameter"""

	pass


class FixtureIncompatibleMetaclass(type):
	"""Metaclass whose "__call__" can't receive the class"""

	def __call__(**kwargs):
		"""Can't actually work

		:param kwargs: Variable keyword parameter
		:returns None: nothing
		"""

		pass


class FixtureClassWIncompatibleMetaclass(metaclass=FixtureIncompatibleMetaclass):
	"""Class whose metaclass "__call__" can't receive the class"""

	pass


class FixtureClassWMethods:
	"""Class with every kind of method

	:param init_arg: The argument to initialize the instance
	"""

	__version__ = '4.5.6'

	def __init__(self, init_arg):
		"""Initialize the instance

		:param init_arg: Any argument
		"""

		self.init_arg = init_arg

	def __call__(self, call_arg):
		"""Make the instances callable

		:param call_arg: Any argument
		:returns tuple: the initialization argument and the argument received
		"""

		return self.init_arg, call_arg

	def instance_method(self, pos_arg, /, *args, kw_arg='kw', **kwargs):
		"""Instance method with every kind of parameter

		:param pos_arg: Positional parameter
		:param args: Variable positional parameter
		:param kw_arg: Keyword parameter
		:param kwargs: Variable keyword parameter
		:returns tuple: the initialization argument and all the arguments received
		"""

		return self.init_arg, pos_arg, args, kw_arg, kwargs

	def varargs_method(*args):
		"""Instance method receiving the instance in its variable positional parameter

		:param args: Variable positional parameter (the instance comes first)
		:returns tuple: the arguments received, without the instance
		"""

		return args[1:]

	def incompatible_method(**kwargs):
		"""Instance method that can't receive the instance

		:param kwargs: Variable keyword parameter
		:returns None: nothing
		"""

		pass

	@classmethod
	def class_method(cls, pos_arg):
		"""Class method

		:param pos_arg: Any argument
		:returns tuple: the class name and the argument received
		"""

		return cls.__name__, pos_arg

	@staticmethod
	def static_method(pos_arg):
		"""Static method

		:param pos_arg: Any argument
		:returns Any: the argument received
		"""

		return pos_arg

	@staticmethod
	def static_method_w_self(self, pos_arg):
		"""Static method whose first parameter is called "self"

		:param self: Not an instance, just a regular parameter
		:param pos_arg: Any argument
		:returns tuple: the arguments received
		"""

		return self, pos_arg

	alias_method = instance_method


FixtureClassWMethods.attached_method = fixture_attached_function


class FixtureSubclassWMethods(FixtureClassWMethods):
	"""Subclass inheriting all the methods"""

	pass


class FixtureSubclassWOverride(FixtureClassWMethods):
	"""Subclass overriding a method"""

	def varargs_method(self, *args):
		"""Override of the parent method

		:param args: Variable positional parameter
		:returns tuple: the arguments received
		"""

		return args


class FixtureSubclassWMarkedMethod(FixtureClassWMethods):
	"""Subclass with a method that just forwards its arguments (marked with "does_not_alter_signature")"""

	@does_not_alter_signature
	def instance_method(self, *args, **kwargs):
		"""Forward the call to the parent implementation

		:param args: Forwarded positional arguments
		:param kwargs: Forwarded keyword arguments
		:returns tuple: whatever the parent implementation returns
		"""

		return super().instance_method(*args, **kwargs)


class FixtureOuterClass:
	"""Outer class of a nested class hierarchy"""

	class FixtureMiddleClass:
		"""Middle class of a nested class hierarchy"""

		class FixtureInnerClass:
			"""Inner class of a nested class hierarchy"""

			def inner_method(self, arg):
				"""Method of a deeply nested class

				:param arg: Any argument
				:returns Any: the argument received
				"""

				return arg


class FixtureEnumerationClass:
	"""Class with every kind of member, for enumerate_object_callables"""

	class_data = 'not callable'
	borrowed_method = str.upper

	class FixtureNestedClass:
		"""Nested class"""

		pass

	def instance_method(self):
		"""Instance method

		:returns str: the name of the method
		"""

		return 'instance_method'

	@classmethod
	def class_method(cls):
		"""Class method

		:returns str: the name of the class
		"""

		return cls.__name__

	@staticmethod
	def static_method(arg):
		"""Static method

		:param arg: Any argument
		:returns Any: the argument received
		"""

		return arg

	@property
	def failing_property(self):
		"""Property that fails if it's ever executed

		:returns None: it always raises
		"""

		raise RuntimeError('The property was executed')


class FixtureEnumerationDict(dict):
	"""Subclass of a builtin class, inheriting C implemented methods (including a class method)"""

	pass


class FixtureEnumerationSlots:
	"""Class using slots, holding a callable in one of them"""

	__slots__ = ('slot_callable', 'slot_data')

	def __init__(self):
		"""Initialize the instance"""

		self.slot_callable, self.slot_data = len, 'not callable'
