"""
实现目标：
    1、通过redis数据库得到Lianjia.py爬取到的详情页URL
    2、从详情页中获取ajax_url中的关键组成参数
    3、存入redis数据库
"""
# -*- coding: utf-8 -*-
import scrapy
import redis
from scrapy.selector import Selector


class GetAjaxUrlSpider(scrapy.Spider):
    name = 'get_ajax_url'
    allowed_domains = ['hz.lianjia.com']
    # start_urls = ['http://hz.lianjia.com/']
    base_url = r'https://hz.lianjia.com/chengjiao/resblock?'

    # 连接Redis数据库
    r_link = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

    def start_requests(self):
        '''从Redis获得详情页url'''
        detail_url = self.r_link.rpop("Lianjia:detail_url")
        while detail_url:
            print("{}被弹出！".format(detail_url))
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse1,
            )
            detail_url = self.r_link.rpop("Lianjia:detail_url")

    def parse1(self, response):
        '''获取ajax的url关键参数 hid & rid '''

        hid_pattern = '//div[@class="transaction"]/div/ul/li[1]/text()'
        rid_pattern = '//section[@class="wrapper"]/div[1]/a[5]/@href'

        selector = Selector(response=response)
        hid = selector.xpath(hid_pattern).extract_first().strip()
        rid = selector.xpath(rid_pattern).extract_first().strip()
        rid = ''.join(list(filter(str.isdigit, rid)))

        ajax_url = self.base_url + "hid={}&rid={}".format(hid, rid)

        self.r_link.rpush('Lianjia:ajax_url', ajax_url)
        print('=' * 40)
        print(ajax_url, "存储成功！")
        print('=' * 40)
