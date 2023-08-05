# -*- coding: utf-8 -*-
import hashlib

from tweb.error_exception import ErrException, ERROR
import urllib.parse
import urllib.request


async def send_sms(business_id, mobile, code, tpl_type=0):
    # 第三方短信服务
    sms_url = 'http://m.5c.com.cn/api/send/index.php'
    sms_apikey = 'd4b4078228dc52dab84e6bbc93705f1e'
    sms_username = 'njbhwl'
    sms_password = 'asdf1234'
    sms_password_md5 = hashlib.md5(sms_password.encode('utf-8')).hexdigest()

    content = '[VOT] 验证码: {}，请注意保密！'.format(code)

    mobile = mobile.replace('-', '')
    values = {
        'username': sms_username,
        'password_md5': sms_password_md5,
        'apikey': sms_apikey,
        'mobile': mobile,
        'content': content,
        'encode': 'UTF-8'
    }

    try:
        data = urllib.parse.urlencode(values)
        req = urllib.request.Request(sms_url + '?' + data)
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
    except Exception as e:
        raise ErrException(ERROR.E50002, e=e)

    if 'success' not in res:
        error = res.split(':')[1]
        raise ErrException(ERROR.E50002, 'error in send sms: %s' % error)
