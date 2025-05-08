import json


def set_windows_title(new_title):
    """
    修改Allure报告的浏览器窗口标题文案Allure Report为自定义的名称
    """
    # allure报告的html文件地址
    title_filepath = r"reports\allures\index.html"
    with open(title_filepath, 'r+', encoding="utf-8") as f:
        # 读取当前文件的所有内容
        all_the_lines = f.readlines()
        f.seek(0)
        f.truncate()
        # 循环遍历每一行的内容，将Allure Report全部替换为new_title(新文案)
        for line in all_the_lines:
            f.write(line.replace("Allure Report", new_title))
        # 关闭文件
        f.close()


def get_json_data(name):
    """
    修改allure报告的json文件
    """
    # 获取summary.json文件的地址
    title_filepath = r"reports\allures\widgets\summary.json"
    with open(title_filepath, 'rb') as f:
        # 加载json文件中的内容给params
        params = json.load(f)
        # 修改内容
        params['reportName'] = name
        # 将修改后的内容保存在dict中
        dict = params
    # 关闭json读模式
    f.close()
    # 返回dict字典内容
    return dict


def write_json_data(dict):
    """
    写入json文件数据
    """
    # 获取summary.json文件的地址
    title_filepath = r"reports\allures\widgets\summary.json"
    with open(title_filepath, 'w', encoding="utf-8") as r:
        # 将dict写入名称为r的文件中
        json.dump(dict, r, ensure_ascii=False, indent=4)
    # 关闭json写模式
    r.close()
