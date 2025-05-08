import os
import time
import warnings
import allure
import pytest
from decimal import Decimal
from commons.database_util import MysqlUtil
from commons.dingding_robot import send_ding
from commons.operation_jenkins import OperationJenkins
from commons.weixin_robot import send_weixin
from commons.yaml_util import clear_extract_yaml, read_config
from commons.logger_util import info_log


@pytest.fixture(scope='session', autouse=True)
def setup_class():
    """
    接口自动化测试开始
    @return:
    """
    info_log("""--------------------------------------------------------------------------------------------------------
                          _         _      _____         _
          __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
         / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
        | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
         \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
              |_|
    -----------------------------------------------------------------开始执行{}项目""".format(read_config('project_name')))
    yield
    info_log('-----------------------------------------------接口自动化测试结束------------------------------------------------')


@pytest.fixture(scope='session', autouse=True)
def clean_extract_data():
    """
    清空extract.yaml文件数据内容
    :return:
    """
    # 禁用HTTPS告警ResourceWarning
    warnings.simplefilter('ignore', ResourceWarning)
    clear_extract_yaml()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    pytest钩子函数，固定写法，每次pytest测试完成后，会自动收集测试结果
    @param terminalreporter: 内部终端报告对象，对象的status属性
    @param exitstatus: 返回给操作系统的返回码
    @param config: pytest配置的config对象
    @return:
    """
    # 收集测试用例总数
    case_total = terminalreporter._numcollected
    if case_total > 0:
        # 收集测试用例通过数
        passed = len(terminalreporter.stats.get("passed", []))
        # 收集测试用例失败数
        failed = len(terminalreporter.stats.get("failed", []))
        # 收集测试用例跳过数
        skipped = len(terminalreporter.stats.get("skipped", []))
        # 收集测试用例错误数
        error = len(terminalreporter.stats.get("error", []))
        # 收集测试用例执行时长，terminalreporter._sessionstarttime：会话开始时间
        duration = time.time() - terminalreporter._sessionstarttime
        # 时间保留2位小数
        duration = Decimal(duration).quantize(Decimal("0.00"))
        # 计算出测试用例执行的成功率
        rate = len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100
        # 成功率保留2位小数
        rate = Decimal(rate).quantize(Decimal("0.00"))

        # 测试结果写入txt文档
        result = os.path.join("reports", "result.txt")
        # 写入测试结果到reports下的result.txt文件
        with open(result, "w") as f:
            f.write("测试用例总数：%s个" % case_total + "\n")
            f.write("通过数：%s个" % passed + "\n")
            f.write("失败数：%s个" % failed + "\n")
            f.write("跳过数：%s个" % skipped + "\n")
            f.write("错误数：%s个" % error + "\n")
            f.write("测试用例执行时长：%s秒" % duration + "\n")
            # %%：%号本身
            f.write("成功率：%s%%" % rate + "\n")

        # 部署到Jenkins持续集成，读取报告地址
        # operation = OperationJenkins()
        # report = operation.get_report_url()

        # 推送结果到钉钉、企业微信的信息定制化
        # content = f"""
        # 各位好！本次接口自动化测试结果如下（请注意失败及错误的接口）：
        # 测试用例总数：{case_total}个
        # 通过数：{passed}个
        # 失败数：{failed}个
        # 跳过数：{skipped}个
        # 错误数：{error}个
        # 测试用例执行时长：{duration}秒
        # 成功率：{rate}%
        # 测试报告的地址：{report}
        # """
        # 调用钉钉推送方法
        # send_ding(content=content)
        # 调用企业微信推送方法
        # send_weixin(content=content)


# @pytest.fixture(scope='session', autouse=True)
# def teardown_class():
#     """
#     后置处理器，session：全局。比如：测试之后的数据清理，就不会对系统造成影响，也不会产生脏数据。
#     @return:
#     """
#     connect = MysqlUtil()
#     yield
#     sql = "select * from member where mobile_phone='18326074762'"
#     res = connect.get_fetchone(sql)
#     info_log(f"接口自动化测试垃圾数据处理结果为：{res}")
#     allure.attach('处理测试数据', 'fixture后置处理', allure.attachment_type.TEXT)
