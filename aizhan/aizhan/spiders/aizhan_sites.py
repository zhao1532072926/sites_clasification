"""

author: Xinling
create-date: (5/2/18)
"""

import os
import scrapy
import logging
from aizhan.items import AizhanItem



class siteSpider(scrapy.Spider):
    name = "aizhan_sites"
    # start_urls = [
    #     "https://top.aizhan.com/top/t3-15/",
    #     "https://top.aizhan.com/top/t3-429/",
    #     "https://top.aizhan.com/top/t3-5/",
    #     "https://top.aizhan.com/top/t3-21/",
    #     "https://top.aizhan.com/top/t3-7/",
    #     "https://top.aizhan.com/top/t1-16/",
    #     "https://top.aizhan.com/top/t3-11/",
    #     "https://top.aizhan.com/top/t3-17/",
    #     "https://top.aizhan.com/top/t3-487/",
    #     "https://top.aizhan.com/top/t3-23/",
    #     "https://top.aizhan.com/top/t3-241/",
    #     "https://top.aizhan.com/top/t3-13/",
    #     "https://top.aizhan.com/top/t27-483/",
    #     "https://top.aizhan.com/top/t3-239/",
    #     "https://top.aizhan.com/top/t3-19/",
    #     "https://top.aizhan.com/top/t1-26/",
    #     "https://top.aizhan.com/top/t1-27/",
    #     "https://top.aizhan.com/top/t25-43/",
    #     "https://top.aizhan.com/top/t25-45/",
    #     "https://top.aizhan.com/top/t25-265/",
    #     "https://top.aizhan.com/top/t3-249/",
    #     "https://top.aizhan.com/top/t2-32/",
    #     "https://top.aizhan.com/top/t25-65/",
    #     "https://top.aizhan.com/top/t2-34/",
    #     "https://top.aizhan.com/top/t27-77/",
    #     "https://top.aizhan.com/top/t25-57/",
    #     "https://top.aizhan.com/top/t25-47/",
    #     "https://top.aizhan.com/top/t25-53/",
    #     "https://top.aizhan.com/top/t25-51/",
    #     "https://top.aizhan.com/top/t25-259/",
    #     "https://top.aizhan.com/top/t25-257/",
    #     "https://top.aizhan.com/top/t25-63/",
    #     "https://top.aizhan.com/top/t25-59/",
    #     "https://top.aizhan.com/top/t27-451/",
    #     "https://top.aizhan.com/top/t27-85/",
    #     "https://top.aizhan.com/top/t3-423/",
    #     "https://top.aizhan.com/top/t2-116/",
    #     "https://top.aizhan.com/top/t33/",
    #     "https://top.aizhan.com/top/t27-95/",
    #     "https://top.aizhan.com/top/t3-48/",
    #     "https://top.aizhan.com/top/t3-49/",
    #     "https://top.aizhan.com/top/t27-75/",
    #     "https://top.aizhan.com/top/t25-439/",
    #     "https://top.aizhan.com/top/t3-115/",
    #     "https://top.aizhan.com/top/t31-133/",
    #     "https://top.aizhan.com/top/t4-53/",
    #     "https://top.aizhan.com/top/t31-455/",
    #     "https://top.aizhan.com/top/t31-477/",
    #     "https://top.aizhan.com/top/t27-271/",
    #     "https://top.aizhan.com/top/t31-139/",
    #     "https://top.aizhan.com/top/t4-58/",
    #     "https://top.aizhan.com/top/t31-127/",
    #     "https://top.aizhan.com/top/t31-131/",
    #     "https://top.aizhan.com/top/t31-119/",
    #     "https://top.aizhan.com/top/t31-117/",
    #     "https://top.aizhan.com/top/t31-123/",
    #     "https://top.aizhan.com/top/t31-121/",
    #     "https://top.aizhan.com/top/t31-125/",
    #     "https://top.aizhan.com/top/t31-129/",
    #     "https://top.aizhan.com/top/t4-67/",
    #     "https://top.aizhan.com/top/t31-137/",
    #     "https://top.aizhan.com/top/t27-83/",
    #     "https://top.aizhan.com/top/t5-69/",
    #     "https://top.aizhan.com/top/t35-193/",
    #     "https://top.aizhan.com/top/t35-367/",
    #     "https://top.aizhan.com/top/t35-183/",
    #     "https://top.aizhan.com/top/t35-363/",
    #     "https://top.aizhan.com/top/t35-195/",
    #     "https://top.aizhan.com/top/t35-465/",
    #     "https://top.aizhan.com/top/t35-383/",
    #     "https://top.aizhan.com/top/t35-179/",
    #     "https://top.aizhan.com/top/t35-181/",
    #     "https://top.aizhan.com/top/t39-233/",
    #     "https://top.aizhan.com/top/t39-231/",
    #     "https://top.aizhan.com/top/t39-227/",
    #     "https://top.aizhan.com/top/t39-473/",
    #     "https://top.aizhan.com/top/t39-229/",
    #     "https://top.aizhan.com/top/t39-225/",
    #     "https://top.aizhan.com/top/t41-235/",
    #     "https://top.aizhan.com/top/t25-61/",
    #     "https://top.aizhan.com/top/t29-103/",
    #     "https://top.aizhan.com/top/t41-411/",
    #     "https://top.aizhan.com/top/t41-237/",
    #     "https://top.aizhan.com/top/t27-73/",
    #     "https://top.aizhan.com/top/t41-481/",
    #     "https://top.aizhan.com/top/t41-235/",
    #     "https://top.aizhan.com/top/t25-61/",
    #     "https://top.aizhan.com/top/t29-103/",
    #     "https://top.aizhan.com/top/t41-411/",
    #     "https://top.aizhan.com/top/t41-237/",
    #     "https://top.aizhan.com/top/t27-73/",
    #     "https://top.aizhan.com/top/t41-481/",
    #     "https://top.aizhan.com/top/t9-102/",
    #     "https://top.aizhan.com/top/t37-205/",
    #     "https://top.aizhan.com/top/t37-203/",
    #     "https://top.aizhan.com/top/t37-207/",
    #     "https://top.aizhan.com/top/t37-201/",
    #     "https://top.aizhan.com/top/t37-389/",
    #     "https://top.aizhan.com/top/t37-467/",
    #     "https://top.aizhan.com/top/t37-215/",
    #     "https://top.aizhan.com/top/t37-199/",
    #     "https://top.aizhan.com/top/t37-219/",
    #     "https://top.aizhan.com/top/t27-89/",
    #     "https://top.aizhan.com/top/t10-111/",
    #     "https://top.aizhan.com/top/t10-112/",
    #     "https://top.aizhan.com/top/t41-413/"
    #
    # ]
    start_urls = ['http://top.aizhan.com',]

    def parse(self, response):
        for category_url in response.xpath('/html/body/div[3]/div/div[2]/ul/li/a/@href').extract():
            yield scrapy.Request(category_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        for sub_category_url in response.xpath('/html/body/div[3]/div/div[3]/div[2]/div[1]/div[1]/ul/li/a/@href').extract():
            yield scrapy.Request(sub_category_url, callback=self.parse_data)

    def parse_data(self, response):

        try:
            sub_category = response.css(
                'body > div.wlist > div > div:nth-child(3) > div.fr > div.cate > div:nth-child(1) > ul > li.on > a::text').extract_first()
            category = response.css(
                'body > div.wlist > div > div:nth-child(3) > div.fr > div.cate > div:nth-child(2) > ul > li.on > a::text').extract_first()
            for site in response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[2]/div/ul/li/div[2]'):
                item = AizhanItem()
                item['url'] = site.xpath('h2/em/text()').extract_first()
                item['category'] = category
                item['sub_category'] = sub_category
                yield item
        except Exception as e:
            print(e)

        next_page = response.css('body > div.wlist > div > div:nth-child(3) > div.fl > div.page > ul > li.on + li >a::attr(href)').extract_first()
        if next_page:
            next_page = 'https://top.aizhan.com'+next_page
            yield scrapy.Request(next_page,callback=self.parse_data)


