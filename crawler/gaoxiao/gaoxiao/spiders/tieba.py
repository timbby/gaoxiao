import datetime
import json
import csv

import scrapy
from urllib.parse import quote

from pymongo import MongoClient

mongo_client = MongoClient('mongodb://admin:123456@localhost:27017', **{
    "serverSelectionTimeoutMS": 1 * 1000,  # 初次建立连接的时候, 默认连接时长, 如果 mongo挂了 这里就是最大连接时长, ms为单位
    "connectTimeoutMS": 10 * 1000,  # 心跳检测中,最长响应时间
    "socketTimeoutMS": 10 * 1000,  # 已经建立了的连接, 执行一次查询最大等候时间
    "maxPoolSize": 100,
    "minPoolSize": 0,
    "waitQueueMultiple": 10,
    "connect": False,
    "maxIdleTimeMS": 30 * 1000
})

db_name = 'school_info'
db = getattr(mongo_client, db_name)
db.authenticate('test', '123456')

school_club_data_coll = getattr(db, 'school_club_data')


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    school_list = csv.DictReader(open("../全国普通高等学校名单.csv", 'r'))

    school_map = {
        f"https://tieba.baidu.com/f?ie=utf-8&kw={quote(school_info['school_name'])}&fr=search": dict(school_info)
        for school_info in school_list
    }

    start_urls = list(school_map.keys())

    def parse(self, response):
        club_name = response.css(".card_title .card_title_fname::text")[0].get().strip()
        school_info = self.school_map.get(response.url)
        school_data = dict()
        school_data['school_info'] = school_info
        school_data['club_name'] = club_name
        school_data['club_url'] = response.url
        for article_selector in response.css(".j_thread_list.clearfix"):
            article_info = json.loads(article_selector.attrib['data-field'])

            article_info['school_data'] = school_data
            title = article_selector.css(".threadlist_title .j_th_tit::text")[0].get()
            article_info['title'] = title
            content = article_selector.css(".threadlist_text .threadlist_abs.threadlist_abs_onlyline::text")
            if content:
                article_info['content'] = content[0].get().strip()
            article_info['last_crawler_time'] = int(datetime.datetime.now().timestamp() * 1000)
            article_id = article_info['id']

            school_club_data_coll.update({'article_id': article_id}, {"$set": article_info}, upsert=True)
