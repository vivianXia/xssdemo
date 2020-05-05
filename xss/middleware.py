# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from xss.settings import WHITELIST_TAGS


class XssViewMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(XssViewMiddleware, self).__init__(get_response)
        self.skip_xss_check = False

    def process_view(self, request, view, args, kwargs):
        if getattr(view, 'skip_xss_check', False):
            self.skip_xss_check = True
        return

    def process_response(self, request, response):
        if self.skip_xss_check:
            return response
        response = HttpResponse(self._clean_data(response.content))
        return response

    @classmethod
    def _clean_data(cls, data):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data)
        for tag in soup.findAll(True):
            if tag.name not in WHITELIST_TAGS:
                tag.extract()
        new = soup.renderContents()
        print(new)
        return new
