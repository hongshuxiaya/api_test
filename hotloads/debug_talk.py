import re
from io import StringIO
from commons.logger_util import info_log
from commons.yaml_util import read_extract_yaml, read_config_yaml
import base64
import hashlib
import os
import random
import time
import yaml
import rsa


class DebugTalk:
    """
    热加载方法
    """
    def get_random_number(self, min, max):
        """
        获取随机数
        :param min:最小值
        :param max:最大值
        :return:
        """
        return random.randint(int(min), int(max))

    def get_base_url(self, one_node):
        """
        获取基础路径
        :param one_node:
        :return:
        """
        return read_config_yaml('BASE', one_node)

    def get_extract_data(self, node_name):
        """
        读取extract.yaml文件
        :param node_name:
        :return:
        """
        return read_extract_yaml(node_name)

    def timestamp(self):
        """
        获取当前时间戳，10位
        @return:
        """
        t = int(time.time())
        return t

    def md5_encode(self, args):
        """
        md5加密，以指定的编码格式编码字符串
        :param args:
        :return:
        """
        # 先把变量专程utf-8的编码格式
        args = str(args).encode('utf-8')
        # md5加密
        args_value = hashlib.md5(args).hexdigest()
        # 返回
        return args_value

    def base64_encode(self, args):
        """
        base64加密，以指定的编码格式编码字符串
        :param args:
        :return:
        """
        # 先把变量转成utf-8的编码格式
        args = str(args).encode('utf-8')
        # base64加密
        base64_value = base64.b64encode(args).decode(encoding='utf-8')
        # 返回
        return base64_value

    def base64_decode(sef, content):
        """
        base64解密
        @return:
        """
        # 原文转为二进制
        content = str(content).encode("utf-8")
        # base64解密(二进制)
        decode_value = base64.b64decode(content)
        # 转成字符串
        encode_str = decode_value.decode("utf-8")
        return encode_str

    def sha1_encode(self, params):
        """
        参数sha1加密
        @param params:
        @return:
        """
        enc_data = hashlib.sha1()
        enc_data.update(params.encode(encoding="utf-8"))
        return enc_data.hexdigest()

    def rsa_public_secret(self, args):
        """
        rsa加密，以指定的编码格式编码字符串
        :param args:
        :return:
        """
        with open("hotloads/public.pem", encoding='utf-8') as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
        # 把变量转成utf-8格式
        args = str(args).encode("utf-8")
        # 把字符串加密成byte类型
        byte_value = rsa.encrypt(args, public_key)
        # 把字节转成字符串格式
        rsa_value = base64.b64encode(byte_value).decode("utf-8")
        return rsa_value

    def signs(self, yaml_path):
        """
        sign签名，以指定的编码格式编码字符串
        :param yaml_path:
        :return:
        """
        # 定义所有参数字典
        all_dict_data = {}
        # 第一步：获得所有的参数，包括url，params，data里面的参数
        with open(os.getcwd() + '/' + yaml_path, encoding="utf-8") as f:
            # 加载yaml的内容
            yaml_value = yaml.load(f, Loader=yaml.FullLoader)
            # 因为yaml_value是一个列表，对列表循环，得到测试用例字典
            for caseinfo in yaml_value:
                if "reuqest" in caseinfo.keys():
                    request_value = caseinfo["request"]
                    if "url" in request_value.keys():
                        url = request_value["url"]  # 得到url地址
                        url = url[url.index("?") + 1:]  # 将?之后的地址取得
                        url_list = url.split("&")  # ['m=u','c=login','a=dorun']
                        for u in url_list:  # 取得单独每个值
                            all_dict_data[u[0:u.index("=")]] = u[u.index("=") + 1:]
                    # 处理params和data参数
                    for key, value in request_value.items():
                        if key in ["params", "data"]:
                            for k, v in value.items():
                                all_dict_data[k] = v
                    # dict中的key根据ASCII码排序
                    all_dict_data = self.dict_asccii_sort(all_dict_data)
                    # 热加载
                    yaml_str = yaml.dump(all_dict_data)
                    yaml_str = self.replace_hotload(yaml_str)
                    all_dict_data = yaml.safe_load(StringIO(yaml_str))
                    info_log(all_dict_data)

        # 第二步  将字典改成 & 拼接的字符串格式
        all_str = ""
        for key, value in all_dict_data:
            all_str = all_str + str(key) + "=" + str(value) + "&"
        all_str = all_str[:-1]  # 因为最后会多出一个& 所以切片除去

        # 第三步之后  假设appid和appsecret已知
        appid = "admin"
        appsecret = "123"
        nonce = str(random.randint(10000000, 999999999))
        timestamp = str(int(time.time()))
        all_str = "appid=" + appid + "&" + "appsecret=" + appsecret + "&" + all_str + "&" + "nonce=" + nonce + "&" + "timestamp=" + timestamp

        # 之后再进行MD5加密
        sign = self.md5_encode(all_str).upper()
        info_log(sign)
        return sign

    def dict_asccii_sort(self, args_dict):
        """
        把字典按照key的ASCII码升序排序
        @param args_dict:
        @return:
        """
        dict_key = dict(args_dict).keys()
        new_list = list(dict_key)
        new_list.sort()
        new_dict = {}
        for key in new_list:
            new_dict[key] = args_dict[key]
        return new_dict

    def replace_hotload(self, yaml_str):
        regexp = "\\${(.*?)\\((.*?)\\)}"
        fun_list = re.findall(regexp, yaml_str)
        for f in fun_list:
            if f[1] == "":  # 没有参数
                # 反射
                new_value = getattr(DebugTalk(), f[0])()
            else:  # 有参数
                new_value = getattr(DebugTalk(), f[0])(*f[1].split(","))
            oldstr = "${" + f[0] + "(" + f[1] + ")}"  # 拼接旧值
            yaml_str = yaml_str.replace(oldstr, str(new_value))
        return yaml_str
