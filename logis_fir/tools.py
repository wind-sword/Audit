import os
import shutil
import sqlite3
import re
import subprocess
import sys
import traceback

from logis_fir.logger import Logger


class tools:
    # 注意这些路径都是相对于根目录下的,由于main函数运行在跟目录下,所以在logis_fir的py文件中使用./而不是../
    db_path = "./db/database.db"
    project_word_path = "./project_word"
    zgfh_word_path = "./zgfh_word"
    sjyj_word_path = "./sjyj_word"
    sjbg_word_path = "./sjbg_word"
    sjjg_word_path = "./sjjg_word"
    jz_excel_path = "./jz_excel"

    # 执行sql
    @classmethod
    def executeSql(cls, sql):
        try:
            print("当前需要执行sql:" + sql)
            con = sqlite3.connect(cls.db_path)
            print('Opened database successfully')
            cur = con.cursor()
            cur.execute(sql)
            print('Execute sql successfully' + '\n')
            data = cur.fetchall()
            con.commit()
            con.close()
            return data
        except:
            log = Logger('./log/logfile.log', level='error')
            log.logger.error("错误:%s", traceback.format_exc())

    # 将一个文件复制到某个文件夹目录下,source代表源文件路径,target代表目标文件夹目录
    @classmethod
    def copyFile(cls, source, target):
        try:
            shutil.copy(source, target)
        except:
            log = Logger('./log/logfile.log', level='error')
            log.logger.error("错误:%s", traceback.format_exc())

    # 将一个文件替换掉目录下另一个文件,source代表源文件路径,target代表目标替换文件名,file_folder表示目标文件夹目录
    @classmethod
    def replaceFile(cls, source, target, file_folder_path):
        try:
            if target != "":
                target = file_folder_path + '/' + target
                os.remove(target)  # 删除目标文件
            shutil.copy(source, file_folder_path)  # 将新文件复制到文件目录下
        except:
            log = Logger('./log/logfile.log', level='error')
            log.logger.error("错误:%s", traceback.format_exc())

    # 根据文件名和文件夹路径打开相应文件
    @classmethod
    def openFile(cls, file_folder, file):
        if file != "":
            # 获取文件路径
            path = os.getcwd() + '/' + file_folder + '/' + file
            try:
                # WIN32下打开文件
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    # LINUX下打开文件
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, path])
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())

    # 根据文件名和文件夹路径删除相应文件
    @classmethod
    def deleteFile(cls, file_folder_path, file):
        if file != "":
            try:
                path = file_folder_path + '/' + file
                os.remove(path)
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())

    # 根据文件路径获取文件名
    @classmethod
    def getFileName(cls, input_file_path):
        return os.path.split(input_file_path)[1]  # 文件名

    # 用正则匹配找出字符串中所有整数,用于解析办文编号
    @classmethod
    def getIntegerFromString(cls, string):
        reg = r"\d+"  # 匹配字符串中的数字
        num = re.findall(reg, string)
        return num

    # 获取字符串中发文类型
    @classmethod
    def getTypeFromString(cls, string):
        index = string.find("〔")
        if index != -1:
            return string[:index]

    # 根据办文字号对数据库查询结果进行排序,data为sql查询结果,结构为元组列表[(),(),...,()],index1表示以元组第几个元素作为key,index2表示解析字符串得到第几个数字
    @classmethod
    def sortByKey(cls, data, index1, index2):
        data.sort(key=lambda x: (int(cls.getIntegerFromString(x[index1])[index2])))
        return data

    # 判断excel单元格是否为整数
    @classmethod
    def judgeInteger(cls, cell):
        if isinstance(cell, str):
            return False
        if isinstance(cell, float):
            if cell.is_integer():
                return True
            else:
                return False

    # 判断文件夹中是否有同名文件出现
    @classmethod
    def judgeExistSameNameFile(cls, file_folder_path, filename):
        fileList = os.listdir(file_folder_path)
        if fileList.count(filename) != 0:
            return True
        else:
            return False
