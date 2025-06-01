#python
"""Function fixtures
Collection of functions with different parameter combinations. Also includes a versioned function.
"""

def fixture_empty_function():
	"""Empty function
	A function without parameters
	
	:returns bool: always True
	"""
	
	return True

def fixture_function_w_positional_args(a, b, /):
	"""
	A function expecting positional parameters
	"""

	pass

def fixture_function_w_positional_args_defaults(a=1, b=2, /):
	"""
	A function accepting positional parameters
	"""

	pass

def fixture_function_w_mixed_args(a, b, /, c, *, d):
	"""
	A function expecting all kinds of parameters
	"""

	pass

def fixture_function_w_varargs(*args):
	"""
	A function accepting a variable number of positional (or positional-or-keyword) parameters
	"""

	pass

def fixture_function_w_keyword_args(*, c, d):
	"""
	A function expecting keyword parameters
	"""

	pass

def fixture_function_w_keyword_args_default(*, c=3, d=4):
	"""
	A function accepting keyword parameters
	"""

	pass

def fixture_function_w_varkw(**kwargs):
	"""
	A function accepting a variable number of keyword parameters
	"""

	pass

def fixture_function_w_default_positional_args(a, b=2, /):
	"""
	"""
	pass

def fixture_function_w_default_mixed_args(a, b, c=False, d=4):
	"""
	"""
	pass

def fixture_function_w_default_keyword_args(*, c, d=True):
	"""
	"""
	pass

def fixture_function_w_version():
	"""Versioned function
	Function with version attribute set
	"""
	pass
fixture_function_w_version.__version__ = '0.1'

def fixture_function_w_all_parameter_combinations(
	pos_req,
	pos_def_none=None,
	pos_def_str='a_str',
	pos_def_bool=False,
	/,
	pos_def_list=['as', 1, True],
	pos_def_dict={1: 'one', 'dct': 6, 'fer': False},
	pos_def_num=2.3,
	*more_pos,
	kw_req,
	kw_def_none=None,
	kw_def_str='another_str',
	kw_def_bool=True,
	kw_def_list=[1, 'tre', 6.7],
	kw_def_dict={1 : 'dfe', 'yufgb': 'sdqwda'},
	kw_def_num=(8+98j),
	**more_kw
):
	"""A "complex" function
	Covering as much parameter combinations as possible
	
	:returns str: cast every parameter into string and concatenates them
	"""
	
	data = (pos_req, pos_def_none, pos_def_str, pos_def_bool, pos_def_list, pos_def_dict, pos_def_num, more_pos, kw_req, kw_def_none, kw_def_str, kw_def_bool, kw_def_list, kw_def_dict, kw_def_num, more_kw)
	
	return ''.join(map(str, data))
	
def fixture_nested_functions_outer():
	"""
	Couple of nested functions (like a decorator). This is the outer one.
	"""
	
	def fixture_nested_functions_inner():
		"""
		Couple of nested functions (like a decorator). This is the inner one.
		"""
		
		pass
	
	return fixture_nested_functions_inner