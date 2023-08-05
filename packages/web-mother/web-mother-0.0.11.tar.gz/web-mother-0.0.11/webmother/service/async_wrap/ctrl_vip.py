# coding:utf-8

from webmother.service import ctrl_vip
from asyncio import get_event_loop


async def vip_create(oid, vip_oid, level, identity_json, *auth_args):
    args = oid, vip_oid, level, identity_json, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_vip.vip_create, *args)


async def vip_remove(oid, vip_oid, *auth_args):
    args = oid, vip_oid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_vip.vip_remove, *args)


async def vip_query(oid, *auth_args):
    args = oid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_vip.vip_query, *args)
