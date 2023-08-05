# coding:utf-8

from tweb.license import License
import config

identity_cfg = {

    # 发证机构代码
    'authority': 'org',

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
        "member_create",  # 20
        "member_read",
        "member_update",
        "member_remove",
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
        "NA"
    ]
}


class Identity(License):
    def __init__(self, text=None):
        super(Identity, self).__init__(text, identity_cfg)
