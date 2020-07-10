# -*- coding:utf-8 -*-
__author__ = 'liuxiaotong'

from views import app

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(8848),
        threaded=True,
        debug=True
    )
