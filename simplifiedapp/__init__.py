#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser, RawDescriptionHelpFormatter
from inspect import getmodule, stack
from logging import getLogger
import sys

from ._introspection import IS_CALLABLE, IS_CLASS, IS_MODULE, get_target, object_metadata, parameters_from_callable
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

	BUILTIN_OPTIONS = {
		'log-level'		: {'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'], 'default' : 'info', 'help' : 'minimum severity of the messages to be logged'},
		'log-to-syslog'	: {'action' : 'store_true', 'default' : False, 'help' : 'send logs to syslog.'},
		# 'input-file'		: {'action' : InputFiles, 'nargs' : 2, 'default' : argparse.SUPPRESS, 'help' : 'read parameters from a file or standard input (using the "-" special name). Consumes 2 parameters: first one is the path (or "-") and second one is the format'},
		# 'output-file'		: {'action' : 'store_true', 'default' : False, 'help' : 'output a JSON object as a string'},
	}

	@classmethod
	def _prepare_callable_parameter(cls, **details):
		'''Extends argument's values
		Uses the defaults, annotations and docstring to extend the argument values (type, action, etc.)
		
		ToDo:
		- Documentation
		'''
		
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
				if 'help' not in result:
					result['help'] = ''
				result['help'] += '(Use the key=value format for each entry)'
			else:
				result['type'] = type(details['default'])
				result['default'] = details['default']
		elif ('positional' in details) and not details['positional']:
			result['required'] = True
			
		if 'annotation' in details:
			LOGGER.warning('Type hinting from parameter annotation is not supported yet')

		if 'docstring' in details:
			if 'type_name' in details['docstring']:
				LOGGER.warning('Type hinting from docstring is not supported yet')
			if 'is_optional' in details['docstring']:
				if details['docstring']['is_optional'] and ('default' not in details):
					errors.append('''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's optional but doesn't match "{parent_description}"'s signature''')
				elif (not details['docstring']['is_optional']) and ('default' in details):
					warnings.append('''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's required but doesn't match "{parent_description}"'s signature''')
			if 'description' in details['docstring']:
				result['help'] = details['docstring']['description']

		if 'version' in details:
			result.update(details)
			result['action'] = 'version'

		return result, errors, warnings
	
	@classmethod
	def from_callable(cls, callable_, from_class=False, parents=None, initial_values={}):
		'''Extract argparse info from callable
		Uses introspection to build a dict out of a callable, usable to build an argparse tree.
		
		ToDo:
		- Documentation
		'''

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
		parameters = cls.params_from_callable(callable_, callable_metadata=callable_metadata, initial_values=initial_values)
		for parameter_name, kwargs in parameters.items():
			result.add_argument('--{}'.format(parameter_name), **kwargs)

		return result

	@classmethod
	def new_base_parser(cls):
		'''Return new base parser
		Builds a base parser, which contains the basic switches added by the module

		ToDo:
		- Documentation
		'''

		LOGGER.debug('Creating new base parser')
		result = cls(formatter_class=LocalFormatterClass, add_help=False)
		for parameter_name, kwargs in cls.BUILTIN_OPTIONS.items():
			result.add_argument(('-{}' if len(parameter_name) == 1 else '--{}').format(parameter_name), **kwargs)

		return result

	@classmethod
	def params_from_callable(cls, callable_, callable_metadata=None, from_class=False, initial_values={}):
		'''Extract argparse info from callable
		Uses introspection to build a dict out of a callable, usable to build an argparse tree.
		
		ToDo:
		- Documentation
		'''

		if callable_metadata is None:
			callable_metadata = {}
		raw_parameters = parameters_from_callable(callable_, callable_metadata=callable_metadata, from_class=from_class)
		if 'version' in callable_metadata:
			raw_parameters['version'] = {'version' : callable_metadata['version']}
		parameters = {}
		for parameter, details in raw_parameters.items():
			parameter_args, errors, warnings = cls._prepare_callable_parameter(**details)
			for error in  errors:
				LOGGER.error(error.format(parameter_name=parameter, parent_description=callable_metadata['name']))
			for warning in  warnings:
				LOGGER.warning(warning.format(parameter_name=parameter, parent_description=callable_metadata['name']))
			if parameter in initial_values:
				parameter_args['default'] = initial_values[parameter]
			parameter_name = '_'.join((callable_metadata['name'], parameter))
			parameter_name = parameter_name.replace('_', '-')
			parameters[parameter_name] = parameter_args

		return parameters


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

	base_parser = IntrospectedArgumentParser.new_base_parser()

	target, target_type = get_target(target=target)

	if target_type == IS_MODULE:
		LOGGER.debug('Generating parser data for target as a module')
		# parser = IntrospectedArgumentParser.from_callable(callable_=target)
	elif target_type == IS_CLASS:
		LOGGER.debug('Generating parser data for target as a class')
		arg_parser_data.update(class_args(target))
	elif target_type == IS_CALLABLE:
		parser = IntrospectedArgumentParser.from_callable(callable_=target, parents=[base_parser])
	else:
		raise RuntimeError('Unknown target type "{}"'.format(target_type))



	result = parser.parse_args(sys_argv)
	print(result)
	return

	# complete_input = {}
	# first_pass = BuiltinParser().parse_args(sys_argv)
	#
	# if first_pass is not None:
	# 	log_parameters = DEFAULT_LOG_PARAMETERS.copy()
	#
	# 	if hasattr(first_pass, 'log_level') and len(first_pass.log_level):
	# 		log_parameters['level'] = first_pass.log_level.upper()
	#
	# 	if hasattr(first_pass, 'log_to_syslog') and first_pass.log_to_syslog:
	# 		log_parameters['handlers'] = [logging.handlers.SysLogHandler(address = '/dev/log')]
	#
	# 	logging.basicConfig(**log_parameters)
	# 	LOGGER.debug('Logging configured  with: %s', log_parameters)
	#
	# 	if hasattr(first_pass, 'input_file'):
	# 		for input_ in first_pass.input_file:
	# 			LOGGER.debug('Merging values from %s', input_)
	# 			complete_input = complete_input | input_
	#
	caller = getmodule(stack()[1][0])
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
	# print(result)
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
