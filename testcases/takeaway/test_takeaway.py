import allure
import pytest
from commons.generate_id import c_id, m_id, s_id
from commons.requests_util import RequestUtil
from commons.parameters_util import read_testcase_file


@allure.epic(next(s_id)+'外卖项目')
@allure.feature(next(m_id)+'外卖模块')
class TestTakeaway:
    @allure.story(next(c_id)+'外卖注册')
    @allure.description("描述：外卖注册")
    @pytest.mark.run(order=1)
    @allure.link(url="https://api.tttt.one/rest-v2/login/sign_up", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_register.yaml'))
    def test_takeaway_register(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖登录')
    @allure.description("描述：外卖登录")
    @pytest.mark.run(order=2)
    @allure.link(url="https://api.tttt.one/rest-v2/login/access_token", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_login.yaml'))
    def test_takeaway_login(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖任务创建')
    @allure.description("描述：外卖任务创建")
    @pytest.mark.run(order=3)
    @allure.link(url="https://api.tttt.one/rest-v2/todo", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_create.yaml'))
    def test_takeaway_create(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖任务查询')
    @allure.description("描述：外卖任务查询")
    @pytest.mark.run(order=4)
    @allure.link(url="https://api.tttt.one/rest-v2/todo", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_search.yaml'))
    def test_takeaway_search(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖任务详情')
    @allure.description("描述：外卖任务详情")
    @pytest.mark.run(order=5)
    @allure.link(url="https://api.tttt.one/rest-v2/todo", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_details.yaml'))
    def test_takeaway_details(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖任务修改')
    @allure.description("描述：外卖任务修改")
    @pytest.mark.run(order=6)
    @allure.link(url="https://api.tttt.one/rest-v2/todo", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_edit.yaml'))
    def test_takeaway_edit(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'外卖任务删除')
    @allure.description("描述：外卖任务删除")
    @pytest.mark.run(order=7)
    @allure.link(url="https://api.tttt.one/rest-v2/todo", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/takeaway/takeaway_delete.yaml'))
    def test_takeaway_delete(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)