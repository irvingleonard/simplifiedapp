#python
"""Classes fixtures
Collection of classes with different parameter and method combinations.
"""

class FancyStuff:
	"""
	Class with helper methods for enhanced output (and equality comparison)
	"""
	
	def __repr__(self):
		return str(vars(self))
	
	def __eq__(self, other):
		return vars(self) == vars(other)


class FixtureEmptyClass(FancyStuff):
	"""
	Just an empty class
	"""

	pass


class FixtureClassWNew(FancyStuff):
	"""
	Class with __new__ (2 param version)
	"""
	
	def __new__(cls, new_pos, /, *, new_kw):
		"""
		Expecting a positional parameter and a keyword parameter
		"""
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.new_kw = new_kw
		return result


class FixtureClassWNewVarargs(FancyStuff):
	"""
	Class with __new__ (2 param and varargs version)
	"""
	
	def __new__(cls, new_pos, /, *args, new_kw):
		"""
		Expecting a positional parameter, varargs, and a keyword parameter
		"""
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.varargs = args
		result.new_kw = new_kw
		return result


class FixtureClassWNewVarkw(FancyStuff):
	"""
	Class with __new__ (2 param and varkwargs version)
	"""
	
	def __new__(cls, new_pos, /, *, new_kw, **kwargs):
		"""
		Expecting a positional parameter, a keyword parameter, and varkwargs
		"""
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.new_kw = new_kw
		result.varkw = kwargs
		return result


class FixtureClassWInit(FancyStuff):
	"""
	Class with __init__ (2 param version)
	"""
	
	def __init__(self, init_pos, /, *, init_kw):
		"""
		Expecting a positional parameter and a keyword parameter
		"""
		
		self.init_pos = init_pos
		self.init_kw = init_kw


class FixtureClassWInitVarargs(FancyStuff):
	"""
	Class with __init__ (2 param and varargs version)
	"""
	
	def __init__(self, init_pos, /, *args, init_kw):
		"""
		Expecting a positional parameter, varargs, and a keyword parameter
		"""
		
		self.init_pos = init_pos
		self.varargs = args
		self.init_kw = init_kw


class FixtureClassWInitVarkw(FancyStuff):
	"""
	Class with __init__ (2 param and varkwargs version)
	"""
	
	def __init__(self, init_pos, /, *, init_kw, **kwargs):
		"""
		Expecting a positional parameter, a keyword parameter, and varkwargs
		"""
		
		self.init_pos = init_pos
		self.init_kw = init_kw
		self.varkw = kwargs


class FixtureClassWNewAndInitComplex(FancyStuff):
	"""
	Class with __new__ and __init__ (complex version)
	"""
	
	def __new__(cls, new_pos, /, *args, new_kw, **kwargs):
		"""
		Expecting dedicated parameters
		"""
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.new_kw = new_kw
		result.new_varargs = args
		result.new_varkw = kwargs
		return result
	
	def __init__(self, new_pos, init_pos, /, *args, init_kw, **kwargs):
		"""
		Expecting dedicated parameters
		"""
		
		self.init_pos = init_pos
		self.init_kw = init_kw
		self.init_varargs = args
		self.init_varkw = kwargs
	
	@staticmethod
	def expected_signature(new_pos, init_pos, /, *args, new_kw, init_kw, **kwargs):
		"""
		The signature expected from the combination of __new__ and __init__
		"""
		
		pass


class FixtureClassWNewAndInitMatching(FancyStuff):
	"""
	Class with __new__ and __init__ (matching version)
	"""
	
	def __new__(cls, foo, /, *, bar):
		"""
		Expecting shared parameters
		"""
		
		result = super().__new__(cls)
		result.new_foo = foo
		result.new_bar = bar
		return result
	
	def __init__(self, foo, /, *, bar):
		"""
		Expecting shared parameters
		"""
		
		self.init_foo = foo
		self.init_bar = bar
	
	@staticmethod
	def expected_signature(foo, /, *, bar):
		"""
		The signature expected from the combination of __new__ and __init__
		"""
		
		pass


class FixtureClassWNewAndInitMismatchPositional(FancyStuff):
	"""
	Class with __new__ and __init__ (mismatch version)
	"""

	def __new__(cls, new_pos, /):
		"""
		Expecting dedicated parameters
		"""

		result = super().__new__(cls)
		result.new_pos = new_pos
		return result

	def __init__(self, init_pos, /):
		"""
		Expecting dedicated parameters
		"""

		self.init_pos = init_pos

	@staticmethod
	def expected_signature(new_pos, /):
		"""
		The signature expected from the combination of __new__ and __init__
		"""

		pass


class FixtureClassWNewAndInitMismatchPositionalOrKeyword(FancyStuff):
	"""
	Class with __new__ and __init__ (mismatch version)
	"""

	def __new__(cls, new_pos):
		"""
		Expecting dedicated parameters
		"""

		result = super().__new__(cls)
		result.new_pos = new_pos
		return result

	def __init__(self, init_pos):
		"""
		Expecting dedicated parameters
		"""

		self.init_pos = init_pos

	@staticmethod
	def expected_signature(new_pos):
		"""
		The signature expected from the combination of __new__ and __init__
		"""

		pass


class FixtureClassWNewAndInitFNew(FancyStuff):
	"""
	Class with __new__ and __init__ (flexible __new__ version)
	"""
	
	def __new__(cls, *args, **kwargs):
		"""
		Completely flexible parameters
		"""
		
		result = super().__new__(cls)
		result.new_args = args
		result.new_kwargs = kwargs
		return result
	
	def __init__(self, foo, /, *, bar):
		"""
		Expecting dedicated parameters
		"""
		
		self.init_foo = foo
		self.init_bar = bar
	
	@staticmethod
	def expected_signature(foo, /, *, bar):
		"""
		The signature expected from the combination of __new__ and __init__
		"""
		
		pass


class FixtureClassWNewAndInitFInit(FancyStuff):
	"""
	Class with __new__ and __init__ (flexible __init__ version)
	"""
	
	def __new__(cls, foo, /, *, bar):
		"""
		Expecting dedicated parameters
		"""
		
		result = super().__new__(cls)
		result.new_foo = foo
		result.new_bar = bar
		return result
	
	def __init__(self, *args, **kwargs):
		"""
		Completely flexible parameters
		"""

		self.init_args = args
		self.init_kwargs = kwargs
	
	@staticmethod
	def expected_signature(foo, /, *, bar):
		"""
		The signature expected from the combination of __new__ and __init__
		"""
		
		pass


class FixtureClassWNewAndInitInvalidPositional(FancyStuff):
	"""
	Class with __new__ and __init__ (invalid positional parameters)
	"""

	def __new__(cls, new_pos, /):
		"""
		Expecting dedicated parameter
		"""

		result = super().__new__(cls)
		result.new_pos = new_pos
		return result

	def __init__(self, new_pos, init_pos, /):
		"""
		Expecting dedicated parameter
		"""

		self.init_pos = init_pos


class FixtureClassWNewAndInitInvalidPositionalOrKeyword(FancyStuff):
	"""
	Class with __new__ and __init__ (invalid positional parameters)
	"""

	def __new__(cls, new_pos):
		"""
		Expecting dedicated parameter
		"""

		result = super().__new__(cls)
		result.new_pos = new_pos
		return result

	def __init__(self, new_pos, init_pos):
		"""
		Expecting dedicated parameter
		"""

		self.init_pos = init_pos


class FixtureClassWNewAndInitInvalidKeyword(FancyStuff):
	"""
	Class with __new__ and __init__ (invalid version)
	"""

	def __new__(cls, *, new_kw):
		"""
		Expecting dedicated parameter
		"""

		result = super().__new__(cls)
		result.new_kw = new_kw
		return result

	def __init__(self, *, init_kw):
		"""
		Expecting dedicated parameter
		"""

		self.init_kw = init_kw


class FixtureClassWMethods(FancyStuff):
	"""
	Class having all kinds of methods
	"""
	
	class_const = 'ultra'

	def __init__(self, init_arg=None):
		"""
		Magic initialization, in case you need to store something.
		"""

		self.init_arg = init_arg
	
	def __call__(self, *args, **kwargs):
		"""
		Calling interface, does little.
		"""
		
		return str(args) + str(kwargs)
	
	def regular_method(self, pos_arg, /):
		"""
		A simple "regular" method.
		"""
		
		return '-'.join(map(str, (self.class_const, self.init_arg, 'bound', pos_arg)))

	@classmethod
	def class_method(cls, pos_arg, /):
		"""
		A simple class method.
		"""
		
		return '-'.join(map(str, (cls.class_const, 'class', pos_arg)))
	
	@staticmethod
	def static_method(pos_arg, /):
		"""
		A simple static method.
		"""
		
		return 'static-' + str(pos_arg)
	
	@staticmethod
	def problematic_static_method(self, second_argument):
		"""
		A static method indistinguishable from a "regular" method.
		"""
		
		raise NotImplementedError('This method would be mis-identified as an instance method')


class FixtureDeepClassL1:
	"""
	Deep class hierarchy. This is level 1.
	"""

	class FixtureDeepClassL2:
		"""
		Deep class hierarchy. This is level 2.
		"""

		class FixtureDeepClassL3(FancyStuff):
			"""
			Deep class hierarchy. This is level 3.
			"""

			def __init__(self, init_arg):
				"""
				Expecting dedicated parameter.
				"""

				self.init_arg = init_arg

			def deep_method(self, pos_arg, /, *, kw_arg):
				"""
				A deep method expecting several parameters.
				"""

				return '-'.join(map(str, (self.init_arg, pos_arg, kw_arg)))