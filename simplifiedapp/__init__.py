#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

ToDo:
- Everything
'''

from argparse import ArgumentParser
from logging import getLogger
import sys

from docstring_parser import parse as docstring_parse

__version__ = '0.8.0dev0'

LOGGER = getLogger(__name__)

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store')


class BaseParser(ArgumentParser):
    pass


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