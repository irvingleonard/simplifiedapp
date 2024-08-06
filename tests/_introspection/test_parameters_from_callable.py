#python
'''
Testing the _introspection.parameters_from_callable function
'''

from unittest import TestCase

from simplifiedapp._introspection import object_metadata, parameters_from_callable

from fixtures import _introspection as introspection_fixture

class TestParametersFromCallable(TestCase):
	'''
	Tests for the parameters_from_callable with simple function
	'''
	
	maxDiff = None
	
	def test_simple_callable(self):
		'''
		Testing with a simple callable
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
		self.assertDictEqual(expected_result, parameters_from_callable(introspection_fixture.test_callable, object_metadata(introspection_fixture.test_callable)))

	def test_instance_method(self):
		'''
		Testing with a instance method
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
		test_object = introspection_fixture.TestClass().test_instance_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))
		
	def test_class_method(self):
		'''
		Testing with a class method
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
		test_object = introspection_fixture.TestClass.test_class_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))
		
	def test_static_method(self):
		'''
		Testing with a static method
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
		test_object = introspection_fixture.TestClass.test_static_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))

