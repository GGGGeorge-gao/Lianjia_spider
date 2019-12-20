"""
实现目标：
    1、调用百度地图api修改MySQL数据库中soldinfo该table的经纬度信息
"""
import pymysql
from baidu_map import getlnglat
import time


data_s = []
db = pymysql.Connection(host="localhost", port=3306, user="root", password="", database="lianjia", charset="utf8")
cursor = db.cursor()
# 构造提取sql表内所有数据的语句
sql = "select * from soldinfo;"
try:
    # 建立光标对象
    cursor.execute(sql)
    results = cursor.fetchall()
    print(len(results))
    for data in results:
        # 判断经纬度是否异常
        if float(data[-2]) < 118.0 or float(data[-2]) > 120.5 or float(data[-1]) < 29.0 or float(data[-1]) > 30.5:
            address = '杭州' + data[16] + '区' + data[8]
            print(data[-2] + ' ' + data[-1])
            houseCode = data[0]
            # 若经纬度异常则加入列表
            data_s.append(dict(
                houseCode=houseCode,
                address=address
            ))
except:
    print("出错了！")

# 遍历所有经纬度异常的数据
for data in data_s:
    print(data['address'])
    loc = getlnglat(data['address'])
    if loc:
        sql_middle = ','.join([key + ' = "%s"' % loc[key] for key in loc.keys()])
        sql_str = 'update soldinfo set ' + sql_middle + 'where houseCode = "' + data['houseCode'] + '";'

        cursor.execute(sql_str)
        db.commit()
        print(sql_str)
        print("===存储成功！===")
    else:
        sql_middle = 'longitude = "-1",latitude = "-1"'
        sql_str = 'update soldinfo set ' + sql_middle + 'where houseCode = "' + data['houseCode'] + '";'

        cursor.execute(sql_str)
        db.commit()
        print(sql_str)
        print("！！！未找到位置信息！!!")
    time.sleep(0.15)

db.close()
