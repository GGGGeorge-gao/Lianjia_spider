"""
实现目标（首先执行）：
    1、遍历链家的搜索页中所有选项分类及筛选条件的所有页数URL
    2、获取详情页URL
    3、写入redis数据库中
"""
# -*- coding: utf-8 -*-
import scrapy
import redis
from scrapy.selector import Selector


class LianjiaSpider(scrapy.Spider):
    name = 'Lianjia'
    allowed_domains = ['hz.lianjia.com']
    # start_urls = ['https://hz.lianjia.com/chengjiao/']
    base_url = 'http://hz.lianjia.com/'

    def __init__(self):
        super(LianjiaSpider, self).__init__()
        # 启用Redis服务
        self.r_link = redis.Redis(port='6379', host='localhost', decode_responses=True, db=1)

    def start_requests(self):
        '''爬取搜索页所在URL'''
        print('start_requests LianjiaSpider1 GO!!!')

        url = self.base_url + 'chengjiao/'
        yield scrapy.Request(
            url=url,
            dont_filter=True,
            callback=self.parse1,
        )

    def parse1(self, response):
        '''遍历所有一级分类'''
        print("PARSE1 GO!!!")

        sort1_pattern = '//div[@data-role="ershoufang"]/div[1]/a/@href'
        sort1_selector = Selector(response=response)
        sort1_list = list(map(lambda a: self.base_url + a, sort1_selector.xpath(sort1_pattern).extract()))

        print("!!!FIXME:{}!!!".format(sort1_list))
        if len(sort1_list):
            for url in sort1_list:
                print("===PARSE1 ", url, " 开始遍历===")
                if url:
                    yield scrapy.Request(
                        url=url,
                        dont_filter=True,
                        callback=self.parse2
                    )

    def parse2(self, response):
        '''遍历所有二级分类'''
        print("PARSE2 GO!!!")

        sort2_pattern = '//div[@data-role="ershoufang"]/div[2]/a/@href'
        sort2_selector = Selector(response=response)
        sort2_list = list(map(lambda a: self.base_url + a, sort2_selector.xpath(sort2_pattern).extract()))

        if len(sort2_list):
            for url in sort2_list:
                print("===PARSE2 ", url, " 开始遍历===")
                yield scrapy.Request(
                    url=url,
                    dont_filter=True,
                    callback=self.parse3,
                )
        extra_url = self.r_link.rpop("Lianjia:resblockSoldUrl")
        print("===resblockSoldUrl提取成功{}===".format(extra_url))
        while extra_url:
            print("===Extra soldUrl ", extra_url, " 被提取===")
            yield scrapy.Request(
                url=extra_url,
                dont_filter=True,
                callback=self.parse3,
            )
            extra_url = self.r_link.rpop("Lianjia:resblockSoldUrl")

    def parse3(self, response):
        print('PARSE3 GO!!!')

        # 遍历每一页
        for page in range(1, 100):
            url = response.url + 'pg{}'.format(page)
            print("===PARSE3 ", url, " 开始遍历===")
            yield scrapy.Request(
                url=url,
                callback=self.parse4,
                meta={'empty': False}
            )

    def parse4(self, response):

        print("PARSE4　GO！！！")
        selector = Selector(response=response)

        li = selector.re(r'<ul class="listContent">(.*?)</ul>')

        '''遍历所有页数，判断li标签是否存在'''
        if not li:
            # 通过XPath获取详情页url信息
            url_pattern = r'//div[@class="content"]/div[1]/ul[@class="listContent"]/li/a/@href'
            url_list = selector.xpath(url_pattern).extract()

            print("======Redis连接信息：Host:{}  Port:{}======".format(self.settings.get('REDIS_HOST'),
                                                                  self.settings.get('REDIS_PORT')))

            # 将URL信息写入Redis数据库
            print('PARSE1 开始写入')
            for u in url_list:
                print("准备写入{}".format(u))
                self.r_link.rpush("Lianjia:detail_url", u)
                print("{}写入成功!".format(u))

            print('=' * 30, '\n', "共计写入url：{}个".format(len(url_list)), '\n', '=' * 30)
        elif li[0] != '':
            # 通过XPath获取详情页url信息
            url_pattern = r'//div[@class="content"]/div[1]/ul[@class="listContent"]/li/a/@href'
            url_list = selector.xpath(url_pattern).extract()

            # 启用Redis服务
            r_link = redis.Redis(port=self.settings.get('REDIS_PORT'), host=self.settings.get('REDIS_HOST'),
                                 decode_responses=True, db=1)
            print("======Redis连接信息：Host:{}  Port:{}======".format(self.settings.get('REDIS_HOST'),
                                                                  self.settings.get('REDIS_PORT')))

            # 将URL信息写入Redis数据库
            print('PARSE4 开始写入')
            for u in url_list:
                print("准备写入{}".format(u))
                r_link.rpush("Lianjia:detail_url", u)
                print("{}写入成功!".format(u))

            print('=' * 30, '\n', "共计写入url：{}个".format(len(url_list)), '\n', '=' * 30)
        elif li[0] == '':
            pass

    # def parse(self, response):
    #     response.m
