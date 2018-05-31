"""
获取指定网站信息
author: Xinling
create-date: (5/27/18)
"""

import re
import requests
import jieba
from jieba import analyse
import chardet
from verification import category
from pymongo import MongoClient

MONGODB_URL = 'mongodb://root:19950113@10.245.146.249:27017/'

def get_keywords(text, sites_info):
    """
    提取网站关键词。
    如果存在keywords标签或description标签，则用标签内容提取关键词
    否则用网站全文提取关键词。
    :param text: 网站html全文
    :param sites_info: 网站信息
    :return: labels-提取到的关键词
    """
    info = []
    for key in ['keywrds', 'description']:
        if key in sites_info:
            info.append(sites_info[key])
    if info:  # 如果存在keywords标签或description标签，则用标签内容提取关键词
        keywords = jieba.analyse.extract_tags(';'.join(info), topK=20, withWeight=True, allowPOS=['n'])
    else:
        keywords = jieba.analyse.extract_tags(text, topK=20, withWeight=True, allowPOS=['n'])
    labels = []
    for x in keywords:
        labels.append({'keyword': x[0], 'rank': x[1]})
    return labels

def get_site_info(url):
    headers = {'user_agent':'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'}
    r = requests.get('http://'+url,headers=headers)
    text  = r.content.decode(chardet.detect(r.content)['encoding'])
    x = r.content.decode('utf-8')
    site_info = {'url':url}
    site_info['title'] = re.findall(re.compile("""<title>([^<>]*?)</title>"""),text)[0]

    # 因为不能确定标签关键词大小写所以用re.I(忽略大小写模式);因为不能确定标签关键词和content的顺序所以要先找到标签，再提取content
    keywords_element = re.findall(re.compile("""<meta[^<>]*?['"]keywords['"][^<>]*?>""", re.I), text)
    if keywords_element:
        site_info['keywords'] = re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""", re.I), keywords_element[0])[
            0]
    description_element = re.findall(re.compile("""<meta[^<>]*?name=.description[^<>]*?>""", re.I), text)
    if description_element:
        site_info['description'] = \
        re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""", re.I), description_element[0])[0]

    site_info['labels'] = get_keywords(text, site_info)

    return site_info

if __name__ == '__main__':
    for url in ['v.qq.com','www.iqiyi.com']:

        site_info = get_site_info(url)
        print(site_info)
        with MongoClient(MONGODB_URL) as client:
            keyword_category_coll = client.keyword_category_proportion.keyword_category_proportion
            print(category(site_info['labels'],keyword_category_coll))
        # print(client.site.detailed_aizhan_sites.find_one({'url': url})['category'])