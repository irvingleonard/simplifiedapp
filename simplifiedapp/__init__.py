#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter, ArgumentParser, RawDescriptionHelpFormatter
from inspect import getmodule, stack
from logging import basicConfig as logging_basicConfig, getLogger
from logging.handlers import SysLogHandler
from pprint import pprint as pretty_print
import sys

from ._introspection import IS_CLASS, IS_FUNCTION, IS_MODULE, enumerate_object_callables, execute_callable, get_target, object_metadata, parameters_from_class, parameters_from_function
from . import argparse_patched

__version__ = '0.8.0.dev4'

LOGGER = getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')


class VarKWParameter(dict):
	'''
	'''

	def __init__(self, input_string, /):
		'''
		'''

		key, value = input_string.split('=', maxsplit=1)
		super().__init__({key : value})


class LocalFormatterClass(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
	'''
	'''
	
	pass


class IntrospectedArgumentParser(ArgumentParser):
	'''
	'''

	BUILTIN_OPTIONS = {
		'--log-level'		: {'choices' : ['notset', 'debug', 'info', 'warning', 'error', 'critical'], 'default' : 'info', 'help' : 'minimum severity of the messages to be logged'},
		'--log-to-syslog'	: {'action' : 'store_true', 'default' : False, 'help' : 'send logs to syslog.'},
		# 'input-file'		: {'action' : InputFiles, 'nargs' : 2, 'default' : argparse.SUPPRESS, 'help' : 'read parameters from a file or standard input (using the "-" special name). Consumes 2 parameters: first one is the path (or "-") and second one is the format'},
		# 'output-file'		: {'action' : 'store_true', 'default' : False, 'help' : 'output a JSON object as a string'},
	}

	@classmethod
	def _prepare_parameter(cls, **details):
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
					errors.append('''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's optional but doesn't match "{parent_description}"'s signature''')
				elif (not details['docstring']['is_optional']) and ('default' in details):
					warnings.append('''Type hinting for parameter "{parameter_name}" from "{parent_description}" suggests it's required but doesn't match "{parent_description}"'s signature''')
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
		'''Prepare parameters
		Takes introspected parameters and convert them into argparse friendly versions.
		
		:param dict raw_parameters: a mapping of parameter name to parameter details like the one returned by "parameters_from_callable"
		:param str container_name: the name of the object containing the provided parameters
		:param dict? initial_values: a mapping of parameter names and values to use as default (overriding the ones in the signature if present)
		:returns dict: a mapping of parameter names and details that can be used to build an ArgumentParser
		'''
		
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
		'''Extract argparse info from class
		Uses introspection to build a dict out of a class, usable to build an argparse tree.

		ToDo:
		- Documentation
		'''
		
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
		'''Return new base parser
		Builds a base parser, which contains the basic switches added by the module

		ToDo:
		- Documentation
		'''

		LOGGER.debug('Creating new base parser')
		result = cls(formatter_class=LocalFormatterClass, add_help=False)
		for parameter_name, kwargs in cls.BUILTIN_OPTIONS.items():
			result.add_argument(parameter_name, **kwargs)

		return result
		
	@classmethod
	def run_callable(cls, callable_, args_w_keys={}):
		'''Extract argparse info from callable
        Uses introspection to build a dict out of a callable, usable to build an argparse tree.

        ToDo:
        - Documentation
        '''

		callable_metadata = object_metadata(callable_)
		callable_args_w_keys, callable_name = {}, callable_metadata['name']
		parameters = parameters_from_callable(callable_, callable_metadata=callable_metadata)
		for key, values in args_w_keys.items():
			if key[:len(callable_name)] == callable_name:
				param_name = key[len(callable_name)+1:]
				if ('special' in parameters[param_name]) and (parameters[param_name]['special'] == 'varkw'):
					callable_args_w_keys[param_name] = {}
					for kw_dict in values:
						callable_args_w_keys[param_name].update(kw_dict)
				else:
					callable_args_w_keys[param_name] = values

		result = execute_callable(callable_, args_w_keys=callable_args_w_keys, callable_metadata=callable_metadata, parameters=parameters)
		return str(result)


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
	base_values, sys_argv = base_parser.parse_known_args(sys_argv)
	initial_values = vars(base_values)

	log_parameters = DEFAULT_LOG_PARAMETERS.copy()
	if hasattr(base_values, 'log_level') and len(base_values.log_level):
		log_parameters['level'] = base_values.log_level.upper()
	if hasattr(base_values, 'log_to_syslog') and base_values.log_to_syslog:
		log_parameters['handlers'] = [SysLogHandler(address = '/dev/log')]
	logging_basicConfig(**log_parameters)
	LOGGER.debug('Logging configured  with: %s', log_parameters)

	target, target_type = get_target(target=target)

	if target_type == IS_MODULE:
		LOGGER.debug('Generating parser data for target as a module')
		raise NotImplementedError('Module target')
	elif target_type == IS_CLASS:
		parser = IntrospectedArgumentParser.from_class(class_=target, parents=[base_parser], initial_values=initial_values)
	elif target_type == IS_FUNCTION:
		parser = IntrospectedArgumentParser.from_callable(callable_=target, parents=[base_parser], initial_values=initial_values)
	else:
		raise RuntimeError('Unknown target type "{}"'.format(target_type))

	args = parser.parse_args(sys_argv)
	args_w_keys = {key.replace('-', '_') : value for key, value in vars(args).items()}
	callable_ = args_w_keys.pop('callable')
	result = parser.run_callable(callable_=callable_, args_w_keys=args_w_keys)

	if isinstance(result, str):
		LOGGER.debug('The result is a string. Printing it as is.')
		print(result, end='')
	else:
		if hasattr(args, 'json') and args.json:
			LOGGER.debug('The result is an object. Printing it as a json string.')
			print(json.dumps(result, default = args._json_default if hasattr(args, '_json_default') else str))
		else:
			LOGGER.debug('The result is an object. Printing it with pprint.')
			pretty_print(result, width = PPRINT_WIDTH)



	return

	
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
