#python
'''Function fixtures
Collection of functions with different parameter combinations. Also includes a versioned function.
'''

def fixture_empty_function():
	'''Empty function
	A function without parameters
	
	:returns bool: always True
	'''
	
	return True

def fixture_function_w_positional_args(a, b, /):
	'''
	'''
	pass

def fixture_function_w_mixed_args(a, b, c, d):
	'''
	'''
	pass

def fixture_function_w_varargs(*args):
	'''
	'''
	pass

def fixture_function_w_keyword_args(*, c, d):
	'''
	'''
	pass

def fixture_function_w_varkw(**kwargs):
	'''
	'''
	pass

def fixture_function_w_default_positional_args(a, b=2, /):
	'''
	'''
	pass

def fixture_function_w_default_mixed_args(a, b, c=False, d=4):
	'''
	'''
	pass

def fixture_function_w_default_keyword_args(*, c, d=True):
	'''
	'''
	pass

def fixture_function_w_version():
	'''Versioned function
	Function with version attribute set
	'''
	pass
fixture_function_w_version.__version__ = '0.1'

def fixture_function_w_all_parameter_combinations(
	pos_req,
	pos_def_none=None,
	pos_def_str='a_str',
	pos_def_bool=False,
	/,
	pos_def_list=['as', 1, True],
	pos_def_dict={'dct' : 6, 'fer' : False, 1 : 'one'},
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
	'''A "complex" function
	Covering as much parameter combinations as possible
	
	:returns str: cast every parameter into string and concatenates them
	'''
	
	data = (pos_req, pos_def_none, pos_def_str, pos_def_bool, pos_def_list, pos_def_dict, pos_def_num, more_pos, kw_req, kw_def_none, kw_def_str, kw_def_bool, kw_def_list, kw_def_dict, kw_def_num, more_kw)
	
	return ''.join(map(str, data))
	