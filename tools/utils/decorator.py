# -*- coding:utf-8 -*-
# @Time: 2021/1/21 18:00
# @Author: Chenyang
# @File: decorator.py
# @Email: sygysut@163.com
# @Direction:

from functools import wraps
import time


def decorator_time(func):
    # calculator executive a function spend time
    @wraps(func)  # prevent some same name attribute be rewritten
    def wraptime(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print("{} spend time {}s".format(func.__name__, time.time()-start_time))
    return wraptime
