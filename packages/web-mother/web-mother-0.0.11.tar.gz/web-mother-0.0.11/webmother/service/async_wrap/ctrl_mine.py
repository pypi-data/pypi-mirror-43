# coding:utf-8

from webmother.service import ctrl_mine
from asyncio import get_event_loop


async def my_identities(appid, uid, access_token, member_type=0):
    args = appid, uid, access_token, member_type
    return await get_event_loop().run_in_executor(None, ctrl_mine.my_identities, *args)


async def my_vip(appid, uid, access_token):
    args = appid, uid, access_token
    return await get_event_loop().run_in_executor(None, ctrl_mine.my_vip, *args)
