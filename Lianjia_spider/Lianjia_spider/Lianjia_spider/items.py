# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaResblockItem(scrapy.Item):
    '''小区数据item'''

    infoType = scrapy.Field()
    resblockID = scrapy.Field()
    name = scrapy.Field()
    buildYear = scrapy.Field()
    buildType = scrapy.Field()
    unitPrice = scrapy.Field()
    sellNum = scrapy.Field()
    rentNum = scrapy.Field()
    rentUrl = scrapy.Field()
    sellUrl = scrapy.Field()
    viewUrl = scrapy.Field()
    pass


class LianjiaSoldInfoItem(scrapy.Item):
    '''已售出数据item'''

    infoType = scrapy.Field()
    houseCode = scrapy.Field()
    titleString = scrapy.Field()
    signPrice = scrapy.Field()
    listPrice = scrapy.Field()
    dealCycle = scrapy.Field()
    signTime = scrapy.Field()
    houseAreaNum = scrapy.Field()
    unitPrice = scrapy.Field()
    resblockName = scrapy.Field()
    year = scrapy.Field()
    buildingType = scrapy.Field()
    framePicUrl = scrapy.Field()
    elevator = scrapy.Field()
    isGarage = scrapy.Field()
    frameOrientation = scrapy.Field()
    decorationType = scrapy.Field()
    districtName = scrapy.Field()
    bizcircleName = scrapy.Field()
    districtId = scrapy.Field()
    subwayInfo = scrapy.Field()
    schoolInfo = scrapy.Field()
    floorInfo = scrapy.Field()
    pass


class LianjiaSellInfoItem(scrapy.Item):
    '''售卖中数据item'''

    infoType = scrapy.Field()
    houseCode = scrapy.Field()
    title = scrapy.Field()
    layoutImgSrc = scrapy.Field()
    roomNum = scrapy.Field()
    buildingArea = scrapy.Field()
    buildYear = scrapy.Field()
    ctime = scrapy.Field()
    orientation = scrapy.Field()
    totalFloor = scrapy.Field()
    decorateType = scrapy.Field()
    hbtName = scrapy.Field()
    isGarage = scrapy.Field()
    address = scrapy.Field()
    communityName = scrapy.Field()
    communityId = scrapy.Field()
    districtName = scrapy.Field()
    districtId = scrapy.Field()
    regionName = scrapy.Field()
    subwayInfo = scrapy.Field()
    schoolName = scrapy.Field()
    price = scrapy.Field()
    unitPrice = scrapy.Field()
    pass


class ResblockSellInfoItem(scrapy.Item):
    '''正在售卖楼盘数据item'''

    infoType = scrapy.Field()
    houseCode = scrapy.Field()
    title = scrapy.Field()
    buildYear = scrapy.Field()
    address = scrapy.Field()
    unitPrice = scrapy.Field()
    tagsInfo = scrapy.Field()
    districtName = scrapy.Field()
    priceConfirmTime = scrapy.Field()
    houseType = scrapy.Field()
    decoration = scrapy.Field()
    resblockName = scrapy.Field()
    buildingAmount = scrapy.Field()
    houseAmount = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    totalPriceMin = scrapy.Field()
    carRatio = scrapy.Field()
    overgroundCarNum = scrapy.Field()
    undergroundCarNum = scrapy.Field()
    virescenceRate = scrapy.Field()
    cubageRate = scrapy.Field()
