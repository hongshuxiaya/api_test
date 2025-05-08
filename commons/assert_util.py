import json
import traceback
import jsonpath
from commons.logger_util import info_log, error_log


class AssertUtil:
    """
    断言封装
    """
    def validate_json_result(self, expect, actuality, status_code):
        """
        json断言封装：返回是json格式
        :param expect: 预期结果
        :param actuality: 实际结果
        :param status_code: 返回的状态码
        :return:
        """
        try:
            # 收集日志
            info_log("预期结果：%s" % expect)
            info_log("实际结果：%s" % actuality)
            # 判断是否断言成功：0成功，1失败
            flag = 0
            # 解析
            if expect and isinstance(expect, list):
                for exp in expect:
                    for key, value in dict(exp).items():
                        # 判断断言方式：equals，contains
                        if key == 'equals':
                            for assert_key, assert_value in dict(value).items():
                                if assert_key == 'status_code':
                                    if status_code != assert_value:
                                        flag = flag + 1
                                        error_log("断言失败:" + assert_key + "不等于" + str(assert_value) + "")
                                else:
                                    key_list = jsonpath.jsonpath(actuality, '$..%s' % assert_key)
                                    if key_list:
                                        if assert_value not in key_list:
                                            flag = flag + 1
                                            error_log("断言失败:" + assert_key + "不等于" + str(assert_value) + "")
                                    else:
                                        flag = flag + 1
                                        error_log("断言失败:返回结果中不存在" + assert_key + "")
                        elif key == 'contains':
                            if value not in json.dumps(actuality):
                                flag = flag + 1
                                error_log("断言失败:返回结果中不包含字符串" + value + "")
                        else:
                            error_log('框架暂不支持此断言方式！')
            # 断言处理
            assert flag == 0
            info_log('接口请求成功！')
            info_log(
                '--------------------------------------------接口请求结束--------------------------------------------\n')
        except Exception as e:
            info_log('接口请求失败！')
            info_log(
                '--------------------------------------------接口请求结束--------------------------------------------\n')
            error_log("断言异常：异常信息：%s" % str(traceback.format_exc()))

    def validate_html_result(self, expect, actuality, status_code):
        """
        html断言封装，返回是html或者text格式
        :param expect: 预期结果
        :param actuality: 实际结果
        :param status_code: 实际的状态码
        :return:
        """
        try:
            # 收集日志
            info_log("预期结果：%s" % expect)
            info_log("实际结果：%s" % actuality)
            # 断言是否成功的标记，0成功，其他是失败
            flag = 0
            # 解析
            if expect and isinstance(expect, list):
                for yq in expect:
                    for key, value in dict(yq).items():
                        # 判断断言方式：equals，contains
                        if key == "equals":
                            for assert_key, assert_value in dict(value).items():
                                if assert_key == "status_code":
                                    if status_code != assert_value:
                                        flag = flag + 1
                                        info_log("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
                        elif key == "contains":
                            if value not in actuality:
                                flag = flag + 1
                                error_log("断言失败：返回结果不包含字符串:" + value + "")
                        else:
                            error_log("框架不支持此断言方式")
            assert flag == 0
            info_log("接口请求成功！")
            info_log(
                "-------------------------------------------接口请求结束---------------------------------------------\n")
        except Exception as e:
            info_log("接口请求失败！")
            info_log(
                "-------------------------------------------接口请求结束---------------------------------------------\n")
            error_log("断言异常：异常信息：%s" % str(traceback.format_exc()))
