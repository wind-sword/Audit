import os
import sqlite3

import xlrd
from PyQt5 import QtCore, QtWidgets

from uipy_dir.zbdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail

class Call_zbdetail(QtWidgets.QWidget,Ui_Form):
    mydata = []
    db_path = "../db/database.db"
    def __init__(self,data):
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

        #self.displayqueDetail()

    # 执行sql语句
    def executeSql(self,sql):
        print("当前需要执行sql:"+sql)
        con = sqlite3.connect(self.db_path)
        print('Opened database successfully')
        cur = con.cursor()
        cur.execute(sql)
        print('Execute sql successfully'+'\n')
        data = cur.fetchall()
        con.commit()
        con.close()
        return data

    #关闭tab
    def mclose(self,index):
        self.tabWidget.removeTab(index)

    # 跳转问题详情
    def jumpqueview(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择问题！")
        else:
            tab_new = Call_quedetail()
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "问题详情")
            self.tabWidget.setCurrentIndex(tab_num)

    def logi(self):
        self.pushButton_file.clicked.connect(self.openFile)

    #根据文件名打开project_word中的专报/公文
    def openFile(self):
        #获取文件路径
        path = os.path.dirname(os.getcwd())+'\project_word\\'+self.lineEdit_file.text()
        print(path)
        os.startfile(path)

    def importExcel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        # 文件路径
        path = p[0]
        path.replace('/','\\\\')

        #获取excel文件
        data = xlrd.open_workbook(path)
        print('All sheets: %s' % data.sheet_names())

        #获取excel第一个sheet,也就是问题表所在sheet
        sheet = data.sheets()[0]
        sheet_name = sheet.name  # 获得名称
        sheet_cols = sheet.ncols  # 获得列数
        sheet_nrows = sheet.nrows  # 获得行数
        print('Sheet Name: %s\nSheet cols: %s\nSheet rows: %s' % (sheet_name, sheet_cols, sheet_nrows))

        #获取第六行数据,也就是问题的数据,后续获取多行数据加上循环,根据具体表结构做修改,此处仅作为演示
        cell5_1 = sheet.row(5)[1].value #被审计领导干部
        cell5_2 = sheet.row(5)[2].value #所在地方或单位
        cell5_3 = sheet.row(5)[3].value #报送文号
        cell5_4 = sheet.row(5)[4].value #审计报告（意见）文号
        cell5_5 = sheet.row(5)[5].value #经责结果报告文号
        cell5_6 = xlrd.xldate.xldate_as_datetime(sheet.cell(5,6).value,0).strftime("%Y/%m/%d")#出具审计报告时间 XXXX-XX-XX
        cell5_7 = sheet.row(5)[7].value #审计组组长
        cell5_8 = sheet.row(5)[8].value #审计组主审
        cell5_9 = sheet.row(5)[9].value #问题描述
        cell5_10 = sheet.row(5)[10].value #是否在审计报告中反映（从下拉菜单中选取）
        cell5_11 = sheet.row(5)[11].value #是否在结果报告中反映（从下拉菜单中选取）
        cell5_12 = sheet.row(5)[12].value #审计对象分类（从下拉菜单中选取）
        cell5_13 = sheet.row(5)[13].value #问题类别（从下拉菜单中选取）
        cell5_14 = sheet.row(5)[14].value #问题定性（从下拉菜单中选取）
        cell5_15 = sheet.row(5)[15].value #问题表现形式（从下拉菜单中选取）
        cell5_16 = sheet.row(5)[16].value #备注（不在前列问题类型中的，简单描述）
        cell5_17 = sheet.row(5)[17].value #问题金额（万元）
        cell5_18 = sheet.row(5)[18].value #移送及处理情况

        sql = "insert into problem values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(cell5_1,cell5_2,cell5_3,cell5_4,cell5_5,cell5_6,cell5_7,cell5_8,cell5_9,cell5_10,cell5_11,cell5_12,cell5_13,cell5_14,cell5_15,cell5_16,cell5_17,cell5_18)
        self.executeSql(sql)

        #导入完成后更新表格
        #self.displayqueDetail()



    #展示项目报文详情
    def displayDetail(self):
        str1 = self.label.text() #专报标题
        self.lineEdit.setText(self.mydata[0][0])

        str2 = self.label_16.text() #报送范围
        self.lineEdit_2.setText(self.mydata[0][1])

        str3 = self.label_4.text() #发文字号
        self.lineEdit_4.setText(self.mydata[0][2])

        str4 = self.label_5.text() #紧急程度
        self.lineEdit_13.setText(self.mydata[0][3])

        str5 = self.label_14.text() #秘密等级
        self.lineEdit_5.setText(self.mydata[0][4])

        str6 = self.label_6.text() #是否公开
        self.lineEdit_14.setText(self.mydata[0][5])

        str7 = self.label_7.text() #拟稿人
        self.lineEdit_8.setText(self.mydata[0][6])

        str8 = self.label_8.text() #拟稿处室分管厅领导
        self.lineEdit_15.setText(self.mydata[0][7])

        str9 = self.label_9.text() #拟稿处室
        self.lineEdit_9.setText(self.mydata[0][8])

        str10 = self.label_10.text() #综合处编辑
        self.lineEdit_10.setText(self.mydata[0][9])

        str11 = self.label_12.text() #综合处审核
        self.lineEdit_11.setText(self.mydata[0][10])

        str12 = self.label_18.text() #秘书处审核
        self.lineEdit_12.setText(self.mydata[0][11])

        str13 = self.label_17.text() #综合处分管厅领导
        self.lineEdit_16.setText(self.mydata[0][12])

        str14 = self.label_15.text() #审计办主任
        self.lineEdit_17.setText(self.mydata[0][13])

        str15 = self.label_file.text() #报文内容
        self.lineEdit_file.setText(self.mydata[0][19])

    #展示问题表格
    def displayqueDetail(self):
        sql = 'select problem.被审计领导干部,problem.所在地方和单位,problem.审计报告文号,problem.出具审计报告时间,problem.审计组组长,problem.审计组主审,problem.审计对象分类,problem.问题类别,problem.问题定性,problem.问题表现形式,problem.问题金额 from problem'
        data = self.executeSql(sql)
        # 打印结果
        #print(data)

        size = len(data)
        #print("项目数目为:"+str(size))
        self.tableWidget.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
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