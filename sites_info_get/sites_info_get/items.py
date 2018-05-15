# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SitesInfoGetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    baidurank = scrapy.Field()
    pagerank = scrapy.Field()
    alexa_ranking = scrapy.Field()
    labels = scrapy.Field()
