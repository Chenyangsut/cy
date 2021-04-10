#!/usr/bin/env python
# coding: utf-8
"""
File: ChromeFake.py
Authors: ChenYang
Date: 2021/4/9 10:33:46
Description:
"""
import time
import traceback
from collections import defaultdict
import json

from selenium import webdriver

from tools.utils.get_config import handle_config


class ChromeFake(object):
    def __init__(self, chrome_path="", options={}):
        self.options = webdriver.ChromeOptions()
        self.option_dict = options
        self.config = handle_config(self.__class__.__name__)
        print(self.config)
        if len(chrome_path) == 0:
            self.executable_path = self.config.get_attribute("basic", "executable_path")
        else:
            self.executable_path = chrome_path
        self._is_alive = False
        self.error_msg = defaultdict(str)
        self.browser = None
        self._init_options()
        self._start()

    def _init_options(self):
        # Initialize chrome options,
        # some value of key need input, but others value is none or default,
        # see configurations if need.
        try:
            if len(self.option_dict) > 0:
                self._add_option()
        except:
            self.error_msg["init_option"] += traceback.format_exc()
        # finally:
        #     self.options.binary_location = self.executable_path

    def _add_option(self):
        temp_dict = self.config.get_section("options")
        value_argument = temp_dict["type"]["value_argument"]
        single_argument = temp_dict["type"]["single_argument"]
        experimental = temp_dict["type"]["experimental"]
        extension = temp_dict["type"]["extension"]
        default_argument = temp_dict["type"]["default_argument"]
        for k, v in self.option_dict.items():
            if k in extension:
                if k == "crx":
                    if not isinstance(v, list):
                        continue
                    for crx_path in k:
                        self.options.add_extension(crx_path)
            elif k in value_argument:
                self.options.add_argument("{}={}".format(k, v))
            elif k in single_argument:
                self.options.add_argument(k)
            elif k in experimental:
                self.options.add_experimental_option("{},{}".format(k, experimental[k][0]))
            elif k in default_argument:
                self.options.add_argument("{}={}".format(k, default_argument[k][0]))
            else:
                self.error_msg["add_options"] += "Not identify config, warning config={}\n".format(k)
        self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 3,'permissions.default.stylesheet':2})

    def _start(self):
        self.browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.options)
        self._is_alive = True
        # try:
        #     self.browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=self.options)
        #     self._is_alive = True
        # except:
        #     self.error_msg["chrome_start"] += traceback.format_exc() + "\n"
        # finally:
        #     return self._is_alive

    def __del__(self):
        if self.browser:
            self.browser.quit()

    def close(self):
        if self.browser:
            self.browser.close()


if __name__ == "__main__":
    options = {"--disable-javascript": "", "blink-setting": "", "--no-sandbox": ""}
    # web = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")
    # web.get("https://www.baidu.com")
    # time.sleep(10)
    # web.quit()

