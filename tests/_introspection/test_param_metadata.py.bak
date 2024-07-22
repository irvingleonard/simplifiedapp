#python
'''
Testing the introspection.param_metadata function
'''

from unittest import TestCase

from inspect import getfullargspec

from simplifiedapp.introspection import object_metadata, param_metadata

from fixtures import introspection as introspection_fixture

class TestParamMetadataCallable(TestCase):
	'''
	Tests for the param_metadata function
	'''
	
	def setUp(self):
		metadata = object_metadata(introspection_fixture.test_callable)
		args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations = getfullargspec(introspection_fixture.test_callable)
		self.params = [(arg, None, annotations.get(arg, None), metadata.get('parameters', {}).get(arg, {})) for arg in args[:-len(defaults)]]
		for i in range(len(defaults)):
			arg = args[-len(defaults)+i]
			self.params.append([(arg, defaults[i], annotations.get(arg, None), metadata.get('parameters', {}).get(arg, {}))])
		self.params.append([(kwarg, None, annotations.get(kwarg, None), metadata.get('parameters', {}).get(kwarg, {})) for kwarg in kwonlyargs[:-len(kwonlydefaults)]])
		self.params.append([(kwarg, value, annotations.get(kwarg, None), metadata.get('parameters', {}).get(kwarg, {})) for kwarg, value in kwonlydefaults.items()])
		print(self.params)
		self.test_object = param_metadata(introspection_fixture.test_callable)
		self.maxDiff = None
	
	def test_annotations_class_str(self):
		'''
		Testing annotation for type str
		'''
		
		expected_result = {'type' : str}
		self.assertDictEqual(expected_result, self.test_object('a', {}, {'a' : str}, ''))

	def test_annotations_choices(self):
		'''
		Testing annotation for choices
		'''
		
		expected_result = {'choices' : ('b', 3, False)}
		self.assertDictEqual(expected_result, self.test_object('a', {}, {'a' : ('b', 3, False)}, ''))

	def test_default_none(self):
		'''
		Testing defaults: None
		'''
		
		expected_result = {'default' : argparse.SUPPRESS}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : None}, {}, ''))

	def test_default_str(self):
		'''
		Testing defaults: str
		'''
		
		expected_result = {'default' : 'v'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 'v'}, {}, ''))
	
	def test_default_false(self):
		'''
		Testing defaults: False
		'''
		
		expected_result = {'default' : False, 'action' : 'store_true'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : False}, {}, ''))
	
	def test_default_true(self):
		'''
		Testing defaults: True
		'''
		
		expected_result = {'default' : True, 'action' : 'store_false'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : True}, {}, ''))

	def test_default_tuple(self):
		'''
		Testing defaults: tuple
		'''
		
		expected_result = {'default' : [], 'action' : 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'nargs' : '+'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : ('v1', 2)}, {}, ''))

	def test_default_tuple_w_nargs(self):
		'''
		Testing defaults: tuple with nargs
		'''
		
		expected_result = {'default' : [], 'action' : 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'nargs' : '*'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : ('v1', 2), 'nargs' : '*'}, {}, ''))

	def test_default_dict(self):
		'''
		Testing defaults: dict
		'''
		
		expected_result = {'default' : [], 'action' : 'extend' if simplifiedapp.ADD_ARGUMENT_ACTION_EXTEND else 'append', 'nargs' : '+', 'help': '(Use the key=value format for each entry)'}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : {'v1' : 1, 2 : 'V2'}}, {}, ''))

	def test_default_int(self):
		'''
		Testing defaults: int
		'''
		
		expected_result = {'default' : 3, 'type' : int}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 3}, {}, ''))

	def test_default_float(self):
		'''
		Testing defaults: float
		'''
		
		expected_result = {'default' : 2.5, 'type' : float}
		self.assertDictEqual(expected_result, self.test_object('a', {'default' : 2.5}, {}, ''))