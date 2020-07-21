# -*- coding: utf-8 -*-
import scrapy

from template.items import TemplateItem


class DownloadmagnicSpider(scrapy.Spider):
    name = 'DownloadMagnic'
    allowed_domains = ['ysjihe.cc']  # 下载网址的域名
    start_urls = ['http://www.ysjihe.cc/download/208192-magnet.html']  # 下载页面网址

    def parse(self, response):
        item = TemplateItem()
        # 获取页面中视频下载链接的提取方式
        magnets = response.xpath("//li[@class='thunder-deal']/@data-link")
        for magnet in magnets:
            if magnet.extract():
                item["magnet"] = magnet.extract()
                yield item


