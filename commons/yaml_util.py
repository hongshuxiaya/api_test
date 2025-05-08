import os
import yaml


def get_object_path():
    """
    获取项目文件的根路径
    :return:返回节点数据
    不加abspath结果：C:\D-drive-63453\python\api_test_frame\api_test_frame\
    加了结果：C:\D-drive-63453\python\api_test_frame\api_test_frame
    """
    return os.path.abspath(os.getcwd().split('commons')[0])


def read_config_yaml(one_node, two_node):
    """
    读取config.yaml配置文件
    :param one_node:第一个节点
    :param two_node:第二个节点
    :return:返回节点数据
    """
    with open(get_object_path() + r'\config\config.yaml', encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value[one_node][two_node]


def read_config(node):
    """
    读取config.yaml配置文件
    :param node:节点
    :return:返回节点数据
    """
    with open(get_object_path() + r'\config\config.yaml', encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value[node]


def read_extract_yaml(node_name):
    """
    读取extract.yaml文件，因为只保存关联数据的键-值对，那么只需要节点名称
    :param node_name:节点名称
    :return:返回节点数据
    """
    with open(get_object_path() + r'\config\extract.yaml', encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        if node_name is None:
            return value
        elif node_name:
            return value[node_name]


def write_extract_yaml(data):
    """
    追加写入extract.yaml文件
    :param data:
    :return:返回节点数据
    写入用w，就会把之前写的内容清空
    所以用a，追加方式
    """
    with open(get_object_path() + r'\config\extract.yaml', encoding='utf-8', mode='a') as f:
        # 允许写入unicode编码
        yaml.dump(data=data, stream=f, allow_unicode=True)


def clear_extract_yaml():
    """
    清空extract.yaml文件，每次取值之前要做初始化清空操作
    :return:返回节点数据
    """
    with open(get_object_path() + r'\config\extract.yaml', encoding='utf-8', mode='w') as f:
        f.truncate()

if __name__ == '__main__':
    print(get_object_path())