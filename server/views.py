# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

from flask import Flask, request, render_template

from utils.mongo_connect import school_club_data_coll

app = Flask(__name__)


@app.route(f'/hello/world', methods=['POST'])
def store_data():
    req = request.json
    print(req)
    return 'hello world'


@app.route(f'/school', methods=['GET'])
def school_list():
    school_data_list = school_club_data_coll.aggregate([{
            "$group": {
                "_id": "$school_data.school_info.school_name",
                "count": {
                    "$sum": 1
                }
            }
        }]
    )
    school_data_list = [
        [item['_id'], item['count']]
        for item in school_data_list
    ]
    print(school_data_list)
    return render_template('word_cloud.html', school_name='', word_cloud_data=school_data_list)


@app.route(f'/school/<school_name>', methods=['GET'])
def school_word_cloud(school_name):
    article_list = school_club_data_coll.find({'school_data.school_info.school_name': school_name}, {'seg_list': 1})
    article_list = [item for item in article_list]
    word_cloud_data = dict()
    for article in article_list:
        for word in article.get('seg_list', []):
            word_cloud_data[word] = word_cloud_data.get(word, 0) + 1

    word_cloud_list = list(word_cloud_data.items())
    word_cloud_list = [
        item
        for item in word_cloud_list
        if item[1] > 1 and len(item[0]) > 1
    ]
    return render_template('word_cloud.html', school_name=school_name, word_cloud_data=word_cloud_list)
