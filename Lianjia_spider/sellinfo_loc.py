"""
实现目标：
    1、调用百度地图api修改MySQL数据库中sellinfo该table里的经纬度信息
"""
import pymysql
from baidu_map import getlnglat
import time

data_s = []
db = pymysql.Connection(host="localhost", port=3306, user="root", password="", database="lianjia", charset="utf8")
cursor = db.cursor()
sql = "select * from sellinfo;"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    for data in results:
        if float(data[-2]) < 118.2 or float(data[-2]) > 120.5 or float(data[-1]) < 29.0 or float(data[-1]) > 30.5:
            address = '杭州' + data[15] + '区' + data[13]
            print(address + data[-2] + '  ' + data[-1])
            houseCode = data[0]
            lng = data[-2]
            lat = data[-1]
            data_s.append(dict(
                houseCode=houseCode,
                address=address,
                lng=lng,
                lat=lat,
            ))
except:
    print("出错了！")

for data in data_s:
    loc = getlnglat(data['address'])

    if loc:
        sql_middle = ','.join([key + ' = "%s"' % loc[key] for key in loc.keys()])
        sql_str = 'update sellinfo set ' + sql_middle + 'where houseCode = "' + data['houseCode'] + '";'
        cursor.execute(sql_str)
        db.commit()
        print(data['address'])
        print(sql_str)
        print("===存储成功！===")
    else:
        sql_middle = 'longitude = "-1",latitude = "-1"'
        sql_str = 'update sellinfo set ' + sql_middle + 'where houseCode = "' + data['houseCode'] + '";'
        cursor.execute(sql_str)
        db.commit()
        print(sql_str)
        print("！！！未找到位置信息！!!")
    time.sleep(0.15)

db.close()
