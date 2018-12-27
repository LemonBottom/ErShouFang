# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErshoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bedroom = scrapy.Field()
    living_room = scrapy.Field()
    area = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    region = scrapy.Field()
    community = scrapy.Field()
    agency = scrapy.Field()
    date = scrapy.Field()

