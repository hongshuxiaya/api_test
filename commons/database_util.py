import pymysql
from commons.logger_util import info_log, error_log
import pymysql.cursors
from commons.yaml_util import read_config_yaml
import oracledb


class MysqlUtil:
    """
    设置mysql数据库工具类
    """
    def __init__(self):
        mysql_conf = {'host': read_config_yaml("MYSQL", "host"),
                      'port': read_config_yaml("MYSQL", "port"),
                      'user': read_config_yaml("MYSQL", "user"),
                      'password': str(read_config_yaml("MYSQL", "password")),
                      'database': read_config_yaml("MYSQL", "database")
                      }
        try:
            # 初始化mysql数据库连接
            self.db = pymysql.connect(**mysql_conf, charset="utf8")
            # 创建数据库游标，cursor=pymysql.cursors.DictCursor，将数据库表字段显示，以key-value形式展示
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            info_log("-------------成功连接到Mysql数据库：host:{host}，database:{database}-----------------".format(**mysql_conf))
        except Exception as e:
            error_log(f"数据库连接失败:{e}")

    def get_version(self):
        """
        获取数据库版本号
        """
        self.cursor.execute("SELECT VERSION()")
        return self.cursor.fetchone()

    def get_fetchone(self, sql):
        """
        获取单条数据查询
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            info_log("-------------------------------------------单条数据查询成功！-------------------------------------------")
            # 查询单条数据，结果返回
            return self.cursor.fetchone()
        except Exception as e:
            error_log(f"单条数据查询错误！错误为：{e}")
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def get_fetchall(self, sql):
        """
        获取多条数据查询
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            info_log("------------------------------------------多条数据查询成功！-------------------------------------------")
            # 查询多条数据，结果返回
            return self.cursor.fetchall()
        except Exception as e:
            error_log(f"多条数据查询错误！错误为：{e}")
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def sql_execute(self, sql):
        """
        执行插入/更新操作
        """
        try:
            # db对象和指针对象同时存在
            if self.db and self.cursor:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交执行sql到数据库，完成insert或者update相关命令操作，非查询时使用提交
                self.db.commit()
                info_log("----------------------------------------插入/更新数据成功！-----------------------------------------")
        except Exception as e:
            # 出现异常时，数据库回滚
            self.db.rollback()
            error_log(f"sql语句执行错误，已执行回滚操作！错误为：{e}")
            # 返回结果为失败
            return False
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def close(self):
        """
        关闭数据库，释放连接池
        """
        # 判断游标对象是否存在
        if self.cursor is not None:
            # 存在则关闭指针
            self.cursor.close()
        # 判断数据库对象是否存在
        if self.db is not None:
            # 存在则关闭数据库对象
            self.db.close()


class OracleUtil:
    """
    设置oracle数据库工具类
    """
    def __init__(self):
        oracle_conf = {'host': read_config_yaml("ORACLE", "host"),
                       'port': read_config_yaml("ORACLE", "port"),
                       'user': read_config_yaml("ORACLE", "user"),
                       'password': str(read_config_yaml("ORACLE", "password")),
                       'service_name': read_config_yaml("ORACLE", "service_name")
                       }
        try:
            # 初始化oracle数据库连接
            self.db = oracledb.connect(**oracle_conf, encoding="utf8")
            # 创建数据库游标
            self.cursor = self.db.cursor()
            info_log("------------成功连接到Oracle数据库：host:{host}，service_name:{service_name}----------".format(**oracle_conf))
        except Exception as e:
            error_log(f"数据库连接失败:{e}")

    def get_fetchone(self, sql):
        """
        获取单条数据查询
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            info_log("-------------------------------------------单条数据查询成功！--------------------------------------------")
            # 查询单条数据，结果返回
            return self.cursor.fetchone()
        except Exception as e:
            error_log(f"单条数据查询错误！错误为：{e}")
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def get_fetchall(self, sql):
        """
        获取多条数据查询
        """
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            info_log("------------------------------------------多条数据查询成功！--------------------------------------------")
            # 查询多条数据，结果返回
            return self.cursor.fetchall()
        except Exception as e:
            error_log(f"多条数据查询错误！错误为：{e}")
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def sql_execute(self, sql):
        """
        执行插入/更新操作
        """
        try:
            # db对象和指针对象同时存在
            if self.db and self.cursor:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交执行sql到数据库，完成insert或者update相关命令操作，非查询时使用
                self.db.commit()
                info_log("----------------------------------------插入/更新数据成功！-----------------------------------------")
        except Exception as e:
            # 出现异常时，数据库回滚
            self.db.rollback()
            error_log(f"sql语句执行错误，已执行回滚操作！错误为：{e}")
            # 返回结果为失败
            return False
        finally:
            # 关闭数据库，释放连接池
            self.close()

    def close(self):
        """
        关闭数据库，释放连接池
        """
        # 判断游标对象是否存在
        if self.cursor is not None:
            # 存在则关闭指针
            self.cursor.close()
        # 判断数据库对象是否存在
        if self.db is not None:
            # 存在则关闭数据库对象
            self.db.close()
