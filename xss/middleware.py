# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bleach
from django.utils.deprecation import MiddlewareMixin


class XssViewMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(XssViewMiddleware, self).__init__(get_response)

    def process_view(self, request, view, args, kwargs):
        if getattr(view, 'skip_xss_check', False):
            return

        for method in ['GET', 'POST']:
            if hasattr(request, method):
                setattr(request, method, self._clean_data(getattr(request, method)))
        return

    @classmethod
    def _clean_data(cls, query_dict):
        data_copy = query_dict.copy()
        for key, values in data_copy.lists():
            clean_value_list = []
            for value in values:
                clean_value_list.append(bleach.clean(text=value))
            data_copy.setlist(key, clean_value_list)
        return data_copy
