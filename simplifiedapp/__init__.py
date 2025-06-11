#! python
"""A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, depends on the complexity of your code.

ToDo:
- Everything
"""

from logging import basicConfig as logging_basicConfig, getLogger
from logging.handlers import SysLogHandler
from pprint import pprint as pretty_print

import sys

from ._defaults import DEFAULT_LOG_PARAMETERS, PPRINT_WIDTH, OS_FILES
from ._introspection import get_target, list_callable_children, object_metadata, Callable, IntrospectedArgumentParser

__version__ = '0.7.4'

LOGGER = getLogger(__name__)


def main(target=None, sys_argv=None):
	"""Simplified run of an app.
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
	"""

	if sys_argv is None:
		sys_argv = sys.argv[1:] if len(sys.argv) > 1 else []

	base_parser = IntrospectedArgumentParser.new_base_parser()
	base_values, callable_values = base_parser.parse_known_args(sys_argv)
	log_parameters = DEFAULT_LOG_PARAMETERS.copy()
	if hasattr(base_values, 'log_level') and len(base_values.log_level):
		log_parameters['level'] = base_values.log_level.upper()
	if hasattr(base_values, 'log_to_syslog') and base_values.log_to_syslog:
		log_parameters['handlers'] = [SysLogHandler(address='/dev/log')]
	logging_basicConfig(**log_parameters)
	LOGGER.debug('Logging configured  with: %s', log_parameters)

	target = get_target(target, depth=2)
	parser = IntrospectedArgumentParser(target)
	args = parser.parse_args(callable_values)
	args_w_keys = {key: value for key, value in vars(args).items()}
	callable_ = args_w_keys.pop('__call__')
	result = callable_(**args_w_keys)

	if isinstance(result, str):
		LOGGER.debug('The result is a string. Printing it as is.')
		print(result, end='')
	else:
		if hasattr(args, 'json') and args.json:
			LOGGER.debug('The result is an object. Printing it as a json string.')
			print(json.dumps(result, default=args._json_default if hasattr(args, '_json_default') else str))
		else:
			LOGGER.debug('The result is an object. Printing it with pprint.')
			pretty_print(result, width=PPRINT_WIDTH)
