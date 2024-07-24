#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser, RawDescriptionHelpFormatter
from logging import getLogger
import sys

from ._introspection import object_metadata, parameters_from_callable
from . import argparse_patched

__version__ = '0.8.0dev0'

LOGGER = getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')

def dict_type_converter(input_string):
	'''
	'''
	
	return input_string


class LocalFormatterClass(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
	'''
	'''
	
	pass


class IntrospectedArgumentParser(ArgumentParser):
	'''
	'''
		
	@classmethod
	def _prepare_callable_parameter(cls, **details):
		'''Extends argument's values
		Uses the defaults, annotations and docstring to extend the argument values (type, action, etc.)
		
		ToDo:
		- Documentation
		'''
		
		result = {}
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
				if 'help' not in result:
					result['help'] = ''
				result['help'] += '(Use the key=value format for each entry)'
			else:
				result['type'] = type(details['default'])
				result['default'] = details['default']
		elif ('positional' in details) and not details['positional']:
			result['required'] = True
			
		if 'annotation' in details:
			print(details['annotation'])
			
		
		return result

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
	
	@classmethod
	def from_callable(cls, callable_, from_class=False):
		'''Extract argparse info from callable
		Uses introspection to build a dict out of a callable, usable to build an argparse tree.
		
		ToDo:
		- Documentation
		'''
		
		callable_metadata = object_metadata(callable_)
		
		result = cls(prog=callable_metadata['name'], description=callable_metadata.get('description', None), epilog=callable_metadata.get('long_description', None), formatter_class=LocalFormatterClass)
		
		return result
	
	@classmethod
	def params_from_callable(cls, callable_, callable_metadata=None, from_class=False):
		'''Extract argparse info from callable
		Uses introspection to build a dict out of a callable, usable to build an argparse tree.
		
		ToDo:
		- Documentation
		'''
		
		parameters = parameters_from_callable(callable_, callable_metadata=callable_metadata, from_class=from_class)
		parameters = {'_'.join((callable_metadata['name'], parameter)) : cls._prepare_callable_parameter(parameter, **details) for parameter, details in parameters.items()}
		return parameters
		for parameter_name, parameter_details in parameters.items():
			result
		
		
		
		if from_class:
			is_boundmethod = False
			if len(args):
				if args[0] == 'self':
					is_boundmethod = True
					args.pop(0)
				elif args[0] in ['cls', 'type']:
					args.pop(0)

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
