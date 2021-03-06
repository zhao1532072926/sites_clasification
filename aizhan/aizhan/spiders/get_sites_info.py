import re
import heapq
import jieba
from jieba import analyse, posseg
from pymongo import MongoClient
import scrapy
from scrapy.utils.project import get_project_settings
from datetime import datetime


class aizhanSitesInfoSpider(scrapy.Spider):

    def __init__(self):
        setting = get_project_settings()
        self.MONGODB_URL = setting['MONGODB_URL']

    name = "aizhanSitesInfo"

    # start_urls = ['http://www.ahedu.cn',]

    def start_requests(self):
        with MongoClient(self.MONGODB_URL) as client:
            aizhan_sites_coll = client.site.detailed_aizhan_sites
            site = aizhan_sites_coll.find_one_and_update({'info_flag':None},update={'$set':{'info_flag':0}})

            while site:
                url = 'http://' + site['url']
                request = scrapy.Request(url,callback=self.parse)
                request.meta['_id'] = site['_id']
                yield request
                site = aizhan_sites_coll.find_one_and_update({'info_flag':None},update={'$set':{'info_flag':0}})

    @staticmethod
    def get_keywords(response, sites_info, n=10, tf_idf=True):
        """
        提取网站关键词。
        如果存在keywords标签或description标签，则用标签内容提取关键词
        否则用网站全文提取关键词。
        :param response: scrapy Response对象，用于全文提取关键词
        :param sites_info: 网站信息
        :param tf_idf: 当keywords或description存在时，是否采用tf-idf算法提取关键词，True为采用，False为根据词频
        :return: labels-提取到的关键词
        """
        info = []
        for key in ['real_title','real_keywrds','real_description']:
            if key in sites_info and sites_info[key]:
                info.append(sites_info[key])
        if not tf_idf and 'keywords' in sites_info:  #如果存在keywords标签或description标签，则用标签内容提取关键词
            cut_results = posseg.cut(';'.join(info))
            keywords_count = {}
            for key in cut_results:
                if key.flag.find('n') < 0:
                    continue
                key = key.word
                if key in keywords_count:
                    keywords_count[key] += 1
                else:
                    keywords_count[key] = 1
            keywords = heapq.nlargest(n,[{'keyword':x,'count':keywords_count[x]} for x in keywords_count], key=lambda x:x['count'])
            return keywords

        if info:  #如果存在keywords标签或description标签，则用标签内容提取关键词
            keywords = jieba.analyse.extract_tags(';'.join(info), topK=n, withWeight=True, allowPOS=['n'])

        else:
            body = response.xpath('/html/body')
            if not body:
                return []
            body_text = body[0].xpath('string(.)').extract_first()
            keywords = jieba.analyse.extract_tags(body_text, topK=n, withWeight=True)
        labels = []
        for x in keywords:
            labels.append({'keyword':x[0],'rank':x[1]})
        return labels




    def parse(self, response):
        from aizhan.items import AizhanDetailedItem

        item = AizhanDetailedItem()
        item['_id'] = response.meta['_id']
        item['url'] = response.url.split('/')[2]


        title = response.xpath('/html/head/title/text()').extract_first()
        item['real_title'] = title.strip() if title else None
        head= response.xpath('/html/head').extract_first()
        if head:
            keywords_element = re.findall(re.compile("""<meta[^<>]*?['"]keywords['"][^<>]*?>""",re.I),head)
            if keywords_element and re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),keywords_element[0]):
                item['real_keywords'] = re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),keywords_element[0])[0]
            description_element = re.findall(re.compile("""<meta[^<>]*?name=.description[^<>]*?>""",re.I),head)
            if description_element and re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),description_element[0]):
                item['real_description'] = re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),description_element[0])[0]
        labels = aizhanSitesInfoSpider.get_keywords(response,item)
        if labels:
            item['labels'] = labels

        # labels_tf = aizhanSitesInfoSpider.get_keywords(response, item, tf_idf=False)
        # if labels_tf:
        #     item['labels_tf'] = labels_tf

        yield item











