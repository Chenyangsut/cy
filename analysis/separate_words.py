# -*- coding:utf-8 -*-
# @Time: 2021/1/15 12:45
# @Author: Chenyang
# @File: separate_words.py
# @Email: sygysut@163.com
# @Direction:

import jieba
import pathlib


def separate_xwlbotxt(file_str, level=1, coding="utf-8", add_words=[], del_words=[]):
    '''
    :param file_str:txt file or parsing text
    :param level:separate result mode, 1 is return lis, 2 is iterator
    :param coding:read file encoding
    :return: list or iterator
    '''
    parsing_str = ""
    if pathlib.Path(file_str).is_file():
        with open(file_str, "r", encoding=coding) as f:
            for line in f:
                parsing_str += line.strip()
    elif isinstance(file_str, str):
        parsing_str = file_str
    else:
        return None
    if add_words:
        for word in add_words:
            jieba.add_word(word)
    if del_words:
        for word in del_words:
            jieba.del_word(word)
    return jieba.lcut(parsing_str)
