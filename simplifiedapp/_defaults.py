#!python
"""

"""

from .argparse_patched import argparse

DEFAULT_LOG_PARAMETERS = {
	'format'	: '%(asctime)s|%(name)s|%(levelname)s:%(message)s',
	'datefmt'	: '%H:%M:%S',
}
PPRINT_WIDTH = 270
OS_FILES = ('.DS_Store',)


class LocalFormatterClass(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
	"""
	"""
	pass