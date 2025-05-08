import os
import shutil
import time
import webbrowser
import pytest
from commons.allure_reports import set_windows_title, get_json_data, write_json_data
from commons.logger_util import info_log
from commons.send_mail import send_mail
from commons.yaml_util import read_config, get_object_path
from commons.zip_files import zip_reports

if __name__ == '__main__':
    pytest.main()
    # 处理生成报告类型
    REPORT_TYPE = read_config('REPORT_TYPE')
    # 使用allure报告
    if REPORT_TYPE == 'allure':
        # 复制environment.xml环境设置到allure报告
        shutil.copy('environment.xml', r'reports\temps')
        # 等待2s
        time.sleep(2)
        # 将reports\temps文件夹下临时生成的json格式的测试报告，-o：输出到reports\allures目录下生成index.html报告
        os.system(r"allure generate reports\temps -o reports\allures --clean")
        # 复制allure报告打开.bat文件到reports\allures下
        shutil.copy(r'reports\allure报告打开.bat', r'reports\allures')
        # 自定义allure报告网页标题
        set_windows_title("自动化测试报告标题")
        # 自定义allure报告标题
        report_title = get_json_data("自动化测试报告")
        write_json_data(report_title)
        # 调用方法，把reports\allures打包成zip文件到reports\report.zip
        # zip_reports(r"reports\allures", r"reports\report.zip")
        # 报告的压缩包reports\report.zip
        # allurereport_path = os.path.join(r"reports", "report.zip")
        # 调用方法，发送报告的压缩包reports\report.zip测试报告到QQ邮箱
        # send_mail(allurereport_path)
        info_log("接口自动化测试完成！")
        # 启动allure服务，自动打开报告
        # os.system(r'allure serve reports\temps')
    # 使用pytest-tmreport的html报告
    elif REPORT_TYPE == 'html':
        htmlreport_path = get_object_path() + r"\reports\report.html"
        webbrowser.open_new_tab(htmlreport_path)
        info_log("接口自动化测试完成！")
        # 发送测试报告到邮箱
        # send_mail(htmlreport_path)
    else:
        info_log("测试报告类型错误！")
