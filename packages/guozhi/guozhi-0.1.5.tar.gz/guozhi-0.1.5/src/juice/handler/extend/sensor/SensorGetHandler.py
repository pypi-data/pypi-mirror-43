#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Adafruit_DHT

from juice.handler.PropHandler import PropGetHandler
from juice.model.PropMessage import PropMessage
from juice.util import GpioUtil


class TempGetHandler(PropGetHandler):
    """
    温度传感器获取，实例化需要设置bcm编号
    """

    def __init__(self, gpio_bcm_num):
        self.gpio = gpio_bcm_num

    """
        传感器温度获取方法
        handle为必须实现的方法
        reply上行消息，返回给服务器
    """

    def handle(self, message):
        self.reply(PropMessage(message.flag, self.temp()))

    def temp(self):
        sensor = Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.gpio)
        return 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)


class SoudGetHandler(PropGetHandler):
    """
    蜂鸣器状态获取，实例化需要设置bcm编号
    """

    def __init__(self, mode, gpio_num):
        self.mode = mode.lower()
        self.gpio = gpio_num

    """
        传蜂鸣器状态获取方法
        handle为必须实现的方法
        reply上行消息，返回给服务器
    """

    def handle(self, message):
        self.reply(PropMessage(message.flag, GpioUtil.GetGPIOStatus(self.mode, self.gpio)))
