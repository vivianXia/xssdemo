# -*- coding: utf-8 -*-
from functools import wraps


def skip_xss_check(func):
    @wraps(func)
    def _func(*args, **kwargs):
        return func(*args, **kwargs)

    _func.skip_xss_check = True
    return _func
