import allure
import pytest
from commons.generate_id import m_id, c_id, s_id
from commons.requests_util import RequestUtil
from commons.parameters_util import read_testcase_file


@allure.epic(next(s_id)+'微信公众号登录')
@allure.feature(next(m_id)+'登录模块')
class TestLogin:
    @allure.story(next(c_id)+'获取统一鉴权码token接口')
    @allure.description("描述：获取统一鉴权码token接口")
    @pytest.mark.run(order=1)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/token=", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("caseinfo", read_testcase_file('/testcases/weixin/get_token.yaml'))
    def test_get_token(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)


@allure.epic(next(s_id)+'微信公众号标签')
@allure.feature(next(m_id)+'标签模块')
class TestFlag:
    @allure.story(next(c_id)+'新建标签接口')
    @allure.description("描述：新建标签接口")
    @pytest.mark.run(order=1)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/tags/create?access_token=", name="接口地址")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize('caseinfo', read_testcase_file('/testcases/weixin/create_flag.yaml'))
    def test_create_flag(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'查询标签接口')
    @allure.description("描述：查询标签接口")
    @pytest.mark.run(order=2)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/token=", name="接口地址")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file('/testcases/weixin/select_flag.yaml'))
    def test_select_flag(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'编辑标签接口')
    @allure.description("描述：编辑标签接口")
    @pytest.mark.run(order=3)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/tags/update?access_token=", name="接口地址")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file('/testcases/weixin/edit_flag.yaml'))
    def test_edit_flag(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'删除标签接口')
    @allure.description("描述：删除标签接口")
    @pytest.mark.run(order=4)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=", name="接口地址")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file('/testcases/weixin/delete_flag.yaml'))
    def test_delete_flag(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+'上传文件接口')
    @allure.description("描述：上传文件接口")
    @pytest.mark.run(order=5)
    @allure.link(url="https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=", name="接口地址")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file('/testcases/weixin/upload_file.yaml'))
    def test_upload_file(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

