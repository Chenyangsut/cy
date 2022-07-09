# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # https://search.jd.com/search?keyword=%E6%89%8B%E6%9C%BA&psort=3&wq=%E6%89%8B%E6%9C%BA&psort=3&ev=exbrand_%E5%B0%8F%E7%B1%B3%EF%BC%88MI%EF%BC%89%5E
    # keyword 搜索名 Search?keyword= 必须
    # enc 编码格式 enc=utf-8 非
    # wq 未知 手机
    # pvid 未知 588c7399f16e4fc8847676f18e83a68f
    # psort 2 价格 3 销量 4 评论数 5 新品 1 综合
    # ev 品牌 exbrand_华为（HUAWEI）%5E  exbrand_小米（MI）%5E
    # click 未知
    # page 页数，网页一般按照1，3，5进行递增，就是一个网址包含两页数据，一页代表30个商品（商品数目足够的话）
    # s 截至商品数，比如第5页，s就为121
    pass

# 添加请求头
