#! python
'''Boilerplate stuff done for you.
This module has some generic classes and functions for several purposes.

ToDo:
- Everything
'''

import logging
import sys

LOGGER = logging.getLogger(__name__)

try:
	import simplifiedapp
except ModuleNotFoundError:
	import __init__ as simplifiedapp

def simplifiedapp_main(target):
	pass

if (len(sys.argv) > 1):
	simplifiedapp.main(target = sys.argv[1], sys_argv = sys.argv[2:])
else:
	simplifiedapp.main(target = simplifiedapp_main)
