import scrapy
import logging

from genshin.items import GinshenItem

logger = logging.getLogger(__name__)


class Wiki2Spider(scrapy.Spider):
    name = 'wiki2'
    allowed_domains = ['wiki.biligame.com/ys']
    start_urls = ['https://wiki.biligame.com/ys/%E6%AD%A6%E5%99%A8']

    def __init__(self):
        self.illegal_word = ("\n", "")

    def parse(self, response):
        table_list = response.xpath("//table[@id='CardSelectTr']/tbody/tr/td[1]/a[1]/@href").extract()
        for i in table_list:
            yield scrapy.Request(url="https://wiki.biligame.com{}".format(i), callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        items = GinshenItem()
        attr_data = {}
        name = response.xpath("//h1[@id='firstHeading']/text()").extract()[0].strip()
        logger.log(logging.INFO, "name:{}".format(name))
        try:
            if len(response.xpath("//div[@id='mw-content-text'][1]/div/table[@class='wikitable']/tbody/tr/th")) > 2:
                ascend_attr = response.xpath(
                    "//div[@id='mw-content-text'][1]/div/table[@class='wikitable']/tbody/tr/th[3]/text()").extract()[
                    0].strip()
                deputy_properties = response.xpath(
                    "//div[@id='mw-content-text'][1]/div/table[@class='wikitable']/tbody/tr/td[3]/text()").extract()
            else:
                ascend_attr = ""
                deputy_properties = [""]*20
            level_list = response.xpath("//div[@id='mw-content-text'][1]/div/table[@class='wikitable'][1]/tbody/tr/td[1]/text()").extract()
            attack_list = response.xpath("//div[@id='mw-content-text'][1]/div/table[@class='wikitable'][1]/tbody/tr/td[2]/text()").extract()
            # logger.log(logging.INFO, "deputy_properties:{}".format(deputy_properties))
            # logger.log(logging.INFO, "level_list:{}".format(level_list))
            # logger.log(logging.INFO, "attack_list:{}".format(attack_list))
            attack_list = [middle_data for middle_data in attack_list if middle_data not in self.illegal_word]
            # logger.log(logging.INFO, "length level:{}, attack:{}, deputy:{}".format(len(level_list), len(attack_list), len(deputy_properties)))
            for i in range(len(attack_list)):
                # attr_data[level_list[i].strip()] = [attack_list[i].split("(")[0].strip(), deputy_properties[i].strip()]
                attr_data[level_list[i].strip()] = [attack_list[i].strip(), deputy_properties[i].strip()]
            items["name"] = name
            items["ascend_attr"] = ascend_attr
            items["attr_data"] = attr_data
        except Exception as e:
            logger.log(logging.ERROR, "Get {} data fail, reason is {}".format(name, e))
            items["name"] = ""
            items["ascend_attr"] = ""
            items["attr_data"] = ""
        yield items



