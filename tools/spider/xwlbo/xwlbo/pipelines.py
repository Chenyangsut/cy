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
        self.suffix = ["2015", "2016", "2017", "2018", "2019", "2020", "2021"]
        self.other = "other"
        self.file_data = {}
        self.num_data = {}
        self.history_data = set()

    def open_spider(self, spider):
        logger.info("Prepare before crawling...")
        if not pathlib.Path(self.root_dir).exists():
            pathlib.Path(self.root_dir).mkdir(parents=True)
        if spider.name == "xwlbotxt":
            for suffix in self.suffix:
                self.file_data[suffix] = open("{}/xwlbo_{}.txt".format(self.root_dir, suffix), "a+", encoding="gb18030")
            self.file_data["other"] = open("{}/xwlbo_other.txt".format(self.root_dir), "a+", encoding="gb18030")
            self.ReadTextHistory()
        logger.info("Prepare over")

    def close_spider(self, spider):
        logger.info("Close spider...")
        if spider.name == "xwlbotxt":
            for txt_file in self.file_data.values():
                txt_file.close()
            logger.info("New xwlbo data numbers are:")
            for suffix in self.num_data:
                logger.info("{} year:{}".format(suffix, self.num_data[suffix]))
            logger.info("All new data numbers are {}".format(sum(self.num_data.values())))

    def process_item(self, item, spider):
        if spider.name == "xwlbotxt":
            # classification by years
            flag = 0
            profile = item["profile"]
            if profile not in self.history_data:
                for suffix in self.suffix:
                    if item["profile"].startswith(suffix):
                        self.file_data[suffix].write("新闻来源:{}\n标题:{}\n具体内容:{}\n{}\n".format(item["profile"], item["title"], item["content"], "**"*20))
                        self.num_data[suffix] = self.num_data.get(suffix, 0) + 1
                        flag = 1
                        break
                    else:
                        continue
                if flag == 0:
                    self.file_data["other"].write("新闻来源:{}\n标题:{}\n具体内容:{}\n{}\n".format(item["profile"], item["title"], item["content"], "**"*20))
        return item

    def ReadTextHistory(self):
        # get history news data
        history_data = []
        history_data_num = {}
        for txt_file in pathlib.Path(self.root_dir).iterdir():
            if not txt_file.is_file():
                continue
            if "xwlbo_" in txt_file.name:
                file_name = txt_file.name
                with open(str(txt_file), "r", encoding="gb18030") as f:
                    for line in f:
                        if not line.startswith("新闻来源:"):
                            continue
                        history_data.append(line.strip().split("新闻来源:")[-1])
                        history_data_num[file_name] = history_data_num.get(file_name, 0) + 1
        self.history_data = set(history_data)
        logger.info("Read history data numbers is: {}".format(history_data_num.items()))
        del history_data, history_data_num


