# -*- coding: utf-8 -*-
import scrapy

from genshin.items import GinshenItem


class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['wiki.biligame.com/ys']
    start_urls = ['https://wiki.biligame.com/ys/%E8%A7%92%E8%89%B2']

    def parse(self, response):
        information_urls = response.xpath("//div[@class='itemhover home-box-tag']/div[@class='center']/div[@class='floatnone']/a/@href").extract()
        for next_page in information_urls:
            page_url = "https://wiki.biligame.com{}".format(next_page)
            # print("next_page: {}".format(page_url))
            yield scrapy.Request(url=page_url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        # print("parse_item")
        items = GinshenItem()
        name = response.xpath("//h1[@id='firstHeading']/text()").extract()[0].strip()
        try:
            items["name"] = name
            attr_data = {}
            character_level = ["1", "20", "40", "50", "60", "70", "80", "90"]
            character_hp = response.xpath("//div[contains(@class,'col-sm-8')][1]/div[@class='poke-bg'][2]/table[@class='wikitable'][1]/tbody/tr[3]/td/text()").extract()[1:]
            character_attack = response.xpath("//div[contains(@class,'col-sm-8')][1]/div[@class='poke-bg'][2]/table[@class='wikitable'][1]/tbody/tr[4]/td/text()").extract()[1:]
            character_defense = response.xpath("//div[contains(@class,'col-sm-8')][1]/div[@class='poke-bg'][2]/table[@class='wikitable'][1]/tbody/tr[5]/td/text()").extract()[1:]
            character_ascend = response.xpath("//div[contains(@class,'col-sm-8')][1]/div[@class='poke-bg'][2]/table[@class='wikitable'][1]/tbody/tr[7]/td/text()").extract()[1:]
            for i in range(len(character_level)):
                attr_data[character_level[i]] = [character_hp[i].strip(), character_attack[i].strip(), character_defense[i].strip(), character_ascend[i].strip()]
            items["attr_data"] = attr_data
            items["ascend_attr"] = response.xpath("//div[contains(@class,'col-sm-8')][1]/div[@class='poke-bg'][2]/table[@class='wikitable'][1]/tbody/tr[7]/td/b/text()").extract()[0].strip()
            # print("items:{}".format(items))
        except:
            items["name"] = ""
            items["attr_data"] = ""
            items["ascend_attr"] = ""
        finally:
            yield items



