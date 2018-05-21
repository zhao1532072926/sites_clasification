"""
统计每个分类下各关键词频率
author: Xinling
create-date: (5/21/18)
"""
from pymongo import MongoClient

MONGODB_URL = 'mongodb://root:19950113@10.245.146.249:27017/'

def category_keywords(goal_coll, meomory_db):
    # 初始化统计信息存储变量
    statistics_count = 0  # 本回合已统计site数，满100存储并重置变量
    statistics_data = {}  # 存储统计信息


    # 计算每个类别中每个关键词出现的次数
    for site in goal_coll.find({'info_flag':1}):
        if not 'labels' in site and 'category' in site and 'sub_category' in site:
            continue
        category = '{}.{}'.format(site['category'],site['sub_category'])
        if category not in statistics_data:
            statistics_data[category] = {}
        for keyword in site['labels']:
            keyword = keyword['keyword']
            if keyword not in statistics_data[category]:
                statistics_data[category][keyword] = 1
            else:
                statistics_data[category][keyword] += 1
        statistics_count += 1

        if statistics_count >= 100:
            for cg in statistics_data:
                for keyword in statistics_data[cg]:
                    meomory_db[cg].update({'keyword':keyword},{'$inc':{'count':statistics_data[cg][keyword]}}, upsert=True)

            statistics_count = 0
            statistics_data = {}


    # 计算每个分类keywords总数，以及每个keyword出现比例
    for cg_coll in meomory_db.collection_names():
        if cg_coll == 'sum_data':
            continue
        sum_keywords = 0
        for keyword_info in meomory_db[cg_coll].find():
            sum_keywords += keyword_info['count']

        meomory_db['sum_data'].update({'category':cg_coll},{'$set':{'sum_keywords_count':sum_keywords}},upsert=True)

        for keyword_info in meomory_db[cg_coll].find():
            proportion = keyword_info.count / sum_keywords
            meomory_db[cg_coll].update({'_id':keyword_info['_id']},{'$set':{'proportion':proportion}})


def main():
    client = MongoClient(MONGODB_URL)
    goal_coll = client.site.aizhan_sites
    memeory_db = client.statisitcs
    category_keywords(goal_coll,memeory_db)


if __name__ == '__main__':
    main()