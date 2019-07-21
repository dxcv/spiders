# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class SzSpidersbdxyPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="47.94.199.114", user="hdg", passwd="1234456", db="basedata", port=3306,
                                    charset="utf8")
        self.cursor = self.conn.cursor()

    def getCompanyName(self):
        sql = 'select com_name from `basedata`.`ori_company_list` where uscc is null order by rand() limit 1'
        self.cursor.execute(sql)
        cnames = self.cursor.fetchall()
        rs = []
        for item in cnames:
            rs.append(item[0])

        return rs
    def process_item(self, item, spider):
        sql = 'update `ori_company_list` set `uscc`= "%s", operate_user=user() where com_name = "%s"' % (item['uscc'], item['cname'])
        try:
            #3 执行sql
            self.cursor.execute(sql)
            #4 提交事务
            self.conn.commit()
            # print(11111111111111111,item['cname'])
        except Exception as e:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        # 在该方法中完成对数据库的关闭
        self.cursor.close()
        self.conn.close()
