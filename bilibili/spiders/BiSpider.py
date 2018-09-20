# -*- coding: utf-8 -*-
import scrapy
from bilibili.items import BiliItem
import json
import jsonpath


class BispiderSpider(scrapy.Spider):
    name = 'Bili'
    allowed_domains = ['bilibili.com']
    pageNum = 1
    url = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&season_type=1&pagesize=20&page='

    start_urls = [url + str(pageNum)]

    def parse(self, response):
        item = BiliItem()
        jsonobj = json.loads(response.body)
        jsonlist = jsonpath.jsonpath(jsonobj, '$.result.data[:]')
        # print(jsonlist)
        for dic in jsonlist:
            item['imgLink'] = dic['cover']
            item['title'] = dic['title']
            item['url'] = dic['link']
            item['follow'] = dic['order']['follow']
            item['play'] = dic['order'].get('play', '即将开播')
            item['score'] = dic['order'].get('score', '即将开播')
            yield item

        if self.pageNum <= 51:
            self.pageNum += 1
            yield scrapy.Request(self.url + str(self.pageNum), callback=self.parse, dont_filter=True,)
