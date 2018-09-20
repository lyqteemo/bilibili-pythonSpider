# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import requests
import pymysql
from scrapy.utils.project import get_project_settings


class BilibiliPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host=get_project_settings().get('MYSQL_HOST'),
                                       db=get_project_settings().get('MYSQL_DBNAME'),
                                       user=get_project_settings().get('MYSQL_USER'),
                                       passwd=get_project_settings().get('MYSQL_PASSWD'),
                                       port=3306,
                                       charset='utf8',
                                       use_unicode=True)

    def process_item(self, item, spider):
        try:
            cur = self.connect.cursor()
            cur.execute("insert into anime(title,url,follow,play,score) value (%s, %s, %s, %s, %s)",
                        (item['title'], item['url'], item['follow'], item['play'], item['score']))
            self.connect.commit()
        except Exception as error:
            print(error)

        image_url = item["imgLink"]
        #response = requests.get(image_url)
        # print(response.content)

        # with open(item['title'].strip() + '.jpg', 'wb') as f:
        # f.write(response.content)
        return item
