# coding:utf-8

from tweb.license import License
import config


class Passport(License):
    profiles = {
        'catalog': {
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
        'grant': {
            'switches': [
                "create",
                "read",
                "update",
                "remove"
            ]
        }
    }

    def __init__(self):
        super(Passport, self).__init__(profiles=self.profiles,
                                       authority=config.PLATFORM,
                                       secret=config.TornadoSettings['cookie_secret'])

    @staticmethod
    def add_profile(domain, profile):
        """
        :param domain:
        :param profile: 示例如下

        'catalog': {
            'switches': [
                "sample_sw1",  # 0
                "sample_sw2"
            ],

            # 共6个数值域可用
            'numbers': [
                "sample_num1",
                "sample_num2"
            ],

            # 共4个范围域可用
            'ranges': [
                "sample_range1",
                "sample_range2"
            ]
        }
        :return:
        """
        if domain in Passport.profiles:
            raise ErrException(ERROR.E50000, extra='duplicated about license profile: %s' % domain)

        Passport.profiles[domain] = profile
