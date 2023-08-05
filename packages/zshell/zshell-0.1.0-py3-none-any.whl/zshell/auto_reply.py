# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    auto_reply.py
   Author :       Zhang Fan
   date：         2019/3/5
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

from zshell._re_type import _re_type


class auto_reply:
    def __init__(self, search, reply_command, wait_flag=True, auto_line_break=True):
        '''
        自动回复的描述
        :param search: 搜索服务器消息, 它可以是一个字符串, 正则表达式, 如果是True表示任何消息
        :param reply_command: 匹配成功后自动回复命令
        :param wait_flag: 自动回复后的等待标记, 它可以是一个字符串, 正则表达式, 自动回复对象, 或者是包含他们的一个可迭代对象, 如果是True表示任何消息
        :param auto_line_break: 命令结尾是否自动添加换行符
        '''
        assert search is True or isinstance(search, (str, _re_type))
        self.search = search
        self.reply_command = reply_command
        self.wait_flag = wait_flag
        self.auto_line_break = auto_line_break
