"""
实现目标：
    1、调用百度地图api修改MySQL数据库中resblockinfo该table的经纬度信息
"""
import pymysql
from baidu_map import getlnglat
import time

data_s = []
db = pymysql.Connection(host="localhost", port=3306, user="root", password="", database="lianjia", charset="utf8")
cursor = db.cursor()
sql = "select * from resblockinfo;"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    for data in results:
        if data[-1] == '-1':
            address = '杭州' + data[1]
            resblockID = data[0]
            data_s.append(dict(
                resblockID=resblockID,
                address=address
            ))
except:
    print("出错了！")

for data in data_s:
    print(data['address'])
    loc = getlnglat(data['address'])
    if loc:
        sql_middle = ','.join([key + ' = "%s"' % loc[key] for key in loc.keys()])
        sql_str = 'update resblockinfo set ' + sql_middle + 'where resblockID = "' + data['resblockID'] + '";'
        cursor.execute(sql_str)
        db.commit()
        print(sql_str)
        print("===存储成功！===")
    else:
        sql_middle = 'longitude = "-1",latitude = "-1"'
        sql_str = 'update resblockinfo set ' + sql_middle + 'where resblockID = "' + data['resblockID'] + '";'
        cursor.execute(sql_str)
        db.commit()
        print(sql_str)
        print("！！！未找到位置信息！!!")
    time.sleep(0.15)

db.close()
