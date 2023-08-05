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
# @FileName: PropGetHandler.py


class PropGetHandler(object):
    """
        属性获取接口，只需实现handle方法，并调用reply方法即可
    """

    def __init__(self):
        self.id = None
        self.client = None
        self.topic = None
        self.reply_topic = None
        self.reply_message = None

    def _reply(self):
        if self.reply_message is None:
            raise ValueError('reply message is not None')
        else:
            self.reply_message.id = self.id
            self.client.prop_reply(self.reply_topic, self.reply_message)

    def execute(self, client, topic, message):
        self.id = message.id
        self.client = client
        self.topic = topic
        self.reply_topic = topic + "_reply"
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


class PropSetHandler(object):
    """
    属性设置接口，只需实现handle方法，并调用reply方法即可
    """

    def __init__(self):
        self.id = None
        self.client = None
        self.topic = None
        self.reply_topic = None
        self.reply_message = None

    def _reply(self):
        if self.reply_message is None:
            raise ValueError('reply message is not None')
        else:
            self.reply_message.id = self.id
            self.client.prop_reply(self.reply_topic, self.reply_message)

    def execute(self, client, topic, set_prop_message):
        self.id = set_prop_message.id
        self.client = client
        self.topic = topic
        self.reply_topic = topic + "_reply"
        self.handle(set_prop_message)
        self._reply()

    def reply(self, reply_message):
        """
        上行消息,不允许重写
        :param reply_message: PropMessage类型，包含flag,value
        :return:
        """
        self.reply_message = reply_message

    def handle(self, set_prop_message):
        """
        云端下发(下行)设置属性消息,需要重写接收set_prop_message进行处理
        :param set_prop_message: PropMessage类型，包含flag,value
        """
        pass
