#!python
"""A setuptools based setup module.

ToDo:
- Everything
"""

import setuptools

import simplifiedapp

setuptools.setup(
	url = 'https://github.com/irvingleonard/simplifiedapp',
	author = 'Irving Leonard',
	author_email = 'irvingleonard@gmail.com',
	license='BSD 2-Clause "Simplified" License',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	keywords = 'cli main setuptools',
	python_requires = '>=3.6',
	packages = setuptools.find_packages(),
	
	**simplifiedapp.object_metadata(simplifiedapp)
)