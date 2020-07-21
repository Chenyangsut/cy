# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TemplatePipeline:
    def __init__(self):
        self.file = open("download_magnet.txt", "w", encoding="gb18030")

    def process_item(self, item, spider):
        # 将下载后的链接储存到临时文件中
        self.file.write("{}\n".format(item["magnet"]))

