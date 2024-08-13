#python
'''
Testing the _introspection.parameters_from_callable function
'''

from unittest import TestCase

from fixtures._introspection import *
from simplifiedapp._introspection import parameters_from_function

class TestParametersFromFunction(TestCase):
	'''
	Tests for the parameters_from_callable with simple function
	'''
	
	maxDiff = None
	
	def test_simple_callable(self):
		'''
		Testing "parameters_from_callable" with a simple callable
		'''
		
		expected_result = {
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True, 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'default': False, 'docstring': {'description': 'Second key word test parameter', 'is_optional': True, 'type_name': 'bool'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False, 'special': 'varkw'},
			'mult1': {'default': 'mult1', 'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'default': 2, 'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter', 'is_optional': False, 'type_name': 'float'}, 'positional': True},
			'pos2': {'annotation': bool, 'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
		}
		self.assertDictEqual(expected_result, parameters_from_function(fixture_documented_function))

	def test_instance_method(self):
		'''
		Testing "parameters_from_callable" with a instance method
		'''
		
		expected_result={
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True, 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False, 'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
			'self': {'positional': True},
		}
		self.assertDictEqual(expected_result, parameters_from_function(FixtureDocumentedClass().fixture_documented_instance_method))
		
	def test_class_method(self):
		'''
		Testing "parameters_from_callable" with a class method
		'''
		
		expected_result={
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True, 'special': 'varargs'},
			'cls': {'positional': True},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False, 'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True}
		}
		self.assertDictEqual(expected_result, parameters_from_function(FixtureDocumentedClass.fixture_documented_class_method))
		
	def test_static_method(self):
		'''
		Testing "parameters_from_callable" with a static method
		'''
		
		expected_result={
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True, 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False, 'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
		}
		self.assertDictEqual(expected_result, parameters_from_function(FixtureDocumentedClass.fixture_documented_static_method))
