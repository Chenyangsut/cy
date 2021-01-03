# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TemplatePipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open("download_magnet.txt", "w", encoding="gb18030")

    def close_spider(self, spider):
        self.file.close()

    # # (可选)此方法如果实现了,那么BookFilterPipeline对象从这里调用,必须返回一个cls(参数)对象,crawler.settings是读取项目目录下的settings中的配置选项！
    # @classmethod
    # def from_crawler(cls, crawler):
    #     count = crawler.settings.get('BOOK_FILTER_COUNT', 0)
    #     return cls(count)

    def process_item(self, item, spider):
        # 将下载后的链接储存到临时文件中
        self.file.write("{}\n".format(item["magnet"]))


class PrepareItemPipeline:

    def process_item(self, item, spider):
        pass