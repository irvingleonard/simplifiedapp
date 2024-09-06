#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from enum import Enum
from importlib import import_module
from inspect import isclass, ismethod
from logging import getLogger
from types import FunctionType, MethodType

from docstring_parser import parse as docstring_parse
from introspection import BoundArguments, Signature
from introspection.parameter import ParameterKind

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

def signature_without_first_parameter(self):
	'''Same signature without the first parameter
	Basically it should be the same as "Signature.without_parameters(0)" but for whatever reason that doesn't achieve the same result.
	'''
	if self.parameters:
		return self.replace(parameters=list(self.parameters.values())[1:])
	else:
		LOGGER.warning('No parameter to remove')
		return self
Signature.without_first_parameter = signature_without_first_parameter


class CallableType(Enum):
	CLASS = 'CLASS'
	INSTANCE = 'INSTANCE'
	FUNCTION = 'FUNCTION'
	METHOD = 'METHOD'
	MODULE = 'MODULE'
	BOUND_METHOD = 'BOUND_METHOD'
	CLASS_METHOD = 'CLASS_METHOD'
	INSTANCE_METHOD = 'INSTANCE_METHOD'
	STATIC_METHOD = 'STATIC_METHOD'
	
	
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
		
		if self.type == CallableType['CLASS']:
			raise NotImplementedError('Instantiating classes')
			LOGGER.debug('Instantiating class "%s" with: %s & %s', self.name, args, kwargs)
			result = self._callable_(*args, **kwargs)
		elif self.type in (CallableType['FUNCTION'], CallableType['STATIC_METHOD'], CallableType['CLASS_METHOD']):
			args, kwargs = self.signature.bind(**args_w_keys).to_varargs()
			LOGGER.debug('Running %s "%s" with: %s & %s', str(self.type).lower(), self.name, args, kwargs)
			result = self._callable_(*args, **kwargs)
		elif self.type == CallableType['INSTANCE_METHOD']:
			raise NotImplementedError('Instance method')
		else:
			raise ValueError('Callable type not supported "{}"'.format(self.type))
		return result
	
	def __getattr__(self, item):
		'''Lazy instantiation
		Wait until they're needed before resolving potentially costly attributes.
		'''
		
		if item == 'is_method':
			value = ismethod(self._callable_)
		elif item == 'metadata':
			value = object_metadata(self._callable_)
		elif item == 'module':
			value = import_module(self._callable_.__module__)
		elif item == 'parents':
			genealogy = self._callable_.__qualname__.split('.')
			#AFAIK there's no way to resolve the local context of a function: meaning that there's no way to "resolve" the locally defined function short of running the outer one.
			if (len(genealogy) > 1) and ('<locals>' not in genealogy):
				value = [getattr(self.module, genealogy[0])]
				for parent in genealogy[1:-1]:
					value.append(getattr(value[-1], parent))
				value.reverse()
			else:
				value = []
		elif item == 'parent':
			# if hasattr(self._callable_, '__self__')
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
		'''Detect the type of callable, produce a signature, and signal the type
		
		There are at least 7 different possible callables:
		- run of the mill function, a plain 'ol regular function, which would yield the regular signature and an "FUNCTION" type
		- class, which would combine the signatures of its "__new__" and "__init__" methods and a type of "CLASS"
		- a class method, where the first parameter is a "type" (called "cls" by regular convention) which will be removed from the signature and a type of "CLASS_METHOD"
		- a static method, which is very similar to the regular function, only that it's a member of the class, will yield the regular method signature and a type of "STATIC_METHOD"
		- a class instance supporting the "__call__" protocol, which would yield the signature of its "__call__" method without the first parameter ("self", by convention) and a type of "INSTANCE"
		- an instance method from a live instance, will yield a method signature without the first parameter ("self" by convention) and a type of "BOUND_METHOD"
		- an instance method from the original class. Although it's still a callable, it couldn't be executed without creating an instance of the class first. It would yield a method signature without the first parameter ("self" by convention) and a type of "INSTANCE_METHOD"
		
		:returns tuple: two items tuple, with the signature in the first position and the type on the second
		'''
		
		if isclass(self._callable_):
			raise NotImplementedError('Callable being a class')
			new_signature = Signature.for_method(self._callable_, '__new__')
			init_signature = Signature.for_method(self._callable_, '__init__')
			#TODO: merge the new and init signatures
			type_ = CallableType['CLASS']
		elif not isinstance(self._callable_, (FunctionType, MethodType)):
			signature = Signature.from_callable(self._callable_.__call__)
			type_ = CallableType['INSTANCE']
		elif self.parent is None:
			signature = Signature.from_callable(self._callable_)
			type_ = CallableType['FUNCTION']
		elif isclass(self.parent):
			signature = Signature.for_method(self.parent, self.name)
			type_ = CallableType['STATIC_METHOD']
			if ismethod(self._callable_):
				signature = signature.without_first_parameter()
				type_ = CallableType['CLASS_METHOD']
			elif signature.parameter_list and (signature.parameter_list[0].name == 'self'):
				LOGGER.warning('Assuming instance method on a class definition based on the first parameter: "self"')
				signature = signature.without_first_parameter()
				type_ = CallableType['INSTANCE_METHOD']
		else:
			signature = Signature.from_callable(getattr(self.parent, self.name))
			class_version = getattr(type(self.parent), self.name)
			if self.is_method and ismethod(class_version):
				signature = signature.without_first_parameter()
				type_ = CallableType['CLASS_METHOD']
			elif self.is_method:
				signature = signature.without_first_parameter()
				type_ = CallableType['BOUND_METHOD']
			else:
				print('Signature is: ', signature.parameters)
				type_ = CallableType['STATIC_METHOD']
				
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
	