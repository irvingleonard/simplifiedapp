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

def param_metadata(arg_name, arg_values, annotations, docstring):
	'''Extends argument's values
	Uses the defaults, annotations and docstring to extend the argument values (type, action, etc.)
	
	ToDo:
	- Documentation
	'''

	# arg_values['help'] = 'ToDo: help string not supported yet'

	if arg_name in annotations:
		if isclass(annotations[arg_name]):
			arg_values['type'] = annotations[arg_name]
		elif isinstance(annotations[arg_name], tuple) or isinstance(annotations[arg_name], list):
			arg_values['choices'] = annotations[arg_name]
	elif 'default' in arg_values:
		if arg_values['default'] is None:
			arg_values['default'] = ARGPARSE_SUPPRESS
		elif type(arg_values['default']) != str:
			if isinstance(arg_values['default'], bool):
				if arg_values['default']:
					arg_values['action'] = 'store_false'
				else:
					arg_values['action'] = 'store_true'
			elif isinstance(arg_values['default'], (tuple, list)):
				arg_values['action'] = 'extend' if ADD_ARGUMENT_ACTION_EXTEND else 'append'
				arg_values['default'] = []
				if 'nargs' not in arg_values:
					arg_values['nargs'] = '+'
			elif isinstance(arg_values['default'], dict):
				arg_values['action'] = 'extend' if ADD_ARGUMENT_ACTION_EXTEND else 'append'
				arg_values['nargs'] = '+'
				arg_values['default'] = []
				if 'help' not in arg_values:
					arg_values['help'] = ''
				arg_values['help'] += '(Use the key=value format for each entry)'
			else:
				arg_values['type'] = type(arg_values['default'])

	return arg_values

def callable_args(callable_, from_class = False):
	'''Extract argparse info from callable
	Uses introspection to build a dict out of a callable, usable to build an argparse tree.
	
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
		varargs, varkw = None, None			#Builtin object.__init__ case, where *args and **kwargs are accepted but only through super()
	LOGGER.debug('Callable "%s" yield signature: %s', callable_, dict(zip(('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs', 'kwonlydefaults', 'annotations'),(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations))))

	if from_class:
		is_boundmethod = False
		if len(args):
			if args[0] == 'self':
				is_boundmethod = True
				args.pop(0)
			elif args[0] in ['cls', 'type']:
				args.pop(0)

	if defaults is None:
		defaults = []
	req_args = {arg : {} for arg in args[:len(args) - len(defaults)]}
	# print('Got req_args {} from args {} and defaults {}'.format(req_args, args, defaults))
	opt_args = {arg : {'default' : arg_default} for arg, arg_default in dict(zip(args[-len(defaults):], defaults)).items()}

	if varargs is not None:
		req_args.update({varargs : {'default' : [], 'nargs' : '*'}})

	if kwonlydefaults is not None:
		opt_args.update({arg : {'default' : arg_default} for arg, arg_default in kwonlydefaults.items()})

	if varkw is not None:
		opt_args.update({varkw : {'default' : {}}})

	metadata = object_metadata(callable_)

	arguments = {arg : param_metadata(arg, arg_values, annotations, docstring = '') for arg, arg_values in req_args.items()}
	arguments.update({('-{}' if len(arg) == 1 else '--{}').format(arg) : param_metadata(arg, arg_values, annotations, docstring = '') for arg, arg_values in opt_args.items()})

	arguments[False] = {'__simplifiedapp_' : (callable_, tuple(args), varargs, tuple(kwonlyargs), varkw)}
	if from_class:
		if is_boundmethod:
			arguments[False] = {'__simplifiedapp_' : (metadata['name'], tuple(args), varargs, tuple(kwonlyargs), varkw)}

	arguments[None] = {METADATA_TO_ARGPARSE[key] : value for key, value in metadata.items() if key in METADATA_TO_ARGPARSE}
	if 'version' in metadata:
		arguments['--version'] = {'action' : 'version', 'version' : metadata['version']}

	LOGGER.debug('Generated arguments: %s', arguments)
	return arguments