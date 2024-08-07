#python
'''
'''

class FancyStuff:
	'''
	'''
	
	def __repr__(self):
		return str(vars(self))
	
	def __eq__(self, other):
		return vars(self) == vars(other)


class FixtureEmptyClass(FancyStuff):
	'''
	'''
	
	pass


class FixtureClassWNew(FancyStuff):
	'''
	'''
	
	def __new__(cls, new_pos, /, *, new_kw):
		'''
		'''
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.new_kw = new_kw
		return result


class FixtureClassWInit(FancyStuff):
	'''
	'''
	
	def __init__(self, init_pos, /, *, init_kw):
		'''
		'''
		
		self.init_pos = init_pos
		self.init_kw = init_kw


class FixtureClassWNewAndInit(FancyStuff):
	'''
	'''
	
	def __new__(cls, new_pos, /, *args, new_kw, **kwargs):
		'''
		'''
		
		result = super().__new__(cls)
		result.new_pos = new_pos
		result.new_kw = new_kw
		return result
	
	def __init__(self, init_pos, /, *args, init_kw, **kwargs):
		'''
		'''
		
		self.init_pos = init_pos
		self.init_kw = init_kw


class FixtureClassWMethods(FancyStuff):
	'''
	'''
	
	class_const = 'ultra'
	def __init__(self, init_arg):
		self.init_arg = init_arg
	
	def bound_method(self, pos_arg, /):
		'''
		'''
		
		return '-'.join(map(str, (self.class_const, self.init_arg, 'bound', pos_arg)))

	@classmethod
	def class_method(cls, pos_arg, /):
		'''
		'''
		
		return '-'.join(map(str, (cls.class_const, 'class', pos_arg)))
	
	@staticmethod
	def static_method(pos_arg, /):
		'''
		'''
		
		return 'static-' + str(pos_arg)


class FixtureDeepClassL1:
	class FixtureDeepClassL2:
		class FixtureDeepClassL3(FancyStuff):
			
			def __init__(self, init_arg):
				self.init_arg = init_arg
			def deep_method(self, pos_arg, /, kw_arg):
				return '-'.join(map(str, (self.init_arg, pos_arg, kw_arg)))