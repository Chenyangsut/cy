# -*- coding: utf-8 -*-
import scrapy
import pathlib
import sys
import logging

_base_dir = pathlib.Path(__file__)
sys.path.insert(0, str(_base_dir.parent.parent.parent.parent.parent.absolute()))

from llsh.items import LlshItem

from conf.spider_conf import BASE_SPIDER

logger = logging.getLogger(__name__)


class AnimalSpider(scrapy.Spider):
    name = 'animal'
    allowed_domains = BASE_SPIDER['animal']['allowed_domains']
    # 人为设置爬取的页面数量
    start_urls = [BASE_SPIDER['animal']['base_page'] + str(i) for i in
                  range(1, BASE_SPIDER['animal']['max_page_num'] + 1)]
    # start_urls = BASE_SPIDER['animal']['start_urls']

    def parse(self, response):
        """
        取每个番剧的详情页面，进行爬取
        """
        parts = response.xpath("//h1[@class='entry-title']/a")
        # logger.info('parts length = [{0}]'.format((len(parts))))
        for part in parts:
            content_page = part.xpath('@href')[0].extract()
            yield scrapy.Request(url=content_page, callback=self.parse_item)

    def parse_item(self, response):
        """
        提取磁链
        """
        item = LlshItem()
        title = response.xpath("//h1[@class='entry-title']/text()")[0].extract()
        magnetic = []
        for i in range(1, 15):
            magnetic.extend(
                response.xpath("//div[@id='content']/article/div//text()".format(i)).re(
                    r'[a-zA-Z0-9]+')[::-1])  # 在广告栏的上面几个分块中提取字符串，因为包含新旧界面所以链接位置不固定，当前定位最大值为上数第14栏
        item['magnetic'] = ''
        for link in magnetic:
            if len(link) > 39:  # 利用长度过滤掉不是下载链接的字符串
                # final_links.append(link)
                item['magnetic'] = link  # 取最后一个下载链接
                break
        item['title'] = title  # 名称
        # item["magnetic"] = ",".join(final_links)
        item['url'] = response.url  # 番剧详情页

        yield item
