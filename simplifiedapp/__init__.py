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

__version__ = '0.5.1'

LOGGER = logging.getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')
BUILTIN_ARGPARSE_OPTIONS = {
	'--log-level'		: {'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'], 'default' : 'info', 'help' : 'minimum severity of the messages to be logged'},
	'--log-to-syslog'	: {'action' : 'store_true', 'default' : False, 'help' : 'send logs to syslog.'},
	'--config-file'		: {'default' : argparse.SUPPRESS, 'help' : 'read this parameters from a configuration file'},
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
					LOGGER.debug('Adding subparsers to parser %s with: %s', argument_parser, subparsers_info)
					subparsers = argument_parser.add_subparsers(**subparsers_info)
					_populate_argparse_parser(subparsers, subparsers_map)
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
				LOGGER.debug('Adding subparser %s with: %s', key, subparser_info)
				subparser = argument_parser.add_parser(key, **subparser_info)
				_populate_argparse_parser(subparser, subparser_arguments)
			elif issubclass(value, BaseCLI):
				LOGGER.debug('Adding BaseCLI %s as %s', value, key)
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
	LOGGER.debug('Adding content to argparser: %s <- %s', argument_parser, parser_content)
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

def load_configuration_from_file(config_file):
	'''Load configuration settings from file.
	It creates a dictionary from an ini-type configuration file's settings. This disable the possibility of having a setting in "DEFAULT" with the same name as another section on the file. It's intended to be used by the "main" function.
	
	ToDo: Documentation
	'''
	
	config_file = pathlib.Path(config_file)
	if config_file.is_file():
		config = configparser.ConfigParser()
		config.optionxform = str
		LOGGER.debug('Reading config file %s', config_file)
		config.read(config_file)
		configuration = {}
		for section, content in config.items():
			if section == 'DEFAULT':
				configuration.update({key : value for key, value in content.items()})
			else:
				configuration[section] = {key : value for key, value in content.items()}
		return configuration
	else:
		LOGGER.warning('Unable to load configuration from %s', str(config_file))
		return {}

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
	
	if hasattr(args, 'config_file'):
		configurations = load_configuration_from_file(args.config_file)
	else:
		configurations = {}
		
	if len(configurations):
		LOGGER.debug('Configurations loaded from file: %s', configurations)
	else:
		LOGGER.debug('No configurations were loaded from file')
	
	vars_args = vars(args)	
	LOGGER.debug('Adding command line parameters to configurations: %s', vars_args)
	configurations.update(vars_args)
	
	if hasattr(args, '_class'):
		if issubclass(args._class, BaseCLI):
			result = args._class(**configurations)._run_cli(**configurations)
		else:
			raise ValueError('Your class should inherit from BaseCLI')
	elif hasattr(args, '_func'):
		result = args._func(**configurations)
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

