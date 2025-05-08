def generate_session_id():
    """
    生成测试用例项目的编号，为了保证allure报告的顺序与pytest设定的执行顾序保持一致
    """
    for i in range(1, 100):
        session_id = 'S' + str(i).zfill(2) + "_"
        yield session_id


def generate_module_id():
    """
    生成测试用例模块的编号
    """
    for i in range(1, 1000):
        module_id = 'M' + str(i).zfill(2) + "_"
        yield module_id


def generate_testcase_id():
    """
    生成测试用例的编号
    """
    for i in range(1, 10000):
        case_id = "C" + str(i).zfill(2) + "_"
        yield case_id


s_id = generate_session_id()
m_id = generate_module_id()
c_id = generate_testcase_id()
