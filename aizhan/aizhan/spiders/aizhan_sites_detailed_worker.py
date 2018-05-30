"""
详细版爱站网爬虫
author: Xinling
create-date: (5/27/18)
"""
import os
import scrapy
import logging
from scrapy import log
import pymongo
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from aizhan.items import AizhanDetailedItem



MONGODB_URL = get_project_settings()['MONGODB_URL']

class siteSpider(scrapy.Spider):
    name = "aizhan_sites_detailed_worker"

    def start_requests(self):
        with MongoClient(MONGODB_URL) as client:
            task = client.site.detailed_aizhan_sites.find_one_and_update({'aizhan_info_flag': None},
                                                                         {"$set": {'aizhan_info_flag': 0}})
            while task:
                request = scrapy.Request(task['task_url'], callback=self.parse)
                request.meta['_id'] = task['_id']
                yield request
                task = client.site.detailed_aizhan_sites.find_one_and_update({'aizhan_info_flag': None},
                                                                             {"$set": {'aizhan_info_flag': 0}})


    def parse(self, response):
        item = AizhanDetailedItem()
        item['_id'] = response.meta['_id']
        item['title'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/h1/text()').extract_first()
        item['alias'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[1]/span/text()').extract_first()
        item['url'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[2]/span/text()').extract_first()
        item['category'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[3]/span/a/text()').extract()
        item['area'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[4]/span/a/text()').extract_first()
        item['keywords'] = response.xpath('//*[@id="keyword"]/text()').extract_first()
        item['description'] = response.xpath('//*[@id="description"]/text()').extract_first()
        item['detailed_description'] = ''.join(
            response.xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/p/text()').extract())
        item['score'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div/dl[1]/dd/text()').extract_first()

        yield item