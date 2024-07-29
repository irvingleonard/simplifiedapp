#!python

def test_callable_all_parameter_combinations(
    pos_req,
    pos_def_none=None,
    pos_def_str='a_str',
    pos_def_bool=False,
    pos_def_list=['as', 1, True],
    pos_def_dict={'dct' : 6, 'fer' : False, 1 : 'one'},
    pos_def_num=2.3,
    *more_pos,
    kw_req,
    kw_def_none=None,
    kw_def_str='another_str',
    kw_def_bool=True,
    kw_def_list=[1, 'tre', 6.7],
    kw_def_dict={1 : 'dfe', 'yufgb': 'sdqwda'},
    kw_def_num=(8+98j),
    **more_kw
):

    pass