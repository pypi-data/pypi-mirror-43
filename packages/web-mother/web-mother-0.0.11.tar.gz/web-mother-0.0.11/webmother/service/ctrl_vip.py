# coding:utf-8

from webmother.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service.identity import Identity
from webmother.service import ctrl_org


def vip_create(oid, vip_oid, level, identity_json, *auth_args):
    """
    在组织下创建客户VIP组，用以管理客户。
    客户可以自主加入最低级VIP组，然后客户升级，即从低级别组中移动到高级别VIP组中，由应用系统根据一定的策略进行升级移动
    :param oid: 申请创建VIP的组织
    :param vip_oid: 将用来容纳VIP客户的组织，注意必须是oid的子组织
    :param level: VIP组的级别，取值0～100，只有level为0的VIP组才支持客户自主加入
    :param identity_json: VIP客户在组织内的权限定义
    :param auth_args: 操作者的鉴权信息
    :return:
    """
    o = ctrl_org.read(oid, *auth_args)
    vip_o = ctrl_org.read(vip_oid, *auth_args)

    # 接收开放会员的组织必须是当前组织的子组织
    if vip_o['node'].find(o['node']) != 0 or vip_o['node'] == o['node']:
        raise ErrException(ERROR.E40000, extra='vip org must be child of %s' % o['node'])

    # 授权检查, 用户必须有该组织和VIP组织的"member.create"权限
    idt = Identity().verify(*auth_args)
    idt.operable(o.get('node'), 'member.create')
    idt.operable(vip_o.get('node'), 'member.create')
    # END

    if db.vip.find_one({'app_org': ObjectId(oid), 'vip_org': ObjectId(vip_oid)}) is not None:
        raise ErrException(ERROR.E40020)

    if db.vip.find_one({'app_org': ObjectId(oid), 'level': level}) is not None:
        raise ErrException(ERROR.E40020, extra='existed about the VIP of level %s' % level)

    now = time.millisecond()
    vip = {
        'app_org': ObjectId(oid),
        'vip_org': ObjectId(vip_oid),
        'level': int(level),
        'identity': Identity().update(vip_o['node'], None, identity_json, idt).text,
        'created': now,
        'updated': now
    }
    result = db.vip.insert_one(vip)
    obj = db.vip.find_one(result.inserted_id, {'_id': 0})
    obj['app_org'] = obj['app_org'].__str__()
    obj['vip_org'] = obj['vip_org'].__str__()
    return obj


def vip_remove(oid, vip_oid, *auth_args):
    o = ctrl_org.read(oid, *auth_args)
    vip_o = ctrl_org.read(vip_oid, *auth_args)

    # 授权检查, 用户必须有该组织和VIP组织的"member.create"权限
    idt = Identity().verify(*auth_args)
    idt.operable(o.get('node'), 'member.remove')
    idt.operable(vip_o.get('node'), 'member.remove')
    # END

    db.vip.delete_one({'app_org': ObjectId(oid), 'vip_org': ObjectId(vip_oid)})

    return {}


def vip_query(oid, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查, 用户必须有该组织和VIP组织的"member.create"权限
    idt = Identity().verify(*auth_args)
    idt.operable(o.get('node'), 'member.read')
    # END

    cursor = db.vip.find({'app_org': ObjectId(oid)}, {'_id': 0, 'app_org': 0})
    array = list()
    for item in cursor:
        item['vip_org'] = ctrl_org.simple_read(item['vip_org'])
        array.append(item)

    return array
