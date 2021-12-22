import os
import shutil
import sqlite3
import re
import subprocess
import sys
import traceback
import xlwt
from PyQt5 import QtWidgets

from logis_fir.logger import Logger


class tools:
    # 注意这些路径都是相对于根目录下的,由于main函数运行在跟目录下,所以在logis_fir的py文件中使用./而不是../
    db_path = "./db/database.db"
    project_word_path = "./project_word"
    zgfh_word_path = "./zgfh_word"
    sjyj_word_path = "./sjyj_word"
    sjbg_word_path = "./sjbg_word"
    sjjg_word_path = "./sjjg_word"

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
            if source != "":
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

    # 根据办文字号对数据库查询结果进行排序,data为sql查询结果,结构为元组列表[(),(),...,()]
    # @param index:表示以data中元组的哪一个下标的元素为依据进行排序
    # @param numOfIndex:表示元素中有几个数字
    @classmethod
    def sortByKey(cls, data, index, numOfIndex):
        if numOfIndex == 1:
            data.sort(key=lambda x: (int(cls.getIntegerFromString(x[index])[0])))
        elif numOfIndex == 2:
            data.sort(key=lambda x: (-int(cls.getIntegerFromString(x[index])[0]),
                                     int(cls.getIntegerFromString(x[index])[1])))
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

    @classmethod
    def excelOut(cls, name, tableWidget):
        # 设置表头格式
        style_head = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = u'微软雅黑'
        font.color = 'black'
        font.height = 230  # 字体大小
        style_head.font = font
        # 设置表头字体在单元格的位置
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
        style_head.alignment = alignment
        # 给表头单元格加框线
        border = xlwt.Borders()
        border.left = xlwt.Borders.THIN  # 左
        border.top = xlwt.Borders.THIN  # 上
        border.right = xlwt.Borders.THIN  # 右
        border.bottom = xlwt.Borders.THIN  # 下
        border.left_colour = 0x40  # 设置框线颜色，0x40是黑色
        border.right_colour = 0x40
        border.top_colour = 0x40
        border.bottom_colour = 0x40
        style_head.borders = border

        # 设置输出字体格式及大小
        style = xlwt.XFStyle()
        font1 = xlwt.Font()
        font1.name = u'宋体'
        font1.color = 'black'
        font1.height = 220  # 字体大小，220就是11号字体
        style.font = font1
        # 设置输出字体在单元格的位置
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
        style.alignment = alignment
        # 给输出单元格加框线
        border = xlwt.Borders()
        border.left = xlwt.Borders.THIN  # 左
        border.top = xlwt.Borders.THIN  # 上
        border.right = xlwt.Borders.THIN  # 右
        border.bottom = xlwt.Borders.THIN  # 下
        border.left_colour = 0x40  # 设置框线颜色，0x40是黑色
        border.right_colour = 0x40
        border.top_colour = 0x40
        border.bottom_colour = 0x40
        style.borders = border
        # 设置输出内容单元格高度
        out_high_style = xlwt.easyxf('font:height 300')
        work_book = xlwt.Workbook(encoding='utf-8')
        sheet = work_book.add_sheet(name, cell_overwrite_ok=True)

        #获取表格行数和列数
        rows = tableWidget.rowCount()
        cols = tableWidget.columnCount()

        #设置表头
        for i in range(cols):
            sheet.write(0, i, tableWidget.horizontalHeaderItem(i).text(), style_head)

        print(cols)
        for i in range(rows):
            # 因为是边读边写，所以每次写完后，要把上次存储的数据清空，存储下一行读取的数据
            mainList = []
            # tableWidget一共有9列,去掉序号列
            for j in range(0, cols):
                mainList.append(tableWidget.item(i, j).text())  # 添加到数组
                # 把mainList中的数据写入表格
                sheet.write(i + 1, j, mainList[j], style)
                # 设置当前列的高度
                sheet.row(i + 1).set_style(out_high_style)
        # 设置表头单元格高度
        head_high_style = xlwt.easyxf('font:height 400')
        sheet.row(0).set_style(head_high_style)
        # 保存
        try:
            work_book.save('./' + name + '.xls')
        except:
            log = Logger('./log/logfile.log', level='error')
            log.logger.error("错误:%s", traceback.format_exc())
        else:
            QtWidgets.QMessageBox.information(None, "提示", "导出成功")
        print(3)