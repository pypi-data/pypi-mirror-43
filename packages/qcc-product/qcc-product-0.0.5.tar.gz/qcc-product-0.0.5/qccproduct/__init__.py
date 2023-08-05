# coding=utf-8

import webmother
from webmother.service.passport import Passport

from qccproduct.db import mongo
from qccproduct import routes

# 在通证中增加对产品域的权限控制能力
Passport.add_profile('product', {
    'switches': [
        "create",
        "read",
        "update",
        "remove",
        "submit",
        "audit",
        "reject",
        "activate",
        "deactivate"
    ],
    'numbers': [
        "visible_level"  # 资源可见级别，越大表示可以看到status值更低的资源，取值范围为资源status取值范围，如0～40
    ],
})


def init(app):
    # 初始化webmother
    webmother.init(app)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
