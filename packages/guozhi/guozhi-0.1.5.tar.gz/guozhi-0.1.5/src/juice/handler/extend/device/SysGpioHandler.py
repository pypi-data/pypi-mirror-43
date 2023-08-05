#!/usr/bin/env python
# -*- coding:utf-8 -*-

from juice.handler.SysHandler import SysHandler
from juice.util import GpioUtil


class GpioInitHandler(SysHandler):
    """
        GPIO针脚初始化
        handle为必须实现的方法
    """

    def handle(self, message):
        data = 'input data format error, must be dict'
        if isinstance(message.data, dict):
            data = 'success'
            try:
                GpioUtil.initGPIOAccessType(
                    message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1),
                    message.data.get(GpioUtil.GPIO_CONST_ACCESS_TYPE, ''),
                    message.data.get(GpioUtil.GPIO_CONST_SIGNAL, ''))
            except Exception, err:
                data = 'failure: %s' % err

        message.data = data
        self.reply(message)


class GpioSetHandler(SysHandler):
    """
        GPIO针脚电平设置(只支持GPIO.OUT模式)
        handle为必须实现的方法
    """

    def handle(self, message):
        data = 'input data format error, must be dict'
        if isinstance(message.data, dict):
            data = 'success'
            try:
                GpioUtil.setGPIOStatus(
                    message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1),
                    message.data.get(GpioUtil.GPIO_CONST_SIGNAL, ''))
            except Exception, err:
                data = 'failure: %s' % err

        message.data = data
        self.reply(message)


class GpioStatusGetHandler(SysHandler):
    """
    GPIO状态获取
    """

    def handle(self, message):
        data = 'input data format error, must be dict'
        if isinstance(message.data, dict):
            data = GpioUtil.GetGPIOStatus(
                message.data.get(GpioUtil.GPIO_CONST_MODE, ''), message.data.get(GpioUtil.GPIO_CONST_NUM, -1))

        message.data = data
        self.reply(message)
