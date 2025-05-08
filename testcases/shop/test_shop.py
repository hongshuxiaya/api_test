import allure
import pytest
from commons.generate_id import m_id, c_id, s_id
from commons.requests_util import RequestUtil
from commons.parameters_util import read_testcase_file
from commons.logger_util import info_log


@allure.epic(next(s_id)+'项目名称：电子商城项目')
@allure.feature(next(m_id)+'模块名称：用户管理模块')
class TestShop:
    def setup_class(self):
        """
        执行测试类之前，需要做的操作
        @return:
        """
        info_log('测试环境初始化....')

    # allure报告的目录结构
    @allure.story(next(c_id)+"登录电子商城系统")
    # 接口描述
    @allure.description("描述：登录电子商城系统")
    # 测试用例执行顺序设置
    @pytest.mark.run(order=1)
    # 接口地址
    @allure.link(url="http://127.0.0.1:8080/dar/user/login", name="接口地址")
    # 测试用例优先级
    @allure.severity(allure.severity_level.CRITICAL)
    # 参数化，yaml数据驱动
    @pytest.mark.parametrize('caseinfo', read_testcase_file("./testcases/shop/login.yaml"))
    def test_login_user(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+"新增用户")
    @allure.description("描述：新增用户")
    @pytest.mark.run(order=2)
    @allure.link(url="http://127.0.0.1:8080/dar/user/addUser", name="接口地址")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file("./testcases/shop/add_user.yaml"))
    def test_add_user(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+"修改用户")
    @allure.description("描述：修改用户")
    @pytest.mark.run(order=3)
    @allure.link(url="http://127.0.0.1:8080/dar/user/updateUser", name="接口地址")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file("./testcases/shop/update_user.yaml"))
    def test_update_user(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+"删除用户")
    @allure.description("描述：删除用户")
    @pytest.mark.run(order=4)
    @allure.link(url="http://127.0.0.1:8080/dar/user/deleteUser", name="接口地址")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file("./testcases/shop/delete_user.yaml"))
    def test_delete_user(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    @allure.story(next(c_id)+"查询用户")
    @allure.description("描述：查询用户")
    @pytest.mark.run(order=5)
    @allure.link(url="http://127.0.0.1:8080/dar/user/queryUser", name="接口地址")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('caseinfo', read_testcase_file("./testcases/shop/query_user.yaml"))
    def test_query_user(self, caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        RequestUtil().analysis_yaml(caseinfo)

    def teardown_class(self):
        """
        测试类的后置操作，如环境数据清除、数据恢复
        @return:
        """
        info_log('正在清理测试数据....')
