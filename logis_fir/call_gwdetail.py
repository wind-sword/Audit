import os
import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.gwdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail
import xlrd


class Call_gwdetail(QtWidgets.QWidget, Ui_Form):
    mydata = []
    db_path = "../db/database.db"

    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.logi()
        self.commandLinkButton.clicked.connect(self.btnbasic)
        self.commandLinkButton_2.clicked.connect(self.btnpro)
        self.commandLinkButton_3.clicked.connect(self.btnimport)
        self.commandLinkButton_4.clicked.connect(self.btnelse)
        self.commandLinkButton_5.clicked.connect(self.btnanother)

        self.pushButton.clicked.connect(self.jumpqueview)
        self.tabWidget.setTabText(0, "问题浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.mydata = data
        self.displayDetail()
        self.displayqueDetail()

    def logi(self):
        self.pushButton_file.clicked.connect(self.openFile)
        self.pushButton_queimport.clicked.connect(self.importExcel)

    # 执行sql语句
    def executeSql(self, sql):
        print("当前需要执行sql:" + sql)
        con = sqlite3.connect(self.db_path)
        print('Opened database successfully')
        cur = con.cursor()
        cur.execute(sql)
        print('Execute sql successfully' + '\n')
        data = cur.fetchall()
        con.commit()
        con.close()
        return data

    # 关闭tab
    def mclose(self, index):
        self.tabWidget.removeTab(index)

    # 跳转问题详情
    def jumpqueview(self):
        row = self.tableWidget.currentRow()
        key = self.tableWidget.item(row, 2).text()
        sql = "select problem.被审计领导干部,problem.所在地方和单位,problem.出具审计报告时间,problem.审计组主审,problem.审计组组长,problem.发文字号,problem.审计报告文号,problem.问题描述"
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择问题！")
        else:
            tab_new = Call_quedetail()
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "问题详情")
            self.tabWidget.setCurrentIndex(tab_num)

    # 根据文件名打开project_word中的专报/公文
    def openFile(self):
        # 获取文件路径
        path = os.path.dirname(os.getcwd()) + '\project_word\\' + self.lineEdit_file_3.text()
        print(path)
        os.startfile(path)

    def importExcel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        # 文件路径
        path = p[0]
        path.replace('/', '\\\\')
        # 用户没有选择文件
        if path != "":
            # 获取excel文件
            data = xlrd.open_workbook(path)
            print('All sheets: %s' % data.sheet_names())

            # 获取excel第一个sheet,也就是问题表所在sheet
            sheet = data.sheets()[0]
            sheet_name = sheet.name  # 获得名称
            sheet_cols = sheet.ncols  # 获得列数
            sheet_nrows = sheet.nrows  # 获得行数
            print('Sheet Name: %s\nSheet cols: %s\nSheet rows: %s' % (sheet_name, sheet_cols, sheet_nrows))

            # 获取第六行数据,也就是问题的数据,后续获取多行数据加上循环,根据具体表结构做修改,此处仅作为演示
            cell5_0 = sheet.row(4)[0].value  # 问题顺序号
            cell5_1 = sheet.row(4)[1].value  # 被审计对象
            cell5_2 = sheet.row(4)[2].value  # 所在地方或单位
            cell5_3 = sheet.row(4)[3].value  # 报送专报期号
            cell5_4 = sheet.row(4)[4].value  # 审计报告（意见）文号
            cell5_5 = xlrd.xldate.xldate_as_datetime(sheet.cell(4, 5).value, 0).strftime(
                "%Y/%m/%d")  # 出具出具审计专报时间 XXXX-XX-XX
            cell5_6 = sheet.row(4)[6].value  # 审计组组长
            cell5_7 = sheet.row(4)[7].value  # 审计组主审
            cell5_8 = sheet.row(4)[8].value  # 问题描述
            cell5_9 = sheet.row(4)[9].value  # 问题一级分类
            cell5_10 = sheet.row(4)[10].value  # 问题二级分类
            cell5_11 = sheet.row(4)[11].value  # 问题三级分类
            cell5_12 = sheet.row(4)[12].value  # 问题四级分类
            cell5_13 = sheet.row(4)[13].value  # 备注（不在前列问题类型中的，简单描述）
            cell5_14 = sheet.row(4)[14].value  # 问题金额（万元）
            cell5_15 = sheet.row(4)[15].value  # 移送及处理情况

            if cell5_3 == self.mydata[0][2]:
                sql = "insert into problem values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s')" % (cell5_0, cell5_1, cell5_2, cell5_3, cell5_4, cell5_5, cell5_6, cell5_7,
                                           cell5_8, cell5_9, cell5_10, cell5_11, cell5_12, cell5_13, cell5_14, cell5_15)
                print(sql)
                self.executeSql(sql)
            else:
                QtWidgets.QMessageBox.information(self, "提示", "问题表与发文文号不符！")

            # 导入完成后更新表格
            self.displayqueDetail()

    # 显示公文详情
    def displayDetail(self):
        str1 = self.label_num.text()  # 发文字号
        self.lineEdit_num.setText(self.mydata[0][2])

        str2 = self.label_num_3.text()  # 公文标题
        self.lineEdit_num_3.setText(self.mydata[0][14])

        str3 = self.label_num_4.text()  # 领导审核意见
        self.textEdit_2.setText(self.mydata[0][15])

        str4 = self.label_num_5.text()  # 审计办领导审核意见
        self.textEdit_4.setText(self.mydata[0][16])

        str5 = self.label_num_6.text()  # 办文情况说明和拟办意见
        self.textEdit_3.setText(self.mydata[0][17])

        str6 = self.label_file_3.text()  # 公文内容
        self.lineEdit_file_3.setText(self.mydata[0][19])

        str7 = self.label_26.text()  # 保密等级
        self.lineEdit_22.setText(self.mydata[0][4])

        str8 = self.label_27.text()  # 是否公开
        self.lineEdit_23.setText(self.mydata[0][5])

        str9 = self.label_35.text()  # 紧急程度
        self.lineEdit_29.setText(self.mydata[0][3])

        str10 = self.label_28.text()  # 审核
        self.lineEdit_24.setText(self.mydata[0][20])

        str11 = self.label_31.text()  # 承办处室
        self.lineEdit_26.setText(self.mydata[0][21])

        str12 = self.label_32.text()  # 承办人
        self.lineEdit_27.setText(self.mydata[0][22])

        str13 = self.label_33.text()  # 联系电话
        self.lineEdit_28.setText(self.mydata[0][23])

        str14 = self.label_34.text()  # 办文日期
        self.dateEdit_7.setDate(QDate.fromString(self.mydata[0][24], 'yyyy/M/d'))

        str15 = self.label_29.text()  # 日期
        self.dateEdit_6.setDate(QDate.fromString(self.mydata[0][24], 'yyyy/M/d'))

        str16 = self.label_30.text()  # 办文编号
        self.lineEdit_25.setText(self.mydata[0][2])

    # 展示问题表格
    def displayqueDetail(self):
        # 选出该项目对应的所有问题
        sql = 'select problem.问题顺序号,problem.被审计领导干部,problem.所在地方和单位,problem.发文字号,problem.审计报告文号,problem.出具审计报告时间,problem.审计组组长,' \
              'problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类,problem.问题四级分类,problem.备注,' \
              'problem.问题金额,problem.移送及处理情况 from problem where 发文字号 =  \'%s\'' % self.mydata[0][2]
        data = self.executeSql(sql)
        # 打印结果
        # print(data)

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem("无"))
                else:
                    self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

    def btnbasic(self):
        self.stackedWidget.setCurrentIndex(0)

    def btnpro(self):
        self.stackedWidget.setCurrentIndex(2)

    def btnimport(self):
        self.stackedWidget.setCurrentIndex(3)

    def btnelse(self):
        self.stackedWidget.setCurrentIndex(1)

    def btnanother(self):
        self.stackedWidget.setCurrentIndex(4)
