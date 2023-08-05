# coding=utf-8
import config
from ws_handler.manage_handler import ManageHandler

base = 'ws/{}'.format(config.DOMAIN)
routes = [
    (r'/%s/manage' % base, ManageHandler)
]
