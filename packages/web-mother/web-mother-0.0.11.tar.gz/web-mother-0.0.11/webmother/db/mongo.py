# coding:utf-8

import pymongo
from tornado.options import options
from tweb import time
from bson.objectid import ObjectId

MongoDB = {
    'active': True,  # 是否启用
    'dev': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'ocdb',
        'user': 'app',
        'pwd': 'Octl2app'
    },
    'prod': {
        'host': 'udl.link',
        'port': 27017,
        'db': 'ocdb',
        'user': 'app',
        'pwd': 'Octl2app'
    }
}

# 系统管理员（在UCenter中注册的有效用户）
big_god = {
    'uid': ObjectId('5c82149ee155ac8c0ef6246e'),
    'name': 'admin'
}

mongo_client = None
mongo_db = None

catalog = None
org = None
org2user = None
catalog2org = None
vip = None


def init():
    if not MongoDB['active']:
        return

    global mongo_client
    global mongo_db
    global catalog
    global org
    global org2user
    global catalog2org
    global vip

    mongo_cfg = MongoDB[options.env]

    if mongo_client is not None:
        return

    mongo_client = pymongo.MongoClient(host=mongo_cfg['host'],
                                       port=mongo_cfg['port'],
                                       username=mongo_cfg['user'],
                                       password=mongo_cfg['pwd'],
                                       authSource=mongo_cfg['db'])
    mongo_db = mongo_client[mongo_cfg['db']]

    # collections
    catalog = mongo_db.catalog
    org = mongo_db.org
    org2user = mongo_db.org2user
    catalog2org = mongo_db.catalog2org
    vip = mongo_db.vip

    # 创建索引
    _catalog_index()
    _org_index()
    _org2user_index()
    _catalog2org_index()
    _vip_index()

    # 初始化系统数据
    _init_data()


def start_session():
    return mongo_client.start_session()


def _catalog_index():
    """
    {
        "_id": ObjectId("5c710622e155ac0c39c8b66d"),
        "parent": ObjectId('5c710a88e155ac0cae6b1edb'),  # 父目录的ID, 为空是表示是根节点
        "node": "root/cat1/mycat",                       # 节点标示，规则：代表了路径，eg. 根目录是root，父目录是root/cat1，当前目录是root/cat1/mycat
        "status": 30,                                    # 状态：-10:已删除；0:编辑中；10:待审；20:休眠中；30:已激活；
        "display": {
            "zh": "我的分类",
            "en": "My Catalog"
        },
        "icon": "http://your.com/icon/mycat.png",
        "created": 1550911010096,
        "updated": 1550911010096
    }
    """
    catalog.create_index('node')
    catalog.create_index([('parent', pymongo.ASCENDING), ("updated", pymongo.ASCENDING)], sparse=True)


def _org_index():
    """
    {
        "_id": ObjectId('5c72aac2e155ac16da86a1d1'),
        "parent": ObjectId('5c72ab8fe155ac16da86a1d2'),  # 父组织ID，为空则表示是根组织
        "node": "root/udl/dev",                          # 节点标示，规则：代表了路径，eg. 根目录是root，父目录是root/cat1，当前目录是root/cat1/mycat
        "status": 30,                                    # 状态：-10:已删除；0:编辑中；10:待审；20:休眠中；30:已激活；
        "display": {
            "zh": "开发部",
            "en": "Dev department"
        },
        "desc": {
            "zh": "负责开发",
            "en": "Design and develop"
        },
        "icon": "http://your.com/icon/org.png",
        "open": 1,                                      # 是否支持开放注册，即用户自主加入该组织
        "created": 1551018723088,
        "updated": 1551018723088
    }
    """
    org.create_index('node')
    org.create_index([('parent', pymongo.ASCENDING), ("updated", pymongo.ASCENDING)], sparse=True)


def _org2user_index():
    """
    {
        "_id": ObjectId('5c738423e155ac16da86a1d3'),
        "org": ObjectId('5c72aac2e155ac16da86a1d1'),  # 组织ID
        "org_node": "udl/dev",                        # 组织节点名
        "user" : {
            "uid" : ObjectId("5c6519b3e155ac198ee63bac"),
            "name" : "admin",
            "nickname" : "Admin",
            "icon": "http://your.com/icon/admin.png"
        },
        "identity": 'member:0000;;|org:000000000;0;', # 身份授权记录
        "type": 0,                                    # 成员类型：0-管理类；1-客户类
        "created": 1551074938026
    }
    """
    org2user.create_index('org')
    org2user.create_index('org_node')
    org2user.create_index('user.uid')


def _catalog2org_index():
    """
    {
        "_id": ObjectId('5c7385ede155ac16da86a1d5'),
        "catalog": ObjectId('5c710622e155ac0c39c8b66d'),        # 分类节点ID
        "catalog_node": "root/cat1/mycat",                      # 分类节点名
        "org": ObjectId('5c72aac2e155ac16da86a1d1'),            # 组织ID
        "passport": '0000000000000000000000000000000000000000',  # 许可证授权记录
        "created": 1551074929275,
        "updated": 1551074929275
    }
    """
    catalog2org.create_index('catalog')
    catalog2org.create_index('catalog_node')
    catalog2org.create_index('org')


def _vip_index():
    """
    只有注册开通了vip会员，才能接收客户端自主注册
    {
        "_id": ObjectId('5c85c9f9e155ac04c9f5ec42'),
        "app_org": ObjectId('5c85ca15e155ac04c9f5ec43'),        # 申请开通向客户开放服务应用的组织ID
        "vip_org": ObjectId('5c85ca52e155ac04c9f5ec44'),        # 接收开放会员注册的组织ID，必须是app_org组织下的子组织
        "level": 0,                                             # VIP组的级别
        "identity": 'member:0000;;|org:000000000;0;',           # 会员身份定义
        "created": 1551074929275,
        "updated": 1551074929275
    }
    """
    vip.create_index('app_org')
    vip.create_index('vip_org')


def _init_data():
    now = time.millisecond()

    world_catalog = catalog.find_one({'node': 'world'})
    if world_catalog is None:
        result = catalog.insert_one({
            "node": "world",
            "status": 30,
            "display": {
                "zh": "根",
                "en": "Root"
            },
            "created": now,
            "updated": now
        })
        world_catalog = catalog.find_one({'_id': result.inserted_id})

    god_org = org.find_one({'node': 'god'})
    if god_org is None:
        result = org.insert_one({
            "node": "god",
            "status": 30,
            "display": {
                "zh": "系统管理",
                "en": "Administration"
            },
            "created": now,
            "updated": now
        })
        god_org = org.find_one({'_id': result.inserted_id})

    c2o = catalog2org.find_one({'catalog': world_catalog['_id'], 'org': god_org['_id']})
    if c2o is None:
        catalog2org.insert_one({
            "catalog": world_catalog['_id'],
            "catalog_node": world_catalog['node'],
            "org": god_org['_id'],
            "passport": "catalog:111111111;-10;|grant:1111;;",
            "created": now,
            "updated": now
        })

    # 只能保证有一个超级管理员, 如有则删除其他用户
    cursor = org2user.find(({'org': god_org['_id'], 'user.uid': {'$ne': big_god['uid']}}))
    for item in cursor:
        org2user.delete_one({'org': god_org['_id'], 'user.uid': item['user']['uid']})

    o2u = org2user.find_one(({'org': god_org['_id'], 'user.uid': big_god['uid']}))
    if o2u is None:
        org2user.insert_one({
            "org": god_org['_id'],
            "org_node": god_org['node'],
            "user": big_god,
            "identity": "member:1111;;|org:111111111;-10;",
            "created": now,
            "updated": now
        })
