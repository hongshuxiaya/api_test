import jenkins
from commons.yaml_util import read_config_yaml


class OperationJenkins:
    """读取Jenkins持续集成的测试报告的信息"""
    def __init__(self):
        self.__config = {"url": read_config_yaml("JENKINS", "url"),
                         "username": read_config_yaml("JENKINS", "username"),
                         "password": read_config_yaml("JENKINS", "password"),
                         "timeout": int(read_config_yaml("JENKINS", "timeout"))
                         }
        self.__server = jenkins.Jenkins(**self.__config)
        # 获取Jenkins上的项目名
        self.job_name = read_config_yaml("JENKINS", "job_name")

    def get_version(self):
        """返回jenkins的版本"""
        version = self.__server.get_version()
        return version
        
    def get_all_jobs(self):
        """读取全部的jobs"""
        all_jobs = self.__server.get_all_jobs()
        return all_jobs

    def build_job_url(self):
        """读取job_name的url地址"""
        job_url = self.__server.build_job_url(name=self.job_name)
        return job_url

    def get_job_number(self):
        """读取Jenkins的job_name最后一个构建号"""
        job_number = self.__server.get_job_info(self.job_name).get("lastBuild").get("number")
        return job_number

    def get_running_builds(self):
        """读取Jenkins的job正在构建的项目"""
        running_builds = self.__server.get_running_builds()
        return running_builds

    def get_build_job_status(self):
        """读取job_name最后一个job构建的状态"""
        build_num = self.get_job_number()
        job_status = self.__server.get_build_info(self.job_name, build_num).get("result")
        return job_status

    def get_console_log(self):
        """获取job_name的控制台日志"""
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_job_description(self):
        """返回job_name的描述信息"""
        description = self.__server.get_job_info(self.job_name).get("description")
        return description

    def get_build_url(self):
        """返回job_name项目的jenkins构建地址"""
        build_url = self.__server.get_job_info(self.job_name).get("url")
        return build_url

    def get_report_url(self):
        """获取job_name测试报告的地址"""
        report_url = self.get_build_url() + 'allure/'
        return report_url
