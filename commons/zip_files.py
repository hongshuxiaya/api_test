import os
import zipfile
from commons.logger_util import info_log
 
 
def zip_reports(dirpath, outfullname):
    """
    压缩指定文件夹到指定目录下
    :param dirpath: 需要打包的目标文件夹路径
    :param outfullname: 压缩文件保存路径+xxxx.zip
    :return:
    """
    zip_files = zipfile.ZipFile(outfullname, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标根路径，只对目标文件夹下的文件及文件夹压缩
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip_files.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip_files.close()
    info_log("已经把文件夹{0}已压缩为{1}！".format(dirpath, outfullname))
