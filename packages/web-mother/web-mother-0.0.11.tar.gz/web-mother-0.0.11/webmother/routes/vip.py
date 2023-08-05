# coding=utf-8

import config
from webmother.http_handler import vip_handler as h

base = '{}/{}/vip'.format(config.VER, config.PLATFORM)
routes = [
    # 添加/删除会员组
    (rf"/{base}/apporg/([a-f0-9]*)/viporg/([a-f0-9]*)/level/([0-9]*)", h.VipHandler),

    # 查询发布应用的组织创建的VIP组列表
    (rf"/{base}/apporg/([a-f0-9]*)/list", h.VipsHandler),
]
