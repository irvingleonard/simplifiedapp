#!python
"""

"""

from importlib import import_module
from inspect import getmembers, getmodule, isclass, stack as inspect_stack
from logging import getLogger
from sys import modules

from .argparse_patched import argparse
from ._defaults import LocalFormatterClass
from .introspection_patched import object_metadata, Callable, CallableType, ParameterKind

LOGGER = getLogger(__name__)

def list_callable_children(object_, /):
	"""Enumerate this callable's functions and classes
	Use introspection to indentify all the classes and function members of this callable. It will ignore all dunder methods except for "__call__".

	:returns tuple: the list of functions and the list of classes
	"""

	functions, classes = [], []
	for name, attr in getmembers(object_):
		if (name in ('__call__',)) or (name[:2] != '__'):
			if isclass(attr):
				classes.append(attr)
			elif callable(attr):
				functions.append(attr)
	return functions, classes


def get_target(target=None, /, depth=1):
	"""Figure out the target and its type
	Use introspection to find the caller. It could find parent callers down the stack using the depth parameter.

	:param target: Optionally pass the target (just passthrough) or as a string to resolve
	:param int depth: How far down the stack should we look. One means this function's caller, two would be the caller's caller, etc.
	:returns object: the target
	"""

	if depth < 1:
		raise ValueError("Minimum depth is 1")

	caller = inspect_stack()
	if len(caller) < 2:
		caller = None
	else:
		caller = getmodule(caller[depth][0])
		LOGGER.debug('Got caller: %s', caller)

	if target is None:
		if caller is None:
			raise RuntimeError('Unsupported shallow call to "get_target" without a target')
		else:
			LOGGER.debug('Target not defined, using caller "%s" as target', caller)
			target = caller
	elif isinstance(target, str):
		LOGGER.debug('Identifying string defined target: %s', target)
		if hasattr(caller, target):
			LOGGER.debug('Target is a member of caller: %s.%s', caller, target)
			target = getattr(caller, target)
		elif target in modules:
			LOGGER.debug('Target is a loaded module: %s', target)
			target = modules[target]
		else:
			try:
				target = import_module(target)
				LOGGER.debug('Target is a loadable module: %s', target)
			except ModuleNotFoundError:
				raise ValueError(f'Target "{target}" could not be identified')
	else:
		LOGGER.debug('Target is an object: %s', target)

	return target


class Argument(dict):
	"""
	"""

	SUPPORTED_DETAILS = ('action', 'nargs', 'const', 'default', 'type', 'choices', 'required', 'help', 'metavar', 'dest', 'deprecated')

	def __contains__(self, key):
		"""

		:param key:
		:type key:
		"""

		try:
			self[key]
		except KeyError:
			return False
		return True

	def __getattr__(self, name):
		"""

		:param name:
		:type name:
		"""

		if name == 'name_or_flags':
			value = self._parameter.name
			if ('action' in self) and (self['action'] == 'store_false'):
				value = 'no-' + value
			if self._parameter.is_optional:
				if len(value) == 1:
					value = '-' + value
				else:
					value = '--' + value
		elif name == '_type':
			value = str
			if self._parameter.kind == ParameterKind.VAR_POSITIONAL:
				value = list
			elif self._parameter.kind == ParameterKind.VAR_KEYWORD:
				value = dict
			# elif self._parameter.has_annotation:
			# 	value = self._parameter.annotation
			elif self._parameter.has_default and (self._parameter.default is not None):
				value = type(self._parameter.default)
			# elif 'type_name' in self._documentation:
			# 	value = self._documentation['type_name']
			# elif 'default' in self._documentation:
			# 	value = type(self._documentation['default'])
		else:
			raise AttributeError(f'Class "{type(self).__name__}" has no attribute "{name}"')

		self.__setattr__(name, value)
		return value

	def __init__(self, parameter, /, **documentation):
		"""

		:param parameter:
		:type parameter:
		:param documentation:
		:type documentation:
		"""

		super().__init__()
		self._parameter = parameter
		self._documentation = documentation

	def __iter__(self):
		"""

		"""

		return iter(self.keys())

	def __len__(self):
		"""

		"""

		return len(self.keys())

	def __missing__(self, key):
		"""

		:param key:
		:type key: str
		"""

		if key == 'action':
			if self.type_in(bool):
				value = 'store_true'
				if ('default' in self) and self['default']:
					value = 'store_false'
			elif self.type_in(frozenset, set, tuple, list, dict):
				value = 'extend'
			else:
				raise KeyError(key)
		elif key == 'nargs':
			if self.type_in(frozenset, set, tuple, list, dict):
				value = '+'
			else:
				raise KeyError(key)
		elif key == 'default':
			if self._parameter.has_default:
				value = self._parameter.default
			elif ('action' in self) and (self['action'] == 'extend'):
				value = []
			else:
				raise KeyError(key)
		elif key == 'type':
			if self.type_in(bool, str):
				raise KeyError(key)
			elif self.type_in(frozenset, set, tuple, list, dict):
				value = str
			else:
				value = self._type
		elif key == 'help':
			if ('description' in self._documentation) and self._documentation['description'].strip():
				value = self._documentation['description'].strip()
			else:
				raise KeyError(key)
		else:
			raise KeyError(key)

		self.__setitem__(key, value)
		return value

	def __repr__(self):
		"""

		"""

		return '{' + ', '.join([f'{key}: {repr(value)}' for key, value in self.items()]) + '}'

	def items(self):
		"""

		"""

		return ((key, self[key]) for key in self.keys())


	def keys(self):
		"""

		"""

		return (key for key in self.SUPPORTED_DETAILS if key in self)

	def type_in(self, *types_):
		"""

		:param types:
		:type types:
		"""

		if isinstance(self._type, str):
			if self._type in (type_ if isinstance(type_, str) else type_.__name__ for type_ in types_):
				return True
		else:
			if id(self._type) in (id(type_) for type_ in types_ if not isinstance(type_, str)):
				return True
			if self._type.__name__ in (type_ if isinstance(type_, str) else type_.__name__ for type_ in types_):
				return True
		return False

	def values(self):
		"""

		"""

		return (self[key] for key in self.keys())


class IntrospectedArgumentParser(argparse.ArgumentParser):
	"""
	"""

	BUILTIN_OPTIONS = {
		'--log-level'	: {
			'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'],
			'default' : 'info',
			'help' : 'minimum severity of the messages to be logged',
		},
		'--log-to-syslog'	: {
			'action' : 'store_true',
			'default' : False,
			'help' : 'send logs to syslog.',
		},
		# 'input-file'		: {'action' : InputFiles, 'nargs' : 2, 'default' : argparse.SUPPRESS, 'help' : 'read parameters from a file or standard input (using the "-" special name). Consumes 2 parameters: first one is the path (or "-") and second one is the format'},
		# 'output-file'		: {'action' : 'store_true', 'default' : False, 'help' : 'output a JSON object as a string'},
	}
	DEFAULT_INIT_PARAMS = {
		'formatter_class'	: LocalFormatterClass,
	}
	DOCUMENTATION_MAP = {
		'name'				: 'prog',
		'description'		: 'description',
		'long_description'	: 'epilog',
	}

	def __init__(self, callable_or_module=None, /, **kwargs):
		"""
		"""

		if callable_or_module is None:
			documentation, documentation_args, callable_ = None, {}, None
		else:
			documentation = object_metadata(callable_or_module)
			documentation_args = {self.DOCUMENTATION_MAP[key] : value for key, value in documentation.items() if key in self.DOCUMENTATION_MAP}
			callable_ = Callable(callable_or_module)

		super().__init__(**(self.DEFAULT_INIT_PARAMS | documentation_args | kwargs))

		if callable_ is None:
			return
		# elif callable_.type == CallableType.MODULE:
		# 	raise NotImplementedError('Module not supported yet')
		# elif callable_.type == CallableType.FUNCTION:

		parameters_doc = documentation['parameters'] if 'parameters' in documentation else {}
		for parameter in callable_.signature.parameter_list:
			argument = Argument(parameter, **(parameters_doc[parameter.name] if parameter.name in parameters_doc else {}))
			print((argument.name_or_flags, argument))
			self.add_argument(argument.name_or_flags, **argument)

		self.set_defaults(__call__=callable_)

	@classmethod
	def _prepare_parameter(cls, **details):
		"""Extends argument's values
		Uses the defaults, annotations and docstring to extend the argument values (type, action, etc.)

		ToDo:
		- Documentation
		"""

		result, errors, warnings = {}, [], []
		if 'default' in details:
			if details['default'] is None:
				result['default'] = SUPPRESS
			elif isinstance(details['default'], str):
				result['default'] = details['default']
			elif isinstance(details['default'], bool):
				if details['default']:
					result['action'] = 'store_false'
				else:
					result['action'] = 'store_true'
			elif isinstance(details['default'], (frozenset, set, tuple, list)):
				result['action'] = 'extend'
				result['default'] = details['default']
				if 'nargs' not in result:
					result['nargs'] = '*'
			elif isinstance(details['default'], dict):
				result['action'] = 'extend'
				result['nargs'] = '*'
				result['default'] = ['='.join((str(key), str(value))) for key, value in details['default'].items()]
				if ('special' in details) and (details['special'] == 'varkw'):
					result['type'] = VarKWParameter
					if 'help' not in result:
						result['help'] = ''
					result['help'] += '(Use the key=value format for each entry)'
			else:
				result['type'] = type(details['default'])
				result['default'] = details['default']
			if ('nargs' not in result) and ('positional' in details) and details['positional']:
				result['nargs'] = '?'
		elif ('positional' in details) and not details['positional']:
			result['required'] = True

		if 'annotation' in details:
			LOGGER.warning('Type hinting from parameter annotation is not supported yet')

		if 'docstring' in details:
			if 'type_name' in details['docstring']:
				LOGGER.warning('Type hinting from docstring is not supported yet')
			if 'is_optional' in details['docstring']:
				if details['docstring']['is_optional'] and ('default' not in details):
					errors.append("""Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's optional but doesn't match "{parent_description}"'s signature""")
				elif (not details['docstring']['is_optional']) and ('default' in details):
					warnings.append("""Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's required but doesn't match "{parent_description}"'s signature""")
			if 'description' in details['docstring']:
				result['help'] = details['docstring']['description']

		if 'version' in details:
			result = {
				'action' : 'version',
				'version' : details['version'],
			}

		return result, errors, warnings

	@classmethod
	def _prepare_parameters(cls, raw_parameters, container_name, initial_values={}):
		"""Prepare parameters
		Takes introspected parameters and convert them into argparse friendly versions.

		:param dict raw_parameters: a mapping of parameter name to parameter details like the one returned by "parameters_from_callable"
		:param str container_name: the name of the object containing the provided parameters
		:param dict? initial_values: a mapping of parameter names and values to use as default (overriding the ones in the signature if present)
		:returns dict: a mapping of parameter names and details that can be used to build an ArgumentParser
		"""

		parameters = {}
		for parameter, details in raw_parameters.items():
			parameter_args, errors, warnings = cls._prepare_parameter(**details)
			for error in errors:
				LOGGER.error(error.format(parameter_name=parameter, parent_description=container_name))
			for warning in warnings:
				LOGGER.warning(warning.format(parameter_name=parameter, parent_description=container_name))
			if parameter in initial_values:
				parameter_args['default'] = initial_values[parameter]
			parameter_name = '_'.join((container_name, parameter))
			parameter_name = parameter_name.replace('_', '-')
			if not details['positional']:
				parameter_name = '--{}'.format(parameter_name)
			parameters[parameter_name] = parameter_args
		return parameters

	@classmethod
	def from_callable(cls, callable_, from_class=False, parents=None, initial_values={}):
		"""Extract argparse info from callable
		Uses introspection to build a dict out of a callable, usable to build an argparse tree.

		ToDo:
		- Documentation
		"""

		LOGGER.debug('Generating parser data for callable: %s', callable_)
		callable_metadata = object_metadata(callable_)

		parser_args = {
			'prog'				: callable_metadata['name'],
			'description'		: callable_metadata.get('description', None),
			'epilog'			: callable_metadata.get('long_description', None),
			'formatter_class'	: LocalFormatterClass,
		}
		if parents is not None:
			parser_args['parents'] = parents
		result = cls(**parser_args)

		raw_parameters = parameters_from_function(callable_, function_metadata=callable_metadata, from_class=from_class)
		if 'version' in callable_metadata:
			raw_parameters['version'] = {'version': callable_metadata['version'], 'positional': False}
		parameters = cls._prepare_parameters(raw_parameters=raw_parameters, container_name=callable_metadata['name'],
											 initial_values=initial_values)
		for parameter_name, kwargs in parameters.items():
			result.add_argument(parameter_name, **kwargs)

		result.set_defaults(callable=callable_)

		return result

	@classmethod
	def from_class(cls, class_, parents=None, initial_values={}):
		"""Extract argparse info from class
		Uses introspection to build a dict out of a class, usable to build an argparse tree.

		ToDo:
		- Documentation
		"""

		LOGGER.debug('Generating parser data for class: %s', class_)
		class_metadata = object_metadata(class_)

		parser_args = {
			'prog'				: class_metadata['name'],
			'description'		: class_metadata.get('description', None),
			'epilog'			: class_metadata.get('long_description', None),
			'formatter_class'	: LocalFormatterClass,
		}
		if parents is not None:
			parser_args['parents'] = parents
		result = cls(**parser_args)
		raw_parameters = parameters_from_class(class_)
		if 'version' in class_metadata:
			raw_parameters['version'] = {'version': class_metadata['version'], 'positional': False}
		parameters = cls._prepare_parameters(raw_parameters=raw_parameters, container_name=class_metadata['name'],
											 initial_values=initial_values)
		for parameter_name, kwargs in parameters.items():
			result.add_argument(parameter_name, **kwargs)

		result.set_defaults(callable=class_)

		return result

	@classmethod
	def new_base_parser(cls):
		"""Return new base parser
		Builds a base parser, which contains the basic switches added by the module

		ToDo:
		- Documentation
		"""

		LOGGER.debug('Creating new base parser')
		result = cls(add_help=False)
		for parameter_name, kwargs in cls.BUILTIN_OPTIONS.items():
			result.add_argument(parameter_name, **kwargs)
		return result

	@classmethod
	def run_callable(cls, callable_, args_w_keys={}):
		"""Extract argparse info from callable
        Uses introspection to build a dict out of a callable, usable to build an argparse tree.

        ToDo:
        - Documentation
        """

		callable_metadata = object_metadata(callable_)
		callable_args_w_keys, callable_name = {}, callable_metadata['name']
		parameters = parameters_from_callable(callable_, callable_metadata=callable_metadata)
		for key, values in args_w_keys.items():
			if key[:len(callable_name)] == callable_name:
				param_name = key[len(callable_name ) +1:]
				if ('special' in parameters[param_name]) and (parameters[param_name]['special'] == 'varkw'):
					callable_args_w_keys[param_name] = {}
					for kw_dict in values:
						callable_args_w_keys[param_name].update(kw_dict)
				else:
					callable_args_w_keys[param_name] = values

		result = execute_callable(callable_, args_w_keys=callable_args_w_keys, callable_metadata=callable_metadata, parameters=parameters)
		return str(result)