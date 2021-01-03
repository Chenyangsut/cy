# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import shutil

class LlshPipeline:
    __slots__ = ["data", "file"]

    def __init__(self):
        self.data = self.read_data("E:/cy/data/spider_file/llsh/all_magnetic.txt")
        shutil.copy("E:/cy/data/spider_file/llsh/all_magnetic.txt", "E:/cy/data/spider_file/llsh/{}.txt".format(time.strftime("%Y-%m-%d_%H_%M_%S")))
        self.file = open("E:/cy/data/spider_file/llsh/all_magnetic.txt", "w", encoding="gb18030")  # 保存文件
        self.file.write("******\ndownload_time:{}\n******\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))  # 记录下载时间

    def read_data(self, original_file):
        original_data = open(original_file, "r", encoding="gb18030")
        try:
            data_list = [line.split("name:")[-1].strip() for line in original_data if line.startswith("name:")]
        except:
            data_list = []
        finally:
            original_data.close()
        return set(data_list)

    def process_item(self, item, spider):
        if item["name"].strip() not in self.data:
            self.file.write("name:{}\nurl :{}\nlink:{}\n******\n".format(item["name"], item["url"], item["magnetic"]))  # 写数据
        return item
