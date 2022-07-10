# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import shutil
import sys
import pathlib
import logging
import json

from scrapy.exporters import JsonLinesItemExporter

_self_dir = pathlib.Path(__file__).parent
logger = logging.getLogger(__name__)

sys.path.insert(0, str(_self_dir.parent.parent.parent.absolute()))

from conf.spider_conf import BASE_SPIDER
from utils.file_manager import check_path_exist
from utils.file_manager import make_dir


class LlshPipeline(object):
    __slots__ = ["data", "file", 'time_format', 'crawler', 'exporter']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        """
        init
        """
        self.time_format = time.strftime("%Y-%m-%d_%H_%M_%S")
        self.crawler = crawler

    def open_spider(self, spider):
        """
        开启spider预处理操作
        """
        if spider.name == 'animal':
            file_dir = BASE_SPIDER[spider.name]['output_dir']
            status = self.check_make_path(file_dir)
            if not status:
                self.crawler.engine.close_spider(spider, 'make directory failed, directory [{0}]'.format(file_dir))
            file_path = str(pathlib.Path(file_dir, '{0}.txt'.format(spider.name)))
            if pathlib.Path(file_path).is_file():
                self.data = self.read_data(file_path)
                shutil.copy(file_path, str(pathlib.Path(file_dir, '{0}-{1}.txt'.format(spider.name, self.time_format))))
            else:
                self.data = set()
            self.file = open(file_path, 'wb')
            self.exporter = JsonLinesItemExporter(self.file, ensure_ascii=False, encoding='gb18030')

    def close_spider(self, spider):
        """
        关闭spider
        """
        if spider.name == 'animal':
            self.data = set()
            self.file.close()

    def read_data(self, original_file):
        """
        读取历史数据
        """
        original_data = open(original_file, "r", encoding="gb18030")
        try:
            data_list = [json.loads(line.strip())['magnetic'] for line in original_data]
        except:
            data_list = []
        finally:
            original_data.close()
        return set(data_list)

    def process_item(self, item, spider):
        if spider.name == 'animal':
            logger.debug('title = [{0}]'.format(item['title']))
            if item["magnetic"].strip() not in self.data:
                logger.debug('start write')
                # self.file.write(
                #     "name:{}\nurl :{}\nlink:{}\n******\n".format(item["name"], item["url"], item["magnetic"]))  # 写数据
                self.exporter.export_item(item)
                self.data.add(item['magnetic'].strip())
        return item

    def check_make_path(self, directory):
        """
        检查目录合,不存在就创建
        :return bool, 创建成功或是已经是目录返回True
        """
        if not check_path_exist(directory):
            status = make_dir(directory)
            if not status:
                return False
        return True
