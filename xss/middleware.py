# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import bleach
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class XssViewMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super(XssViewMiddleware, self).__init__(get_response)

    def process_response(self, request, response):
        # if getattr(view, 'skip_xss_check', False):
        #     return
        #
        # for method in ['GET', 'POST']:
        #     if hasattr(request, method):
        #         setattr(request, method, self._clean_data(getattr(request, method)))
        # return
        print('before')
        print(response.content)

        # result.content = result.content
        # try:
        #     jsondata = json.loads(result.content)
        #     result.content = json.dumps(self.jsonXssFilter(jsondata))
        # except:
        #     print('exception')
        #     result.content = self.jsonXssFilter(result.content)

        response = HttpResponse(self.jsonXssFilter(response.content))

        # response.content(self.jsonXssFilter(response.content))
        print('after')
        print(response.content)
        return response

    def jsonXssFilter(self, data):
        tags = ['a', 'img', 'br', 'strong', 'b', 'code', 'pre', 'p', 'div', 'em', 'span', 'h1', 'h2', 'h3', 'h4', 'h5',
                'h6', 'table', 'ul', 'ol', 'tr', 'th', 'td', 'hr', 'li', 'u', 'html', 'head', 'body',
                'meta', 'form', 'title', 'input']
        attributes = {'a': ['href', 'title', 'target'],
                      'img': ['width', 'height', 'src', 'alt'],
                      '*': ['class', 'style', 'type', 'method', 'action', 'charset', 'lang', 'name'],
                      }
        payloads = {
            '\'': '&apos;',
            '"': '&quot;',
            '<': '&lt;',
            '>': '&gt;'
        }
        payloads_bytes = {
            b'\'': b'&apos;',
            b'"': b'&quot;',
            b'<': b'&lt;',
            b'>': b'&gt;'
        }
        if type(data) == dict:
            new = {}
            for key, values in data.items():
                new[key] = self.jsonXssFilter(values)
        elif type(data) == list:
            new = []
            for i in data:
                new.append(self.jsonXssFilter(i))
        elif type(data) == int or type(data) == float:
            new = data
        elif type(data) == str:
            print('str')
            new = data
            # new = bleach.clean(text=data)
            for key, value in payloads_bytes.items():
                new = new.replace(key, value)
        elif type(data) == bytes:
            print('bytes')
            #new = bleach.clean(text=data.decode('utf-8'), tags=tags, attributes=attributes).encode('utf-8')

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(data)

            for tag in soup.findAll(True):
                if tag.name not in tags:
                    tag.extract()
            new = soup.renderContents()
            print(new)
            return new
            # new = data.replace(b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n', b'')
            # new = new.replace(b'</html>\n', b'')
            # for key, value in payloads_bytes.items():
            #     new = new.replace(key, value)
            # return b'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n' + new + b'</html>\n'
        else:
            print('>>> unknown type:')
            print(type(data))
            new = data
        return new

    @classmethod
    def _clean_data(cls, query_dict):
        data_copy = query_dict.copy()
        for key, values in data_copy.lists():
            clean_value_list = []
            for value in values:
                clean_value_list.append(bleach.clean(text=value))
            data_copy.setlist(key, clean_value_list)
        return data_copy
