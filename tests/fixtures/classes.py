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


class FixtureDeepClassL1:
	class FixtureDeepClassL2:
		class FixtureDeepClassL3:
			pass