"""
根据统计对网站进行分类
author: Xinling
create-date: (5/26/18)
"""

import logging
from pymongo import MongoClient

MONGODB_URL = 'mongodb://root:19950113@10.245.146.249:27017/'

def category(keywrods,coll):
    """
    根据传入的关键词及权重对网站分类（rule）
    :param keywrods: [(keyword,rank)]
    :param coll:
    :return:
    """
    category = {}
    for keywrod in keywrods:
        keyword_category_info = coll.find_one({'keyword':keywrod['keyword']})
        if not keyword_category_info:
            continue
        for category_info in keyword_category_info['category_proportion']:
            if category_info['category'] not in category:
                category[category_info['category']] = category_info['category_proportion']*keywrod['rank']
            else:
                category[category_info['category']] += category_info['category_proportion'] * keywrod['rank']
    max = {'category':None,'proportion':-1}
    for x in category:
        if category[x] > max['proportion']:
            max = {'category':x, 'proportion':category[x]}
    return max['category']


def verification():
    """
    对比aizhan_sites中的数据进行验证分类准确率
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    formatt = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatt)
    logger.addHandler(console)

    with MongoClient(MONGODB_URL) as client:
        keyword_category_coll = client.keyword_category_proportion.keyword_category_proportion
        i,pass_count,loss_count = [0] * 3
        for sites in client.site.aizhan_sites.find({'info_flag':1}):
            if 'labels' not in sites or 'category' not in sites or 'sub_category' not in sites:
                continue
            i += 1
            right_category = '{}.{}'.format(sites['category'],sites['sub_category'])
            calculate_category = category(sites['labels'],keyword_category_coll)
            if right_category == calculate_category:
                pass_count += 1
            else:
                loss_count += 1
            logger.info('第{}个网站，类别：{}；计算类别{}；正确网站数：{}；错误网站数{};当前正确率：{:.2%};网站：{}'.format(i,right_category,calculate_category,pass_count,loss_count,pass_count/i,sites['title']))

if __name__ == '__main__':
    verification()