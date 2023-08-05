# coding:utf-8

from tweb.license import License
import config


class Identity(License):
    profiles = {
        'org': {
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
        },
        'member': {
            'switches': [
                "create",
                "read",
                "update",
                "remove"
            ]
        }
    }

    def __init__(self):
        super(Identity, self).__init__(profiles=self.profiles,
                                       authority=config.DOMAIN,
                                       secret=config.TornadoSettings['cookie_secret'])
