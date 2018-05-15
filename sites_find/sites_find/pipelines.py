# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from datetime import datetime

class SitesFindPipeline(object):
    def __init__(self):
        setting = get_project_settings()
        self.MONGODB_URL = setting['MONGODB_URL']

    def open_spider(self, spider):
        self.client = MongoClient(self.MONGODB_URL)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'sitesFind':

            # 将发现的url存入sites_unverified集合
            sites_coll = self.client.site.sites_unverified
            for url in item['url']:
                data = {'url':url}
                try:
                    sites_coll.insert(data)
                except Exception as e:
                    print(e)

            #更新记录集合
            dt = datetime.now().strftime("%Y-%m-%d %H")
            self.client.site.num_log.update({'datetime':dt},{'$inc':{'sites_unverified_num':len(item['url'])}})
            self.client.site.num_log.update({'datetime':dt},{'$inc':{'sites_finding_num':-1}})


        return item
