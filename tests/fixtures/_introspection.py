#! python
'''Test fixture module
Simple fixture module for object_metadata.
'''

__version__ = '2.1.3.post3'

def fixture_documented_function(pos1, pos2:bool, /, mult1='mult1', mult2=2, *args, kw1, kw2=False, **kwargs):
		'''Test fixture callable
		A callable test fixture for the object_metadata function.
		
		:param float pos1: First positional test parameter
		:param pos2: Second positional test parameter
		:param mult1: First pos/kw test parameter
		:param mult2: Second pos/kw test parameter with default
		:param args: Any other positional arguments
		:param kw1: First key word test parameter
		:param bool? kw2: Second key word test parameter
		:param kwargs: All other keyword arguments
		:returns None: nothing useful, really
		'''
		
		pass

fixture_documented_function.__version__ = '0.1.3.dev1'

class FixtureDocumentedClass:
	'''Test fixture class
	A class test fixture for the object_metadata function.
	
	:param param1: First positional test parameter
	:param param2: Second positional test parameter
	:returns TestClass: an initialized instance
	'''
	
	__version__ = '2.4.5'
	
	def fixture_documented_instance_method(self, pos1, pos2, /, mult1, mult2, *args, kw1, kw2, **kwargs):
		'''Test fixture callable
		A callable test fixture for the object_metadata function.
		
		:param pos1: First positional test parameter
		:param pos2: Second positional test parameter
		:param mult1: First pos/kw test parameter
		:param mult2: Second pos/kw test parameter with default
		:param args: Any other positional arguments
		:param kw1: First key word test parameter
		:param kw2: Second key word test parameter
		:param kwargs: All other keyword arguments
		:returns bool: Assuming it returns some kind of flag
		'''
		
		pass
	
	@classmethod
	def fixture_documented_class_method(cls, pos1, pos2, /, mult1, mult2, *args, kw1, kw2, **kwargs):
		'''Test fixture callable
		A callable test fixture for the object_metadata function.
		
		:param pos1: First positional test parameter
		:param pos2: Second positional test parameter
		:param mult1: First pos/kw test parameter
		:param mult2: Second pos/kw test parameter with default
		:param args: Any other positional arguments
		:param kw1: First key word test parameter
		:param kw2: Second key word test parameter
		:param kwargs: All other keyword arguments
		:returns bool: Assuming it returns some kind of flag
		'''
		
		pass
	
	@staticmethod	
	def fixture_documented_static_method(pos1, pos2, /, mult1, mult2, *args, kw1, kw2, **kwargs):
		'''Test fixture callable
		A callable test fixture for the object_metadata function.
		
		:param pos1: First positional test parameter
		:param pos2: Second positional test parameter
		:param mult1: First pos/kw test parameter
		:param mult2: Second pos/kw test parameter with default
		:param args: Any other positional arguments
		:param kw1: First key word test parameter
		:param kw2: Second key word test parameter
		:param kwargs: All other keyword arguments
		:returns bool: Assuming it returns some kind of flag
		'''
		
		pass

