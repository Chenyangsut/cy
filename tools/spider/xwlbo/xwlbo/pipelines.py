# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import time
import pathlib
import logging

logger = logging.getLogger(__name__)

class XwlboPipeline:
    def __init__(self):
        self.time = time.strftime("%Y-%m-%d_%H_%M_%S")
        self.root_dir = "E:/cy/data/spider_file/xwlbo"

    def open_spider(self, spider):
        logger.info("Prepare before crawling...")
        if not pathlib.Path(self.root_dir).exists():
            pathlib.Path(self.root_dir).mkdir(parents=True)
        if spider.name == "xwlbotxt":
            txt_file = pathlib.Path(self.root_dir).joinpath("{}.txt".format(self.time))
            self.txt_file = open(str(txt_file), "w", encoding="gb18030")

    def close_spider(self, spider):
        logger.info("Close spider...")
        if spider.name == "xwlbotxt":
            self.txt_file.close()

    def process_item(self, item, spider):
        if spider.name == "xwlbotxt":
            self.txt_file.write("新闻来源:{}\n标题:{}\n具体内容:{}\n{}\n".format(item["profile"], item["title"], item["content"], "**"*20))
        return item
