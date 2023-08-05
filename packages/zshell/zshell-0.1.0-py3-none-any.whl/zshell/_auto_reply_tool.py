# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    _auto_reply_tool.py
   Author :       Zhang Fan
   date：         2019/3/5
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import copy
from collections import Iterable

from zshell.auto_reply import auto_reply
from zshell._re_type import check_is_re_compile
from zshell._re_type import _re_type


class _auto_reply_tool:
    def __init__(self):
        self.auto_reply_saver = None

    def check_auto_reply(self, server_msg):
        '''检查自动回复'''
        if not server_msg:
            return

        for item in self.auto_reply_saver:  # type:auto_reply
            result = self._check(server_msg, item)
            if result:
                return result

    def _check(self, server_msg, search):
        if search is True:
            return True

        if isinstance(search, str):
            if search in server_msg:
                return search

        elif check_is_re_compile(search):
            if search.search(server_msg):
                return search

        elif isinstance(search, auto_reply):
            if self._check(server_msg, search.search):
                return search

    def _parser_auto_replys(self, wait_flag):
        if wait_flag is True:
            return [True]

        if isinstance(wait_flag, (str, _re_type, auto_reply)):
            wait_flag = [wait_flag]
        else:
            assert isinstance(wait_flag, Iterable)
        return copy.deepcopy(wait_flag)

    def set_wait_flag(self, wait_flag):
        self.auto_reply_saver = self._parser_auto_replys(wait_flag)
