"""
详细版爱站网爬虫
author: Xinling
create-date: (5/27/18)
"""
import os
import scrapy
import logging
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from aizhan.items import AizhanDetailedItem


MONGODB_URL = get_project_settings()['MONGODB_URL']

class siteSpider(scrapy.Spider):
    name = "aizhan_sites_detailed"

    start_urls = ['http://top.aizhan.com',]
    # start_urls = ['https://top.aizhan.com/top/t2-34/',]

    def parse(self, response):
        for category_url in response.xpath('/html/body/div[3]/div/div[2]/ul/li/a/@href').extract():
            yield scrapy.Request(category_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        for sub_category_url in response.xpath('/html/body/div[3]/div/div[3]/div[2]/div[1]/div[1]/ul/li/a/@href').extract():
            yield scrapy.Request(sub_category_url, callback=self.parse_list)

    def parse_list(self, response):

        try:
            with MongoClient(MONGODB_URL) as client:
                for site in response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[2]/div/ul/li/div[2]'):
                    site_url = site.xpath('//h2/a/@href').extract_first()
                    if client.site.new_aizhan_sites.find_one({'url':site_url}):
                        continue
                    rank = {}
                    rank['alexa_rank'] = site.xpath('//div/span[1]/text()').extract_first()
                    rank['page_rank'] = site.xpath('//div/span[2]/a/text()').extract_first()
                    rank['baidu_rank'] = site.xpath('//div/span[3]/text()').extract_first()

                    request = scrapy.Request(site_url, callback=self.parse_data)
                    request.meta['rank'] = rank
                    yield request
        except Exception as e:
            print(e)

        next_page = response.css('body > div.wlist > div > div:nth-child(3) > div.fl > div.page > ul > li.on + li >a::attr(href)').extract_first()
        if next_page:
            next_page = 'https://top.aizhan.com'+next_page
            yield scrapy.Request(next_page,callback=self.parse_list)

    def parse_data(self, response):
        item = AizhanDetailedItem()
        item['title'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/h1/text()').extract_first()
        item['alias'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[1]/span/text()').extract_first()
        item['url'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[2]/span/text()').extract_first()
        item['category'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[3]/span/a/text()').extract()
        item['area'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/ul/li[4]/span/a/text()').extract_first()
        item['keywords'] = response.xpath('//*[@id="keyword"]/text()').extract_first()
        item['description'] = response.xpath('//*[@id="description"]/text()').extract_first()
        item['detailed_description'] = '\n'.join(response.xpath('/html/body/div[3]/div/div[4]/div[2]/div[1]/div/p/text()').extract())
        item['score'] = response.xpath('/html/body/div[3]/div/div[2]/div[2]/div/dl[1]/dd/text()').extract_first()
        item['alexa_rank'] = response.meta['rank']['alexa_rank']
        item['page_rank'] = response.meta['rank']['page_rank']
        item['baidu_rank'] = response.meta['rank']['baidu_rank']

        yield item