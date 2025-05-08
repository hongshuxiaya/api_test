import json
import traceback
import yaml
from commons.logger_util import error_log
from commons.yaml_util import get_object_path


def read_testcase_file(yaml_path):
    """
    读取yaml测试用例文件
    :param yaml_path:
    :return:
    """
    try:
        with open(get_object_path() + yaml_path, encoding='utf-8') as f:
            caseinfo = yaml.load(f, Loader=yaml.FullLoader)
            if len(caseinfo) >= 2:     # 如果有多组值，则返回本身，不使用ddt方法
                return caseinfo
            else:
                if "parameterize" in dict(*caseinfo).keys():
                    # 需要解析parameterize数据驱动
                    new_caseinfo = analysis_parameters(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo
    except Exception as e:
        error_log("读取测试用例的yaml文件报错：%s" % str(e))
        raise e


def analysis_parameters(caseinfo):
    """
    分析参数化
    :param caseinfo:
    :return:
    """
    try:
        caseinfo_str = json.dumps(caseinfo)
        data_list = caseinfo["parameterize"]
        # 规范数据驱动写法
        length_success = True
        key_length = len(data_list[0])  # 获取param第一行长度
        # 循环数据
        for param in caseinfo["parameterize"]:
            if len(param) != key_length:
                length_success = False
                error_log("此条数据有误：%s" % param + "数据规范有问题")
                continue  # 一旦param长度不相等结束当前循环
        # 替换值
        new_caseinfo = []
        if length_success:
            for x in range(1, len(data_list)):  # 行
                raw_caseinfo = caseinfo_str  # 每一行的caseinfo
                for y in range(0, len(data_list[x])):  # 列
                    # 判断如果是int类型或者float类型那么需要处理
                    if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                        # 替换
                        raw_caseinfo = raw_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"', str(data_list[x][y]))
                    else:
                        # 替换
                        raw_caseinfo = raw_caseinfo.replace("$ddt{" + data_list[0][y] + "}", str(data_list[x][y]))
                new_caseinfo.append(json.loads(raw_caseinfo))  # 每一行字典追加至new_caseinfo
        # 返回解析的测试用例
        return new_caseinfo
    except Exception as e:
        error_log("数据驱动报错：%s" % str(traceback.format_exc()))
        raise e
