# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import shutil


class LlshPipeline:
    def __init__(self):
        shutil.copy("all_magnetic.txt", "spider_file/llsh/{}.txt".format(time.strftime("%Y-%m-%d_%H_%M_%S")))
        self.file = open("all_magnetic.txt", "w", encoding="gb18030")  # 保存文件
        self.file.write("******\ndownload_time:{}\n******\n".format(time.strftime("%Y-%m-%d %H:%M:%S")))  # 记录下载时间

    def process_item(self, item, spider):
        self.file.write("name:{}\nurl :{}\nlink:{}\n******\n".format(item["name"], item["url"], item["magnetic"]))  # 写数据
        return item
