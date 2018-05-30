# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AizhanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    keywords = scrapy.Field()
    labels = scrapy.Field()
    labels_tf = scrapy.Field()

    pagerank = scrapy.Field()
    baidurank = scrapy.Field()
    alexa_ranking = scrapy.Field()

class AizhanDetailedItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    alias = scrapy.Field()
    task_url = scrapy.Field()
    category = scrapy.Field()
    area = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    detailed_description = scrapy.Field()
    score = scrapy.Field()
    alexa_rank = scrapy.Field()
    page_rank = scrapy.Field()
    baidu_rank = scrapy.Field()

    url = scrapy.Field()
    real_title = scrapy.Field()
    real_keywords = scrapy.Field()
    real_description = scrapy.Field()
    labels = scrapy.Field()

