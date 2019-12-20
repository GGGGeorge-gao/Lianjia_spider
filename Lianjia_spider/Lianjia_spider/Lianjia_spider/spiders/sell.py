"""
实现目标：
    1、从redis中读取售卖详情页URL
    2、获得ajaxURL并写入redis
"""
# -*- coding: utf-8 -*-
import scrapy
import redis
from scrapy.selector import Selector
from math import ceil
import re


class SellSpider(scrapy.Spider):
    name = 'sell'
    allowed_domains = ['https://hz.lianjia.com/']
    # start_urls = ['http://https://hz.lianjia.com//']
    base_url = 'https://hz.lianjia.com/api/newhouserecommend?type=2&id='

    def __init__(self):
        super(SellSpider, self).__init__()
        self.r_link = redis.Redis(port='6379', host='localhost', decode_responses=True, db=1)

    def start_requests(self):
        sell_url = '1'

        # 遍历Redis中所有sell_url
        while sell_url:
            sell_url = self.r_link.rpop("Lianjia:resblockSellUrl")
            print("===sell_url被弹出{}===".format(sell_url))
            yield scrapy.Request(
                url=sell_url,
                callback=self.parse2,
            )

    def parse2(self, response):
        sort_selector = Selector(response=response)
        sort_pattern = '//div[@class="leftContent"]/ul[@class="sellListContent"]/li/a/@href'
        sellUrl = sort_selector.xpath(sort_pattern).extract()

        for url in sellUrl:
            id = re.findall(r'\d+', url)
            if id:
                ajax_url = self.base_url + id[0]
                self.r_link.rpush("Lianjia:sellAjax", ajax_url)
                print("===ajax_url存储成功{}===".format(ajax_url))

        page_pattern = '//h2[@class="total fl"]/span/text()'
        page = ceil(int(sort_selector.xpath(page_pattern).extract_first().strip(' ')) / 30)
        for i in range(2, page + 1):
            yield scrapy.Request(
                url=response.url + 'pg' + str(i),
                callback=self.parse3,
            )

    def parse3(self, response):
        sort_selector = Selector(response=response)
        sort_pattern = '//div[@class="leftContent"]/ul[@class="sellListContent"]/li/a/@href'
        sellUrl = sort_selector.xpath(sort_pattern).extract()
        for url in sellUrl:
            id = re.findall(r'\d+', url)
            if id:
                ajax_url = self.base_url + id[0]
                self.r_link.rpush("Lianjia:sellAjax", ajax_url)
                print("===ajax_url存储成功{}===".format(ajax_url))



