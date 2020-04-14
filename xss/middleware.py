# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import bleach
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from xss.settings import sec_settings


logger = logging.getLogger(__name__)


class XssViewMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(XssViewMiddleware, self).__init__(get_response)

    def process_view(self, request, view, args, kwargs):
        print('process view')
        # if getattr(view, 'escape_xss_check', False):
        #     print('escape check')
        #     return None
        # else:
        #     print('continue checking')

        self.__escape_param_list = getattr(
            view, 'escape_clean_param') if hasattr(view,
                                                   'escape_clean_param') else []
        for method in ['GET', 'POST']:
            if hasattr(request, method):
                setattr(request,
                        method,
                        self.__escape_data(getattr(request, method)))
        return None

    def __escape_data(self, query_dict):
        '''
        参数转义
        '''
        print(query_dict)
        data_copy = query_dict.copy()
        for _get_key, _get_value_list in data_copy.lists():
            new_value_list = []
            for _get_value in _get_value_list:
                if _get_key in self.__escape_param_list:
                    new_value = _get_value
                else:
                    new_value = self.clean_xss(text_string=_get_value,
                                          extend=sec_settings.BLEACH_WHITE_LIST)

                if sec_settings.BLEACH_SHOW and new_value != _get_value:
                    if settings.DEBUG:
                        print('XSS : Transfer  %s  To  %s' % (
                            _get_value, new_value))
                    else:
                        logger.warning('XSS : Transfer  %s  To  %s' % (
                            _get_value, new_value))
                new_value_list.append(new_value)
            data_copy.setlist(_get_key, new_value_list)
        return data_copy

    def clean_xss(self, text_string, level='high', extend={}):
        '''
        使用 Bleach 消毒字符串，kwargs 中如果没有配置参数，则去 level 套餐中取。
        kwargs 的格式可以参考 settings 中 BLEACH_HIGH。
        '''
        bleach_allow = getattr(sec_settings, '_'.join(['BLEACH', level.upper()]))
        print(bleach_allow)

        attributes = {}
        for k in set(
            bleach_allow['attributes'].keys()
        ).union(set(extend.get('attributes', {}).keys())):
            attributes[k] = list(set(
                bleach_allow['attributes'].get(k, [])
            ).union(set(extend.get('attributes', {}).get(k, []))))

        print('attributes=%s' % attributes)
        print('tags=%s' % list(set(bleach_allow['tags']).union(set(extend.get('tags', [])))))

        return bleach.clean(text=text_string,
                            tags=list(set(bleach_allow['tags']).union(
                                set(extend.get('tags', [])))),
                            attributes=attributes,
                            )
