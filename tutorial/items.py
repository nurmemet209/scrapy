# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#轮毂
class HubItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    price=scrapy.Field()
    img=scrapy.Field()

class CrarBrandItem(scrapy.Item):
    en_name = scrapy.Field()
    