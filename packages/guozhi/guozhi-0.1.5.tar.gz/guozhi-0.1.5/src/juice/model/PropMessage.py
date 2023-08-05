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

import json
import uuid


class PropMessage(object):
    def __init__(self, flag, value):
        self.id = str(uuid.uuid1())
        self.flag = flag
        self.value = value

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'flag': self.flag,
            'value': self.value
        })

    __repr__ = __str__


if __name__ == '__main__':
    aa = PropMessage("flag", "asd")
    print aa
    print type(str({"flag": "flag", "value": "asd"}))
