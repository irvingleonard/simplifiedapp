#python
'''
Testing the _introspection.parameters_from_callable function
'''

from unittest import TestCase

from fixtures._introspection import *
from simplifiedapp._introspection import IS_CLASS_METHOD, IS_INSTANCE_METHOD, IS_STATIC_METHOD, parameters_from_method

class TestParametersFromMethod(TestCase):
	'''
	Tests for the parameters_from_method function
	'''
	
	maxDiff = None
	
	def test_instance_method(self):
		'''
		Testing parameters_from_method with an instance method
		'''
		
		expected_parameters = {
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True, 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False, 'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
		}
		result_parameters, result_type = parameters_from_method(FixtureDocumentedClass.fixture_documented_instance_method)
		self.assertDictEqual(expected_parameters, result_parameters)
		self.assertEqual(IS_INSTANCE_METHOD, result_type)

	def test_class_method(self):
		'''
		Testing parameters_from_method with a class method
		'''

		expected_parameters = {
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True,
					 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False,
					   'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
		}
		result_parameters, result_type = parameters_from_method(
			FixtureDocumentedClass.fixture_documented_class_method)
		self.assertDictEqual(expected_parameters, result_parameters)
		self.assertEqual(IS_CLASS_METHOD, result_type)
		
	def test_static_method(self):
		'''
		Testing parameters_from_method with a static method
		'''

		expected_parameters = {
			'args': {'default': [], 'docstring': {'description': 'Any other positional arguments'}, 'positional': True,
					 'special': 'varargs'},
			'kw1': {'docstring': {'description': 'First key word test parameter'}, 'positional': False},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}, 'positional': False},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'positional': False,
					   'special': 'varkw'},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}, 'positional': True},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}, 'positional': True},
			'pos1': {'docstring': {'description': 'First positional test parameter'}, 'positional': True},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}, 'positional': True},
		}
		result_parameters, result_type = parameters_from_method(
			FixtureDocumentedClass.fixture_documented_static_method)
		self.assertDictEqual(expected_parameters, result_parameters)
		self.assertEqual(IS_STATIC_METHOD, result_type)
