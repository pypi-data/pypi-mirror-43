#!/usr/bin/python
# coding:utf-8

import config
from tweb.error_exception import ErrException, ERROR
from tweb import tools
import random
from tweb import rdpool
import json


def gen_code(way_type, indicator, timeout):
    """
    :param way_type: 接收方式，eg. sms, email
    :param indicator: 手机号码或者email地址
    :param timeout: 超时时间
    :return: (code, {'code_token': 'xxxxxx', 'timeout': timeout})
    """
    ttl = rdpool.rds.ttl(_key_limit(indicator))
    # if ttl is not None and ttl > 0:
    #     raise ErrException(ERROR.E40304, extra='Please retry after {} seconds'.format(ttl))

    code_token = tools.gen_id3()
    code = random.randint(100000, 999999)

    rdpool.rds.set(_key(code_token, code), json.dumps({'type': way_type, 'indicator': indicator}), timeout)

    ret = {'code_token': code_token, 'timeout': timeout}

    # 记录该号码或者地址上次发送信息，用以放置频繁发送
    rdpool.rds.set(_key_limit(indicator), ret, 60)

    return code, ret


async def verify_code(code_token, code):
    key = _key(code_token, code)
    data = rdpool.rds.get(key)
    if data is None:
        raise ErrException(ERROR.E40103)

    rdpool.rds.delete(key)
    record = json.loads(data)
    return record


def _key(code_token, code):
    return '{}/user/code/{}/{}'.format(config.DOMAIN, code_token, code)


def _key_limit(indicator):
    return '{}/user/code/limit/{}'.format(config.DOMAIN, indicator)
