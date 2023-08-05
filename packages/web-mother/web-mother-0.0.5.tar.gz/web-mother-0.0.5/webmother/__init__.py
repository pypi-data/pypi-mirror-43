# coding=utf-8

import ucenter
from ucenter.db import mongo as uc_mongo

from webmother.db import mongo
from webmother import routes


def init(app):

    # 初始化UCenter数据库
    uc_mongo.init()

    # 加载UCenter API路由
    app.load_routes(ucenter.routes)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
