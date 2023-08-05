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
        "status_level"  # 可以查询节点和元素的最低状态值：-10：已逻辑删除，0：编辑中，10：待审中，20：休眠中，30：激活中
    ],
})


def init(app):
    # 初始化webmother
    webmother.init(app)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    app.load_routes(routes)
