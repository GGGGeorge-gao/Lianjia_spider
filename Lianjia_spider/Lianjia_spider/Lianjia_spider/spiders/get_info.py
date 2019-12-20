"""
实现目标：
    1、获取redis数据库中的ajax_rul
    2、解析ajax并从中获取小区、售卖中、已售卖的数据
    3、创建item并传入管道文件
    4、将ajax中的小区售卖中、已售卖详情页URL写入redis
"""
# -*- coding: utf-8 -*-
from ..items import LianjiaResblockItem, LianjiaSoldInfoItem, LianjiaSellInfoItem
import scrapy
import redis
import json
import random


class GetInfoSpider(scrapy.Spider):
    name = 'get_info'
    allowed_domains = ['http://hz.lianjia.com/']
    # start_urls = ['http://http://hz.lianjia.com/']

    # 连接Redis数据库
    r_link = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

    def start_requests(self):
        '''从redis获得ajax信息的url'''
        ajax_url = '1'
        while ajax_url:
            ajax_url = self.r_link.rpop("Lianjia:ajax_url").replace('#', '', 3)
            print("---{}被弹出---".format(ajax_url))
            yield scrapy.Request(
                url=ajax_url,
                callback=self.parse1,
            )

    def parse1(self, response):
        '''获取ajax内的关键信息'''
        response = json.loads(response.text)

        # 根据json中不同类型的数据创建Item对象
        resblock_info = response['data']['resblock']
        item_resblock = LianjiaResblockItem()
        item_resblock['resblockID'] = random.sample(response['data']['soldList'], 1)[0]['resblockID']
        item_resblock['name'] = resblock_info['name']
        item_resblock['buildYear'] = resblock_info['buildYear']
        item_resblock['buildType'] = resblock_info['buildType']
        item_resblock['unitPrice'] = resblock_info['unitPrice']
        item_resblock['sellNum'] = resblock_info['sellNum']
        item_resblock['rentNum'] = resblock_info['rentNum']
        item_resblock['rentUrl'] = resblock_info['rentUrl']
        item_resblock['sellUrl'] = resblock_info['sellUrl']
        item_resblock['viewUrl'] = resblock_info['viewUrl']
        item_resblock['infoType'] = 'resblock'
        yield item_resblock

        sold_info = response['data']['soldList']
        item_sold = LianjiaSoldInfoItem()
        for house_sold in sold_info:
            item_sold['houseCode'] = house_sold['houseCode']
            item_sold['titleString'] = house_sold['titleString']
            item_sold['signPrice'] = house_sold['signPrice']
            item_sold['listPrice'] = house_sold['listPrice']
            item_sold['dealCycle'] = house_sold['dealCycle']
            item_sold['signTime'] = house_sold['signTime']
            item_sold['houseAreaNum'] = house_sold['houseAreaNum']
            item_sold['unitPrice'] = house_sold['unitPrice']
            item_sold['resblockName'] = house_sold['resblockName']
            item_sold['year'] = house_sold['year']
            item_sold['buildingType'] = house_sold['buildingType']
            item_sold['framePicUrl'] = house_sold['framePicUrl']
            item_sold['elevator'] = house_sold['elevator']
            item_sold['isGarage'] = house_sold['isGarage']
            item_sold['frameOrientation'] = house_sold['frameOrientation']
            item_sold['decorationType'] = house_sold['decorationType']
            item_sold['districtName'] = house_sold['districtName']
            item_sold['bizcircleName'] = house_sold['bizcircleName']
            item_sold['districtId'] = house_sold['districtId']
            item_sold['subwayInfo'] = house_sold['subwayInfoString']
            item_sold['schoolInfo'] = house_sold['schoolInfoString']
            item_sold['floorInfo'] = house_sold['floorInfo']
            item_sold['infoType'] = 'sold'
            yield item_sold

        sell_info = response['data']['sellList']
        item_sell = LianjiaSellInfoItem()
        for house_sell in sell_info.values():
            item_sell['houseCode'] = house_sell['houseCode']
            item_sell['title'] = house_sell['title']
            item_sell['layoutImgSrc'] = house_sell['layoutImgSrc']
            item_sell['roomNum'] = house_sell['roomNum']
            item_sell['buildingArea'] = house_sell['buildingArea']
            item_sell['buildYear'] = house_sell['buildYear']
            item_sell['ctime'] = house_sell['ctime']
            item_sell['orientation'] = house_sell['orientation']
            item_sell['totalFloor'] = house_sell['totalFloor']
            item_sell['decorateType'] = house_sell['decorateType']
            item_sell['hbtName'] = house_sell['hbtName']
            item_sell['isGarage'] = house_sell['isGarage']
            item_sell['address'] = house_sell['address']
            item_sell['communityName'] = house_sell['communityName']
            item_sell['communityId'] = house_sell['communityId']
            item_sell['districtName'] = house_sell['districtName']
            item_sell['districtId'] = house_sell['districtId']
            item_sell['regionName'] = house_sell['regionName']
            item_sell['subwayInfo'] = house_sell['subwayInfo']
            item_sell['schoolName'] = house_sell['schoolName']
            item_sell['price'] = house_sell['price']
            item_sell['unitPrice'] = house_sell['unitPrice']
            item_sell['infoType'] = 'sell'
            yield item_sell

        resblockSoldUrl = self.allowed_domains[0][:-1] + response['data']['resblockSoldUrl']
        resblockSellUrl = self.allowed_domains[0][:-1] + response['data']['resblockSellUrl']
        self.r_link.rpush("Lianjia:resblockSoldUrl", resblockSoldUrl)
        self.r_link.rpush("Lianjia:resblockSellUrl", resblockSellUrl)
