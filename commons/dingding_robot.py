import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from commons.logger_util import info_log
from commons.yaml_util import read_config_yaml


def get_sign():
    """
    签名计算
    @return:
    """
    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人生成的密钥
    secret = read_config_yaml("DINGDING", "secret")
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_ding(content, at_all=True):
    """
    机器人向钉钉群推送测试结果
    @param content: 推送的内容
    @param at_all: @钉钉群里面的所有人，默认为True
    """
    timestamp_sign = get_sign()
    # 需要拿到钉钉机器人的Webhook地址+timestamp+sign
    url = f'{read_config_yaml("DINGDING", "url")}&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": content}, "at": {"isAtAll": at_all}}
    res = requests.post(url=url, json=data, headers=headers)
    info_log("发送钉钉测试结果成功！")
    return res.text
