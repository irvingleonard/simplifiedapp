#! python
'''Boilerplate stuff done for you.
This module has some generic classes and functions for several purposes.

ToDo:
- Everything
'''

import abc
import argparse
import configparser
import json
import logging
import logging.handlers
import os
import pathlib
import pprint
import sys

__version__ = '0.6.0'

LOGGER = logging.getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')

######################## I/O Classes ########################

class BaseFile():
	'''Parent class for all modules
	All the formats should inherit from this one and it shouldn't be instantiated directly.
	'''
	
	def __init__(self, string_, mode = 'r', **kwargs):
		'''Init magic
		Using the argparse builtin file handling
		'''
		
		super().__init__()
		self.file = argparse.FileType(mode, **kwargs)(string_)
	
	def __getattr__(self, name):
		'''Getattr magic
		Used to lazy load the content in the file
		'''
		
		if name == 'content':
			LOGGER.debug('Processing input %s', self.file.name)
			value = self._get_content()
			self.__setattr__(name, value)
			return value
		else:
			raise AttributeError(name)
	
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
		
		result = other.copy()
		result.update(self.content)
		return result

	def __repr__(self):
		return self.file.name
		
	def __str__(self):
		return self._encode_content()


class ConfFile(BaseFile):
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


class JSONFile(BaseFile):
	def _get_content(self):
		LOGGER.debug('Loading JSON data')
		return json.load(self.file)


class InputFiles(argparse.Action):
	
	_SUPPORTED_FORMATS = {
		'conf'	: ConfFile,
		'json'	: JSONFile,
	}
	
	def __init__(self, option_strings, dest, nargs = None, **kwargs):
		if (nargs is None) or not isinstance(nargs, int) or (nargs != 2):
			raise ValueError('InputFile requires exactly 2 arguments (file path & file format)')
		
		super().__init__(option_strings, dest, nargs = nargs, **kwargs)
	
	def __call__(self, parser, namespace, values, option_string=None):
		reported_format = values[1]
		if reported_format.lower() not in self._SUPPORTED_FORMATS:
			raise ValueError('Input file format not supported: {}'.format(reported_format))
		item = self._SUPPORTED_FORMATS[reported_format.lower()](values[0])
		items = getattr(namespace, self.dest, None)
		if items is None:
			items = []
		items.append(item)
		setattr(namespace, self.dest, items)
		
	def __or__(self, other):
		return self


######################## End of I/O Classes ########################

BUILTIN_ARGPARSE_OPTIONS = {
	'--log-level'		: {'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'], 'default' : 'info', 'help' : 'minimum severity of the messages to be logged'},
	'--log-to-syslog'	: {'action' : 'store_true', 'default' : False, 'help' : 'send logs to syslog.'},
	'--input-file'		: {'action' : InputFiles, 'nargs' : 2, 'default' : argparse.SUPPRESS, 'help' : 'read parameters from a file or standard input (using the "-" special name)'},
	'--json'			: {'action' : 'store_true', 'default' : False, 'help' : 'output a JSON object as a string'},
}

class BaseCLI(metaclass = abc.ABCMeta):
	'''Abstract class for CLI implementation.
	The class side of the CLI protocol, you can add it to your class mixin to be used in the main function.
	
	ToDo: Documentation
	'''
	
	@classmethod
	def _build_argparser(cls, parent_parser = None):
		'''Default argparse creation
		It will build the argparse content and trigger the object creation using build_argparse_parser
		
		ToDo: Documentation
		'''
		
		parser_content = {}
		
		if hasattr(cls, '_ARGPARSE_OPTIONS'):
			parser_content.update(cls._ARGPARSE_OPTIONS)
		
		if parent_parser is None:
			parser_content.update(BUILTIN_ARGPARSE_OPTIONS)
		
		if False in parser_content:
			parser_content[False]['_class'] = cls
		else:
			parser_content[False] = {'_class' : cls}
		
		if hasattr(cls, '_result_json_default'):
			parser_content[False]['_json_default'] = cls._result_json_default
		
		return build_argparse_parser(module_object = sys.modules[cls.__module__], parent_parser = parent_parser, parser_content = parser_content)
	
	def _run_cli(self, *args, func = None, **kwargs):
		'''Execution logic.
		The class side of the CLI execution protocol. It searches for a class method with the requested name and executes it.

		ToDo: Documentation
		'''
		
		if func is None:
			raise ValueError('No functionality was requested.')
		
		if func.find('-') > -1:
			func = func.replace('-', '_')
		
		try:
			return getattr(self, func)(*args, **kwargs)
		except Exception:
			LOGGER.exception('Running %s failed', func)


def _populate_argparse_parser(argument_parser, parser_content):
	'''Parser building
	Recursive builder, for tree creation.
	'''
	
	for key, value in parser_content.items():
		if isinstance(key, bool):
			if key:
				if isinstance(value, tuple):
					subparsers_info, subparsers_map = value
					subparsers_info['dest'] = 'func'
# 					LOGGER.warning('Adding subparsers to parser %s with: %s', argument_parser, subparsers_info)
					subparsers = argument_parser.add_subparsers(**subparsers_info)
					_populate_argparse_parser(subparsers, subparsers_map)
				else:
					raise ValueError('The argparser value is not supported: {}'.format(parser_content))
			else:
# 				LOGGER.warning('Adding defaults to parser %s: %s', argument_parser, value)
				argument_parser.set_defaults(**value)
		elif isinstance(key, str):
			if isinstance(value, dict):
# 				LOGGER.warning('Adding argument %s with: %s', key, value)
				argument_parser.add_argument(key, **value)
			elif isinstance(value, tuple):
				subparser_info, subparser_arguments = value
# 				LOGGER.warning('Adding subparser %s with: %s', key, subparser_info)
				subparser = argument_parser.add_parser(key, **subparser_info)
				_populate_argparse_parser(subparser, subparser_arguments)
			elif issubclass(value, BaseCLI):
# 				LOGGER.warning('Adding BaseCLI %s as %s', value, key)
				subparser = argument_parser.add_parser(key)
				value._build_argparser(subparser)
			else:
				raise ValueError('The argparser value is not supported: {}'.format(parser_content))
		else:
			raise ValueError('The argparser key "{}" is not supported: {}'.format(key, parser_content))
	
	return argument_parser

def build_argparse_parser(module_object, parent_parser = None, parser_content = None):
	'''Argparse creation
	Create an argparser object based on the supplied information.
	
	The supported arguments are:
	- module_object: is the module's object, probably from sys.modules. It's used to process the module's docstring for metadata gathering purposes
	- parent_parser: is used to build this parser as a child for another parser. If present it should be the subparser already tied to the the parent parser.
	- parser_content: is a dictionary containing the elements to build the argument parser. The specifics live in the documentation.
	
	ToDo: Documentation
	'''	
	
	module_metadata = setuptools_get_metadata(module_object)
		
	if parent_parser is None:
		argument_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	else:
		argument_parser = parent_parser
	
	if 'description' in module_metadata:
		argument_parser.description = module_metadata['description']
	
	if 'long_description' in module_metadata:
		argument_parser.epilog = module_metadata['long_description']
	
	if 'version' in module_metadata:
		argument_parser.add_argument('--version', action = 'version', version = module_metadata['version'])
	
	if parser_content is None:
		parser_content = BUILTIN_ARGPARSE_OPTIONS.copy()
	else:
		parser_content.update(BUILTIN_ARGPARSE_OPTIONS)
# 	LOGGER.warning('Adding content to argparser: %s <- %s', argument_parser, parser_content)
	argument_parser = _populate_argparse_parser(argument_parser, parser_content)
	
	return argument_parser

def files_in_module_dir(module, dir_name, exclude = OS_FILES):
	'''Build tree of file names.
	It's a simple "walk" over a directory tree and return the file names. Includes a list of file names to be ignored.
	
	ToDo: Documentation
	'''
	
	module = pathlib.Path(module)
	
	if not module.is_dir():
		raise ValueError('{} is not a directory'.format(module.reolve()))
	
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

def main(argparser_like, module_name = '__main__'):
	'''Simplified run of an app.
	Performs a simplified procedure of an app run. It expects an argparse object that must contain a _class or _func attribute.
	
	The arg_parser object can also have:
	- log_level: to set the logging level, anything supported by the "logging" module.
	- log_to_syslog: configures the logging module to send the logs to syslog. This is only supported in POSIX where a "/dev/log" device exists.
	- config_file: if this is set, it should contain the path to a configuration file, that will be parsed an used as the base of the app configuration.
	- json: transforms the resulting object into a json string. If the result is a string this won't happen.
	- _json_default: if this is set, it should point to a function that will be used in the json conversion as the default casting. If not defined, "str" is then used (everything is casted to string).
	
	Results; if your code returns:
	- a string, it will be printed as is.
	- any other type of object will be printed with pprint
	- any other type of object, and the json flag was passed as True, then it will be printed as a json string (json.dumps)
	
	ToDo:
	- Documentation
	- Add support to log_file (send logs to file)
	'''
	
	if isinstance(argparser_like, argparse.ArgumentParser):
		arg_parser = argparser_like
	elif isinstance(argparser_like, dict):
		arg_parser = build_argparse_parser(sys.modules[module_name], parser_content = argparser_like)
	elif issubclass(argparser_like, BaseCLI):
		arg_parser = argparser_like._build_argparser()
	else:
		raise ValueError('Argparser or content not supported: {}'.format(argparser_like))
	
	args = arg_parser.parse_args()
	
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
	LOGGER.debug('Adding command line parameters to configurations: %s', vars_args)
	complete_input.update(vars_args)
	
	if hasattr(args, '_class'):
		if issubclass(args._class, BaseCLI):
			result = args._class(**complete_input)._run_cli(**complete_input)
		else:
			raise ValueError('Your class should inherit from BaseCLI')
	elif hasattr(args, '_func'):
		result = args._func(**complete_input)
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

def setuptools_get_metadata(module):
	'''Gets metadata for setuptools.setup
	It gathers some dynamic information from several sources for the package setup.py
	
	ToDo: Documentation
	'''
	
	metadata = {'name' : module.__name__}
	
	if hasattr(module, '__version__'):
		metadata['version'] = module.__version__
		
	if hasattr(module, '__doc__') and len(module.__doc__):
		doc_lines = module.__doc__.splitlines()
		if len(doc_lines[0]):
			metadata['description'] = doc_lines[0]
		if (len(doc_lines) > 1) and len(doc_lines[1]):
			metadata['long_description'] = doc_lines[1]
	
	return metadata

