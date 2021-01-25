# -*- coding:utf-8 -*-
# @Time: 2021/1/22 19:34
# @Author: Chenyang
# @File: get_config.py
# @Email: sygysut@163.com
# @Direction: Read config file


import traceback
import pathlib
import configobj

from cy.conf.base import BASE_CONF_DIR


def handle_config(file_name="cy", file_path=""):
    """
    handle config manager
    :param file_name: config file name, no extension
    :param file_path: config file path
    :return: object for config file
    """
    config = None

    config_path = file_path if file_path else str(pathlib.Path(BASE_CONF_DIR).joinpath("{}.conf".format(file_name)))
    try:
        config = ConfigObj(config_path)
    except:
        print("Exception : {}".format(traceback.format_exc()))

    return config


class ConfigObj(object):
    """Config file parser."""

    def __init__(self, conf_path):
        """
        :param conf_path: config file path.
        """
        self.conf_path = conf_path
        self.config = configobj.ConfigObj(conf_path, encoding="utf8")

    def get_all_config(self):
        return self.config

    def get_section(self, section):
        values = self.config.get(section, None)
        if values:
            for key in values.keys():
                values[key] = format_result(str(values[key]))
        return values

    def get_attribute(self, section, attribute):
        res = values = self.config.get(section, None)
        if values:
            res = format_result(str(values.get(attribute, "")))

        return res

    def set_section(self, section, value, new=False):
        if new or section in self.config:
            self.config[section] = value
            self.config.write()

    def set_attribute(self, section, attribute, value, new=False):
        if new or all([section in self.config and attribute in self.config[section]]):
            self.config[section][attribute] = value
            self.config.write()

    def delete_section(self, section):
        if section in self.config:
            del self.config[section]
            self.config.write()

    def delete_attribute(self, section, attribute):
        if section in self.config and attribute in self.config[section]:
            del self.config[section][attribute]
            self.config.write()


def format_result(value):
    value = bool_convert(value)
    value = num_convert(value)
    return value


def bool_convert(value):
    """Convert multi type of value to bool"""
    if value in ['yes', 'on', '1', 'True', 'true']:
        res = True
    elif value in ['no', 'off', '0', 'False', 'false']:
        res = False
    else:
        res = value
    return res


def num_convert(value):
    """Convert multi type of value to num"""
    if not isinstance(value, str):
        return value
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
