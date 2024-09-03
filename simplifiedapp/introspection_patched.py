#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from importlib import import_module
from inspect import isclass
from logging import getLogger

from docstring_parser import parse as docstring_parse
from introspection import BoundArguments, Signature
from introspection.parameter import ParameterKind

LOGGER = getLogger(__name__)

IS_CLASS, IS_FUNCTION, IS_METHOD, IS_MODULE = 'CLASS', 'FUNCTION', 'METHOD', 'MODULE'
IS_CLASS_METHOD, IS_INSTANCE_METHOD, IS_STATIC_METHOD = 'CLASS_METHOD', 'INSTANCE_METHOD', 'STATIC_METHOD'

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

def signature_variable_positional_parameter(self):
	'''
	
	'''
	for parameter in self.parameter_list:
		if parameter.kind == ParameterKind.VAR_POSITIONAL:
			return parameter
	return None
Signature.variable_positional_parameter = property(signature_variable_positional_parameter)

def signature_variable_keyword_parameter(self):
	'''

	'''
	for parameter in self.parameter_list:
		if parameter.kind == ParameterKind.VAR_KEYWORD:
			return parameter
	return None
Signature.variable_keyword_parameter = property(signature_variable_keyword_parameter)


class Callable:
	'''
	
	'''
	
	FORWARD_METADATA = ('name', 'version', 'description', 'long_description')
	
	def __init__(self, callable_):
		'''
		
		'''
		
		if not callable(callable_):
			raise ValueError('The argument provided "{}" is not a callable'.format(callable_))
		
		super().__init__()
		
		self._callable_ = callable_
	
	def __call__(self, *multiple_args_w_keys, **args_w_keys):
		'''Execute the callable
		"Call" this callable with the applicable parameters found in "args_w_keys". The parameters are provided as needed (positionals or as keywords) based on the callable signature.
			'''
		
		if self.type == IS_CLASS:
			raise NotImplementedError('Instantiating classes')
			LOGGER.debug('Instantiating class "%s" with: %s & %s', self.name, args, kwargs)
			result = self._callable_(*args, **kwargs)
		elif self.type in (IS_FUNCTION, IS_STATIC_METHOD, IS_CLASS_METHOD):
			args, kwargs = self.signature.bind(**args_w_keys).to_varargs()
			LOGGER.debug('Running %s "%s" with: %s & %s', str(self.type).lower(), self.name, args, kwargs)
			result = self._callable_(*args, **kwargs)
		elif self.type == IS_INSTANCE_METHOD:
			raise NotImplementedError('Instance method')
		else:
			raise ValueError('Callable type not supported "{}"'.format(self.type))
		return result
	
	def __getattr__(self, item):
		'''
		
		'''
		
		if item == 'metadata':
			value = object_metadata(self._callable_)
		elif item == 'module':
			value = import_module(self._callable_.__module__)
		elif item == 'parents':
			genealogy = self._callable_.__qualname__.split('.')
			if len(genealogy) > 1:
				value = [getattr(self.module, genealogy[0])]
				for parent in genealogy[1:-1]:
					value.append(type(self)(getattr(parents[-1], parent)))
				value.reverse()
			else:
				value = []
		elif item == 'parent':
			value = self.parents[0] if self.parents else None
		elif item in ('signature', 'type'):
			signature, type_ = self._get_signature_detect_type()
			setattr(self, 'signature', signature)
			setattr(self, 'type', type_)
			value = signature if item == 'signature' else type_
		elif (item in self.FORWARD_METADATA) and (item in self.metadata):
			return self.metadata[item]
		else:
			return getattr(self._callable_, item)
			
		setattr(self, item, value)
		return value
	
	def _get_signature_detect_type(self):
		'''
		
		'''
		
		if isclass(self._callable_):
			raise NotImplementedError('Callable being a class')
		elif self.parent is None:
			signature = Signature.from_callable(self._callable_)
			type_ = IS_FUNCTION
		else:
			signature = Signature.for_method(self.parent, self.name)
			type_ = IS_STATIC_METHOD
			if signature.parameter_list:
				if signature.parameter_list[0].name == 'self':
					signature = signature.without_parameters(0)
					type_ = IS_INSTANCE_METHOD
				elif signature.parameter_list[0].name in ('cls', 'type'):
					signature = signature.without_parameters(0)
					type_ = IS_CLASS_METHOD
			
		return signature, type_
	
	@staticmethod
	def _signature_for_class(class_):
		'''

		'''
		
		pass
	def bind(self, *args, **kwargs):
		'''

		'''
		
		fixed_args, fixed_kwargs = [], {}
		for parameter_name, parameter in self.signature.parameters.items():
			if parameter.kind in (ParameterKind.POSITIONAL_ONLY, ParameterKind.POSITIONAL_OR_KEYWORD):
				if len(args):
					fixed_args.append(args.pop(0))
				elif parameter_name in kwargs:
					fixed_args.append(kwargs.pop(parameter_name))
				elif parameter.default == parameter.empty:
					raise TypeError('Missing required {} parameter "{}"'.format(parameter.kind, parameter_name))
				elif self.signature.variable_positional_parameter is not None:
					fixed_args.append(parameter.default)
			elif parameter.kind == ParameterKind.VAR_POSITIONAL:
				if parameter_name in kwargs:
					fixed_args += kwargs.pop(parameter_name)
				if args:
					fixed_args += args
					args = []
			elif parameter.kind == ParameterKind.KEYWORD_ONLY:
				if parameter_name in kwargs:
					fixed_kwargs[parameter_name] = kwargs.pop(parameter_name)
				elif parameter.default == parameter.empty:
					raise TypeError('Missing required keyword only parameter "{}"'.format(parameter_name))
			elif parameter.kind == ParameterKind.VAR_KEYWORD:
				if parameter_name in kwargs:
					fixed_kwargs |= kwargs.pop(parameter_name)
				if kwargs:
					fixed_kwargs |= kwargs
					kwargs = {}
		
		if args:
			LOGGER.warning('Ignoring unused args: %s', args)
		if kwargs:
			LOGGER.warning('Ignoring unused kwargs: %s', kwargs)
		
		return self.signature.bind(*fixed_args, **fixed_kwargs)
	