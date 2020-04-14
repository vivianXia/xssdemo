# -*- coding: utf-8 -*-

from django.utils.decorators import available_attrs
from django.utils.functional import wraps


def xss_attributes_safe(*attributes, **param_list_dict):
    def _wrapped_func(view_func):
        def wrapped_view(*args, **kwargs):
            return view_func(*args, **kwargs)
        if param_list_dict.get('param_list'):
            wrapped_view.escape_clean_param = param_list_dict['param_list']
        else:
            wrapped_view.escape_clean_param = list(attributes)
        return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
    return _wrapped_func
