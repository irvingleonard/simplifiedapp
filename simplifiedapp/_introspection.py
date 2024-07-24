#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from argparse import SUPPRESS as ARGPARSE_SUPPRESS
from inspect import getfullargspec, isclass
from logging import getLogger

from docstring_parser import parse as docstring_parse

LOGGER = getLogger(__name__)

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

def parameters_from_callable(callable_, callable_metadata=None, from_class=False):
	'''Callable parameters details
	Uses introspection to extract the parameters required/allowed by callable and as much details as possible from them.
	
	ToDo:
	- Documentation
	'''
	
	try:
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(callable_)
	except TypeError:
		LOGGER.debug('Signature inspect failed. Using generic signature for callable: %s', callable_)
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = [], 'args', 'kwargs', None, [], None, {}	#Generic signature: just args and kwargs, whatever you pass will be.
		if from_class:
			args = ['self']	# Default will be bound method
	
	if from_class and (callable_ is object.__init__):
		#Builtin object.__init__ case, where *args and **kwargs are accepted but only through super()
		varargs, varkw = None, None
	
	LOGGER.debug('Callable "%s" yield signature: %s' % (callable_, dict(zip(('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs', 'kwonlydefaults', 'annotations'),(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations)))))
	
	if defaults is None:
		defaults = []
	if kwonlydefaults is None:
		kwonlydefaults = {}
	
	parameters = {arg : {'positional' : True} for arg in args[:len(args)-len(defaults)]}
	for i in range(len(defaults)):
		parameters[args[-len(defaults)+i]] = {'default' : defaults[i], 'positional' : True}
	if varargs is not None:
		parameters[varargs] = {'default' : (), 'positional' : True}
	parameters.update({kwarg : {'default' : kwonlydefaults[kwarg], 'positional' : False} if kwarg in kwonlydefaults else {'positional' : False} for kwarg in kwonlyargs})
	if varkw is not None:
		parameters[varkw] = {'default' : {}, 'positional' : False}
	
	for param, annotation in annotations.items():
		parameters[param]['annotation'] = annotation
		
	if (callable_metadata is not None) and ('parameters' in callable_metadata):
		for param, docstring in callable_metadata['parameters'].items():
			if param not in parameters:
				LOGGER.warning('Docstring references a missing parameter: %s', param)
			else:
				parameters[param]['docstring'] = docstring
			
	return parameters

