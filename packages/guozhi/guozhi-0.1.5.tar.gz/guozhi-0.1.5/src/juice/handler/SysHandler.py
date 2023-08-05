#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time   : 2019/3/1 16:46
# @Author : yebing
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : guozhi
# @FileName: SysHandler.py


class SysHandler(object):
    """
      系统方法处理接口，只需实现handle方法，并调用reply方法即可
    """

    def __init__(self):
        self.id = None
        self.client = None
        self.topic = None
        self.reply_message = None

    def _reply(self):
        if self.reply_message is None:
            raise ValueError('reply message is not None')
        else:
            self.reply_message.id = self.id
            self.reply_message.type = self.reply_message.type + "_reply"
            self.client.sys_reply(self.reply_message)

    def execute(self, client, topic, message):
        self.id = message.id
        self.client = client
        self.topic = topic
        self.handle(message)
        self._reply()

    def reply(self, reply_message):
        """
        上行消息,不允许重写
        :param reply_message: PropMessage类型，包含flag,value
        :return:
        """
        self.reply_message = reply_message

    def handle(self, message):
        """
        云端下发(下行)设置属性消息,需要重写接收flag进行处理
        :param message: PropMessage,原始的发送信息属性名称
        """
        pass
