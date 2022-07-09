import scrapy
from urllib import parse

from cy.conf.spider_conf import DOWNLOAD_FIELD_DICT


class Jd11Spider(scrapy.Spider):
    name = 'jd_11'
    allowed_domains = ['www.jd.com']
    data_list = ["手机", "笔记本电脑"]
    start_urls = ["http://www.jd.com//Search?keyword={}".format(parse.quote(i)) for i in data_list]
    # https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%89%8B%E6%9C%BA&pvid=daed6d5480134f6ea835ce3d397f3b4b
    # https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&pvid=cbcad35c5a1a42fe96dee7f31b9bbd6a
    # shell command:scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36" https://www.jd.com
    # headers={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    # "cookie": "1148232;areaId=1;ipLoc-djd=1-2805-0-0;PCSYCityID=CN_110000_110100_0;user-key=5ff426fd-9700-497d-b454-20e44059cea3;cn=0;rkv=1.0;__jda=76161171.150623251.1605017089.1612251816.1617621148.8;__jdc=76161171;shshshfp=47d87ab0f06b8130106dc12304dbd421; __jdb = 76161171.12.150623251|8.1617621148;shshshsID=81435ba537baa1842bd288e034fbf24b_12_1617621622943"
    # cookies={}

    def parse(self, response):
        pass
