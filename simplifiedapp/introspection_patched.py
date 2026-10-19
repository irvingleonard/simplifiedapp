#! python
"""Extension to the introspection module
These are some patches and some other net new additions for the "introspection" module.
"""

from enum import Enum, auto as enum_auto
from importlib import import_module
from inspect import getattr_static, isclass, ismethod, ismodule, signature as inspect_signature
from logging import getLogger
from pathlib import Path
from types import BuiltinFunctionType, ClassMethodDescriptorType, FunctionType, MethodDescriptorType, MethodType, MethodWrapperType, WrapperDescriptorType
from warnings import warn

from introspection import Signature, get_attributes, static_mro, static_vars
from introspection import mark as introspection_mark
from introspection.errors import MethodNotFound
from introspection.mark import does_not_alter_signature
from introspection.parameter import Parameter, ParameterKind

try:
	from docstring_parser import parse as docstring_parse
except ImportError:
	docstring_parse = None

LOGGER = getLogger(__name__)


def object_metadata(obj, /, param_attributes=('default', 'description', 'is_optional', 'type_name'), return_attributes=('description', 'is_generator', 'return_name', 'type_name')):
	"""Gets metadata from an object
	It tries to get some meta information from the provided object by leveraging the object's details (name and version) and whatever can be learned from the docstring (using the optional "docstring_parser" module).

	:param obj: The object to build the metadata for
	:type obj: Any
	:param param_attributes: attributes to include from the parsing of the parameters
	:type param_attributes: iterable
	:param return_attributes: attributes to include from the parsing of the return
	:type return_attributes: iterable
	:returns dict: dictionary containing metadata details
	"""

	metadata = {'name': Path(obj.__file__).name if obj.__name__ == '__main__' and hasattr(obj, '__file__') else obj.__name__}

	if hasattr(obj, '__version__'):
		metadata['version'] = obj.__version__

	if (docstring_parse is not None) and hasattr(obj, '__doc__') and (obj.__doc__ is not None) and len(obj.__doc__):
		docstring = (docstring_parse(obj.__doc__))
		if docstring.short_description:
			metadata['description'] = docstring.short_description
		if docstring.long_description:
			metadata['long_description'] = docstring.long_description
		if len(docstring.params):
			docstring_params = {}
			for param in docstring.params:
				docstring_param = {}
				for param_attr in param_attributes:
					docstring_param_attr = getattr(param, param_attr)
					if docstring_param_attr is not None:
						docstring_param[param_attr] = docstring_param_attr
				docstring_params[param.arg_name] = docstring_param
			metadata['parameters'] = docstring_params
		if docstring.returns:
			docstring_return = {}
			for return_attr in return_attributes:
				docstring_return_attr = getattr(docstring.returns, return_attr)
				if docstring_return_attr is not None:
					docstring_return[return_attr] = docstring_return_attr
			metadata['returns'] = docstring_return

	return metadata


def _bind_class_member(member, instance, owner):
	"""Bind a member found in a class namespace
	Do what retrieving the member from the class (or from one of its instances) would do, but only for the descriptors known to be harmless (the ones implementing methods). Any other member is returned as is, so no user code (like a property) gets executed.

	:param member: The raw member, as found in the class namespace
	:param instance: The instance the member is retrieved from, or None if it's retrieved from the class itself
	:param type owner: The class the member is retrieved from (or the class of the instance)
	:returns Any: the bound member
	"""

	if isinstance(member, staticmethod):
		return member.__func__
	elif isinstance(member, classmethod):
		return MethodType(member.__func__, owner)
	elif isinstance(member, ClassMethodDescriptorType) and issubclass(owner, member.__objclass__):
		return member.__get__(instance, owner)
	elif instance is None:
		return member
	elif isinstance(member, FunctionType):
		return MethodType(member, instance)
	elif isinstance(member, (MethodDescriptorType, WrapperDescriptorType)) and isinstance(instance, member.__objclass__):
		return member.__get__(instance, owner)
	else:
		# Anything else (including C implemented methods of an unrelated class, which can't be bound) is returned as is
		return member


def enumerate_object_callables(obj, /):
	"""Enumerate the functions and classes of an object
	Find all the callable members of the provided object (a module, a class, an instance, etc.), including the special ("__dunder__") ones. The members are looked up statically, so no user code (like a property) gets executed in the process; methods are bound the same way that retrieving them from the object would.

	Modules usually import names from other modules, which aren't actual members: classes and functions are only included if they're listed in the "__all__" of the module (the explicit declaration of its public names, which covers C accelerator modules like "_heapq" for "heapq") or if they were defined in a module with the same root module (the first one in the dotted path), so packages re-exporting the content of their submodules, or submodules importing from their siblings, work as expected.

	:param obj: The object to find members of
	:returns tuple: the list of functions (any callable that isn't a class) and the list of classes, both sorted by member name
	"""

	if ismodule(obj):
		members = dict(static_vars(obj))
		module_root, public_names = obj.__name__.split('.')[0], set(members.get('__all__', ()))
	else:
		owner = obj if isclass(obj) else type(obj)
		instance = None if isclass(obj) else obj
		members = {}
		for mro_class in reversed(static_mro(owner)):
			members |= {name: _bind_class_member(member, instance, owner) for name, member in static_vars(mro_class).items()}
		if instance is not None:
			members |= get_attributes(instance)

	functions, classes = [], []
	for name, member in sorted(members.items()):
		if not callable(member):
			continue
		if ismodule(obj) and (name not in public_names) and (isclass(member) or isinstance(member, (FunctionType, BuiltinFunctionType))):
			member_module = getattr(member, '__module__', None)
			if isinstance(member_module, str) and (member_module.split('.')[0] != module_root):
				# Imported from an unrelated module
				continue
		if isclass(member):
			classes.append(member)
		else:
			functions.append(member)
	return functions, classes


def signature_variable_positional_parameter(self):
	"""Variable positional parameter
	Returns the variable positional parameter or None (read only property)

	:returns Parameter?: the VAR_POSITIONAL parameter, or None if there isn't one
	"""
	for parameter in self.parameter_list:
		if parameter.kind is ParameterKind.VAR_POSITIONAL:
			return parameter
	return None
Signature.variable_positional_parameter = property(signature_variable_positional_parameter)


def signature_variable_keyword_parameter(self):
	"""Variable keyword parameter
	Returns the variable keyword parameter or None (read only property)

	:returns Parameter?: the VAR_KEYWORD parameter, or None if there isn't one
	"""
	for parameter in self.parameter_list:
		if parameter.kind is ParameterKind.VAR_KEYWORD:
			return parameter
	return None
Signature.variable_keyword_parameter = property(signature_variable_keyword_parameter)


if not hasattr(Signature, '_from_callable_original'):
	# Keep the upstream implementation only once, in case the module gets executed again (a reload, for example); otherwise the patched version would end up calling itself
	Signature._from_callable_original = Signature.from_callable.__func__
@classmethod
def signature_from_callable(cls, callable_, /, *, follow_wrapped=True, use_signature_db=True):
	"""Enhance upstream from_callable
	The original "from_callable" method fails with an AttributeError for C implemented "__init__" methods (like "object.__init__" or "dict.__init__"), because it looks up their "__module__" attribute, which those don't have. The standard library's "inspect.signature" handles them fine.

	:param callable_: The callable to get the signature for
	:param bool? follow_wrapped: Whether to unwrap decorated callables (passed to upstream)
	:param bool? use_signature_db: Whether to look up the signature in upstream's database (passed to upstream)
	:returns Signature: the signature of the callable
	"""

	if isinstance(callable_, (MethodWrapperType, WrapperDescriptorType)) and (callable_.__name__ == '__init__'):
		return cls.from_signature(inspect_signature(callable_))
	return cls._from_callable_original(cls, callable_, follow_wrapped=follow_wrapped, use_signature_db=use_signature_db)
Signature.from_callable = signature_from_callable


def mark_has_mark(func, mark, /):
	"""Enhance upstream has_mark
	The original "has_mark" function fails with a TypeError for callables that don't support weak references (like C implemented methods: "object.__init__", "type.__call__", etc.) because the marks are stored in a "WeakKeyDictionary". Such callables can't be marked to begin with, so they don't have any mark.

	:param func: The callable to check for the mark
	:param mark: The mark to look for
	:returns bool: True if the callable, or any of the callables it wraps, has the mark
	"""

	for wrapped in introspection_mark.iter_wrapped(func):
		try:
			if mark in introspection_mark.MARKS.get(wrapped, ()):
				return True
		except TypeError:
			continue
	return False
introspection_mark.has_mark = mark_has_mark


@staticmethod
def signature_supplying_method(class_, method_name, /):
	"""Find the implementation of a method that supplies its signature
	Search the MRO of the class for the first implementation of the method that isn't marked with "introspection.mark.does_not_alter_signature" (meaning that it just forwards its arguments to the next implementation).

	:param type class_: The class to search the method in
	:param str method_name: The name of the method
	:returns Any: the implementation, as found in the namespace of the class that defines it (unbound, so it could be a staticmethod or a classmethod object)
	:raises MethodNotFound: if there's no unmarked implementation of the method in the MRO
	"""

	for mro_class in static_mro(class_):
		class_vars = static_vars(mro_class)
		if (method_name in class_vars) and not introspection_mark.has_mark(class_vars[method_name], does_not_alter_signature):
			return class_vars[method_name]
	raise MethodNotFound(method_name, class_)
Signature.supplying_method = signature_supplying_method


@classmethod
def signature_from_class_default(cls, class_, /):
	"""Get the signature for the provided class, as instantiated by "type.__call__"
	Instantiating a class requires the execution of two different methods with the very same arguments. The signature for such "call" would be the merger of the signature of both methods.

	Sadly, although the upstream Signature objects claim that they "support anything callable" they choke when getting the signature of a class that defines both methods (__new__ and __init__).

	:param class_: The class to get the signature for
	:returns Signature: the calculated signature for the class
	"""

	if not isclass(class_):
		raise ValueError(f'The argument provided "{class_}" is not a class')

	pos_params, kw_params = [], []
	model_varargs, model_varkw = Parameter('args', ParameterKind.VAR_POSITIONAL), Parameter('kwargs', ParameterKind.VAR_KEYWORD)
	new_method = cls.supplying_method(class_, '__new__')
	new_signature = Signature.from_callable(new_method)
	if (not new_signature.parameter_list) or (new_signature.parameter_list[0].kind in (ParameterKind.KEYWORD_ONLY, ParameterKind.VAR_KEYWORD)):
		raise ValueError(f'Incompatible {class_.__name__}.__new__: it has no positional parameter to receive the class')
	elif new_signature.parameter_list[0].kind is not ParameterKind.VAR_POSITIONAL:
		# The class is received by the first positional parameter, regardless of its name. A leading *args absorbs it instead, and remains available for the rest of the arguments.
		new_signature = new_signature.without_parameters(0)
	for parameter in new_signature.parameter_list:
		if parameter.kind in (ParameterKind.POSITIONAL_ONLY, ParameterKind.POSITIONAL_OR_KEYWORD):
			pos_params.append(parameter)
		elif parameter.kind is ParameterKind.KEYWORD_ONLY:
			kw_params.append(parameter)
	new_varargs, new_varkw = new_signature.variable_positional_parameter, new_signature.variable_keyword_parameter

	init_method = cls.supplying_method(class_, '__init__')
	init_signature = Signature.from_callable(init_method)
	if (not init_signature.parameter_list) or (init_signature.parameter_list[0].kind in (ParameterKind.KEYWORD_ONLY, ParameterKind.VAR_KEYWORD)):
		raise ValueError(f'Incompatible {class_.__name__}.__init__: it has no positional parameter to receive the instance')
	elif init_signature.parameter_list[0].kind is not ParameterKind.VAR_POSITIONAL:
		# The instance is received by the first positional parameter, regardless of its name. A leading *args absorbs it instead, and remains available for the rest of the arguments.
		init_signature = init_signature.without_parameters(0)

	new_pos_count, new_kw_names = len(pos_params), {parameter.name for parameter in kw_params}
	for i, parameter in enumerate(init_signature.parameter_list):
		if parameter.kind in (ParameterKind.POSITIONAL_ONLY, ParameterKind.POSITIONAL_OR_KEYWORD):
			if i < new_pos_count:
				# Both methods receive the same positional arguments, the matching parameter from __new__ already covers this one
				if parameter.name != pos_params[i].name:
					warn(f'Mismatching {class_.__name__}.__new__ and {class_.__name__}.__init__ positional parameters: {pos_params[i].name} & {parameter.name}', category=SyntaxWarning)
			elif new_varargs is not None:
				pos_params.append(parameter)
			elif (parameter.kind is ParameterKind.POSITIONAL_OR_KEYWORD) and (new_varkw is not None):
				# __new__ can't take it positionally, so it can only be passed as a keyword
				kw_params.append(parameter.replace(kind=ParameterKind.KEYWORD_ONLY))
			else:
				raise ValueError(f'Incompatible positional parameter found in {class_.__name__}.__init__: {parameter.name}')
		elif parameter.kind is ParameterKind.KEYWORD_ONLY:
			if parameter.name in new_kw_names:
				continue
			elif new_varkw is not None:
				kw_params.append(parameter)
			else:
				raise ValueError(f'Incompatible keyword parameter found in {class_.__name__}.__init__: {parameter.name}')
	init_varargs, init_varkw = init_signature.variable_positional_parameter, init_signature.variable_keyword_parameter

	if (new_method is object.__new__) and (init_method is object.__init__):
		pass
	elif init_method is object.__init__:
		if new_varargs is not None:
			pos_params.append(new_varargs)
		if new_varkw is not None:
			kw_params.append(new_varkw)
	elif new_method is object.__new__:
		if init_varargs is not None:
			pos_params.append(init_varargs)
		if init_varkw is not None:
			kw_params.append(init_varkw)
	else:
		if (new_varargs is not None) and (init_varargs is not None):
			pos_params.append(model_varargs)
		if (new_varkw is not None) and (init_varkw is not None):
			kw_params.append(model_varkw)

	return Signature(parameters=pos_params + kw_params, forward_ref_context=class_.__module__)
Signature._from_class_default = signature_from_class_default


@classmethod
def signature_from_class(cls, class_, /):
	"""Get the signature for the provided class
	Calling a class actually calls the "__call__" method of its metaclass, which receives the class as its first argument. The default one, "type.__call__", triggers the class' "__new__" and "__init__" methods; that case is handled by "Signature._from_class_default". A metaclass can override "__call__" to do something else entirely, in which case the signature of such method (without the parameter receiving the class) is the signature of the class.

	:param class_: The class to get the signature for
	:returns Signature: the calculated signature for the class
	"""

	if not isclass(class_):
		raise ValueError(f'The argument provided "{class_}" is not a class')

	metaclass = type(class_)
	call_method = cls.supplying_method(metaclass, '__call__')
	if call_method is type.__dict__['__call__']:
		return cls._from_class_default(class_)

	call_signature = Signature.from_callable(call_method)
	if (not call_signature.parameter_list) or (call_signature.parameter_list[0].kind in (ParameterKind.KEYWORD_ONLY, ParameterKind.VAR_KEYWORD)):
		raise ValueError(f'Incompatible {metaclass.__name__}.__call__: it has no positional parameter to receive the class')
	elif call_signature.parameter_list[0].kind is not ParameterKind.VAR_POSITIONAL:
		# The class is received by the first positional parameter, regardless of its name. A leading *args absorbs it instead, and remains available for the rest of the arguments.
		call_signature = call_signature.without_parameters(0)
	return call_signature
Signature.from_class = signature_from_class


class CallableType(Enum):
	"""Callable types
	List of callable types identified by the module so far:
	- CLASS: a class
	- INSTANCE: a class instance supporting the "__call__" protocol
	- FUNCTION: a run of the mill function (a plain 'ol regular function)
	- BOUND_METHOD: an instance method from a live instance
	- CLASS_METHOD: a class method, where the first parameter is a "type" (called "cls" by regular convention)
	- INSTANCE_METHOD: an instance method from the original class. Although it's still a callable, it can't be executed without creating an instance of the class first
	- STATIC_METHOD: a static method, which is very similar to the regular function, only that it's a member of the class
	"""

	CLASS = enum_auto()
	INSTANCE = enum_auto()
	FUNCTION = enum_auto()
	BOUND_METHOD = enum_auto()
	CLASS_METHOD = enum_auto()
	INSTANCE_METHOD = enum_auto()
	STATIC_METHOD = enum_auto()


class Callable:
	"""Describes a callable
	This is mostly about "executing"/"running" the callable. It requires a lot of processing based on all the possible "things" that are callables.
	"""

	FORWARD_METADATA = ('name', 'version', 'description', 'long_description')

	def __init__(self, callable_, parent=None):
		"""Magic initialization
		Check that the provided "callable_" is actually callable and store it.

		:param callable_: The callable that will be handled by the class
		:param type? parent: The class the callable was retrieved from, if any. A function retrieved from a class only knows the class that defines it (which might be a parent of the former) and, if that class was defined inside a function, not even that. If not provided, it will be inferred from the callable itself on a best effort basis.
		:returns None: init shouldn't return anything
		"""

		if not callable(callable_):
			raise ValueError('The argument provided "{}" is not a callable'.format(callable_))

		self._callable_, self._parent_ = callable_, parent
		if parent is not None:
			# Bound callables already carry what they're bound to (more specific than any class), so the provided parent is only validated
			if self._check_parent(parent):
				self.parent = parent

	def __reduce__(self):
		"""Support for copy and pickle
		The lazily resolved attributes (like the module) might not be copyable nor picklable, and they can be resolved again anyway, so only the initialization arguments are kept.

		:returns tuple: the class and the arguments to initialize a new instance
		"""

		return type(self), (self._callable_, self._parent_)

	def _check_parent(self, parent):
		"""Validate an explicitly provided parent
		The parent should be a class where the callable can actually be found: the class of the instance (or the class itself) that a method is bound to (or one of its parents), the class (or a subclass of the class) that a method descriptor belongs to, or a class having the function as one of its attributes (as resolved through its MRO, under any name).

		:param type parent: The class to validate
		:returns bool: True if the parent should be used, False if the callable is already bound to something (which is more specific). It raises an exception if the parent is invalid
		"""

		if not isclass(parent):
			raise TypeError(f'The parent provided "{parent}" is not a class')

		bound_to = getattr(self._callable_, '__self__', None)
		if (bound_to is not None) and not ismodule(bound_to):
			if not (isinstance(bound_to, parent) or (isclass(bound_to) and issubclass(bound_to, parent))):
				raise ValueError(f'The callable "{self._callable_}" is bound to "{bound_to}", which is neither an instance nor a subclass of the parent provided "{parent}"')
			return False
		elif hasattr(self._callable_, '__objclass__'):
			is_member = issubclass(parent, self._callable_.__objclass__)
		elif isinstance(self._callable_, FunctionType):
			# The function is looked up by identity, not by its name: the name it was defined with could be different from the attribute holding it (an alias, a function attached to the class later, etc.). Only the attributes resolved through the MRO count, so a function overridden in the parent isn't a member of it.
			resolved_attributes = {}
			for mro_class in static_mro(parent):
				for attribute_name, class_attribute in static_vars(mro_class).items():
					resolved_attributes.setdefault(attribute_name, class_attribute)
			is_member = any(getattr(class_attribute, '__func__', class_attribute) is self._callable_ for class_attribute in resolved_attributes.values())
		else:
			is_member = False
		if not is_member:
			raise ValueError(f'The callable "{self._callable_}" is not a member of the parent provided "{parent}"')
		return True

	def __call__(self, /, *args, **kwargs):
		"""Execute the callable
		Call the callable with the provided arguments, as is (like a regular Python call).

		An "INSTANCE_METHOD" requires an instance of its parent class before it can be executed, so it expects exactly 4 positional arguments instead (and no keyword arguments): the positional and keyword arguments to instantiate the parent class, followed by the positional and keyword arguments for the method.

		:param args: The positional arguments to execute the callable with (or the 4 items described above for instance methods)
		:param kwargs: The keyword arguments to execute the callable with
		:returns Any: the result of "running" this callable with the provided arguments
		"""

		if self.type is CallableType['INSTANCE_METHOD']:
			if kwargs or (len(args) != 4):
				raise TypeError('An instance method requires exactly 4 positional arguments (parent_args, parent_kwargs, method_args, method_kwargs) and no keyword arguments')
			parent_args, parent_kwargs, method_args, method_kwargs = args
			parent_instance = self.parent(*parent_args, **parent_kwargs)
			return self._callable_(parent_instance, *method_args, **method_kwargs)

		return self._callable_(*args, **kwargs)

	def __getattr__(self, item):
		"""Lazy instantiation
		Wait until they're needed before resolving potentially costly attributes. It will set the attribute to the object so this will only be run at most once for each missing attribute.

		Some attributes are forwarded to the metadata dict, which are controlled by "self.FORWARD_METADATA". If the attribute request is not found here or forwarded to the metadata, then it's forwarded to the stored "callable", except for special ("__dunder__") names, which belong to this object and its protocols (copy, pickle, etc.)

		:param str item: The name of the attribute that is missing
		:returns Any: the value of such attribute
		"""

		if (item == '_callable_') or ((item[:2] == '__') and (item[-2:] == '__')):
			# Not set yet (an instance created without "__init__", like copy and pickle do) or a special name: forwarding those to the callable is wrong
			raise AttributeError(f'"{type(self).__name__}" object has no attribute "{item}"')
		elif item == 'is_method':
			value = ismethod(self._callable_)
		elif item == 'metadata':
			value = object_metadata(self._callable_)
		elif item == 'module':
			value = import_module(self._callable_.__module__)
		elif item == 'parents':
			genealogy = getattr(self._callable_, '__qualname__', '').split('.')
			if '<locals>' in genealogy:
				if genealogy[-2] == '<locals>':
					# Defined directly in a function (a nested function), not in a class
					value = []
				else:
					# Classes defined inside a function can't be reached from the module. The only reference to the defining class is the "__class__" closure cell, which the compiler creates for methods using "super()" or "__class__".
					code = getattr(self._callable_, '__code__', None)
					if (code is None) or ('__class__' not in code.co_freevars):
						raise ValueError(f'Unable to find the class that defines "{self._callable_.__qualname__}" (it was defined inside a function); provide it with the "parent" parameter')
					value = [self._callable_.__closure__[code.co_freevars.index('__class__')].cell_contents]
			elif len(genealogy) > 1:
				value = [getattr(self.module, genealogy[0])]
				for parent in genealogy[1:-1]:
					value.append(getattr(value[-1], parent))
				value.reverse()
			else:
				value = []
		elif item == 'parent':
			bound_to = getattr(self._callable_, '__self__', None)
			if (bound_to is not None) and not ismodule(bound_to):
				value = bound_to
			elif hasattr(self._callable_, '__objclass__'):
				value = self._callable_.__objclass__
			elif self.parents:
				value = self.parents[0]
			else:
				value = None
		elif item == 'parent_metadata':
			if self.parent is None:
				raise AttributeError(f'The callable "{self._callable_}" has no parent')
			value = object_metadata(self.parent)
		elif item[:7] == 'parent_':
			parent_metadata = self.parent_metadata
			if item[7:] not in parent_metadata:
				raise AttributeError(f'The parent of "{self._callable_}" has no "{item[7:]}" metadata')
			return parent_metadata[item[7:]]
		elif item in ('signature', 'type'):
			signature, type_ = self._get_signature_detect_type()
			if item == 'signature':
				value = signature
				setattr(self, 'type', type_)
			else:
				value = type_
				setattr(self, 'signature', signature)
		elif item in self.FORWARD_METADATA:
			if item not in self.metadata:
				raise AttributeError(f'The callable "{self._callable_}" has no "{item}" metadata')
			return self.metadata[item]
		else:
			return getattr(self._callable_, item)

		setattr(self, item, value)
		return value

	def _get_signature_detect_type(self):
		"""Detect the type of callable, produce a signature, and signal the type
		The possible types are described in "CallableType". The signature yielded for each one of them:
		- CLASS: the one from "Signature.from_class" (the merger of its "__new__" and "__init__" methods, or its metaclass' "__call__" method if overridden)
		- BOUND_METHOD and CLASS_METHOD: the one of the bound method, which doesn't include the already bound instance or class
		- STATIC_METHOD: the regular method signature
		- INSTANCE_METHOD: the method signature without the parameter receiving the instance ("self", by convention). If the method is marked with "introspection.mark.does_not_alter_signature", the signature comes from the implementation that supplies it instead (as found by "Signature.supplying_method")
		- FUNCTION: the regular signature
		- INSTANCE: the one of its "__call__" method without the first parameter ("self", by convention)

		Static methods and instance methods look the same when retrieved from a class (plain functions); they're told apart by looking at the raw attribute in the class (with "inspect.getattr_static"), which is a "staticmethod" object for the former.

		:returns tuple: two items tuple, with the signature in the first position and the type on the second
		"""

		bound_to = getattr(self._callable_, '__self__', None)
		if isclass(self._callable_):
			signature = Signature.from_class(self._callable_)
			type_ = CallableType['CLASS']
		elif (bound_to is not None) and not ismodule(bound_to):
			# Bound methods, either Python ones or builtin ones (like "[].append"). Builtin functions are "bound" to their module, so those are excluded.
			signature = Signature.from_callable(self._callable_)
			type_ = CallableType['CLASS_METHOD'] if isclass(bound_to) else CallableType['BOUND_METHOD']
		elif isinstance(self._callable_, (FunctionType, MethodDescriptorType, WrapperDescriptorType)) and isclass(self.parent):
			if isinstance(getattr_static(self.parent, self.name, None), staticmethod):
				signature = Signature.from_callable(self._callable_)
				type_ = CallableType['STATIC_METHOD']
			else:
				method = Signature.supplying_method(self.parent, self.name) if introspection_mark.has_mark(self._callable_, does_not_alter_signature) else self._callable_
				signature = Signature.from_callable(method)
				if (not signature.parameter_list) or (signature.parameter_list[0].kind in (ParameterKind.KEYWORD_ONLY, ParameterKind.VAR_KEYWORD)):
					raise ValueError(f'Incompatible {self.parent.__name__}.{self.name}: it has no positional parameter to receive the instance')
				elif signature.parameter_list[0].kind is not ParameterKind.VAR_POSITIONAL:
					# The instance is received by the first positional parameter, regardless of its name. A leading *args absorbs it instead, and remains available for the rest of the arguments.
					signature = signature.without_parameters(0)
				type_ = CallableType['INSTANCE_METHOD']
		elif isinstance(self._callable_, (FunctionType, BuiltinFunctionType)):
			signature = Signature.from_callable(self._callable_)
			type_ = CallableType['FUNCTION']
		else:
			signature = Signature.from_callable(self._callable_)
			type_ = CallableType['INSTANCE']

		return signature, type_
