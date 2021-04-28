import os
import shutil
import sqlite3


class tools:
    db_path = "../db/database.db"
    project_word_path = "../project_word"
    zgfh_word_path = "../zgfh_word"

    # 执行sql
    @classmethod
    def executeSql(cls, sql):
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

    # 将一个文件复制到某个目录下,source代表源文件路径,target代表目标文件夹目录
    @classmethod
    def copyFile(cls, source, target):
        try:
            shutil.copy(source, target)
        except Exception as e:
            print("Unable to copy file. %s\n" % e)

    # 将一个文件替换掉目录下另一个文件,source代表源文件,target代表目标替换文件名
    @classmethod
    def replaceFile(cls, source, target):
        print(source)
        print(target)
        try:
            if target != "":
                target = cls.project_word_path + '/' + target
                os.remove(target)  # 删除目标文件
            shutil.copy(source, cls.project_word_path)  # 将新文件复制到路径下
        except Exception as e:
            print("Unable to replace file. %s\n" % e)

    # 根据文件名打开相应文件
    @classmethod
    def openFile(cls, file_folder, file):
        if file != "":
            # 获取文件路径
            path = os.path.dirname(os.getcwd()) + '\\' + file_folder + '\\' + file
            try:
                os.startfile(path)
            except Exception as e:
                print("Unable to open file. %s\n" % e)

    # 根据文件路径获取文件名
    @classmethod
    def getFileName(cls, input_file_path):
        return os.path.split(input_file_path)[1]  # 文件名
