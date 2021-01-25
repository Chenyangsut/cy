# -*- coding:utf-8 -*-
# @Time: 2021/1/25 13:25
# @Author: Chenyang
# @File: singleton.py
# @Email: sygysut@163.com
# @Direction:

import time
import threading


class Singleton(object):
    # Create singleton by __new__.
    # obj = Singleton
    _instance_lock = threading.Lock()  # 加锁！未加锁部分并发执行,加锁部分串行执行,速度降低,但是保证了数据安全,比如在初始化未完成的情况下

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance


class SingletonType(type):
    # Create singletontype by type.
    # metaclass=Singletontype when you create a new class
    _instance_lock = threading.Lock()  # 加锁！未加锁部分并发执行,加锁部分串行执行,速度降低,但是保证了数据安全

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


# class Singleton(object):
#     # Create singleton by class
#     # obj = Singleton.instance()
#     _instance_lock = threading.Lock()
#
#     def __init__(self):
#         time.sleep(1)
#
#     @classmethod
#     def instance(cls, *args, **kwargs):
#         if not hasattr(Singleton, "_instance"):
#             with Singleton._instance_lock:
#                 if not hasattr(Singleton, "_instance"):
#                     Singleton._instance = Singleton(*args, **kwargs)
#         return Singleton._instance


# class Singleton(object):
#     # models
#     # from a import singleton
#     def foo(self):
#         pass
# singleton = Singleton()


# def Singleton(cls):
#     # Use singleton as decorate
#     # @Singleton
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton

