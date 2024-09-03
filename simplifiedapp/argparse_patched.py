#python
'''
'''

from logging import getLogger
from pprint import pformat

import argparse


LOGGER = getLogger(__name__)


def objects_are_family(first, second, raise_exception=True):
	'''
	'''
	
	first_type, second_type = type(first), type(second)
	# print('Comparing', first_type, 'and', second_type, sep=' ')
	if issubclass(first_type, second_type) or issubclass(second_type, first_type):
		return True
	else:
		if raise_exception:
			raise ValueError("Can't compare unrelated objects {} and {}".format(first_type, second_type))
		else:
			return False

### Enhanced output for better troubleshooting ###
	
def argument_group_repr(self):
	'''
	'''
	
	args = ['<parent_container>']
	for attr in ('title', 'description', 'prefix_chars', 'argument_default', 'conflict_handler'):
		args.append('='.join((attr, repr(getattr(self, attr)))))
	return '{}({})'.format(self.__class__.__name__, ', '.join(args))
argparse._ArgumentGroup.__repr__ = argument_group_repr

### Patch equality comparison across the board ###

def compare_objects(self, other, /):
	'''Compare objects for equality
	Compare 2 objects based on their __dict__ content. Also require them to be related (have the same class or one being child of the other)
	'''
	
	objects_are_family(self, other)
	my_vars, other_vars = vars(self), vars(other)
	if hasattr(self, 'ATTRIBUTE_EQUALITY_IGNORE_LIST'):
		my_vars = {key : value for key, value in my_vars.items() if key not in self.ATTRIBUTE_EQUALITY_IGNORE_LIST}
	if hasattr(other, 'ATTRIBUTE_EQUALITY_IGNORE_LIST'):
		other_vars = {key : value for key, value in other_vars.items() if key not in other.ATTRIBUTE_EQUALITY_IGNORE_LIST}
	# print('Comparing vars', my_vars, 'and', other_vars, sep=' ')
	result = my_vars == other_vars
	if not result:
		print('Found a discrepancy: \n{}\nand\n{}'.format(pformat(my_vars), pformat(other_vars)))
	return result
	
argparse._AttributeHolder.__eq__ = compare_objects
argparse.HelpFormatter.__eq__ = compare_objects
argparse.FileType.__eq__ = compare_objects
argparse._ActionsContainer.__eq__ = compare_objects

### Ignoring attributes to avoid errors ###

argparse._HelpAction.ATTRIBUTE_EQUALITY_IGNORE_LIST = ('container',)
argparse._VersionAction.ATTRIBUTE_EQUALITY_IGNORE_LIST = ('container',)

### ArgumentParser equality special ###

def argument_parser_eq(self, other, /):
	'''Special __eq__ for ArgumentParser
	The __init__ method adds an entry to the "_registries" pointing to a function defined locally, meaning that it will be pointing to a "different" function on every instance (which will ALWAYS compare as different).
	'''
	
	objects_are_family(self, other)
	my_vars, other_vars = vars(self), vars(other)
	del my_vars['_registries']['type']
	del other_vars['_registries']['type']
	result = my_vars == other_vars
	if not result:
		print('Found a discrepancy: \n{}\nand\n{}'.format(pformat(my_vars), pformat(other_vars)))
	return result
argparse.ArgumentParser.__eq__ = argument_parser_eq

