"""
获取网站的seo信息
author: Xinling
create-date: (4/25/18)
"""

import scrapy
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

class seoInfoSpider(scrapy.Spider):

    name = 'aizhanSeoInfo'

    def __init__(self):
        setting = get_project_settings()
        self.MONGODB_URL = setting['MONGODB_URL']

    def start_requests(self):
        with MongoClient(self.MONGODB_URL) as client:
            sites_coll = client.site.aizhan_sites
            site = sites_coll.find_one_and_update({'seo_flag':None},update={'$set':{'seo_flag':0}})

            while site:
                # cursor.execute(update_sql,(result['id']))
                url = 'https://www.aizhan.com/cha/' + site['url'] + '/'
                request = scrapy.Request(url,callback=self.parse)
                request.meta['id'] = site['_id']
                yield request
                site = sites_coll.find_one_and_update({'seo_flag': None}, update={'$set': {'seo_flag': 0}})

    def parse(self, response):
        from aizhan.items import AizhanItem
        item = AizhanItem()
        item['id'] = response.meta['id']

        baidurank = response.xpath('//*[@id="baidurank_br"]/img/@alt').extract_first()
        if baidurank:
            item['baidurank'] = baidurank

        pagerank= response.xpath('//*[@id="google_pr"]/img/@alt').extract_first()
        if pagerank:
            item['pagerank'] = pagerank

        alexa_ranking = response.xpath('//*[@id="alexa_rank"]/text()').extract_first()
        if alexa_ranking:
            item['alexa_ranking'] = alexa_ranking

        yield item