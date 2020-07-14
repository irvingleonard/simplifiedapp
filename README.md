# simplifiedapp

Handling the biolerplate code for your python project. By keeping some simple standards you can leverage this module to make some boilerplate function for you.

The CLI helpers can be used in the class mode or the function mode. Also, it can be implemented on a regular python module or a single file script/module. The combination of all that would yield four different possibilities. This documentation covers two, and the other two can be derived from there.

## A note about metadata

It's a good idea to add docstrings to your modules, classes, and functions. This module uses your module's docstring to derive descriptions which are used for different purposes. 

The expected format is:
- the first line in the docstring should be a simple description of your module, just a couple words
- the second line should include a longer explanation of what the module does

You shouldn't use strict line length for this lines (like [PEP 8](https://www.python.org/dev/peps/pep-0008/) suggests) or if you do, then make the longer description fit in a single line.

You should also use the `__version__` variable in your module following [PEP 396](https://www.python.org/dev/peps/pep-0396/), which is picked up by the code and will be leverage later by different tools.

## The script - function example

This assumes a very basic use case, in which you would be running a single function with some required and some optional parameters. It will concern a single file called *myscript.py*.

### `myscript.py`

```
#! python
'''En example script.
This script has an example function for documentation purposes.
'''

import simplifiedapp

__version__ = '0.7.3-post1'	#This value is used for the --version switch

def main(self, *args, i_need_this = None, a_boolean_switch = False, **kwargs): #The i_need_this parameter (or any parameter for that matter) can't be a positional argument or else it won't work. Your function MUST accept **kwargs (and it's a good idea to accept *args too)
	pass #do stuff

_ARGPARSE_OPTIONS = { #There's a documentation subsection for this data structure.
		'i-need-this'			: {'help' : 'This piece of information is required'},
		'--this-would-be-nice'	: {'default' : argparse.SUPPRESS, 'help' : 'It would be nice to have this. If not provided, there will be no attribute for it in the resulting argparser (because of the default)'},
		'--a-boolean-switch'	: {'action' : 'store_true', 'default' : False, 'help' : 'To be or not to be.'},
		False	: {'_func' : main} #This references your main function
	}
	
if __name__ == '__main__':
	simplifiedapp.main(_ARGPARSE_OPTIONS)
```

## The module - class example

This assumes a rather complex use case, in which there will be some subcommands and one of them will be implemented in a different module. There will be a python module (*mymodule*), with an `__init__.py` and a `__main__.py` files living inside a module directory. There will be an *othermodule* that will implement something similar. You would be using a class to implement your functionalities.

### `__init__.py`

```
#! python
'''An example module.
This module has an example class for documentation purposes.
'''

import simplifiedapp

__version__ = '0.7.3-post1' #This value is used for the --version switch and also in the setuptools helper

import othermodule

class MyExampleClass(simplifiedapp.BaseCLI):
	'''The example class
	This is the main subject of the module
	'''
	
	_ARGPARSE_OPTIONS = { #There's a documentation subsection for this data structure.
		'something-shared'	: {'help' : 'This will exists for all the commands'},
		True	: ({'help' : 'Possible jumps'}, {
			'spring'	: ({'help' : 'sprang out of there'}, {
				'foo'	: {'help' : 'I need this'},
				'--bar'	: {'help' : 'this I can spare'},
			}),
			'skip'	: ({'help' : 'skipping home'}, {
				'--baz'	: {'action' : 'store_true', 'default' : False, 'help' : 'to bar or not to bar'},
			}),
			'leap'	: ({'help' : 'leap of faith'}, {
				'qux' : {'nargs' : '*', 'help' : 'get any number of foo'},
			}),
			'hop'	: othermodule.AnotherExampleClass, #This assumes that the AnotherExampleClass that lives in othermodule inherits from BaseCLI too (or something with the same interface).
		}),
	}
	
	def spring(self, *args, foo = None, bar = 'initial_value', **kwargs): #The foo parameter (or any parameter for that matter) can't be a positional argument or else it won't work. Your function MUST accept **kwargs (and it's a good idea to accept *args too)
		'''The spring function
		Some springing needs to be done
		'''
		
		pass #Do stuff...
		
	def skip(self, *args, baz = False, **kwargs):
		pass
		
	def leap(self, *args, qux = (), **kwargs):
		pass
```

### `__main__.py`

```
#!python
'''An example module
This module has an example class for documentation purposes.

This is the execution module
'''

import simplifiedapp

try:
	import mymodule
except ModuleNotFoundError:
	import __init__ as mymodule

simplifiedapp.main(mymodule.Main)
```

## _ARGPARSE_OPTIONS

This data structure is a dictionary with some specific format. The rationale is to use the [argparse module](https://docs.python.org/dev/library/argparse.html) in a declarative way. There are currently two basic argparser methods supported:
- the dict key is string and the value is dict: this will trigger a call to [add_argument method](https://docs.python.org/dev/library/argparse.html#the-add-argument-method) where the key will be the **argument name** and the value will be unpacked as keyword arguments.
- the dict key is bool False and the value is dict: this will trigger a call to [set_defaults method](https://docs.python.org/dev/library/argparse.html#argparse.ArgumentParser.set_defaults) unpacking the value to be used as keyword arguments.

### Using subparsers

The use of subparser is also supported. For this purpose there are another two argparser methods that are supported:
- the dict key is bool True and the value is a tuple: this will trigger a call to [add_subparsers method](https://docs.python.org/dev/library/argparse.html#argparse.ArgumentParser.add_subparsers) and will use the first element in the value tuple (that MUST be a dict) as keyword arguments via unpacking. The second element in the tuple will be a dict of subparsers with subparser/subcommand names as keys.
- the dict key is a string and the value is a tuple: this will trigger a call to [add_parser method](https://docs.python.org/dev/library/argparse.html#argparse.ArgumentParser.add_subparsers) on the parent special action object returned by add_subparsers. It will use the first element in the tuple (that MUST be a dict) as keyword arguments via unpacking. The second element of the tuple will be a dict containing this subparser's arguments
- the dict key is a string and the value is a subclass of BaseCLI: it will work very similar to the previous case. The arguments in this case are built using the class mechanism.

## Results

Your code's return values will be printed differently based on the type:
- strings will be printed as is, without any processing at all
- any other type of object will be printed using the [pprint.pprint](https://docs.python.org/dev/library/pprint.html#pprint.pprint) function
- any other type of object, and the json flag was passed as True, then it will be printed as a [json.dumps](https://docs.python.org/dev/library/json.html#json.dumps) string

## A note on configuration building

The code will parse the arguments passed via command line and build a *configuration* dictionary out of it. It will also try to parse the configuration file if it was requested (via `--config-file`) which should be a standard [configparser](https://docs.python.org/dev/library/configparser.html) file (basically an INI file). If the configuration file is parsed, the **DEFAULT** section values will be converted to a dictionary and merged into the *configuration*; the others sections, if they exist, will be added to the *configuration* under the *section* key, as dictionaries.

## setuptools

Because you'll be packaging your module, you'll have to create a `setup.py` file and populate it. There's a function that can help you assuming that the previous metadata suggestions were followed

```
#!python
"""A setuptools based setup module.
Just using setuptools to package/install this module
"""

import setuptools

import simplifiedapp

import mymodule

setuptools.setup(
	url = 'https://example.com/path/to/my/app/site',
	author = 'A random coder (me)',
	author_email = 'arandomcoder@example.com',
	license='Whatever license you see fits', #You might add some specific license, use the classifiers (next parameter)
	classifiers = [	#Possible classifiers are documented in https://pypi.org/classifiers/
		'Some :: Classifier',
		'Another :: Classifier',
		'Classifier :: The Third',
		'Something :: From the PyPI :: URL',
		'Even :: More :: Weird Looking although Intelligible :: Strings',
	],
	keywords = 'some keywords',
	python_requires = '>=3.5',
	packages = setuptools.find_packages(),
	
	**simplifiedapp.setuptools_get_metadata(mymodule)
)
```

The name, version, description and long_description parameters are derived from mymodule. If those doesn't work odds are that there might be something non-compliant (with the metadata suggestions) in your module.
