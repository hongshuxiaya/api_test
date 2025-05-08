import json
import re
import traceback
import allure
import jsonpath
import requests
import urllib3
from commons.assert_util import AssertUtil
from commons.logger_util import info_log, error_log
from commons.yaml_util import write_extract_yaml, read_config_yaml
from hotloads.debug_talk import DebugTalk


class RequestUtil:
    # 获得session会话对象，自动管理cookie
    session = requests.session()

    def __init__(self):
        self.last_method = None
        self.base_url = ""
        self.last_headers = {}

    def analysis_yaml(self, caseinfo):
        """
        规范yaml测试用例文件的写法
        :param caseinfo:
        :return:
        """
        try:
            # 测试用例中必须有的四个一级关键字：name，base_url，request，validate，将caseinfo转换成字典格式，得到所有的key值
            caseinfo_keys = dict(caseinfo).keys()
            if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validate' in caseinfo_keys:
                # 同样再次将caseinfo转换成字典格式，取得request_keys里面的键
                request_keys = dict(caseinfo['request']).keys()
                # request关键字必须包含两个二级关键字：method，url
                if 'method' in request_keys and 'url' in request_keys:
                    # 读取到数据后给到变量，再del操作删掉caseinfo里面的值
                    name = caseinfo['name']
                    allure.attach(name, '接口名称')
                    self.base_url = caseinfo['base_url']
                    method = caseinfo['request']['method']
                    #del 用于删掉指定key值，跟pop方法差不多
                    del caseinfo['request']['method']
                    url = caseinfo['request']['url']
                    del caseinfo['request']['url']
                    headers = None
                    # 通过jsonpath的方式来判断是否存在headers，存在就取出来放到变量中
                    if jsonpath.jsonpath(caseinfo, '$.request.headers'):
                        headers = caseinfo['request']['headers']
                        allure.attach(str(headers), '请求头信息', allure.attachment_type.TEXT)
                        del caseinfo['request']['headers']
                    files = None
                    # 文件的方式提取，存放到变量中
                    if jsonpath.jsonpath(caseinfo, '$.request.files'):
                        files = caseinfo['request']['files']
                        # 因为这里的值还是一个字典，文件上传不能是传参字典，所以要取得字典key对应的value值。对字典进行循环，value是文件流
                        for file_key, file_value in dict(files).items():
                            files[file_key] = open(file=file_value, mode="rb")
                        del caseinfo['request']['files']
                    # 把method，url，headers，files这四个数据从caseinfo['request']去掉之后，再把剩下的传给**kwargs
                    #上面del删除的目的，是因为不确定最后是传param，json还是data所以用del，删除到剩下的然后传给requests中的kwagr s
                    res = self.send_request(name=name, method=method, url=url, headers=headers, files=files,
                                            **caseinfo['request'])
                    content_type = res.headers['Content-Type']
                    info_log("响应头：content_type:%s" % content_type)
                    return_text = res.text
                    allure.attach(return_text, '响应信息', allure.attachment_type.TEXT)
                    status_code = res.status_code
                    allure.attach(str(status_code), '响应状态码', allure.attachment_type.TEXT)
                    # 如果返回是json类型，json类型支持正则提取和jsonpath提取
                    if 'json' in content_type:
                        # 前提是返回json格式
                        return_data = res.json()
                        # 提取接口关联的变量，既要支持正则表达式，又要支持json提取，正则只支持取字符串
                        if 'extract' in caseinfo_keys:
                            for file_key, file_value in dict(caseinfo['extract']).items():
                                # 正则表达式提取
                                if '(.*?)' in file_value or '(.+?)' in file_value:
                                    zz_value = re.findall(file_value, return_text)
                                    if zz_value:
                                        if len(zz_value) == 1:    # 提取单个值
                                            extract_data = {file_key: zz_value[0]}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                        else:     # 提取多个值
                                            extract_data = {file_key: zz_value}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                else:  # jsonpath方式提取
                                    js_value = jsonpath.jsonpath(return_data, file_value)
                                    if js_value:
                                        if len(js_value) == 1:   # 提取单个值
                                            extract_data = {file_key: js_value[0]}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                        else:     # 提取多个值
                                            extract_data = {file_key: js_value}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                            # 断言
                            expect = caseinfo['validate']
                            AssertUtil().validate_json_result(expect, return_data, status_code)
                        else:
                            # 如果没有提取关键字extract，那么就直接进行断言
                            expect = caseinfo['validate']
                            AssertUtil().validate_json_result(expect, return_data, status_code)
                    # 如果是txt响应,就用正则提取
                    elif 'html' or 'text' in content_type:
                        # 提取接口关联的变量,既要支持正则表达式，又要支持json提取，正则只支持取字符串
                        if 'extract' in caseinfo_keys:
                            for file_key, file_value in dict(caseinfo['extract']).items():
                                # 正则表达式提取
                                if '(.+?)' in file_value or '(.*?)' in file_value:
                                    zz_value = re.findall(file_value, return_text)
                                    if zz_value:
                                        if len(zz_value) == 1:   # 提取单个值
                                            extract_data = {file_key: zz_value[0]}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                        else:   # 提取多个值
                                            extract_data = {file_key: zz_value}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                else:   # jsonpath方式提取
                                    js_value = jsonpath.jsonpath(return_text, file_value)
                                    if js_value:
                                        if len(js_value) == 1:    # 提取单个值
                                            extract_data = {file_key: js_value[0]}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                                        else:    # 提取多个值
                                            extract_data = {file_key: js_value}
                                            write_extract_yaml(extract_data)
                                            info_log(f"提取到接口关联的参数：{extract_data}")
                            # 断言
                            expect = caseinfo['validate']
                            AssertUtil().validate_html_result(expect, return_text, status_code)
                        else:
                            # 如果没有提取关键字extract，那么就直接进行断言
                            expect = caseinfo['validate']
                            AssertUtil().validate_html_result(expect, return_text, status_code)
                    else:
                        error_log(f"响应头未查找到html，text，json字符串，实际响应头为{content_type}")
                else:
                    error_log("在request一级关键字下必须包括两个二级关键字：method，url")
            else:
                error_log("必须有的四个一级关键字：name，base_url，request，validate")
        except Exception as e:
            error_log("分析yaml文件异常：异常信息：%s" % str(traceback.format_exc() + repr(e)))

    def replace_load(self, data):
        """
        热加载替换解析
        :param data:
        :return:
        """
        # 字典类型转换成字符串
        if data and isinstance(data, dict) or isinstance(data, list):  # 如果data不为空并且数据类型为字典
            str_data = json.dumps(data)
        else:
            str_data = data
        # 替换值
        for i in range(1, str_data.count('${') + 1):
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("${")
                end_index = str_data.index("}", start_index)
                old_value = str_data[start_index:end_index + 1]
                # 取出旧的参数名称的值，索引切片
                function_name = old_value[2:old_value.index('(')]
                # 取出旧的参数名称的值，索引切片
                args_value = old_value[old_value.index('(') + 1:old_value.index(')')]
                # 反射(通过一个函数的字符串直接去调用这个方法)，传递的两个参数通过","分割成两个参数，进行解包
                new_value = getattr(DebugTalk(), function_name)(*args_value.split(','))
                # 参数类型为int，把新的值强转为str
                str_data = str_data.replace(old_value, str(new_value))
        # 还原数据类型
        if data and isinstance(data, dict) or isinstance(data, list):  # 如果data不为空并且数据类型为字典
            # 统一转换成字符串类型
            data = json.loads(str_data)
        else:
            data = str_data
        # 返回
        return data

    def send_request(self, name, method, url, headers=None, files=None, **kwargs):
        """
        统一发送请求方法
        :param files: 文件上传
        :param name: 接口名称
        :param headers: 请求头
        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 剩余的请求参数
        :return:
        """
        try:
            # 获取接口设置的超时时间
            timeout = read_config_yaml("API_TIMEOUT", "timeout")
            # 处理method方法
            self.last_method = str(method).lower()
            allure.attach(self.last_method, '请求方法')
            # 处理基础路径，拼接测试环境地址
            self.base_url = self.replace_load(self.base_url) + self.replace_load(url)
            allure.attach(self.base_url, '接口地址')
            # 处理请求头
            if headers and isinstance(headers, dict):
                self.last_headers = self.replace_load(headers)
                allure.attach(str(self.last_headers), '请求头信息', allure.attachment_type.TEXT)
            # 请求数据替换：可能是params，data，json
            for key, value in kwargs.items():
                if key in ['params', 'data', 'json']:
                    # 替换${}格式
                    kwargs[key] = self.replace_load(value)
            # 收集日志
            info_log('---------------------------------------------接口请求开始---------------------------------------------')
            info_log(f"接口名称：{name}")
            info_log(f"请求方式:{self.last_method}")
            info_log(f"请求路径:{self.base_url}")
            info_log(f"请求头：{self.last_headers}")
            res_params = json.dumps(kwargs, ensure_ascii=False)
            if 'params' in kwargs.keys():
                allure.attach(res_params, '请求参数', allure.attachment_type.TEXT)
                info_log("请求参数：%s" % kwargs['params'])
            elif 'data' in kwargs.keys():
                allure.attach(res_params, '请求参数', allure.attachment_type.TEXT)
                info_log("请求参数：%s" % kwargs['data'])
            elif 'json' in kwargs.keys():
                allure.attach(res_params, '请求参数', allure.attachment_type.TEXT)
                info_log("请求参数：%s" % kwargs['json'])
            elif 'files' in kwargs.keys():
                allure.attach(res_params, '请求参数', allure.attachment_type.TEXT)
                info_log("文件上传：%s" % kwargs['files'])
            info_log("文件上传：%s" % files)
            urllib3.disable_warnings(urllib3.connectionpool.InsecureRequestWarning)
            # 发送请求
            response = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers, timeout=timeout, files=files, verify=False,
                                                   **kwargs)
            return response
        except Exception as e:
            error_log("发送请求异常：异常信息：%s" % str(traceback.format_exc() + repr(e)))
