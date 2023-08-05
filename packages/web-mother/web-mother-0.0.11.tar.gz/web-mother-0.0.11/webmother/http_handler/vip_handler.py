# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
from webmother.service.async_wrap import ctrl_vip


class VipHandler(base_handler.BaseHandler):
    """
    获取我的组织列表
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, oid, vip_oid, level):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_vip.vip_create(oid, vip_oid, level, {}, identity, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, oid, vip_oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_vip.vip_remove(oid, vip_oid, identity, access_token)
        return self.write(ret)


class VipsHandler(base_handler.BaseHandler):
    """
    查询组织创建的VIP组列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid):
        identity = self.request.headers.get('x-signed-identity')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_vip.vip_query(oid, identity, access_token)
        return self.write({'list': array})
