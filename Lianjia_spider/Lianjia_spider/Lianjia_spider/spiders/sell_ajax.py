"""
实现目标：
    1、从redis获取售卖信息的URL
    2、创建item对象并传入管道文件
"""
# -*- coding: utf-8 -*-
import scrapy
import redis
from ..items import ResblockSellInfoItem
import json


class SellAjaxSpider(scrapy.Spider):
    name = 'sell_ajax'
    allowed_domains = ['https://hz.lianjia.com/']

    # start_urls = ['http://https://hz.lianjia.com//']

    def __init__(self):
        super(SellAjaxSpider, self).__init__()
        self.r_link = redis.Redis(port='6379', host='localhost', decode_responses=True, db=1)

    def start_requests(self):
        url = '1'
        while url:
            url = self.r_link.rpop("Lianjia:sellAjax")
            print('---{}被弹出---'.format(url))
            yield scrapy.Request(
                url=url,
                callback=self.parse1,
            )

    def parse1(self, response):
        '''获取ajax里的关键信息'''
        response = json.loads(response.text)['data']

        # 创建Item对象并传入管道文件
        for data in response:
            item = ResblockSellInfoItem()
            item['infoType'] = 'resblockSell'
            item['houseCode'] = data['id']
            item['title'] = data['build_name']
            item['buildYear'] = data['open_time']
            item['address'] = data['store_addr']
            item['unitPrice'] = data['price']
            item['tagsInfo'] = data['tags']
            item['districtName'] = data['district_name']
            item['priceConfirmTime'] = data['price_confirm_time'].split(' ')[0]
            item['houseType'] = data['house_type']
            item['decoration'] = data['decoration']
            item['resblockName'] = data['resblock_name']
            item['buildingAmount'] = data['building_count']
            item['houseAmount'] = data['house_amount']
            item['longitude'] = data['longitude']
            item['latitude'] = data['latitude']
            item['totalPriceMin'] = data['total_price_min']
            item['carRatio'] = data['carRatio'][2:]
            item['overgroundCarNum'] = data['overground_car_num']
            item['undergroundCarNum'] = data['underground_car_num']
            item['virescenceRate'] = data['virescence_rate']
            item['cubageRate'] = data['cubage_rate']
            yield item
