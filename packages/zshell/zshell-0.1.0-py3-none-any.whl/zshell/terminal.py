# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    terminal.py
   Author :       Zhang Fan
   date：         2019/3/5
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import sys
import time
import threading

import paramiko

from zshell.auto_reply import auto_reply
from zshell._auto_reply_tool import _auto_reply_tool


class terminal:
    show_server_msg = True
    encoding = 'utf-8'
    send_command_wait = 0.3
    auto_reply_check_time = 0.1

    def __init__(self, host: str, port: int, user: str, password: str):
        self._connected = False
        self._server_msg_saver = []
        self._server_msg_locker = threading.Lock()
        self._now_command = None

        self._auto_reply_tool = _auto_reply_tool()

        self._receive_thread = threading.Thread(target=self._receive_msg)
        self._receive_thread.setDaemon(True)

        self._connect(host, port, user, password)

    def _connect(self, host: str, port: int, user: str, password: str):
        '''连接到服务器'''
        self._transport = paramiko.Transport((host, port))
        self._transport.start_client()
        self._transport.auth_password(user, password)

        self._channel = self._transport.open_session()
        self._channel.get_pty()
        self._channel.invoke_shell()
        self._connected = True

        self._sftp = None

        self._receive_thread.start()

    def __del__(self):
        self.close()

    def close(self):
        '''关闭连接'''
        if self._connected:
            self._connected = False
            if self._sftp:
                self._sftp.close()
                self._sftp = None
            self._channel.close()
            self._transport.close()

    def _write_stream(self, text):
        '''输出数据到流'''
        if self.show_server_msg:
            sys.stdout.write(text)
            sys.stdout.flush()

    def _receive_msg(self):
        '''接收'''
        while True:
            outmsg = self._channel.recv(4096)
            if len(outmsg) == 0:
                self._write_stream('\n\n*** the server is disconnected ***')
                self.close()
                break

            msg = outmsg.decode(self.encoding)
            self._write_stream(msg)

            if self._now_command and msg.replace('\r\n', '\n') == self._now_command:
                continue

            with self._server_msg_locker:
                self._server_msg_saver.append(msg)

    def _send_command(self, command, auto_line_break=True):
        with self._server_msg_locker:
            self._server_msg_saver.clear()

        if auto_line_break:
            command += '\n'

        if self._connected:
            self._now_command = command
            self._channel.sendall(command)
            if self.send_command_wait:
                time.sleep(self.send_command_wait)

    def run(self, command, wait_flag=None, auto_line_break=True):
        '''
        远程执行命令
        :param command: 命令
        :param wait_flag: 等待标记, 它可以是一个字符串, 正则表达式, 自动回复对象, 或者是包含他们的一个可迭代对象
        :param auto_line_break: 命令结尾是否自动添加换行符
        :return: 如果等待则返回是哪个数据匹配的服务器消息
        '''
        self._send_command(command, auto_line_break=auto_line_break)
        return self.wait(wait_flag)

    def wait(self, wait_flag):
        '''等待消息'''
        self._auto_reply_tool.set_wait_flag(wait_flag or True)

        while self._connected:
            with self._server_msg_locker:
                server_msg = ''.join(self._server_msg_saver)
                self._server_msg_saver.clear()

            if server_msg:
                result = self._auto_reply_tool.check_auto_reply(server_msg)
                if result:
                    if isinstance(result, auto_reply) and result.reply_command:
                        return self.run(result.reply_command, wait_flag=result.wait_flag,
                                        auto_line_break=result.auto_line_break)
                    return result
            time.sleep(self.auto_reply_check_time)

    def put(self, localpath, remotepath):
        '''上传本地文件到服务器'''
        if not self._sftp:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)

    def get(self, remotepath, localpath):
        '''从服务器下载文件到本地'''
        if not self._sftp:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)
