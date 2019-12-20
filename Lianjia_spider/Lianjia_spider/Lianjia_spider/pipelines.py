"""
管道文件实现目标：
    1、判断item类型
    2、构建sql语句并写入MySQL数据库
"""
import pymysql
from scrapy.exceptions import DropItem


class LianjiaSpiderPipeline(object):
    def __init__(self):
        self.mysql_conn = pymysql.Connection(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='lianjia',
            charset='utf8',
        )

        # 集合去重
        self.id_resblock = set()
        self.id_sell = set()
        self.id_sold = set()
        self.id_resblockInfo = set()

    def process_item(self, item, spider):
        # 判断传入Item对象的类型
        if item['infoType'] == 'resblock':
            if item['resblockID'] in self.id_resblock:
                raise DropItem("Resblock {} exists!".format(item['resblockID']))
            else:
                self.id_resblock.add(item['resblockID'])
                item.pop('infoType')
                cs = self.mysql_conn.cursor()

                # 构造sql语句
                sql_columns = ','.join([key for key in item.keys()])
                sql_values = ','.join(['"%s"' % item[key] for key in item.keys()])
                sql_str = 'insert into resblockInfo ({}) value ({});'.format(sql_columns, sql_values)

                # 判断MySQL是否含有该条数据
                try:
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===resblock写入MySQL成功===")
                except:
                    # 若MySQL中已存在则将其覆盖
                    print("===resblock数据已存在{}===".format(item['resblockID']))
                    sql_middle = ','.join([key + ' = "%s"' % item[key] for key in item.keys()])
                    sql_str = 'update resblockInfo set ' + sql_middle + 'where resblockID = "' + item['resblockID'] + '";'
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===resblockInfo重写MySQL成功===")

        # 原理如上
        elif item['infoType'] == 'sold':
            if item['houseCode'] in self.id_sold:
                raise DropItem("Sold {} exists!".format(item['houseCode']))
            else:
                self.id_sold.add(item['houseCode'])
                item.pop('infoType')
                cs = self.mysql_conn.cursor()

                # 构造sql语句
                sql_columns = ','.join([key for key in item.keys()])
                sql_values = ','.join(['"%s"' % item[key] for key in item.keys()])
                sql_str = 'insert into soldInfo ({}) value ({});'.format(sql_columns, sql_values)
                print(sql_str)

                try:
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===soldInfo写入MySQL成功===")
                except:
                    print("===soldInfo数据已存在{}===".format(item['houseCode']))
                    sql_middle = ','.join([key + ' = "%s"' % item[key] for key in item.keys()])
                    sql_str = 'update soldInfo set ' + sql_middle + 'where houseCode = "' + item['houseCode'] + '";'
                    print("修改soldInfo插入语句为{}".format(sql_str))
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===soldInfo重写MySQL成功===")

        elif item['infoType'] == 'sell':
            if item['houseCode'] in self.id_sell:
                raise DropItem("Sell {} exists!".format(item['houseCode']))
            else:
                self.id_sell.add(item['houseCode'])
                item.pop('infoType')
                cs = self.mysql_conn.cursor()
                sql_columns = ','.join([key for key in item.keys()])
                sql_values = ','.join(['"%s"' % item[key] for key in item.keys()])
                sql_str = 'insert into sellInfo ({}) value ({});'.format(sql_columns, sql_values)
                try:
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===sellInfo写入MySQL成功===")
                except:
                    print("===sellInfo数据已存在{}===".format(item['houseCode']))
                    sql_middle = ','.join([key + ' = "%s"' % item[key] for key in item.keys()])
                    sql_str = 'update sellInfo set ' + sql_middle + 'where houseCode = "' + item['houseCode'] + '";'
                    print("修改sellInfo插入语句为{}".format(sql_str))
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===sellInfo重写MySQL成功===")

        elif item['infoType'] == 'resblockSell':
            if item['houseCode'] in self.id_resblockInfo:
                raise DropItem("Resblock sell {} exists!".format(item['houseCode']))
            else:
                self.id_resblockInfo.add(item['houseCode'])
                item.pop('infoType')
                cs = self.mysql_conn.cursor()
                sql_columns = ','.join([key for key in item.keys()])
                sql_values = ','.join(['"%s"' % item[key] for key in item.keys()])
                sql_str = 'insert into resblocksell ({}) value ({});'.format(sql_columns, sql_values)
                print(sql_str)
                try:
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===resblocksell写入MySQL成功===")
                except:
                    print("===resblocksell数据已存在{}===".format(item['houseCode']))
                    sql_middle = ','.join([key + ' = "%s"' % item[key] for key in item.keys()])
                    sql_str = 'update resblocksell set ' + sql_middle + 'where houseCode = "' + item['houseCode'] + '";'
                    print("修改resblocksell插入语句为{}".format(sql_str))
                    cs.execute(sql_str)
                    self.mysql_conn.commit()
                    print("===resblocksell重写入MySQL成功===")

        else:
            raise DropItem("No used item found{}!".format(item))

        return item
