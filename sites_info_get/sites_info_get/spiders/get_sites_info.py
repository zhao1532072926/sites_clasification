import re
import heapq
import jieba
from jieba import analyse
from pymongo import MongoClient
import scrapy
from scrapy.utils.project import get_project_settings
from datetime import datetime


class siteInfoSpider(scrapy.Spider):

    def __init__(self):
        setting = get_project_settings()
        self.MONGODB_URL = setting['MONGODB_URL']

    name = "sitesInfo"


    def start_requests(self):
        with MongoClient(self.MONGODB_URL) as client:
            sites_unverified_coll = client.site.aizhan_sites1
            sites = sites_unverified_coll.find({})

            for site in sites:
                url = 'http://' + site['url']
                request = scrapy.Request(url,callback=self.parse)
                yield request
    # def start_requests(self):
    #     with MongoClient(self.MONGODB_URL) as client:
    #         sites_unverified_coll = client.site.sites_unverified
    #         sites = sites_unverified_coll.find_one_and_delete({})
    #
    #         while sites:
    #             # cursor.execute(update_sql,(result['id']))
    #             # 更新记录集合
    #             dt = datetime.now().strftime("%Y-%m-%d %H")
    #             client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_unverified_num': -1}}, upsert=True)
    #             client.site.num_log.update({'datetime': dt}, {'$inc': {'sites_verifing_num': 1}}, upsert=True)
    #
    #             url = 'http://' + sites['url']
    #             request = scrapy.Request(url,callback=self.parse)
    #             yield request
    #             sites = sites_unverified_coll.find_one_and_delete({})

    def get_keywords(self,response, sites_info):
        """
        提取网站关键词。
        如果存在keywords标签或description标签，则用标签内容提取关键词
        否则用网站全文提取关键词。
        :param response: scrapy Response对象，用于全文提取关键词
        :param sites_info: 网站信息
        :return: labels-提取到的关键词
        """
        info = []
        for key in ['keywrds','description']:
            if key in sites_info:
                info.append(sites_info[key])
        if info:  #如果存在keywords标签或description标签，则用标签内容提取关键词
            keywords = jieba.analyse.extract_tags(';'.join(info), topK=20, withWeight=True, allowPOS=['n'])
        else:
            body = response.xpath('/html/body')[0]
            body_text = body.xpath('string(.)').extract_first()
            keywords = jieba.analyse.extract_tags(body_text, topK=20, withWeight=True)
        labels = []
        for x in keywords:
            labels.append({'keyword':x[0],'rank':x[1]})
        return labels

    def get_keywords_only_tf(self,response, sites_info,n=10):
        """
        提取网站关键词。
        如果存在keywords标签或description标签，则用标签内容提取关键词(词频)
        否则用网站全文提取关键词。
        :param response: scrapy Response对象，用于全文提取关键词
        :param sites_info: 网站信息
        :return: labels-提取到的关键词
        """
        info = []
        for key in ['keywrds','description']:
            if key in sites_info:
                info.append(sites_info[key])
        if info:  #如果存在keywords标签或description标签，则用标签内容提取关键词
            keywords = {}
            results = jieba.cut(';'.join(info))
            for key in results:
                if key in keywords:
                    keywords[key] += 1
                else:
                    keywords[key] = 1
            keywords = heapq.nlargest(n, [{'key':x,'count':results[x]} for x in results], key=lambda x:x['count'])
        else:
            body = response.xpath('/html/body')[0]
            body_text = body.xpath('string(.)').extract_first()
            keywords = jieba.analyse.extract_tags(body_text, topK=n, withWeight=True)
        labels = []
        for x in keywords:
            labels.append({'keyword':x[0],'rank':x[1]})
        return labels



    def parse(self, response):
        from sites_info_get.items import SitesInfoGetItem
        try:
            item = SitesInfoGetItem()
            item['url'] = response.url.split('/')[2]


            title = response.xpath('/html/head/title/text()').extract_first()
            item['title'] = title.strip() if title else None
            head= response.xpath('/html/head').extract_first()
            keywords_element = re.findall(re.compile("""<meta[^<>]*?['"]keywords['"][^<>]*?>""",re.I),head)
            if keywords_element:
                item['keywords'] = re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),keywords_element[0])[0]
            description_element = re.findall(re.compile("""<meta[^<>]*?name=.description[^<>]*?>""",re.I),head)
            if description_element:
                item['description'] = re.findall(re.compile("""<meta[^<>]*?content="(.*?)"[^<>]*?>""",re.I),description_element[0])[0]
            labels = self.get_keywords(response,item)
            if labels:
                item['labels'] = labels
            # request = scrapy.Request('https://www.aizhan.com/cha/{site}'.format(site=item['url']),callback=self.parse_final)
            # request.meta['item'] = item
            yield item
        except Exception as e:
            print(e)











