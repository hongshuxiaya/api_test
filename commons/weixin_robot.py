import requests
from commons.logger_util import info_log
from commons.yaml_util import read_config_yaml


def send_weixin(content):
    """
    机器人向企业微信群推送测试结果
    @param content: 推送的内容
    @return:
    """
    url = f'{read_config_yaml("WEIXIN", "url")}'
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    # @全体成员
    data = {"msgtype": "markdown","markdown": {"content": content, "mentioned_list": ["@all", ]}}
    res = requests.post(url=url, json=data, headers=headers)
    info_log("发送企业微信测试结果成功！")
    return res.text
