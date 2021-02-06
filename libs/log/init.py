# -*- coding:utf-8 -*-
# @Time: 2021/2/5 13:49
# @Author: Chenyang
# @File: init.py
# @Email: sygysut@163.com
# @Direction:


import json
import logging
import logging.config
import pathlib

from cy.conf.base import BASE_CONF_DIR
from cy.libs.singleton import SingletonType


log_conf_path = str(pathlib.Path(BASE_CONF_DIR).joinpath("logger.json"))


class InitLog(object):
    __metaclass__ = SingletonType

    def __init__(self, file_path=log_conf_path, level=logging.INFO, config_name="basic"):
        log_path = file_path
        if pathlib.Path(log_path).exists():
            with open(log_path, "r") as f:
                config = json.load(f)
                print(config)
                logging.config.dictConfig(config[config_name])
        else:
            logging.basicConfig(level=level)
        logger = logging.getLogger(config_name)
        logger.info("Start logging ...")


InitLog()