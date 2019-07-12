# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class COMItem(scrapy.Item):
    id = scrapy.Field()
    place = scrapy.Field()

class PRIXItem(scrapy.Item):
    id = scrapy.Field()
    place = scrapy.Field()
    rent_apart_hybrid_high = scrapy.Field()
    rent_apart_hybrid_low= scrapy.Field()
    rent_apart_hybrid_value = scrapy.Field()
    rent_apart_t1_high = scrapy.Field()
    rent_apart_t1_low= scrapy.Field()
    rent_apart_t1_value = scrapy.Field()
    rent_apart_t2_high = scrapy.Field()
    rent_apart_t2_low= scrapy.Field()
    rent_apart_t2_value = scrapy.Field()
    rent_apart_t3_high = scrapy.Field()
    rent_apart_t3_low= scrapy.Field()
    rent_apart_t3_value = scrapy.Field()
    rent_apart_t4_high = scrapy.Field()
    rent_apart_t4_low= scrapy.Field()
    rent_apart_t4_value = scrapy.Field()
    sell_apart_high = scrapy.Field()
    sell_apart_low= scrapy.Field()
    sell_apart_value = scrapy.Field()
    sell_house_high = scrapy.Field()
    sell_house_low= scrapy.Field()
    sell_house_value = scrapy.Field()
    sell_hybrid_high = scrapy.Field()
    sell_hybrid_low= scrapy.Field()
    sell_hybrid_value = scrapy.Field()
    zips = scrapy.Field()
