import logging
import time
from commons.yaml_util import read_config_yaml, get_object_path
import colorlog


class LoggerUtil:
    """
    封装日志
    """
    def __init__(self):
        self.console_handler = None
        self.file_handler = None
        self.file_log_path = None
        self.logger = None
    # 设置日志颜色
    log_color = {'DEBUG': 'white', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red'}

    def create_log(self, logger_name='log'):
        """
        创建一个日志对象
        :param logger_name: 固定写法
        :return:
        """
        self.logger = logging.getLogger(logger_name)
        # 设置全局的日志级别等级(DEBUG<INFO<WARNING<ERROR<CRITICAL)
        self.logger.setLevel(logging.DEBUG)
        # 防止日志重复
        if not self.logger.handlers:
            # ---------------------------------------------------文件日志-----------------------------------------------------
            # 获取日志文件的名称
            self.file_log_path = get_object_path() + '/logs/' + format(time.strftime("%Y_%m_%d_%H%M%S")) + ".log"
            # 创建文件日志的控制器
            self.file_handler = logging.FileHandler(filename=self.file_log_path, mode='a', encoding='utf-8')
            # 设置文件日志的级别
            file_log_level = str(read_config_yaml('LOG', 'log_level')).lower()
            if file_log_level == 'debug':
                self.file_handler.setLevel(logging.DEBUG)
            elif file_log_level == 'info':
                self.file_handler.setLevel(logging.INFO)
            elif file_log_level == 'warning':
                self.file_handler.setLevel(logging.WARNING)
            elif file_log_level == 'error':
                self.file_handler.setLevel(logging.ERROR)
            elif file_log_level == 'critical':
                self.file_handler.setLevel(logging.CRITICAL)
            # 设置文件日志的格式
            self.file_handler.setFormatter(fmt=logging.Formatter(read_config_yaml('LOG', 'file_log_format')))
            # 将控制器加入到日志对象
            self.logger.addHandler(self.file_handler)
            # ---------------------------------------------------控制台日志-----------------------------------------------------
            # 创建控制台日志的控制器
            self.console_handler = logging.StreamHandler()
            # 设置控制台日志的级别
            console_log_level = read_config_yaml('LOG', 'log_level').lower()
            if console_log_level == 'debug':
                self.console_handler.setLevel(logging.DEBUG)
            elif console_log_level == 'info':
                self.console_handler.setLevel(logging.INFO)
            elif console_log_level == 'warning':
                self.console_handler.setLevel(logging.WARNING)
            elif console_log_level == 'error':
                self.console_handler.setLevel(logging.ERROR)
            elif console_log_level == 'critical':
                self.console_handler.setLevel(logging.CRITICAL)
            # 设置控制台日志的格式
            self.console_handler.setFormatter(fmt=colorlog.ColoredFormatter(read_config_yaml('LOG', 'console_log_format'), log_colors=self.log_color))
            # 将控制器加入到日志对象
            self.logger.addHandler(self.console_handler)
        return self.logger


def info_log(log_massage):
    """
    函数：输出正常记录日志
    :param log_massage:
    :return:
    """
    LoggerUtil().create_log().info(log_massage)


def error_log(log_massage):
    """
    函数：输出错误日志
    :param log_massage:
    :return:
    """
    LoggerUtil().create_log().error(log_massage)
    raise AssertionError(log_massage)
