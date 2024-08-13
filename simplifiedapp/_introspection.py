#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from importlib import import_module
from inspect import getfullargspec, getmembers, getmodule, isclass, ismodule, stack as inspect_stack
from logging import getLogger
from sys import modules

from docstring_parser import parse as docstring_parse

LOGGER = getLogger(__name__)

IS_CLASS, IS_FUNCTION, IS_METHOD, IS_MODULE = 'CLASS', 'FUNCTION', 'METHOD', 'MODULE'
IS_CLASS_METHOD, IS_INSTANCE_METHOD, IS_STATIC_METHOD = 'CLASS_METHOD', 'INSTANCE_METHOD', 'STATIC_METHOD'

def enumerate_object_callables(obj):
	'''Enumerate object functions and classes
	Use instrospection to indentify all the classes and function members of the provided object. It will ignore all dunder methods except for "__call__".
	
	:param obj: the object to find members of
	:returns tuple: the list of functions and the list of classes
	'''
	
	functions, classes = [], []
	for name, attr in getmembers(obj):
		if (name in ('__call__',)) or (name[:2] != '__'):
			if isclass(attr):
				classes.append(attr)
			elif callable(attr):
				functions.append(attr)
	return functions, classes
	
def execute_callable(callable_, args_w_keys={}, parameters=None, callable_metadata=None):
	'''Execute a callable
	"Call" the provided callable with the applicable parameters found in "args_w_keys". The parameters are provided as needed (positionals or as keywords) based on the callable signature.
	'''
	
	callable_type, parent = identify_callable(callable_)
	if callable_metadata is None:
		callable_metadata = object_metadata(callable_)
	
	if callable_type == IS_CLASS:
		if parameters is None:
			parameters = parameters_from_class(callable_)
		args, kwargs = prepare_arguments(parameters=parameters, args_w_keys=args_w_keys)
		LOGGER.debug('Instantiating class "%s" with: %s & %s', callable_metadata['name'], args, kwargs)
		result = callable_(*args, **kwargs)
	elif callable_type == IS_FUNCTION:
		if parameters is None:
			parameters = parameters_from_function(callable_, function_metadata=callable_metadata)
		args, kwargs = prepare_arguments(parameters=parameters, args_w_keys=args_w_keys)
		LOGGER.debug('Running function "%s" with: %s & %s', callable_metadata['name'], args, kwargs)
		result = callable_(*args, **kwargs)
	else:
		parameters, method_type = parameters_from_method(method=callable_, method_metadata=callable_metadata)
		args, kwargs = prepare_arguments(parameters=parameters, args_w_keys=args_w_keys)
		if method_type == IS_INSTANCE_METHOD:
			parent_instance = execute_callable(parent, args_w_keys=args_w_keys)
			instance_method = getattr(parent_instance, callable_metadata['name'])
			LOGGER.debug('Running instance method "%s" with: %s & %s', instance_method.__qualname__, args, kwargs)
			result = instance_method(*args, **kwargs)
		else:
			LOGGER.debug('Running %s "%s" with: %s & %s', method_type, callable_metadata['name'], args, kwargs)
			result = callable_(*args, **kwargs)
	
	return result

def get_target(target=None):
	'''Figure out the target and its type
	Use introspection to find the caller. It wouldn't be the caller to this function but the caller to this function's caller or whatever is passed as parameter. It also figures out if it's a module, a class, or a function

	:param target: Optionally pass the target (just passthrough) or a string to resolve
	:returns tuple: the target and the corresponding IS_FUNCTION, IS_CLASS, or IS_MODULE
	'''

	caller = inspect_stack()
	if len(caller) < 2:
		caller = None
	else:
		caller = getmodule(caller[2][0])
		LOGGER.debug('Got caller: %s', caller)

	if target is None:
		if caller is None:
			raise RuntimeError('Unsupported shallow call to "get_target" without a target')
		else:
			LOGGER.debug('Target not defined, using caller "%s" as target', caller)
			target = caller
	elif isinstance(target, str):
		LOGGER.debug('Identifying string defined target: %s', target)
		if target in modules:
			LOGGER.debug('Target is a loaded module: %s', target)
			target = modules[target]
		elif hasattr(caller, target):
			LOGGER.debug('Target is a member of caller: %s.%s', caller, target)
			target = getattr(caller, target)
		else:
			try:
				target = import_module(target)
				LOGGER.debug('Target is a loadable module: %s', target)
			except ModuleNotFoundError:
				raise ValueError('Target "{}" could not be identified'.format(target))
	else:
		LOGGER.debug('Target is an object: %s', target)

	try:
		if ismodule(target):
			target_type = IS_MODULE
		elif isclass(target):
			target_type = IS_CLASS
		else:
			target_type = IS_FUNCTION
	except Exception as error:
		raise ValueError('Target ({}) is not supported: {}'.format(target, error))

	return target, target_type

def identify_callable(callable_):
	'''Identify a callable
	Detects if a callable is a class, a class/instance/static method, or a function. For methods and deep classes it also returns the parent class.
	
	:param callable_: the callable that needs to be identified
	:returns tuple: the "callable type" and its parent. The callable type will be one of: IS_CLASS, IS_FUNCTION, IS_METHOD.
	'''
	
	if not callable(callable_):
		raise ValueError('The argument provided "{}" is not a callable'.format(callable_))
	
	genealogy = callable_.__qualname__.split('.')
	if len(genealogy) == 1:
		parent = None
	elif len(genealogy) > 1:
		module = import_module(callable_.__module__)
		parents = [getattr(module, genealogy[0])]
		for parent in genealogy[1:-1]:
			parents.append(getattr(parents[-1], parent))
		parent = parents[-1]
	else:
		raise NotImplementedError('Got callable with no __qualname__ "{}"'.format(callable_))
	
	if isclass(callable_):
		callable_type = IS_CLASS
	elif parent is None:
		callable_type = IS_FUNCTION
	else:
		callable_type = IS_METHOD
	
	return callable_type, parent

def object_metadata(obj):
	'''Gets metadata from an object
	It tries to get some meta information from the provided object by leveraging the object's details (name and version) and whatever can be learned from the docstring.

	:param obj: The object to build the metadata for
	:returns dict: dictionary containing metadata details
	'''

	DOCSTRING_PARAM_ATTRS = ('default', 'description', 'is_optional', 'type_name')
	DOCSTRING_RETURN_ATTRS = ('description', 'is_generator', 'return_name', 'type_name')

	metadata = {'name' : obj.__name__}

	if hasattr(obj, '__version__'):
		metadata['version'] = obj.__version__

	if hasattr(obj, '__doc__') and (obj.__doc__ is not None) and len(obj.__doc__):
		docstring = (docstring_parse(obj.__doc__))
		if docstring.short_description:
			metadata['description'] = docstring.short_description
		if docstring.long_description:
			metadata['long_description'] = docstring.long_description
		if len(docstring.params):
			docstring_params = {}
			for param in docstring.params:
				docstring_param = {}
				for param_attr in DOCSTRING_PARAM_ATTRS:
					docstring_param_attr = getattr(param, param_attr)
					if docstring_param_attr is not None:
						docstring_param[param_attr] = docstring_param_attr
				docstring_params[param.arg_name] = docstring_param
			metadata['parameters'] = docstring_params
		if docstring.returns:
			docstring_return = {}
			for return_attr in DOCSTRING_RETURN_ATTRS:
				docstring_return_attr = getattr(docstring.returns, return_attr)
				if docstring_return_attr is not None:
					docstring_return[return_attr] = docstring_return_attr
			metadata['returns'] = docstring_return

	return metadata

def parameters_from_callable(callable_, callable_metadata=None):
	'''
	
	'''
	
	callable_type, parent = identify_callable(callable_)
	if callable_type == IS_CLASS:
		parameters = parameters_from_class(callable_)
	elif callable_type == IS_FUNCTION:
		parameters = parameters_from_function(callable_, function_metadata=callable_metadata)
	else:
		parameters, method_type = parameters_from_method(method=callable_, method_metadata=callable_metadata)
	
	return parameters

def parameters_from_class(class_):
	'''Class parameters details
	Uses introspection to extract the parameters required/allowed by class and as much details as possible from them. This is trickier and different from the method version because class instantiation includes a call to __new__ and another to __init__ each of which could require different combination of parameters.
	'''
	
	parameters, kw_parameters, new_varargs, new_varkw = {}, {}, None, None
	parameters_new, new_is_static = parameters_from_method(class_.__new__)
	for parameter, details in parameters_new.items():
		if ('positional' in details) and details['positional']:
			if ('special' in details) and (details['special'] == 'varargs'):
				new_varargs = parameter
			parameters[parameter] = details
		elif ('special' in details) and (details['special'] == 'varkw'):
			new_varkw = parameter
		else:
			kw_parameters[parameter] = details
	
	init_varargs, init_varkw = None, None
	parameters_init, init_is_bound = parameters_from_method(class_.__init__)
	for parameter, details in parameters_init.items():
		if ('positional' in details) and details['positional']:
			if ('special' in details) and (details['special'] == 'varargs'):
				init_varargs = parameter
			if parameter not in parameters:
				parameters[parameter] = details
			else:
				LOGGER.debug('Parameter used by __new__ and __init__: %s | %s', parameter, details)
		elif ('special' in details) and (details['special'] == 'varkw'):
			init_varkw = parameter
		else:
			if parameter not in kw_parameters:
				kw_parameters[parameter] = details
			else:
				LOGGER.debug('Parameter used by __new__ and __init__: %s | %s', parameter, details)
	
	if init_varargs is not None:
		parameters[init_varargs] = parameters_init[init_varargs]
	elif new_varargs is not None:
		parameters[new_varargs] = parameters_new[new_varargs]
	
	if init_varkw is not None:
		kw_parameters[init_varkw] = parameters_init[init_varkw]
	elif new_varkw is not None:
		kw_parameters[new_varkw] = parameters_new[new_varkw]
		
	return parameters | kw_parameters

def parameters_from_function(function_, function_metadata=None, from_class=False):
	'''Function parameters details
	Uses introspection to extract the parameters required/allowed by a function and as much details as possible from them.
	
	:param obj function_: the function to process
	:param dict? function_metadata: a mapping with the details of the function as returned by "object_metadata"
	:param bool? from_class: a flag signaling that it should be treated as a method
	:returns dict: a mapping of parameters and details
	'''
	
	try:
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(function_)
	except TypeError:
		LOGGER.debug('Signature inspect failed. Using generic signature for callable: %s', function_)
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = [], 'args', 'kwargs', None, [], None, {}	#Generic signature: just args and kwargs, whatever you pass will be.
		if from_class:
			args = ['self']	# Default will be bound method
	
	if function_ in [object.__init__, object.__new__]:
		#Builtin object.__init__ case, where *args and **kwargs are accepted but only through super()
		#Builtin object.__new__ simply forwards whatever is passed as *args and **kwargs to __init__. You should get the list of parameters from that one instead.
		varargs, varkw = None, None
	
	LOGGER.debug('Function "%s" yield signature: %s' % (function_, dict(zip(('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs', 'kwonlydefaults', 'annotations'),(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations)))))
	
	if defaults is None:
		defaults = []
	if kwonlydefaults is None:
		kwonlydefaults = {}
	
	parameters = {arg : {'positional' : True} for arg in args[:len(args)-len(defaults)]}
	for i in range(len(defaults)):
		parameters[args[-len(defaults)+i]] = {'default' : defaults[i], 'positional' : True}
	if varargs is not None:
		parameters[varargs] = {'default' : [], 'positional' : True, 'special' : 'varargs'}
	parameters.update({kwarg : {'default' : kwonlydefaults[kwarg], 'positional' : False} if kwarg in kwonlydefaults else {'positional' : False} for kwarg in kwonlyargs})
	if varkw is not None:
		parameters[varkw] = {'default' : {}, 'positional' : False, 'special' : 'varkw'}
	
	for param, annotation in annotations.items():
		parameters[param]['annotation'] = annotation

	if function_metadata is None:
		function_metadata = object_metadata(function_)
	if 'parameters' in function_metadata:
		for param, docstring in function_metadata['parameters'].items():
			if param not in parameters:
				LOGGER.warning('Docstring references a missing parameter: %s', param)
			else:
				parameters[param]['docstring'] = docstring
			
	return parameters

def parameters_from_method(method, method_metadata=None):
	'''Method parameters details
	Uses introspection to extract the parameters required/allowed by method and as much details as possible from them. Also returns the type of method (bound, class, static)
	'''

	parameters = parameters_from_function(method, function_metadata=method_metadata, from_class=True)
	method_type = IS_STATIC_METHOD
	if len(parameters):
		first_param = tuple(parameters.keys())[0]
		if first_param == 'self':
			del parameters[first_param]
			method_type = IS_INSTANCE_METHOD
		elif first_param in ['cls', 'type']:
			del parameters[first_param]
			method_type = IS_CLASS_METHOD

	return parameters, method_type

def prepare_arguments(parameters, args_w_keys={}):
	'''Prepare arguments for callable
	Create the list of "args" and the mapping of "kwargs" to be used with a callable.

	:param dict parameters: A mapping of parameters and details, as returned from "parameters_from_callable"
	:param dict args_w_keys: A mapping of parameters and values to be added to args and kwargs
	:returns tuple: positional arguments "args" and keyword arguments "kwargs"
	'''
	
	args, kwargs = [], {}
	for parameter, details in parameters.items():
		if ('positional' in details) and details['positional']:
			if ('special' in details) and (details['special'] == 'varargs'):
				if parameter in args_w_keys:
					args += args_w_keys[parameter]
			elif parameter in args_w_keys:
				args.append(args_w_keys[parameter])
			elif 'default' in details:
				args.append(details['default'])
			else:
				raise ValueError('Missing value for parameter "{}"'.format(parameter))
		elif ('special' in details) and (details['special'] == 'varkw'):
			if parameter in args_w_keys:
				kwargs |= args_w_keys[parameter]
		elif parameter in args_w_keys:
			kwargs[parameter] = args_w_keys[parameter]
		elif 'default' in details:
			kwargs[parameter] = details['default']
		else:
			raise ValueError('Missing value for parameter "{}"'.format(parameter))

	return args, kwargs
