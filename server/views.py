# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

from flask import Flask, request

app = Flask(__name__)


@app.route(f'/hello/world', methods=['POST'])
def store_data():
    req = request.json
    print(req)
    return 'hello world'
