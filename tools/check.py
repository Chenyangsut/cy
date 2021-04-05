# -*- coding:utf-8 -*-
# @Time: 2021/3/2 22:13
# @Author: Chenyang
# @File: check.py
# @Email: sygysut@163.com
# @Direction:


import pandas
import pathlib

from cy.tools.utils.get_config import handle_config

check_config = handle_config(file_name="base")


def get_check_data():
    root_dir = check_config.get_attribute(section="cy_data", attribute="base_dir")
    check_sub = "check/2021"
    check_dir = str(pathlib.Path(root_dir).joinpath(check_sub))
    for xlsx_file in pathlib.Path(check_dir).iterdir():
        if not xlsx_file.is_file():
            continue
        if ".xlsx" not in xlsx_file.name:
            continue
        datastamp = xlsx_file.stem
        check_data = pandas.read_excel(str(xlsx_file), index_col=0)
        print(check_data.columns)
        columns = check_data.columns
        for column in columns:
            print(check_data[column])


get_check_data()
