# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from datetime import datetime

class AizhanPipeline(object):
    def __init__(self):
        setting = get_project_settings()
        self.MONGODB_URL = setting['MONGODB_URL']

    def open_spider(self, spider):
        self.client = MongoClient(self.MONGODB_URL)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'aizhan_sites':
            data = {key:item[key] for key in item}
            data['gettime'] = datetime.now()
            coll = self.client.site.aizhan_sites2
            coll.insert(data)

        if spider.name == 'aizhanSitesInfo':
            # sites_coll = self.client.site.sites
            # data = {key:item[key] for key in item}
            # try:
            #     sites_coll.insert(data)
            #     # 更新记录集合
            #     dt = datetime.now().strftime("%Y-%m-%d %H")
            #     self.client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_verified_num': 1}}, upsert=True)
            #     self.client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_verifing_num': -1}}, upsert=True)
            # except Exception as e:
            #     data['err'] = str(e)
            #     self.site.err.insert(data)
            aizhan_sites_coll = self.client.site.aizhan_sites
            keys = ['url','keywords','description','title','labels']
            data = {key: item[key] for key in item}
            aizhan_sites_coll.update({'url':data['url']},{'$set':data},upsert=True)


        return item
