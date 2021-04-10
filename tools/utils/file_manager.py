#!/usr/bin/env python
# coding: utf-8
"""
File: file_manager.py
Authors: ChenYang
Date: 2021/3/29 13:12:38
"""
import pathlib


def check_path_exist(file_path, check_type=1):
    """

    :param file_path: input file path or folder path, etc
    :param check_type: 1 is check folder, 2 is check file
    :return: if exits return True, else False
    """
    if check_type == 1:
        return pathlib.Path(file_path).is_dir()
    elif check_type == 2:
        return pathlib.Path(file_path).is_file()
    else:
        return False


def make_dir(folder_path, parents=True):
    """

    :param folder_path: need make new direction path
    :param parents: need make parents folder
    :return: execute result, error message (success is "")
    """
    folder_obj = pathlib.Path(folder_path)
    if folder_obj.is_dir():
        return True, ""
    elif folder_obj.is_file():
        return False, "The direction path is a file."
    else:
        folder_obj.mkdir(parents=parents, exist_ok=True)
        return folder_obj.is_dir(), ""


def read_file(file_path, chunk_size=16777216, encoding="utf8"):
    """
    This only read file method, read less line but big file use chunk_size,
    when one line data not big, recommend use for line in f
    :param file_path: text file path.
    :param chunk_size: split text data size.
    :param encoding: text encode type.
    :return: execute status, text data or error message.
    """
    file_obj = pathlib.Path(file_path)
    if not file_obj.is_file():
        return False, "The input path not a file."
    string_list = []
    if file_obj.stat().st_size > chunk_size:
        with open(file_path, "rb", encoding=encoding) as f:
            for file_data in read_file_by_cycle(f, chunk_size=chunk_size):
                if file_data:
                    string_list.append(file_data)
                else:
                    break
        string = "".join(string_list)
    else:
        with open(file_path, "r", encoding=encoding) as f:
            for line in f:
                string_list.append(line)
        string = "".join(string_list)
    del string_list
    return True, string


def read_file_by_cycle(file_open_obj, chunk_size=1024 * 1024 * 16):
    """

    :param file_open_obj: opened text file object.
    :param chunk_size: split size.
    :return: text data.
    """
    while 1:
        data = file_open_obj.read(chunk_size)
        if not data:
            break
        yield data


if __name__ == "__main__":
    file = pathlib.Path("../test/batch_task")
    print(file.stat().st_size)
