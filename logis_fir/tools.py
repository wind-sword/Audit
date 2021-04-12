import os
import shutil
import sqlite3


class tools:
    db_path = "../db/database.db"
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

    # 将一个文件复制到某个目录下
    @classmethod
    def copyFile(cls, source, target):
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)

    # 根据文件名打开相应文件
    @classmethod
    def openFile(cls, file_folder, file):
        # 获取文件路径
        path = os.path.dirname(os.getcwd()) + '\\' + file_folder + '\\' + file
        # print(path)
        os.startfile(path)

