
import os
import scrapy
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from pybloom_live import BloomFilter
from datetime import datetime
# from site_label.site_label.items import SitesItem

BLOOM_FILE = os.path.dirname(__file__) + '/sites.blm'

class siteFindSpider(scrapy.Spider):

    name = "sitesFind"

    def start_requests(self):
        setting = get_project_settings()
        MONGODB_URL = setting['MONGODB_URL']
        with MongoClient(MONGODB_URL) as client:
            sites_coll = client.site.sites
            url_data = sites_coll.find_and_modify(
                query={'flag_find':None},update={'$set':{'flag_find':1}})   # mongo中的null会匹配没有该字段的记录，传入None会转化为null

            while url_data:
                # 更新记录集合
                dt = datetime.now().strftime("%Y-%m-%d %H")
                client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_unfinded_num': -1}})
                client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_finding_num': 1}})

                url = 'http://' + url_data['url']
                yield scrapy.Request(url,callback=self.parse)

                url_data = sites_coll.find_and_modify(
                    query= {'flag_find': None}, update={'$set': {'flag_find': 1}})  # 为下一个循环提取任务



    def parse(self, response):
        from sites_find.items import SitesFindItem
        item  = SitesFindItem()  # 初始化项目对象
        urls_set = set()  # 用于去重的集合

        try:
            urls = response.xpath('//a/@href').extract()
            for url in urls:
                if url.find('http') == -1:  # 判断外链条件1：存在http子字符串
                    continue
                domain = url.split('/')[2]   # ‘http(s)://xxx.xx(/yy)’ -> ['http(s)','','xxx.xx'(,'yy')] -> 'xxx.xx'
                if domain != response._url.split('/')[2]:   # 判断外链条件2：网址不等于返回该response的网址
                    urls_set.add(domain)   #利用集合去重

            bf = BloomFilter.fromfile(open(BLOOM_FILE, 'rb'))
            item['url'] = []
            for url in urls_set:
                if bf.add(url):
                    continue
                item['url'].append(url)
            yield item
            bf.tofile(open(BLOOM_FILE,'wb'))
        except Exception as e:
            print(e)


