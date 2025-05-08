import allure
import pytest
from commons.generate_id import c_id, m_id, s_id
from commons.requests_util import RequestUtil
from commons.parameters_util import read_testcase_file


@allure.epic(next(s_id)+'论坛加密登录')
@allure.feature(next(m_id)+'论坛模块')
class TestPhp:
    @allure.story(next(c_id)+'论坛首页')
    @allure.description("描述：论坛首页")
    @pytest.mark.run(order=1)
    @allure.link(url="http://47.107.116.139/phpwind", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/php/php_page.yaml'))
    def test_php_page(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'论坛登录')
    @allure.description("描述：论坛登录")
    @pytest.mark.run(order=2)
    @allure.link(url="http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/php/php_login.yaml'))
    def test_php_login(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'sign签名接口')
    @allure.description("描述：sign签名接口")
    @pytest.mark.run(order=3)
    @allure.link(url="http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/php/sign_case.yaml'))
    def test_sign_case(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)
