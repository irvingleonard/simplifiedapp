FIXTURE_EMPTY_PARAMETERS = {}

FIXTURE_POSITIONAL_ARGS = {
	'a': {'positional': True},
	'b': {'positional': True},
}

FIXTURE_VARARGS = {'args': {'default': [], 'positional': True, 'special': 'varargs'}}

FIXTURE_KEYWORD_ARGS = {
	'c': {'positional': False},
	'd': {'positional': False},
}

FIXTURE_VARKW = {'kwargs': {'default': {}, 'positional': False, 'special': 'varkw'}}

FIXTURE_DEFAULT_POSITIONAL_ARGS = {
	'a': {'positional': True},
	'b': {'default': 2, 'positional': True},
}

FIXTURE_DEFAULT_KEYWORD_ARGS = {
	'c': {'positional': False},
	'd': {'default': True, 'positional': False},
}

FIXTURE_VERSION = {'version' : {'version': '0.1', 'positional': False}}

FIXTURE_ALL_PARAMETER_COMBINATIONS = {
	'pos_req': {'positional': True},
	'pos_def_none': {'default': None, 'positional': True},
	'pos_def_bool': {'default': False, 'positional': True},
	'pos_def_str': {'default': 'a_str', 'positional': True},
	'pos_def_list': {'default': ['as', 1, True], 'positional': True},
	'pos_def_dict': {'default': {1: 'one', 'dct': 6, 'fer': False}, 'positional': True},
	'pos_def_num': {'default': 2.3, 'positional': True},
	'more_pos': {'default': [], 'positional': True, 'special': 'varargs'},
	'kw_req': {'positional': False},
	'kw_def_none': {'default': None, 'positional': False},
	'kw_def_bool': {'default': True, 'positional': False},
	'kw_def_str': {'default': 'another_str', 'positional': False},
	'kw_def_list': {'default': [1, 'tre', 6.7], 'positional': False},
	'kw_def_dict': {'default': {1: 'dfe', 'yufgb': 'sdqwda'}, 'positional': False},
	'kw_def_num': {'default': (8+98j), 'positional': False},
	'more_kw': {'default': {}, 'positional': False, 'special': 'varkw'},
}