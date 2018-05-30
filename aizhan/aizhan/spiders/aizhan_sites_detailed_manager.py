"""
详细版爱站网爬虫
author: Xinling
create-date: (5/27/18)
"""
import os
import scrapy
import logging
from scrapy import log
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from aizhan.items import AizhanDetailedItem



MONGODB_URL = get_project_settings()['MONGODB_URL']

class siteSpider(scrapy.Spider):
    name = "aizhan_sites_detailed_manager"

    start_urls = ['http://top.aizhan.com',]
    # start_urls = ['https://top.aizhan.com/top/t2-34/',]

    def parse(self, response):
        for category_url in response.xpath('/html/body/div[3]/div/div[2]/ul/li/a/@href').extract():
            yield scrapy.Request(category_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        i = 0
        for sub_category_url in response.xpath('/html/body/div[3]/div/div[3]/div[2]/div[1]/div[1]/ul/li/a/@href').extract():
            i += 1
            yield scrapy.Request(sub_category_url, callback=self.parse_list)
            log.msg('小类：'+sub_category_url,level=log.WARNING)
    def parse_list(self, response):

        try:
            # with MongoClient(MONGODB_URL) as client:
            i = 0
            for site in response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[2]/div/ul/li/div[2]'):
                item = AizhanDetailedItem()
                item['alexa_rank'] = site.xpath('div/span[1]/text()').extract_first()
                item['page_rank'] = site.xpath('div/span[2]/a/text()').extract_first()
                item['baidu_rank'] = site.xpath('div/span[3]/text()').extract_first()
                item['task_url'] = site.xpath('h2/a/@href').extract_first()

                yield item
                i += 1
            log.msg('网站：' + str(i), level=log.WARNING)
        except Exception as e:
            print(e)

        # next_page = response.css('body > div.wlist > div > div:nth-child(3) > div.fl > div.page > ul > li.on + li >a::attr(href)').extract_first()
        # if next_page:
        #     next_page = 'https://top.aizhan.com'+next_page
        #     yield scrapy.Request(next_page,callback=self.parse_list)

