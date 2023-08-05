# coding:utf-8

from tweb.license import License
import config


passport_cfg = {

    # 发证机构代码
    'authority': 'catalog',

    # 发证机构代签名密码
    'secret': config.TornadoSettings['cookie_secret'],

    # 共40个开关可用
    'switches': [
        "create",  # 0
        "read",
        "update",
        "remove",
        "submit",
        "audit",
        "reject",
        "activate",
        "deactivate",
        "NA",
        "NA",  # 10
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "passport_create",  # 20
        "passport_read",
        "passport_update",
        "passport_remove",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",  # 30
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "element_create",  # 40
        "element_read",
        "element_update",
        "element_remove",
        "element_submit",
        "element_audit",
        "element_reject",
        "element_activate",
        "element_deactivate",
        "NA",
        "NA",  # 50
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",  # 60
        "NA",
        "NA",
        "NA"
    ],

    # 共10个数值域可用
    'numbers': [
        "status_level",  # 可以查询节点和元素的最低状态值：-10：已逻辑删除，0：编辑中，10：待审中，20：休眠中，30：激活中
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA",
        "NA"
    ]
}


class Passport(License):

    def __init__(self, text=None):
        super(Passport, self).__init__(text, passport_cfg)
