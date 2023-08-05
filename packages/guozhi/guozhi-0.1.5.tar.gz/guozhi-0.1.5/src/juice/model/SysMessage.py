#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time   : 2019/3/1 16:00
# @Author : yebing
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : guozhi
# @FileName: SysMessage.py

import json
import uuid


class SysMessage(object):
    def __init__(self, type_name, data):
        self.id = str(uuid.uuid1())
        self.type = type_name
        self.data = data

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'type': self.type,
            'data': self.data
        })

    __repr__ = __str__


if __name__ == '__main__':
    aa = SysMessage("flag", {"gpio_num": 0, "mode": "bcm"})
    print aa
