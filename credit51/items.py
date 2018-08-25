# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Credit51Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    ct1 = scrapy.Field()
    ct2 = scrapy.Field()
    tit = scrapy.Field()
    tit_url = scrapy.Field()
    pst_aut = scrapy.Field()
    aut_url = scrapy.Field()
    rel_tim = scrapy.Field()
    new_com_aut = scrapy.Field()
    new_com_tim = scrapy.Field()
    cid = scrapy.Field()
    com_aut = scrapy.Field()
    com_aut_url = scrapy.Field()
    aut_rel_tim = scrapy.Field()
    com = scrapy.Field()
    flr = scrapy.Field()
