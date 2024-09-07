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
from introspection import Signature
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

Signature._replace_original = Signature.replace
def signature_replace(self, *args, **kwargs):
	'''Enhance upstream replace
	The original "replace" method doesn't take into account the "forward_ref_context" attribute which means that any signature "replaced" will be an incomplete "introspection.Signature" object.
	'''
	result = self._replace_original(*args, **kwargs)
	result.forward_ref_context = self.forward_ref_context
	return result
Signature.replace = signature_replace

def signature_variable_positional_parameter(self):
	'''Variable positional parameter
	Returns the variable positional parameter or None (read only property)
	'''
	for parameter in self.parameter_list:
		if parameter.kind == ParameterKind.VAR_POSITIONAL:
			return parameter
	return None
Signature.variable_positional_parameter = property(signature_variable_positional_parameter)

def signature_variable_keyword_parameter(self):
	'''Variable keyword parameter
	Returns the variable keyword parameter or None (read only property)
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
	'''Callable types
	List of callable types identified by the module so far
	'''
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
	'''Describe a callable
	This is mostly about "executing"/"running" the callable. It requires a lot of processing based on all the possible "things" that are callables.
	'''
	
	FORWARD_METADATA = ('name', 'version', 'description', 'long_description')
	
	def __init__(self, callable_, warn_extra_args=True):
		'''Magic initialization
		Check that the provided "callable_" is actually callable and store it.
		
		:param callable_: The callable that will be handled by the class
		:returns None: init shouldn't return anything
		'''
		
		if not callable(callable_):
			raise ValueError('The argument provided "{}" is not a callable'.format(callable_))
		
		super().__init__()
		
		self._callable_ = callable_
		self._warn_extra_args = warn_extra_args
	
	def __call__(self, *multiple_args_w_keys, **args_w_keys):
		'''Execute the callable
		"Call" this callable with the applicable parameters found in "args_w_keys". The parameters are provided as needed (positionals or as keywords) based on the callable signature.
		
		:param multiple_args_w_keys: a couple (just 2) positional arguments that should be dicts used only when the callable is an instance method; the first one will be used to instantiate the parent class and the second will be used to execute the actual method
		:param args_w_keys: The arguments to execute the callable with. For instance methods it can be used for shared arguments; it will be used for the class and the method updated by the dicts in multiple_args_w_keys if provided.
		:returns Any: the result of "running" this callable with the provided parameters
		'''
		
		if self.type == CallableType['INSTANCE_METHOD']:
			if len(multiple_args_w_keys) == 2:
				parent_args_w_keys, callable_args_w_keys = multiple_args_w_keys
				parent_args_w_keys = args_w_keys | parent_args_w_keys
				callable_args_w_keys = args_w_keys | callable_args_w_keys
			elif not multiple_args_w_keys:
				parent_args_w_keys = callable_args_w_keys = args_w_keys
			else:
				raise TypeError('Invalid arguments for instance method')
			
			parent_args, parent_kwargs = type(self)(self.parent).bind(**parent_args_w_keys)
			parent_instance = self.parent(*parent_args, **parent_kwargs)
			
			callable_args, callable_kwargs = self.bind(**callable_args_w_keys)
			callable_method = getattr(parent_instance, self.name)
			return callable_method(*callable_args, **callable_kwargs)
		
		elif multiple_args_w_keys:
			LOGGER.warning('Ignoring positional arguments provided for callable that is not an instance method: %s', multiple_args_w_keys)
		
		args, kwargs = self.bind(**args_w_keys)
		return self._callable_(*args, **kwargs)
	
	def __getattr__(self, item):
		'''Lazy instantiation
		Wait until they're needed before resolving potentially costly attributes.
		
		It will set the attribute to the object so this will only be run at most once for each missing attribute.
		
		Some attributes are forwarded to the metadata dict, which are controlled by "self.FORWARD_METADATA".
		
		If the attribute request is not found here or forwarded to the metadata, then it's forwarded to the stored "callable"
		
		:param str item: The name of the attribute that is missing
		:returns Any: the value of such attribute
		'''
		
		if item == 'is_method':
			value = ismethod(self._callable_)
		elif item == 'metadata':
			value = object_metadata(self._callable_)
		elif item == 'module':
			value = import_module(self._callable_.__module__)
		elif item == 'parents':
			genealogy = self._callable_.__qualname__.split('.')
			#AFAIK there's no way to resolve the local context of a function short of evaluating/running it.
			if (len(genealogy) > 1) and ('<locals>' not in genealogy):
				value = [getattr(self.module, genealogy[0])]
				for parent in genealogy[1:-1]:
					value.append(getattr(value[-1], parent))
				value.reverse()
			else:
				value = []
		elif item == 'parent':
			if hasattr(self._callable_, '__self__'):
				value = self._callable_.__self__
			elif self.parents:
				value = self.parents[0]
			else:
				value = None
		elif item in ('signature', 'type'):
			signature, type_ = self._get_signature_detect_type()
			if item == 'signature':
				value = signature
				setattr(self, 'type', type_)
			else:
				value = type_
				setattr(self, 'signature', signature)
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
		
		Had been unable to find a way to tell a static method from an instance method apart while on a class definition. Best solution so far is to rely on the first parameter being "self". Having a static method with a first parameter called "self" (perfectly valid code) will break this logic.
		
		:returns tuple: two items tuple, with the signature in the first position and the type on the second
		'''
		
		if isclass(self._callable_):
			signature = self._signature_for_class(self._callable_)
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
			type_ = CallableType['BOUND_METHOD']
				
		return signature, type_
	
	@staticmethod
	def _signature_for_class(class_):
		'''Get the signature for the provided class
		Instantiating a class requires the execution of two different methods with the very same arguments. The signature for such "call" would be the merger of the signature of both methods.
		
		Sadly, although the upstream Signature objects claim that they "support anything callable" they choke when getting the signature of a class that defines both methods (__new__ and __init__).
		
		:param class_: The class to get the signature for
		:returns Signature: the calculated signature for the class
		'''
		
		pos_params, varargs, kw_params, varkw = [], [], [], []
		new_method = getattr(class_, '__new__')
		if new_method is not object.__new__:
			new_signature = Signature.from_callable(new_method).without_first_parameter()
			for parameter in new_signature.parameter_list:
				if parameter.kind in (ParameterKind.POSITIONAL_ONLY, ParameterKind.POSITIONAL_OR_KEYWORD):
					pos_params.append(parameter)
				elif parameter.kind == ParameterKind.KEYWORD_ONLY:
					kw_params.append(parameter)
			new_varargs, new_varkw = new_signature.variable_positional_parameter, new_signature.variable_keyword_parameter
			if new_varargs is not None:
				varargs = [new_varargs]
			if new_varkw is not None:
				varkw = [new_varkw]
		
		init_method = getattr(class_, '__init__')
		if init_method is not object.__init__:
			init_signature = Signature.from_callable(init_method).without_first_parameter()
			for parameter in init_signature.parameter_list:
				if (parameter.kind in (ParameterKind.POSITIONAL_ONLY, ParameterKind.POSITIONAL_OR_KEYWORD)) and (parameter not in pos_params):
					pos_params.append(parameter)
				elif (parameter.kind == ParameterKind.KEYWORD_ONLY) and (parameter not in kw_params):
					kw_params.append(parameter)
			if new_method is object.__new__:
				init_varargs, init_varkw = init_signature.variable_positional_parameter, init_signature.variable_keyword_parameter
				if init_varargs is not None:
					varargs = [init_varargs]
				if init_varkw is not None:
					varkw = [init_varkw]
		
		return Signature(parameters=pos_params+varargs+kw_params+varkw, forward_ref_context=class_.__module__)
	
	def bind(self, *args, **kwargs):
		'''Get the "args" list and the "kwargs" dict for the callable signature
		Another implementation of bind, sadly, neither "introspection.Signature.bind" nor "inspect.Signature.bind" methods are very helpful for this use case. The "BoundArguments" versions are not completely there either. Instead, wrote the "goal" of all those into this method and called it a day.
		
		For parameters that could be passed as positional or keyword this method will always use the positional option, makes things simpler. Missing required parameters will raise a TypeError. Unused arguments will yield logging warnings.
		
		:param args: The positional arguments to be used to bind to the signature
		:param kwargs: The keyword arguments to be used to bind to the signature
		:returns Any: the value of such attribute
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
		
		if self._warn_extra_args:
			if args:
				LOGGER.warning('Ignoring unused args: %s', args)
			if kwargs:
				LOGGER.warning('Ignoring unused kwargs: %s', kwargs)
		
		return tuple(fixed_args), fixed_kwargs
	