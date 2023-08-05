# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    _re_type.py
   Author :       Zhang Fan
   date：         2019/3/5
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import re

_re_type = type(re.compile(''))


def check_is_re_compile(obj):
    return isinstance(obj, _re_type)
