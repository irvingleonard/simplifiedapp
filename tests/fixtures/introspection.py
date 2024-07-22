#! python
'''Test fixture module
Simple fixture module for object_metadata.
'''

__version__ = '2.1.3.post3'

def test_callable(pos1, pos2:bool, /, mult1='mult1', mult2=2, *args, kw1, kw2=False, **kwargs):
		'''Test fixture callable
		A callable test fixture for the object_metadata function.
		
		:param float pos1: First positional test parameter
		:param pos2: Second positional test parameter
		:param mult1: First pos/kw test parameter
		:param mult2: Second pos/kw test parameter with default
		:param kw1: First key word test parameter
		:param bool? kw2: Second key word test parameter
		:returns None: nothing useful, really
		'''
		
		pass

test_callable.__version__ = '0.1.3.dev1'


class TestClass:
	'''Test fixture class
	A class test fixture for the object_metadata function.
	
	:param param1: First positional test parameter
	:param param2: Second positional test parameter
	:returns TestClass: an initialized instance
	'''
	
	__version__ = '2.4.5'
	
	pass

