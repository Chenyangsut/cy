# -*- coding:utf-8 -*-
# @Time: 2021/2/5 13:09
# @Author: Chenyang
# @File: logger.py
# @Email: sygysut@163.com
# @Direction:


import logging
import pathlib


from cy.libs.log.init import InitLog
from cy.conf.base import MAIN_HOME

InitLog()


def get_log_level(_file_=None):
    log_level = "main.unknown"
    if _file_:
        filepath = str(pathlib.Path(_file_).resolve())
        # filepath = os.path.join(os.path.abspath(os.path.join(os.path.dirname(_file_), os.path.pardir)), _file_)
        print(filepath)
        log_level = filepath.replace(MAIN_HOME, "main")[:-3].replace("/", ".").replace("\\", ".")
    print(log_level)
    return log_level


def get_logger(_file_=None):
    logger = logging.getLogger(get_log_level(_file_=_file_))
    return logger

