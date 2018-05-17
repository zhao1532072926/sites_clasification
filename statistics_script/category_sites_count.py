"""
统计每个分类网站的总数
author: Xinling
create-date: (5/16/18)
"""

from pymongo import MongoClient

def categorys_sites_count(goal_coll,memory_coll):
    """
    对指定网站数据集合（带有分类数据），统计各个分类网站数量
    :param mongo_coll: 统计目标的 mongodb集合的header
    :param memory_coll: 存储统计数据的 mongodb集合的header
    :return: 无
    """

    categorys_counts = {'category_info_err_sites':0}
    for site in goal_coll.find():
        if not ('category'in site and 'sub_category' in site):
            categorys_counts['category_info_err_sites'] += 1
        elif site['category'] in categorys_counts:
            categorys_counts[site['category']]['count'] += 1
            if site['sub_category'] in categorys_counts[site['category']]:
                categorys_counts[site['category']][site['sub_category']] += 1
            else:
                categorys_counts[site['category']][site['sub_category']] = 1
        else:
            categorys_counts[site['category']] = {'count':1}
            categorys_counts[site['category']][site['sub_category']] = 1

    category_info_err_sites = categorys_counts.pop('category_info_err_sites')
    memory_coll.insert({'category_info_err_sites': category_info_err_sites} if category_info_err_sites>0 else {})
    for category in categorys_counts:
        info_dealed = {
            'category':category,
            'count':categorys_counts[category].pop('count'),
            'sub_category':[{'sub_category':x,'count':categorys_counts[category][x]} for x in categorys_counts[category]]
        }
        memory_coll.insert(info_dealed)

    return None


def aizhan_categorys_sites_count():
    """
    爱站网信息（aizhan_sites）统计
    :return:
    """
    MONGODB_URL = 'mongodb://root:19950113@10.245.146.249:27017/'
    client = MongoClient(MONGODB_URL)
    goal_coll = client.site.aizhan_sites
    memory_coll = client.site.aizhan_category_count
    categorys_sites_count(goal_coll, memory_coll)

if __name__ == "__main__":
    aizhan_categorys_sites_count()
