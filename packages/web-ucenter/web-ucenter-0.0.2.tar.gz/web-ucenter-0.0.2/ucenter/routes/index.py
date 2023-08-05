# coding=utf-8
import config
from ucenter.http_handler.index_handler import IndexHandler

base = '{}'.format(config.DOMAIN)
routes = [
    (r"/%s" % base, IndexHandler),
]
