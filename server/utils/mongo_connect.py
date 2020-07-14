# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

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


if __name__ == "__main__":
    print(school_club_data_coll.find({})[0])
    print([
        item
        for item in school_club_data_coll.aggregate([{
            "$group": {
                "_id": "$school_data.school_info.school_name",
                "count": {
                    "$sum": 1
                }
            }
        }]
    )])
