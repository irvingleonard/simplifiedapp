#! python
'''A simple way to run your python code from the CLI
The module uses introspection to try and expose your code to the command line. It won't work in all cases, it depends on the complexity of your code.

This is the executable part.
'''

import logging
import sys

LOGGER = logging.getLogger(__name__)

try:
	import simplifiedapp
except ModuleNotFoundError:
	import __init__ as simplifiedapp

target, sys_argv = simplifiedapp, []
if len(sys.argv) > 1:
	if ((len(sys.argv[1]) == 2) and sys.argv[1].startswith('-')) or sys.argv[1].startswith('--'):
		sys_argv = sys.argv[1:]
	elif len(sys.argv) > 2:
		target = sys.argv[1]
		sys_argv = sys.argv[2:]

simplifiedapp.main(target = target, sys_argv = sys_argv)
