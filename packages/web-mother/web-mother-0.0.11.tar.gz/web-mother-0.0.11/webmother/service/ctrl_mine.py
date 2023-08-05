# coding:utf-8

from webmother.db import mongo as db
from bson.objectid import ObjectId
from webmother.service.identity import Identity
from webmother.service import ctrl_org
from tweb.error_exception import ErrException, ERROR
from bson.errors import InvalidId
from ucenter.services import ctrl_user
from tweb import time


def my_identities(appid, uid, access_token, member_type=0):
    """
    获取我的身份（组织）列表
    :param appid: 应用ID，其值就是某个org的组织ID
    :param uid:
    :param access_token:
    :param member_type: 成员类型，0: 管理类；1：客户类；2：全部
    :return:
    """
    if appid is None:
        raise ErrException(ERROR.E40000, extra='no appid')
    try:
        ObjectId(appid)
    except InvalidId:
        raise ErrException(ERROR.E40000, extra='invalid appid')

    app_org = ctrl_org.simple_read(appid, raw=True)
    app_node = app_org['node']

    if member_type >= 2:
        cursor = db.org2user.find({'user.uid': ObjectId(uid)}, {'user': 0})
    else:
        cursor = db.org2user.find({'user.uid': ObjectId(uid), 'type': {'$eq': member_type}}, {'user': 0})
    array = list()
    for item in cursor:

        # 判断是否是appid标示的组织或者其子组织，也即用户只能查询appid组织限制的范围之内的身份认证
        org_node = item['org_node']
        if org_node.find(app_node) != 0:
            continue

        idt = Identity().parse(item['identity'])
        item['signed_identity'] = idt.signed(item['org_node'], uid, access_token)
        item['identity'] = idt.json

        item['open_id'] = item.pop('_id').__str__()
        item['org'] = ctrl_org.simple_read(item['org'])

        array.append(item)

    return array


def my_vip(appid, uid, access_token):
    """
    查询我的VIP会员信息，如果没有注册会员，默认会添加到level=0的vip组中
    :param appid: 应用ID，即发布应用的组织ID
    :param uid: 用户ID
    :param access_token: 用户登录UCenter后获取的访问token
    """
    u = ctrl_user.get(uid)
    if u is None:
        raise ErrException(ERROR.E40000, extra='invalid user [%s]' % uid)

    uid = u['id']
    user = {
        'uid': ObjectId(uid),
        'name': u.get('name'),
        'nickname': u.get('nickname'),
        'email': u.get('email'),
        'mobile': u.get('mobile'),
        'icon': u.get('icon')
    }

    # 查询所有会员组
    cursor = db.vip.find({'app_org': ObjectId(appid)})
    open_vip = None
    vip_list = list()
    for v in cursor:
        vip_list.append(v['vip_org'])
        if v['level'] == 0:
            open_vip = v

    if len(vip_list) == 0:
        # 组织没有注册开放注册会员功能
        raise ErrException(ERROR.E40400, extra='not open registering publicly for clients')

    o2u = db.org2user.find_one({'org': {'$in': vip_list}, 'user.uid': ObjectId(uid)}, {'user': 0})
    if o2u is None:
        if open_vip is None:
            raise ErrException(ERROR.E40400, extra='no lever of 0 vip registered')

        vo = db.org.find_one({'_id': open_vip['vip_org']})
        if vo is None:
            raise ErrException(ERROR.E40400, extra='not found vip org [%s]' % open_vip['vip_org'])

        # 如果没有，则将用户添加到level为0的会员组中
        now = time.millisecond()
        result = db.org2user.insert_one({
            "org": vo['_id'],
            "org_node": vo['node'],
            "identity": Identity().parse(open_vip['identity']).text,
            "user": user,
            "created": now,
            "updated": now
        })
        o2u = db.org2user.find_one(result.inserted_id)

    # 暂时不开放VIP会员对VIP组织的操作，故将identity域数据不返回
    '''
    idt = Identity().parse(o2u['identity'])
    o2u['signed_identity'] = idt.signed(o2u['org_node'], uid, access_token)
    o2u['identity'] = idt.json
    '''
    o2u.pop('identity')

    o2u['vip_id'] = o2u.pop('_id').__str__()
    o2u['org'] = ctrl_org.simple_read(o2u['org'])

    return o2u
