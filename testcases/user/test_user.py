import allure
import pytest
from commons.generate_id import m_id, c_id, s_id
from commons.requests_util import RequestUtil
from commons.parameters_util import read_testcase_file


@allure.epic(next(s_id)+'商城加密登录')
@allure.feature(next(m_id)+'登录模块')
class TestUser:
    @allure.story(next(c_id)+'md5加密登录接口')
    @allure.description("描述：md5加密登录接口")
    @pytest.mark.run(order=1)
    @allure.link(url="http://101.34.221.219:5000/md5login", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/user/md5_case.yaml'))
    def test_md5_login(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'base64加密登录接口')
    @allure.description("描述：base64加密登录接口")
    @pytest.mark.run(order=2)
    @allure.link(url="http://101.34.221.219:5000/base64login", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/user/base64_case.yaml'))
    def test_base64_login(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'rsa加密登录接口')
    @allure.description("描述：rsa加密登录接口")
    @pytest.mark.run(order=3)
    @allure.link(url="http://101.34.221.219:5000/rsalogin", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/user/rsa_case.yaml'))
    def test_rsa_login(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)
