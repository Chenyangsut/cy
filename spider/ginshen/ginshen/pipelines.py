# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import time
import shutil
import logging


logger = logging.getLogger(__name__)


class GinshenPipeline:

    def __init__(self):
        self.data = []
        self.count = 0
        self.error = 0
        self.time = time.strftime("%Y-%m-%d_%H_%M_%S")

    def open_spider(self, spider):
        logger.log(logging.INFO, "1")
        if spider.name == "wiki":
            try:
                shutil.copy("E:/cy/data/spider_file/genshin/wiki/character.txt", "E:/cy/data/spider_file/genshin/wiki/character-{}.txt".format(self.time))
            except Exception as e:
                logger.log(logging.WARNING, "拷贝文件失败 --{}".format(e))
            finally:
                self.character_file = open("E:/cy/data/spider_file/genshin/wiki/character.txt", "w", encoding="gb18030")

        if spider.name == "wiki2":
            try:
                shutil.copy("E:/cy/data/spider_file/genshin/wiki/weapon.txt",
                            "E:/cy/data/spider_file/genshin/wiki/weapon-{}.txt".format(self.time))
            except Exception as e:
                logger.log(logging.WARNING, "拷贝文件失败 --{}".format(e))
            finally:
                self.weapon_file = open("E:/cy/data/spider_file/genshin/wiki/weapon.txt", "w", encoding="gb18030")

    def close_spider(self, spider):
        if spider.name == "wiki":
            self.character_file.close()
        if spider.name == "wiki2":
            self.weapon_file.close()

    def process_item(self, item, spider):
        if spider.name == "wiki":
            try:
                if item["name"] and item["name"] not in self.data:
                    self.character_file.write('{3}"name":"{0}","ascend":"{2}","attr":"{1}"{4}\n'.format(item["name"], item["attr_data"], item["ascend_attr"], "{", "}"))
                    self.data.append(item["name"])
                    self.count += 1
                    logger.log(logging.INFO, "添加第{}条数据".format(self.count))
            except Exception as e:
                self.error += 1
                logger.log(logging.WARNING, "共失败{}条数据, 本条数据失败原因：{}".format(self.error, e))
        elif spider.name == "wiki2":
            try:
                 if item["name"]:
                     self.weapon_file.write('{3}"name":"{0}","ascend":"{1}","attr":"{2}"{4}\n'.format(item["name"], item["ascend_attr"], item["attr_data"], "{", "}"))
                     self.data.append(item["name"])
                     self.count += 1
                     logger.log(logging.INFO, "添加第{}条数据".format(self.count))
            except Exception as e:
                self.error += 1
                logger.log(logging.WARNING, "共失败{}条数据，本条数据失败原因：{}".format(self.error, e))
        return item

    # # (可选)此方法如果实现了,那么BookFilterPipeline对象从这里调用,必须返回一个cls(参数)对象,crawler.settings是读取项目目录下的settings中的配置选项！
    # @classmethod
    # def from_crawler(cls, crawler):
    #     count = crawler.settings.get('BOOK_FILTER_COUNT', 0)
    #     return cls(count)


class PrepareItemPipeline:

    def __init__(self):
        self.length = 2

    def process_item(self, item, spider):
        if len(item["name"]) < self.length:
            return item
        if spider.name == "wiki":
            if item["attr_data"]:
                for key, value in item["attr_data"].items():
                    middle_value = [information if information else "-" for information in value]
                    item["attr_data"][key] = middle_value
        if spider.name == "wiki2":
            pass
        return item





