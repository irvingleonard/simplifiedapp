#! python
'''Boilerplate stuff done for you.
This module has some generic classes and functions for several purposes.

ToDo:
- Everything
'''

import argparse
import configparser
import inspect
import json
import logging
import logging.handlers
import os
import pathlib
import pprint
import re
import sys
import types

__version__ = '0.7.1'

# EARLY_DEBUG = True

LOGGER = logging.getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
DOCSTRING_FORMAT = re.compile('(?P<description>\A.+?$)(?:\n(?P<long_description>.+?)(?:^\s*\n.*)?)?\Z', re.IGNORECASE | re.MULTILINE | re.DOTALL)
METADATA_TO_ARGPARSE = {'description' : 'description', 'long_description' : 'epilog'}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')

try:
	_parser = argparse.ArgumentParser()
	_parser.add_argument("--foo", action="extend", nargs="+", type=str)
except ValueError:
	ADD_ARGUMENT_ACTION_EXTEND = False
else:
	ADD_ARGUMENT_ACTION_EXTEND = True

######################## I/O Classes ########################

class BaseValues:
	
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
    pass


DEFAULT_ARGUMENT_PARSER = (argparse.ArgumentParser, [], {'formatter_class' : ArgparseFormatterClass})
BUILTIN_ARGPARSE_OPTIONS = {
	'--log-level'		: {'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'], 'default' : 'info', 'help' : 'minimum severity of the messages to be logged'},
	'--log-to-syslog'	: {'action' : 'store_true', 'default' : False, 'help' : 'send logs to syslog.'},
	'--input-file'		: {'action' : InputFiles, 'nargs' : 2, 'default' : argparse.SUPPRESS, 'help' : 'read parameters from a file or standard input (using the "-" special name)'},
	'--json'			: {'action' : 'store_true', 'default' : False, 'help' : 'output a JSON object as a string'},
}


def object_metadata(obj):
	'''Gets metadata from an object
	It tries to get some meta information from the provided object

	ToDo: Documentation
	'''
	
	metadata = {'name' : obj.__name__}
	
	if hasattr(obj, '__version__'):
		metadata['version'] = obj.__version__
		
	if hasattr(obj, '__doc__') and (obj.__doc__ is not None) and len(obj.__doc__):
		metadata.update(re.match(DOCSTRING_FORMAT, obj.__doc__).groupdict())

	if ('long_description' in metadata) and (metadata['long_description'] is not None) and len(metadata['long_description']):
		try:
			indentation = len(re.match('\A(\s*)\S+.*', metadata['long_description']).groups()[0])
			metadata['long_description'] = '\n'.join([line[indentation:] for line in metadata['long_description'].splitlines()])
		except Exception:
			LOGGER.debug('Current (weak) docstring parsing failed in: %s', metadata['long_description'])
	
	# pprint.pprint(metadata)
	return metadata


def param_metadata(arg_name, arg_values, annotations, docstring):
	'''Extends argument's values
	Uses the defaults, annotations and docstring to extend the argument values (type, action, etc.)
	
	ToDo:
	- Documentation
	'''

	# arg_values['help'] = 'ToDo: help string not supported yet'

	if arg_name in annotations:
		if inspect.isclass(annotations[arg_name]):
			arg_values['type'] = annotations[arg_name]
		elif isinstance(annotations[arg_name], tuple) or isinstance(annotations[arg_name], list):
			arg_values['choices'] = annotations[arg_name]
	elif 'default' in arg_values:
		if arg_values['default'] is None:
			arg_values['default'] = argparse.SUPPRESS
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


def callable_args(callable_, call_ = '', skip_builtin = None):
	'''Extract argparse info from callable
	Uses introspection to build a dict out of a callable, usable to build an argparse tree.
	
	ToDo:
	- Documentation
	'''
	
	try:
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = inspect.getfullargspec(callable_)
	except TypeError:
		LOGGER.debug('Signature inspect failed. Using generic signature for callable: %s', callable_)
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = [], 'args', 'kwargs', None, [], None, {}	#Generic signature: just args and kwargs, whatever you pass will be.
	if (callable_.__name__ == '__init__') and hasattr(callable_, '__objclass__') and (callable_.__objclass__ == object):
		varargs, varkw = None, None			#Builtin object.__init__ case, where *args and **kwargs are accepted but only through super()
	LOGGER.debug('Callable "%s" yield signature: %s', callable_, dict(zip(('args', 'varargs', 'varkw', 'defaults', 'kwonlyargs', 'kwonlydefaults', 'annotations'),(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations))))

	if (skip_builtin is not None) and len(args) and (args[0] == skip_builtin):
		args.pop(0)

	if defaults is None:
		defaults = []
	req_args = {arg : {} for arg in args[:len(args) - len(defaults)] if arg not in ([] if skip_builtin is None else (skip_builtin,))}
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

	if call_ is not None:
		if not call_:
			call_ = callable_
		arguments[False] = {'__simplifiedapp_' : (call_, tuple(args), varargs, tuple(kwonlyargs), varkw)}

	arguments[None] = {METADATA_TO_ARGPARSE[key] : value for key, value in metadata.items() if key in METADATA_TO_ARGPARSE}
	if 'version' in metadata:
		arguments['--version'] = {'action' : 'version', 'version' : metadata['version']}

	LOGGER.debug('Generated arguments: %s', arguments)
	return arguments


def class_args(class_, allowed_privates = ('__call__',)):
	'''Extract argparse info from class
	Uses introspection to build a dict out of a class, usable to build an argparse tree.
	
	ToDo:
	- Diferentiate the instantiation from the call. Allow __call__ to be a subparser an let the "class parameters" be about __init__
	- Add support for immutable objects (add the __new__ method into the process) 
	- Documentation
	'''

	class_opts = callable_args(getattr(class_, '__init__'), call_ = class_, skip_builtin = 'self')

	subparsers = {}
	for name, callable_ in inspect.getmembers(class_, inspect.isroutine):
		if (name[0] == '_') and (name not in allowed_privates):
			continue
		try:
			args = callable_args(callable_, call_ = name, skip_builtin = 'self')
		except Exception:
			LOGGER.exception("Member %s of class %s couldn't be processed", name, class_)
		else:
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
	- a False key is used to store the "argparse defaults", and the value should be a dict
	- a string key with a dict value denotes an argument. The key will be the argument name and the value the other attributes
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
	
	ToDo: Documentation
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
	- Documentation
	- Generalize "output" via output_file (instead of the lonely json)
	- Add support to log_file (send logs to file)
	'''

	try:
		if EARLY_DEBUG:
			log_parameters = DEFAULT_LOG_PARAMETERS.copy()
			log_parameters['level'] = 'DEBUG'
			logging.basicConfig(**log_parameters)
			LOGGER.debug('Logging configured  with: %s', log_parameters)
	except Exception:
		if hasattr(sys.modules[__name__], 'EARLY_DEBUG') and (EARLY_DEBUG):
			raise

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

	arg_parser_data = BUILTIN_ARGPARSE_OPTIONS.copy()
	try:
		if inspect.ismodule(target):
			arg_parser_data.update(module_args(target))
		elif inspect.isclass(target):
			arg_parser_data.update(class_args(target))
		else:
			arg_parser_data.update(callable_args(target))
	except Exception as error:
		raise ValueError("Main's target ({}) is not supported: {}".format(target, error))

	LOGGER.debug('Parser object tree is: %s', arg_parser_data)
	# pprint.pprint(arg_parser_data)
	keyword_args = DEFAULT_ARGUMENT_PARSER[2].copy()
	if None in arg_parser_data:
		keyword_args.update(arg_parser_data[None])
	args = build_parser(parser_content = arg_parser_data, argument_parser = DEFAULT_ARGUMENT_PARSER[0](*DEFAULT_ARGUMENT_PARSER[1], **keyword_args)).parse_args(sys_argv)
	
	log_parameters = DEFAULT_LOG_PARAMETERS.copy()
	
	if hasattr(args, 'log_level') and len(args.log_level):
		log_parameters['level'] = args.log_level.upper()
		
	if hasattr(args, 'log_to_syslog') and args.log_to_syslog:
		log_parameters['handlers'] = [logging.handlers.SysLogHandler(address = '/dev/log')]
	
	logging.basicConfig(**log_parameters)
	LOGGER.debug('Logging configured  with: %s', log_parameters)
	
	complete_input = {}
	if hasattr(args, 'input_file'):
		for input_ in args.input_file:
			LOGGER.debug('Merging values from %s', input_)
			complete_input = complete_input | input_
	
	vars_args = vars(args)
	complete_input.update(vars_args)
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
