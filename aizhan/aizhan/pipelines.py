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
            coll = self.client.site.aizhan_sites
            coll.insert(data)

        elif spider.name == 'aizhanSitesInfo':
            aizhan_sites_coll = self.client.site.detailed_aizhan_sites
            data = {key: item[key] for key in item}
            data['info_flag'] = 1
            aizhan_sites_coll.update({'_id':item['_id']},{'$set':data},upsert=True)

        elif spider.name == 'aizhanSeoInfo':
            sites_coll = self.client.site.detailed_aizhan_sites
            data = {key:item[key] for key in item}
            id = data.pop('_id')
            data['seo_flag'] = 1
            sites_coll.update_one(filter={'_id':id},update={'$set':data})

        elif spider.name == 'aizhan_sites_detailed_manager':
            data = {key: item[key] for key in item}
            data['gettime'] = datetime.now()
            coll = self.client.site.detailed_aizhan_sites_fpage
            coll.insert(data)

        elif spider.name == 'aizhan_sites_detailed_worker':
            data = {key: item[key] for key in item}
            data['gettime'] = datetime.now()
            id = data.pop('_id')
            data['aizhan_info_flag'] = 1
            coll = self.client.site.detailed_aizhan_sites
            coll.update_one({'_id':id},update={'$set':data})

        return item
