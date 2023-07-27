#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

import argparse
import collections.abc
import configparser
import inspect
import json
import logging
import logging.handlers
import os
import pathlib
import pprint
import sys
import types

from docstring_parser import parse as docstring_parse

__version__ = '0.8.0dev0'

LOGGER = logging.getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')

def object_metadata(obj):
	'''Gets metadata from an object
	It tries to get some meta information from the provided object by leveraging the object's details (name and version) and whatever can be learned from the docstring.

	:param obj: The object build the metadata for
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


class HashableInstance:
	'''Make anything hashable
	Make any instance of any type hashable by deriving the value for equivalent hashable types (tuples from lists...). This is a bad thing in most cases but if you know what you're doing it might help you with things. Rule of thumb: don't change ANYTHING of those mutable types once you trigger the hash generation, otherwise things will break.
	'''

	def __new__(cls, value):
		'''Magic creation
		Just return hashable values; otherwise return a HashableInstance with the value linked.
		'''

		try:
			hash(value)
		except TypeError:
			return object.__new__(cls)
		else:
			return value

	def __init__(self, value):
		'''Magic initialization
		Just link the value
		'''

		self._value = value

	def __hash__(self):
		'''Ḿagic hashing
		Trigger the type conversion and hash from there.
		'''

		if isinstance(self._value, collections.abc.Mapping):
			return hash(HashableInstance([(k, HashableInstance(v)) for k, v in self._value.items()]))
		elif isinstance(self._value, collections.abc.Sequence):
			return hash(tuple([HashableInstance(i) for i in self._value]))
		elif isinstance(self._value, set):
			return hash(frozenset(self._value))
		else:
			raise TypeError("Couldn't force a hash on <{}> instance: {}".format(type(self._value), self._value))


######################## I/O Classes ########################

class BaseValues:
	'''Dict with merge support
	Python 3.9 introduced the bar operator to merge dictionaries. This is the base of the configuration loading (merging dictionaries from different sources)
	'''
	
	def __init__(self, content):
		'''Init magic
		Simply store the content for future use
		'''
		
		self.content = content
		
	def __or__(self, other):
		'''Update
		"Merge" the content of both files and return a dict
		'''
		
		result = self.content.copy()
		result.update(other.content)
		return result
		
	def __ror__(self, other):
		'''Reflected update
		Update a builtin dict (or similar) and return a dict
		'''
		
		return BaseValues(other) | self
		
	def __repr__(self):
		return repr(self.content)
		
	def __str__(self):
		return str(self.content)


class BaseFile(BaseValues):
	'''Parent class for all modules
	All the formats should inherit from this one and it shouldn't be instantiated directly.
	'''
	
	def __init__(self, string_, mode = 'r', **kwargs):
		'''Init magic
		Using the argparse builtin file handling
		'''
		
		self.file = argparse.FileType(mode, **kwargs)(string_)
	
	def __del__(self):
		self.file.close()
	
	def __getattr__(self, name):
		'''Getattr magic
		Used to lazy load the content in the file
		'''
		
		if name == 'content':
			LOGGER.debug('Processing input %s', self.file.name)
			value = self._get_content()
		else:
			raise AttributeError(name)

		self.__setattr__(name, value)
		return value

	def __repr__(self):
		return self.file.name
		
	def __str__(self):
		return self._encode_content()


class JSONFile(BaseFile):
	def _get_content(self):
		LOGGER.debug('Loading JSON data')
		return json.load(self.file)


class INIFile(BaseFile):
	def _get_content(self):
		LOGGER.debug('Loading config (ini) data')
		config = configparser.ConfigParser()
		config.optionxform = str
		config.read_file(self.file)
		values = {}
		for section, content in config.items():
			if section == 'DEFAULT':
				LOGGER.debug('Adding settings from default section')
				values.update({key : value for key, value in content.items()})
			else:
				LOGGER.debug('Adding settings from section %s', section)
				values[section] = {key : value for key, value in content.items()}
		return values


class InputFiles(argparse.Action):
	
	_SUPPORTED_FORMATS = {
		'json'	: JSONFile,
		'ini'	: INIFile,
	}
	
	def __init__(self, option_strings, dest, nargs = None, **kwargs):
		if (nargs is None) or not isinstance(nargs, int) or (nargs != 2):
			raise ValueError('InputFile requires exactly 2 arguments (file path & file format)')
		
		super().__init__(option_strings, dest, nargs = nargs, **kwargs)
	
	def __call__(self, parser, namespace, values, option_string = None):
		reported_format = values[1]
		if reported_format.lower() not in self._SUPPORTED_FORMATS:
			raise ValueError('Input file format not supported: {}'.format(reported_format))
		item = self._SUPPORTED_FORMATS[reported_format.lower()](values[0])
		items = getattr(namespace, self.dest, None)
		if items is None:
			items = []
		items.append(item)
		setattr(namespace, self.dest, items)


######################## End of I/O Classes ########################


class ArgparseFormatterClass(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
	'''Default formatter class
	The way to "mix" formatter classes in argparse is by creating a new one that inherits from the ones that are needed, hence this class.
	'''
	pass


class ArgparseArgument(frozenset):
	'''Structure of an argparse argument
	This class defines an argument to be used in the argparse parser. It's supposed to be immutable, so changing values after instantiation will break stuff: don't do it.
	'''

	def __new__(cls, names, **options):
		'''Magic creation
		Creating a frozenset, after figuring out what the content should be.
		'''

		if isinstance(names, str):
			names = (names,)
		return frozenset.__new__(cls, [name.lstrip('-') for name in names])

	def __init__(self, names, **options):
		'''Magic initialization
		Adding the options to the already created object.
		'''

		self.options = options

	def __hash__(self):
		'''Magic hashing
		Take into consideration the "options" as part of the hash
		'''

		options_keys = list(self.options.keys())
		options_keys.sort()
		return hash(HashableInstance((self.names(), [(key, self.options[key]) for key in options_keys])))

	def __repr_(self):
		'''Magic representation
		Valid python code to recreate this object
		'''

		params = [repr(tuple(self)[0]) if self.nargs() == 1 else repr(tuple(self))]
		params.extend(['{} = {}'.format(key, repr(value)) for key, value in self.options.items()])
		return '{}({})'.format(type(self).__name__, ', '.join(params))

	def __str__(self):
		'''Magic string
		Simplified string representation of the object
		'''

		return '{{{}}}'.format(' '.join(self.names()))

	@classmethod
	def from_inspect(cls, name, values, annotations, docstring):
		'''Create from inspect
		Uses the results of an inspect call to create an argument with as much details as possible.

		ToDo:
		- Docstring processing
		- Improved dict handling
		- Documentation
		'''

		# values['help'] = 'ToDo: help string not supported yet'

		if name in annotations:
			if inspect.isclass(annotations[name]):
				values['type'] = annotations[name]
			elif isinstance(annotations[name], tuple) or isinstance(annotations[name], list):
				values['choices'] = annotations[name]
		elif 'default' in values:
			if values['default'] is None:
				values['default'] = argparse.SUPPRESS
			elif type(values['default']) != str:
				if isinstance(values['default'], bool):
					if values['default']:
						values['action'] = 'store_false'
					else:
						values['action'] = 'store_true'
				elif isinstance(values['default'], (tuple, list)):
					values['action'] = 'extend'
					values['default'] = list(values['default'])
					if 'nargs' not in values:
						values['nargs'] = '+'
				elif isinstance(values['default'], dict):
					values['action'] = 'extend'
					values['nargs'] = '+'
					values['default'] = []
					if 'help' not in values:
						values['help'] = ''
					values['help'] += '(Use the key=value format for each entry)'
				else:
					values['type'] = type(values['default'])

		return cls(name, **values)

	def names(self):
		'''Ordered list of names
		This will return a list with the names with "-" (ready for argparse) ordered with whatever list.sort() does to a list of strings.

		The ordering part is important since this is used to create hash which means that argument with the same list of names should ALWAYS return the same "names" (in the same order) which should not be expected from set or frozenset.
		'''

		names_ = list(self)
		names_.sort()
		return [('-{}' if len(name) == 1 else '--{}').format(name) for name in names_]

	def length(self):
		'''Params to be consummed
		This will be the number of "parameters" (as in sys.argv) to be "consummed" by this argument. It will include the argument name itself (minimum is 1). This is leveraged in some ad-hoc sys.argv processing (for the multipass process).
		'''

		if 'nargs' in self.options:
			if isinstance(self.options['nargs'], int):
				return self.options['nargs'] + 1
			else:
				raise ValueError('Variable length for argument: {}'.format(self))
		elif ('action' in self.options) and (self.options['action'] in ('store_const', 'store_true', 'store_false', 'append_const', 'count', 'help', 'version')):
			return 1
		else:
			return 2


class ArgparseParser(set):
	'''Structure of an argparse parser
	This class defines a parser to be used in the argparse tree. It will be a set of ArgparseArgument that will also have a dict of "defaults" (to be set with argparser.set_defaults()) and options, for the argparse.parser initializer.
	'''

	DEFAULT_OPTIONS = {
		'formatter_class'	: ArgparseFormatterClass,
		'argument_default'	: argparse.SUPPRESS,
	}
	METADATA_MAP = {'description' : 'description', 'long_description' : 'epilog'}

	def __init__(self, *arguments, defaults = None, **options):
		'''Magic initialization
		Build the underlying set with the provided arguments. Also store the options and defaults.
		'''

		super().__init__(arguments)
		self.defaults = {} if defaults is None else defaults
		self.options = self.DEFAULT_OPTIONS.copy()
		self.options.update(options)

	def __contains__(self, item):
		'''Magic search
		Enables the use of "item in ArgparseParser".
		'''

		if isinstance(item, ArgparseArgument):
			return super().__contains__(item)

		if isinstance(item, str):
			item = item.lstrip('-')

		for element in self:
			if item in element:
				return True
		return False

	def __eq__(self, other):
		'''Magic equality
		Two ArgparseParsers are equal when everything matches.
		'''

		return (self.options == other.options) and (self.defaults == other.defaults) and (super().__eq__(other))

	def __ne__(self, other):
		'''Magic inequality
		Two ArgparseParsers are not equal when anything doesn't match.
		'''

		return (self.options != other.options) or (self.defaults != other.defaults) or (super().__ne__(other))

	def __repr__(self):
		'''Magic representation
		Valid python code to recreate this object
		'''

		params = [repr(arg) for arg in self]
		if len(self.defaults):
			params.append('defauls = {}'.format(repr(self.defaults)))
		params.extend(['{} = {}'.format(key, repr(value)) for key, value in self.options.items() if key not in self.DEFAULT_OPTIONS])

		return '{}({})'.format(type(self).__name__, ', '.join(params))

	def __str__(self):
		'''Magic string
		Simplified string representation of the object
		'''

		return '{{{}}}'.format(', '.join([repr(str(item)) for item in self]))

	def build(self, subparsers = None):
		'''Argparse parser building
		Recursive builder, for tree creation.

		The items in parser_content, which is expected to be a dict or compatible, are processed recursively:
		- a string key with a dict value denotes an argument. The key will be the argument name and the value the other attributes
		- a False key is used to store the "argparse defaults", and the value should be a dict
		- a True key with a tuple value denotes subparsers,
		- a string key with a tuple value denotes a subparser
		'''

		if subparsers is None:
			argument_parser = argparse.ArgumentParser(**self.options)
		else:
			argument_parser = subparsers.add_parser(**self.options)

		for arg in self:
			argument_parser.add_argument(*arg.names(), **arg.options)

		for default_key, default_value in self.defaults.items():
			argument_parser.set_defaults(default_key, default_value)

		return argument_parser

		for key, value in parser_content.items():
			if isinstance(key, bool):
				if key:
					if isinstance(value, tuple):
						subparsers_info, subparsers_map = value
						LOGGER.debug('Adding subparsers to parser %s with: %s', argument_parser, subparsers_info)
						subparsers = argument_parser.add_subparsers(**subparsers_info)
						build_parser(subparsers_map, subparsers)
					else:
						raise ValueError('The argparser value is not supported: {}'.format(parser_content))
				else:
					LOGGER.debug('Adding defaults to parser %s: %s', argument_parser, value)
					argument_parser.set_defaults(**value)
			elif isinstance(key, str):
				if isinstance(value, dict):
					LOGGER.debug('Adding argument %s with: %s', key, value)
					argument_parser.add_argument(key, **value)
				elif isinstance(value, tuple):
					subparser_info, subparser_arguments = value
					subparser_info = list(subparser_info)
					subparser_info[0] = subparser_info[0] + DEFAULT_ARGUMENT_PARSER[1]
					subparser_info[1].update(DEFAULT_ARGUMENT_PARSER[2])
					if None in subparser_arguments:
						subparser_info[1].update(subparser_arguments[None])
					LOGGER.debug('Adding subparser %s with: %s', key, subparser_info)
					subparser = argument_parser.add_parser(key, *subparser_info[0], **subparser_info[1])
					build_parser(subparser_arguments, subparser)
				else:
					raise ValueError('The argparser value is not supported: {}'.format(parser_content))
			elif key is None:
				LOGGER.debug('Skipping parser metadata')
			else:
				raise ValueError('The argparser key "{}" is not supported: {}'.format(key, parser_content))

		return argument_parser

	@classmethod
	def from_callable(cls, callable_, class_method = False):
		'''Create ArgparseParser from callable
		Uses introspection to build a ArgparseParser out of a callable.

		ToDo:
		- Documentation
		'''

		try:
			args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(callable_)
		except TypeError:
			LOGGER.debug('Signature inspect failed. Using generic signature for callable: %s', callable_)
			args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = [], 'args', 'kwargs', [], [], None, {} # Generic signature: just args and kwargs, whatever you pass will be.
			if class_method:
				args = ['self'] # Default will be bound method
		else:
			if defaults is None:
				defaults = []
		if class_method and ((callable_ is object.__init__) or (callable_ is object.__new__)):
			varargs, varkw = None, None	# Builtin object.__init__ case, where *args and **kwargs are accepted but only through super()
		LOGGER.debug('Callable "%s" yield signature: %s', callable_, dict(zip(('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs', 'kwonlydefaults', 'annotations'),(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations))))

		if class_method:
			is_boundmethod = False
			if len(args):
				if args[0] == 'self':
					is_boundmethod = True
					args.pop(0)
				elif args[0] in ['cls', 'type']:
					args.pop(0)

		metadata = object_metadata(callable_)
		parser = cls(defaults = {'__simplifiedapp_' : (metadata['name'] if class_method and is_boundmethod else callable_, tuple(args), varargs, tuple(kwonlyargs), varkw)}, **{cls.METADATA_MAP[key] : value for key, value in metadata.items() if key in cls.METADATA_MAP})

		for arg in args[:len(args) - len(defaults)]:
			parser.add(ArgparseArgument.from_inspect(arg, {}, annotations, docstring = ''))

		for arg, arg_default in dict(zip(args[-len(defaults):], defaults)).items():
			parser.add(ArgparseArgument.from_inspect(arg, {'default' : arg_default}, annotations, docstring = ''))

		if varargs is not None:
			parser.add(ArgparseArgument.from_inspect(varargs, {'default' : [], 'nargs' : '*'}, annotations, docstring = ''))

		if kwonlydefaults is not None:
			for arg, arg_default in kwonlydefaults.items():
				parser.add(ArgparseArgument.from_inspect(arg, {'default' : arg_default}, annotations, docstring = ''))

		if varkw is not None:
			parser.add(ArgparseArgument.from_inspect(varkw, {'default' : {}}, annotations, docstring = ''))

		if 'version' in metadata:
			parser.add(ArgparseArgument('version', action = 'version', version = metadata['version']))

		return parser

	@classmethod
	def from_class(cls, class_, allowed_privates = ()):
		'''Extract argparse info from class
		Uses introspection to build a dict out of a class, usable to build an argparse tree.

		ToDo:
		- Add support for immutable objects (add the __new__ method into the process)
		- Add support for class_methods and static_methods
		- Documentation
		'''

		allowed_privates = ['__call__'] + list(allowed_privates)

		class_opts_init = callable_args(getattr(class_, '__init__'), from_class = True)
		class_opts_new = callable_args(getattr(class_, '__new__'), from_class = True)
		class_opts[False]['__simplifiedapp_'] = (class_, *class_opts[False]['__simplifiedapp_'][1:])

		subparsers = {}
		for name, callable_ in inspect.getmembers(class_, inspect.isroutine):
			if (name[0] == '_') and (name not in allowed_privates):
				LOGGER.debug('Skipping private method "%s" in class %s', name, class_)
				continue
			elif callable_ is object.__new__:
				LOGGER.debug("Skipping object's __new__ in class %s", class_)
				continue
			try:
				args = callable_args(callable_, from_class = True)
			except Exception:
				LOGGER.exception("Member %s of class %s couldn't be processed", name, class_)
			else:
				if isinstance(args[False]['__simplifiedapp_'][0], str):
					args[False]['__simplifiedapp_'] = (class_opts[False]['__simplifiedapp_'], args[False]['__simplifiedapp_'])
				subparsers[name] = (([], {}), args)

		metadata = object_metadata(class_)
		class_opts[None] = {METADATA_TO_ARGPARSE[key] : value for key, value in metadata.items() if key in METADATA_TO_ARGPARSE}
		if 'version' in metadata:
			class_opts['--version'] = {'action' : 'version', 'version' : metadata['version']}
		if subparsers:
			class_opts[True] = ({'title' : str(class_.__name__) + ' methods'}, subparsers)

		LOGGER.debug('Generated class options: %s', class_opts)
		return class_opts


class BuiltinParser(ArgparseParser):

	AUTO_PARAMS = ('-h', '--help', '--version')
	DEFAULT_ARGUMENTS = [
		ArgparseArgument('log-level', choices = ['notset', 'debug', 'info', 'warning', 'error', 'critical'], default = 'info', help = 'minimum severity of the messages to be logged'),
		ArgparseArgument('log-to-syslog', action = 'store_true', default = False, help = 'send logs to syslog.'),
		ArgparseArgument('input-file', action = InputFiles, nargs = 2, default = argparse.SUPPRESS, help = 'read parameters from a file or standard input (using the "-" special name)'),
		ArgparseArgument('json', action = 'store_true', default = False, help = 'output a JSON object as a string')
	]

	def __init__(self, *extra_arguments):
		super().__init__(*self.DEFAULT_ARGUMENTS)
		for argument in extra_arguments:
			self.add(argument)

	def parse_args(self, sys_argv):

		cleaned_sys_argv = []

		if len(frozenset(sys_argv) & frozenset(self.AUTO_PARAMS)):
			return None

		for arg in self:
			for name in arg.names():
				if name in sys_argv:
					if ('action' in arg.options) and ((arg.options['action'] in ('append', 'extend')) or (arg.options['action'] is InputFiles)):
						start_point = 0
						while True:
							try:
								index = sys_argv.index(name, start_point)
							except ValueError:
								break
							else:
								start_point = index + len(arg)
								cleaned_sys_argv.extend(sys_argv[index : start_point])
					else:
						index = sys_argv.index(name)
						cleaned_sys_argv.extend(sys_argv[index : index + len(arg)])

		return self.build().parse_args(cleaned_sys_argv)




def module_args(module, allowed_privates = ('__call__',)):
	'''Extract argparse info from module
	Uses introspection to build a dict out of a module, usable to build an argparse tree.
	
	ToDo: Documentation
	'''

	subparsers = {}
	mod_opts = {}
	for name, callable_ in inspect.getmembers(module, inspect.isroutine):
		if name[0] == '_' and (name not in allowed_privates):
			LOGGER.debug('Skipping private callable: %s', name)
			continue
		try:
			args = callable_args(callable_)
		except Exception as error:
			LOGGER.warning('Uncompatible callable %s: %s', name, error)
			pass
		else:
			subparsers[name] = (([], {}), args)

	for name, class_ in inspect.getmembers(module, inspect.isclass):
		try:
			args = class_args(class_)
		except Exception as error:
			LOGGER.warning('Uncompatible class %s: %s', name, error)
			pass
		else:
			subparsers[name] = (([], {}), args)

	metadata = object_metadata(module)
	mod_opts[None] = {METADATA_TO_ARGPARSE[key] : value for key, value in metadata.items() if key in METADATA_TO_ARGPARSE}
	if 'version' in metadata:
		mod_opts['--version'] = {'action' : 'version', 'version' : metadata['version']}
	if subparsers:
		mod_opts[True] = ({'title' : metadata['name'] + ' callables'}, subparsers)

	return mod_opts

def build_parser(parser_content, argument_parser = None):
	'''Argparse parser building
	Recursive builder, for tree creation.

	The items in parser_content, which is expected to be a dict or compatible, are processed recursively:
	- a string key with a dict value denotes an argument. The key will be the argument name and the value the other attributes
	- a False key is used to store the "argparse defaults", and the value should be a dict
	- a True key with a tuple value denotes subparsers,
	- a string key with a tuple value denotes a subparser
	'''
	
	LOGGER.debug('Building parser (%s) with: %s', argument_parser, parser_content)
	if argument_parser is None:
		argument_parser = DEFAULT_ARGUMENT_PARSER[0](*DEFAULT_ARGUMENT_PARSER[1], **DEFAULT_ARGUMENT_PARSER[2])

	for key, value in parser_content.items():
		if isinstance(key, bool):
			if key:
				if isinstance(value, tuple):
					subparsers_info, subparsers_map = value
					LOGGER.debug('Adding subparsers to parser %s with: %s', argument_parser, subparsers_info)
					subparsers = argument_parser.add_subparsers(**subparsers_info)
					build_parser(subparsers_map, subparsers)
				else:
					raise ValueError('The argparser value is not supported: {}'.format(parser_content))
			else:
				LOGGER.debug('Adding defaults to parser %s: %s', argument_parser, value)
				argument_parser.set_defaults(**value)
		elif isinstance(key, str):
			if isinstance(value, dict):
				LOGGER.debug('Adding argument %s with: %s', key, value)
				argument_parser.add_argument(key, **value)
			elif isinstance(value, tuple):
				subparser_info, subparser_arguments = value
				subparser_info = list(subparser_info)
				subparser_info[0] = subparser_info[0] + DEFAULT_ARGUMENT_PARSER[1]
				subparser_info[1].update(DEFAULT_ARGUMENT_PARSER[2])
				if None in subparser_arguments:
					subparser_info[1].update(subparser_arguments[None])
				LOGGER.debug('Adding subparser %s with: %s', key, subparser_info)
				subparser = argument_parser.add_parser(key, *subparser_info[0], **subparser_info[1])
				build_parser(subparser_arguments, subparser)
			else:
				raise ValueError('The argparser value is not supported: {}'.format(parser_content))
		elif key is None:
			LOGGER.debug('Skipping parser metadata')
		else:
			raise ValueError('The argparser key "{}" is not supported: {}'.format(key, parser_content))
	
	return argument_parser

def run_call(call_, complete_input, parent = None):
	'''Execute a callable
	Unpacks the call_ tuple, runs some checks and get some defaults if there's missing info. Returns the result of such run.
	
	ToDo:
	- Add support for asyncio (async/await methods)
	- Documentation
	'''

	if len(call_) != 5:
		raise ValueError('Malformed call tuple')
	else:
		LOGGER.debug('Running call with: %s', call_)

	callable_, pos_args, args_name, kw_args, kwargs_name = call_

	if isinstance(callable_, str):
		if parent is None:
			raise ValueError('A callable "string" requires a parent object')
		else:
			callable_ = getattr(parent, callable_)

	positional_values = [complete_input[key] if key in complete_input else None for key in pos_args]
	if (args_name is not None) and (args_name in complete_input) and (complete_input[args_name] is not None):
		positional_values += complete_input[args_name]

	keyword_values = {key : value for key, value in complete_input.items() if key in kw_args}
	if (kwargs_name is not None) and (kwargs_name in complete_input) and (complete_input[kwargs_name] is not None):
		for kwequal in complete_input[kwargs_name]:
			key, value = kwequal.split('=', maxsplit = 1)
			if (key in pos_args) or (key in kw_args):
				LOGGER.warning('Skipping %s for available switch: %s', kwargs_name, key)
			else:
				keyword_values[key] = value

	return callable_(*positional_values, **keyword_values)

def main(target = None, sys_argv = None):
	'''Simplified run of an app.
	Performs a simplified procedure of an app run. It will build and argparse object out of a module, class, or callable referenced via "target" and run it.

	target can be the name of the module/class/callable, as a string, or the actual object. If "None", then the target will be the calling module.

	The following options will be added automatically:
	- log_level: to set the logging level, anything supported by the "logging" module.
	- log_to_syslog: configures the logging module to send the logs to syslog. This is only supported in POSIX where a "/dev/log" device exists.
	- input_file: if this is set, it should contain the path to an input file and a second parameter stating the format. The file will be parsed an used as part of the configuration.
	- json: transforms the resulting object into a json string. If the result is a string this won't happen.
	- _json_default: if this is set, it should point to a function that will be used in the json conversion as the default casting. If not defined, "str" is then used (everything is casted to string).
	
	A callable will be called and passed all the configuration options. In the case of a class method, a class instance will be created first, passing all the configuration to the constructor and then the instance method will be called with all the configuration.

	Results; if your code returns:
	- a string, it will be printed as is.
	- any other type of object will be printed with pprint
	- any other type of object, and the json flag was passed as True, then it will be printed as a json string (json.dumps)
	
	ToDo:
	- Implement a multipass algorithm, early loading the input_files
	- Generalize "output" via output_file (instead of the lonely json)
	- Add support to log_file (send logs to file)
	- Documentation
	'''

	if sys_argv is None:
		sys_argv = sys.argv[1:] if len(sys.argv) > 1 else []

	complete_input = {}
	first_pass = BuiltinParser().parse_args(sys_argv)

	if first_pass is not None:
		log_parameters = DEFAULT_LOG_PARAMETERS.copy()

		if hasattr(first_pass, 'log_level') and len(first_pass.log_level):
			log_parameters['level'] = first_pass.log_level.upper()

		if hasattr(first_pass, 'log_to_syslog') and first_pass.log_to_syslog:
			log_parameters['handlers'] = [logging.handlers.SysLogHandler(address = '/dev/log')]

		logging.basicConfig(**log_parameters)
		LOGGER.debug('Logging configured  with: %s', log_parameters)

		if hasattr(first_pass, 'input_file'):
			for input_ in first_pass.input_file:
				LOGGER.debug('Merging values from %s', input_)
				complete_input = complete_input | input_

	caller = inspect.getmodule(inspect.stack()[1][0])
	LOGGER.debug('Got caller: %s', caller)

	if target is None:
		LOGGER.debug('Target not defined, using caller "%s" as target', caller)
		target = caller
	elif isinstance(target, str):
		LOGGER.debug('Identifying string defined target: %s', target)
		if target in sys.modules:
			LOGGER.debug('Target is a loaded module: %s', target)
			target = sys.modules[target]
		elif hasattr(caller, target):
			LOGGER.debug('Target is a member of caller: %s.%s', caller, target)
			target = getattr(caller, target)
		else:
			try:
				target = __import__(target)
				LOGGER.debug('Target is a loadable module: %s', target)
			except ModuleNotFoundError:
				raise ValueError('Target "{}" could not be identified'.format(target))
	else:
		LOGGER.debug('Target is an object: %s', target)

	result = ArgparseParser.from_callable(target)
	print(result)
	return result


	arg_parser_data = BUILTIN_ARGPARSE_OPTIONS.copy()
	try:
		if inspect.ismodule(target):
			LOGGER.debug('Generating parser data for target as a module')
			arg_parser_data.update(module_args(target))
		elif inspect.isclass(target):
			LOGGER.debug('Generating parser data for target as a class')
			arg_parser_data.update(class_args(target))
		else:
			LOGGER.debug('Generating parser data for target as a callable')
			arg_parser_data.update(callable_args(target))
	except Exception as error:
		raise ValueError("Main's target ({}) is not supported: {}".format(target, error))

	LOGGER.debug('Parser object tree is: %s', arg_parser_data)
	# pprint.pprint(arg_parser_data)
	keyword_args = DEFAULT_ARGUMENT_PARSER[2].copy()
	if None in arg_parser_data:
		keyword_args.update(arg_parser_data[None])
	args = build_parser(parser_content = arg_parser_data, argument_parser = DEFAULT_ARGUMENT_PARSER[0](*DEFAULT_ARGUMENT_PARSER[1], **keyword_args)).parse_args(sys_argv)
	LOGGER.debug('Complete input before CLI merge: %s', complete_input)
	complete_input.update(vars(args))
	LOGGER.debug('Complete input is: %s', complete_input)
	
	if hasattr(args, '__simplifiedapp_'):
		if len(args.__simplifiedapp_) == 2:
			instance_call, method_call = args.__simplifiedapp_
			instance = run_call(instance_call, complete_input)
			result = run_call(method_call, complete_input, parent = instance)
		else:
			result = run_call(args.__simplifiedapp_, complete_input)
	else:
		raise RuntimeError('No executable/callable was found')

	if isinstance(result, str):
		LOGGER.debug('The result is a string. Printing it as is.')
		print(result, end='')
	else:
		if hasattr(args, 'json') and args.json:
			LOGGER.debug('The result is an object. Printing it as a json string.')
			print(json.dumps(result, default = args._json_default if hasattr(args, '_json_default') else str))
		else:
			LOGGER.debug('The result is an object. Printing it with pprint.')
			pprint.pprint(result, width = PPRINT_WIDTH)


######################## Legacy functions ########################


def files_in_module_dir(module, dir_name, exclude = OS_FILES):
	'''Build tree of file names.
	It's a simple "walk" over a directory tree and return the file names. Includes a list of file names to be ignored.
	
	ToDo: Documentation
	'''
	
	module = pathlib.Path(module)
	
	if not module.is_dir():
		raise ValueError('{} is not a directory'.format(module.resolve()))
	
	dir = module / dir_name
	if not dir.is_dir():
		raise Exception('{} is not a directory'.format(dir.resolve()))
	
	result = []
	
	for relative_element in os.listdir(str(dir.resolve())):
		
		element = dir / relative_element
		if relative_element in exclude:
			LOGGER.warning('Skipping %s', element.resolve())
			continue
		if element.is_dir():
			result += files_in_module_dir(module, pathlib.Path(dir_name) / relative_element, exclude = exclude)
		elif element.is_file():
			result.append(str(pathlib.Path(dir_name) / relative_element))
		else:
			LOGGER.warning('%s is not a file or directory', element.resolve())
		
	return result
