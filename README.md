# simplifiedapp

A simple way to run your python code from the CLI.

The module uses introspection to try and expose your code to the command line. It won't work in all cases, depends on the complexity of your code.

### Functions

The simplest situation is a function (callable). A function might require some parameters and accept other if provided. This is translated into required and optional parameters to argparse. The annotations are translated into type checks otherwise the inputs are expected to be strings (argparse's default behavior). There are some "parameter names" that are used internally; if you use such parameter names on your function odds are that there will be issues. Such parameter names include:
- __simplifiedapp_
- log_level
- log_to_syslog
- input_file
- json

```
def main(self, i_need_this, *args, a_boolean_switch = False, **kwargs): #Your function MUST accept **kwargs (and it's a good idea to accept *args too)
	pass #do stuff

if __name__ == '__main__':
	simplifiedapp.main(main)	# simplifiedapp.main('main'), as a string, will also work (for your dynamic calling needs)
```

### Classes

The target can also be a class. Subparsers are created for every available and not special method in the class. If the class has a `__call__` method then it can be "run", otherwise you'll get an error. While running class subparsers, you must provide the parameters required by `__init__` and by `__call__` (and you could also provide optional parameters to both).

```
class MyExampleClass:
	'''The example class
	This is the main subject of the module
	'''
	
	def spring(self, foo, *args, bar = 'initial_value', **kwargs): #TYour function MUST accept **kwargs (and it's a good idea to accept *args too)
		'''The spring function
		Some springing needs to be done
		'''
		
		pass #Do stuff...
		
	def skip(self, *args, baz = False, **kwargs):
		pass
		
	def leap(self, *args, qux = (), **kwargs):
		pass

f __name__ == '__main__':
	simplifiedapp.main(MyExampleClass)	# simplifiedapp.main('MyExampleClass'), as a string, will also work (for your dynamic calling needs)
```

### Modules

The modules can't be "run" by themselves, instead they contain subparsers for their classes and functions.

You just probably want to add something like this in you module's `__main__.py`


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

simplifiedapp.main(mymodule)	# simplifiedapp.main('mymodule'), as a string, will also work (for your dynamic calling needs)
```

## Docstrings

It's a good idea to add docstrings to your modules, classes, and functions. Your module's docstrings are parsed to derive descriptions which are used for different purposes. 

The expected format is:
- the first line in the docstring should be a simple description of your module, just a couple words
- the second line and up to the first empty line (or the end of the string) could be a paragraph that should include a longer explanation of what the module does.

You shouldn't use strict line length for the first line (like [PEP 8](https://www.python.org/dev/peps/pep-0008/) suggests) or if you do, make it fit in a single line.

## Versioning

You should use the `__version__` variable in your module following [PEP 396](https://www.python.org/dev/peps/pep-0396/)

This will provide the `--version` switch in the command line and can also be used to automate the setuptools call in 'setup.py'.

## Input

The first step of the run is to build a `configuration` dictionary out of several sources:
- The CLI arguments -> The module exposes your callable's parameters, which can (or must) be provided via command line
- The input files -> configuration living in files can be fed via the `--input-file` switch. So far INI and JSON files are supported.

### INI Input

The code will parse the arguments passed via command line and build a *configuration* dictionary out of it. It will also try to parse the configuration file if it was requested (via `--input-file /path/to/file ini`) which should be a standard [configparser](https://docs.python.org/dev/library/configparser.html) file. If the configuration file is parsed, the **DEFAULT** section values will be converted to a dictionary and merged into the *configuration*; the others sections, if they exist, will be added to the *configuration* under the *section* key, as dictionaries.

### JSON Input

A valid JSON file has an object (`dict`) as the root, which is merged directly into the `configuration` dictionary.

## Execution

When you trigger an execution it starts by doing some boilerplate stuff, basically the setup of the logging system (based on the CLI arguments). Then the `configuration` dictionary (with only CLI parameters so far) gets udpated with any `--input-file` provided.

The configuration values are then fed to the target and a result is expected.

The result gets a different treatment depending on several factors:
- If the result is a string, it will be printed "as is", not even a line change gets added at the end (default behavior for [print](https://docs.python.org/3/library/functions.html#print)).
- Otherwise it's printed with [pprint.pprint](https://docs.python.org/dev/library/pprint.html#pprint.pprint)
- If the `--json` switch was passed, then it gets printed with [json.dumps](https://docs.python.org/dev/library/json.html#json.dumps)

## setuptools

You can leverage some functions to simplify the packaging of your module. Basically, the `object_metadata` can save you some updating in the `setup.py` file by doing:

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
	python_requires = '>=3.7',
	packages = setuptools.find_packages(),
	
	**simplifiedapp.object_metadata(mymodule)
)
```

The name, version, description and long_description parameters are derived from mymodule. If those doesn't work odds are that there might be something non-compliant (with the metadata suggestions) in your module.
