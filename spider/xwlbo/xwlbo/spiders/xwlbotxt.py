import scrapy
from xwlbo.items import XwlboItem


class XwlbotxtSpider(scrapy.Spider):
    # some 2016 or early news because typography difficult, and this time in order to make 2020 cloud, so ignore some
    name = 'xwlbotxt'
    allowed_domains = ['www.xwlbo.com']
    start_urls = ['http://www.xwlbo.com/']

    def start_requests(self):
        # sevaral days xwlbo
        for i in range(70):
            yield scrapy.Request(url="http://www.xwlbo.com/txt_{}.html".format(i), callback=self.parse, dont_filter=True)

    def parse(self, response):
        # get daily xwlbo
        txt_content_pages = response.xpath(
            "//div[@id='tab_con1']/div[@class='text_list']/ol[@class='xwlist']/li/a/@href").extract()
        for content_page in txt_content_pages:
            yield scrapy.Request(url=content_page, callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        # get each chapter xwlbo
        item = XwlboItem()
        item["profile"] = response.xpath("//div[@id='content']/div[@class='zhibo']/div[@class='title']/h2/text()").extract()[0]
        chapters = response.xpath("//div[@id='tab_con2']/div[@class='text_content']/p/strong/a/@href").extract()

        for chapter in chapters:
            url = chapter if "www.xwlbo.com" in chapter else "http://www.xwlbo.com/{}".format(chapter)
            request = scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)
            request.meta["item"] = item
            yield request

    def parse_content(self, response):
        item = response.meta["item"]
        try:
            title = response.xpath("//div[@id='content']/div[@class='zhibo']/div[@class='title']/h2/text()").extract()[0]
            content = "".join(response.xpath("//div[@id='tab_con2']/div[@class='text_content']/p/text()").extract())
            item["title"] = title
            item["content"] = content
            yield item
        except:
            pass



