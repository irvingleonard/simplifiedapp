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
			'args': {'default': (), 'docstring': {'description': 'Any other positional arguments'}, 'type': tuple},
			'kw1': {'docstring': {'description': 'First key word test parameter'}},
			'kw2': {'default': False, 'docstring': {'description': 'Second key word test parameter', 'is_optional': True, 'type_name': 'bool'}},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'type': dict},
			'mult1': {'default': 'mult1', 'docstring': {'description': 'First pos/kw test parameter'}},
			'mult2': {'default': 2, 'docstring': {'description': 'Second pos/kw test parameter with default'}},
			'pos1': {'docstring': {'description': 'First positional test parameter', 'is_optional': False, 'type_name': 'float'}},
			'pos2': {'annotation': bool, 'docstring': {'description': 'Second positional test parameter'}},
		}
		self.assertDictEqual(expected_result, parameters_from_callable(introspection_fixture.test_callable, object_metadata(introspection_fixture.test_callable)))

	def test_instance_method(self):
		'''
		Testing with a instance method
		'''
		
		expected_result={
			'args': {'default': (), 'docstring': {'description': 'Any other positional arguments'}, 'type': tuple},
			'kw1': {'docstring': {'description': 'First key word test parameter'}},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'type': dict},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}},
			'pos1': {'docstring': {'description': 'First positional test parameter'}},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}},
			'self': {},
		}
		test_object = introspection_fixture.TestClass().test_instance_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))
		
	def test_class_method(self):
		'''
		Testing with a class method
		'''
		
		expected_result={
			'args': {'default': (), 'docstring': {'description': 'Any other positional arguments'}, 'type': tuple},
			'cls': {},
			'kw1': {'docstring': {'description': 'First key word test parameter'}},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'type': dict},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}},
			'pos1': {'docstring': {'description': 'First positional test parameter'}},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}}
		}
		test_object = introspection_fixture.TestClass.test_class_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))
		
	def test_static_method(self):
		'''
		Testing with a static method
		'''
		
		expected_result={
			'args': {'default': (), 'docstring': {'description': 'Any other positional arguments'}, 'type': tuple},
			'kw1': {'docstring': {'description': 'First key word test parameter'}},
			'kw2': {'docstring': {'description': 'Second key word test parameter'}},
			'kwargs': {'default': {}, 'docstring': {'description': 'All other keyword arguments'}, 'type': dict},
			'mult1': {'docstring': {'description': 'First pos/kw test parameter'}},
			'mult2': {'docstring': {'description': 'Second pos/kw test parameter with default'}},
			'pos1': {'docstring': {'description': 'First positional test parameter'}},
			'pos2': {'docstring': {'description': 'Second positional test parameter'}},
		}
		test_object = introspection_fixture.TestClass.test_static_method
		self.assertDictEqual(expected_result, parameters_from_callable(test_object, object_metadata(test_object)))

