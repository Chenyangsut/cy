# -*- coding: utf-8 -*-
import scrapy

from llsh.items import LlshItem


class AnimalSpider(scrapy.Spider):
    name = 'animal'
    allowed_domains = ['www.com']
    start_urls = ['https://www.com']

    def start_requests(self):
        # 人为设置爬取的页面数量
        for i in range(1, 125):
            yield scrapy.Request(url="https://www.com/page/{}/".format(i), callback=self.parse)

    def parse(self, response):
        # 取每个番剧的详情页面，进行爬取
        parts = response.xpath("//h1[@class='entry-title']/a")
        for part in parts:
            content_page = part.xpath("@href")[0].extract()
            yield scrapy.Request(url=content_page, callback=self.parse_item)


    def parse_item(self, response):
        item = LlshItem()
        name = response.xpath("//h1[@class='entry-title']/text()")[0].extract()
        magnetic = []
        for i in range(1, 15):
            magnetic.extend(response.xpath("//div[@id='metaslider-id-3222']/preceding-sibling::*[{}]//text()".format(i)).re(r'[a-zA-Z0-9]+')[::-1])  # 在广告栏的上面几个分块中提取字符串，因为包含新旧界面所以链接位置不固定，当前定位最大值为上数第14栏
        item["magnetic"] = ""
        for link in magnetic:
            if len(link) > 31:  # 利用长度过滤掉不是下载链接的字符串
                # final_links.append(link)
                item["magnetic"] = link  # 取最后一个下载链接
                break
        item["name"] = name  # 名称
        # item["magnetic"] = ",".join(final_links)
        item["url"] = response.url  # 番剧详情页

        yield item



