#!/usr/bin/env python
# -*- coding:utf-8 -*-

from juice.handler.SysHandler import SysHandler
from juice.util import Util


class SysArmGetHandler(SysHandler):
    """
        系统CPU内存占比响应方法
        handle为必须实现的方法
    """

    def handle(self, message):
        message.data = Util.get_raspberry_prop_info("get_mem_arm")
        self.reply(message)


class SysGpuGetHandler(SysHandler):
    """
        系统GPU内存占比响应方法
        handle为必须实现的方法
    """

    def handle(self, message):
        message.data = Util.get_raspberry_prop_info("get_mem_gpu")
        self.reply(message)


class SysVoltsGetHandler(SysHandler):
    """
        系统核心电压响应方法
        handle为必须实现的方法
    """

    def handle(self, message):
        message.data = Util.get_raspberry_prop_info("measure_volts_core")
        self.reply(message)


class SysTempGetHandler(SysHandler):
    """
        温度响应方法
        handle为必须实现的方法
    """

    def handle(self, message):
        message.data = Util.get_raspberry_prop_info("measure_temp")
        self.reply(message)
