import scrapy
from urllib import parse


class Jd11Spider(scrapy.Spider):
    name = 'jd_11'
    allowed_domains = ['www.jd.com']
    start_urls = ["https://www.jd.com"]
    # data_list = ["手机", "笔记本电脑"]
    #
    # start_urls = ["http://www.jd.com//Search?keyword={}".format(parse.quote(i)) for i in data_list]
    # https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&pvid=cbcad35c5a1a42fe96dee7f31b9bbd6a
    # shell command:scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36" https://www.jd.com

    def parse(self, response):
        pass
