"""
    该demo无任何意义，仅供测试使用
"""
import pymysql

houseCode_s = set()
db = pymysql.Connection(host="localhost", port=3306, user="root", password="", database="lianjia", charset="utf8")
cursor = db.cursor()
sql = "select * from resblocksell;"

cursor.execute(sql)
results = cursor.fetchall()
print(len(results))
for data in results:
    if data[0] in houseCode_s:
        sql_columns = ','.join([key for key in item.keys()])
        sql_values = ','.join(['"%s"' % item[key] for key in item.keys()])
        sql_str = 'insert into resblocksell ({}) value ({});'.format(sql_columns, sql_values)
else:
        houseCode_s.add(data[0])


