"""
初始化布隆过滤器
author: Xinling
create-date: (4/25/18)
"""
import os
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from pybloom_live import BloomFilter

def bloom_file_init():
    path = '../spiders/sites.blm'
    is_exist = os.path.exists(path)
    # 判断是否存在bloom文件
    # 判断存在就读取
    if is_exist:
        bf = BloomFilter.fromfile(open(path, 'rb'))
    # 没有该文件则创建bf对象 最后的时候保存文件
    else:
        bf = BloomFilter(10000000, 0.01)

    with MongoClient(get_project_settings()['MONGODB_URL']) as client:
        sites_coll = client.site.sites
        sites_unverified_coll = client.site.sites_unverified
        for x in sites_coll.find():
            result = bf.add(x['url'])
            print(x['url'],' ',result)
        for x in sites_unverified_coll.find({}):
            result = bf.add(x['url'])
            print(x['url'], ' ', result)

    bf.tofile(open(path, 'wb'))


if __name__ == '__main__':
    # bloom_file_init()
    print(os.path.dirname(__file__)   )
