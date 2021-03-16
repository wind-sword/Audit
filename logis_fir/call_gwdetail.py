import os
import shutil
import sqlite3
import sys

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
        self.commandLinkButton_6.clicked.connect(self.btnzgfh)
        self.commandLinkButton_7.clicked.connect(self.btnzglr)

        self.tabWidget.setTabText(0, "问题浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.mydata = data
        self.displayDetail()

    def logi(self):
        # 打开公文文件
        self.pushButton_file.clicked.connect(self.openFile)
        # 导入问题表
        self.pushButton_queimport.clicked.connect(self.importExcel1)
        # 问题详情查看
        self.pushButton.clicked.connect(self.jumpqueview)

        # 录入收文信息
        self.pushButton_3.clicked.connect(self.insertrev)
        # 录入批文信息
        self.pushButton_4.clicked.connect(self.insertprev)

        # 选择发函文件
        self.pushButton_5.clicked.connect(self.btnchoosefile1)
        # 保存发函文件
        self.pushButton_6.clicked.connect(self.savefile1)

        # 选择问题Excel表
        self.pushButton_7.clicked.connect(self.btnchoosefile2)
        # 导入问题整改情况
        self.pushButton_8.clicked.connect(self.importExcel2)

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
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择问题！")
        else:
            # 主键1:序号
            key1 = self.tableWidget.item(row, 0).text()
            # 主键2:发文字号
            key2 = self.tableWidget.item(row, 3).text()
            sql = "select problem.被审计领导干部,problem.所在地方和单位,problem.出具审计报告时间,problem.审计组主审,problem.审计组组长,problem.发文字号," \
                  "problem.审计报告文号,problem.问题描述 from problem where 问题顺序号 = \'%s\' and 发文字号 =  \'%s\'" % (key1, key2)
            data = self.executeSql(sql)
            print(data)
            tab_new = Call_quedetail(data)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "序号%s问题详情" % key1)
            self.tabWidget.setCurrentIndex(tab_num)

    # 保存整改发函文件(暂未实现)
    def savefile1(self):
        print("保存整改发函文件成功")

    # source对应的文件复制一份到target(project_word)文件夹下,copy方法保留当前文件权限,暂未考虑同名文件
    def copyFile(self, source, target):
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())

    # 根据文件名打开project_word中的专报/公文
    def openFile(self):
        # 获取文件路径
        path = os.path.dirname(os.getcwd()) + '\project_word\\' + self.lineEdit_file_3.text()
        print(path)
        os.startfile(path)

    # 根据excel中的左边问题基本信息导入问题表
    def importExcel1(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        # 文件路径
        path = p[0]
        path.replace('/', '\\\\')

        # 判断用户是否选择文件
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

            # 读取excel数据
            for i in range(4, sheet_nrows):
                celli_0 = sheet.row(i)[0].value  # 问题顺序号
                celli_1 = sheet.row(i)[1].value  # 被审计对象
                celli_2 = sheet.row(i)[2].value  # 所在地方或单位
                celli_3 = sheet.row(i)[3].value  # 报送专报期号
                celli_4 = sheet.row(i)[4].value  # 审计报告（意见）文号
                celli_5 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 5).value, 0).strftime(
                    "%Y/%m/%d")  # 出具出具审计专报时间 XXXX-XX-XX
                celli_6 = sheet.row(i)[6].value  # 审计组组长
                celli_7 = sheet.row(i)[7].value  # 审计组主审
                celli_8 = sheet.row(i)[8].value  # 问题描述
                celli_9 = sheet.row(i)[9].value  # 问题一级分类
                celli_10 = sheet.row(i)[10].value  # 问题二级分类
                celli_11 = sheet.row(i)[11].value  # 问题三级分类
                celli_12 = sheet.row(i)[12].value  # 问题四级分类
                celli_13 = sheet.row(i)[13].value  # 备注（不在前列问题类型中的，简单描述）
                celli_14 = sheet.row(i)[14].value  # 问题金额（万元）
                celli_15 = sheet.row(i)[15].value  # 移送及处理情况

                sql = "insert into problem values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s')" % (celli_0, celli_1, celli_2, celli_3, celli_4, celli_5, celli_6, celli_7,
                                           celli_8, celli_9, celli_10, celli_11, celli_12, celli_13, celli_14, celli_15)
                print(sql)
                self.executeSql(sql)

            # 导入完成后更新表格
            self.displayqueDetail()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请选择文件!")

    # 根据excel中的右边问题整改信息导入问题表
    def importExcel2(self):
        path = self.lineEdit_2.text()
        path.replace('/', '\\\\')
        # 判断用户是否选择文件
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

            # 读取excel数据
            for i in range(4, sheet_nrows):
                celli_0 = sheet.row(i)[0].value  # 问题顺序号
                celli_3 = sheet.row(i)[3].value  # 报送专报期号
                celli_16 = sheet.row(i)[16].value  # 整改责任部门
                celli_17 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 17).value, 0).strftime("%Y/%m/%d") # 应上报整改报告时间
                celli_18 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 18).value, 0).strftime("%Y/%m/%d")# 实际上报整改报告时间
                celli_19 = sheet.row(i)[19].value  # 整改情况
                celli_20 = sheet.row(i)[20].value  # 已整改金额
                celli_21 = sheet.row(i)[21].value  # 追责问责人数
                celli_22 = sheet.row(i)[22].value  # 推动制度建设数目
                celli_23 = sheet.row(i)[23].value  # 推动制度建设文件
                celli_24 = sheet.row(i)[24].value  # 部分整改情况具体描述
                celli_25 = sheet.row(i)[25].value  # 未整改原因说明
                celli_26 = sheet.row(i)[26].value  # 下一步整改措施及时限
                celli_27 = sheet.row(i)[27].value  # 认定整改情况
                celli_28 = sheet.row(i)[28].value  # 认定整改金额
                celli_29 = sheet.row(i)[29].value  # 整改率

                sql = "insert into rectification values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s')" % (celli_0,celli_3,celli_16, celli_17, celli_18, celli_19, celli_20, celli_21, celli_22, celli_23,
                                 celli_24, celli_25, celli_26, celli_27, celli_28, celli_29)
                print(sql)
                self.executeSql(sql)
            QtWidgets.QMessageBox.information(self, "提示", "录入成功!")
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请选择文件!")

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

    # 展示收文信息,同时判断是应该插入收文还是修改收文
    def displayrev(self):
        sql = "select 收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,文件标题,处理结果,审核,发文字号,承办处室,承办人,联系电话 from revfile where 发文字号 = " \
              "\'%s\'" % self.mydata[0][2]
        data = self.executeSql(sql)
        # print(data)
        if len(data) == 0:

            # 从公文信息中读取已知信息填充
            self.lineEdit_6.setText(self.mydata[0][4])  # 密级
            self.lineEdit_7.setText(self.mydata[0][5])  # 是否公开
            self.lineEdit_36.setText(self.mydata[0][3])  # 紧急程度
            self.lineEdit_35.setText(self.mydata[0][14])  # 文件标题
            self.lineEdit_31.setText(self.mydata[0][2])  # 办文编号
            self.lineEdit_34.setText(self.mydata[0][21])  # 承办处室
            self.lineEdit_32.setText(self.mydata[0][22])  # 承办人
            self.lineEdit_39.setText(self.mydata[0][23])  # 电话

        else:
            # 有数据就隐藏插入按钮
            self.pushButton_3.hide()

            str1 = self.label_11.text()  # 收文时间
            self.dateEdit.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))

            str2 = self.label_19.text()  # 密级
            self.lineEdit_6.setText(data[0][1])

            str3 = self.label_39.text()  # 是否公开
            self.lineEdit_7.setText(data[0][2])

            str4 = self.label_44.text()  # 紧急程度
            self.lineEdit_36.setText(data[0][3])

            str5 = self.label_47.text()  # 来文单位
            self.lineEdit_38.setText(data[0][4])

            str6 = self.label_45.text()  # 来文字号
            self.lineEdit_37.setText(data[0][5])

            str7 = self.label_43.text()  # 文件标题
            self.lineEdit_35.setText(data[0][6])

            str8 = self.label_41.text()  # 处理结果
            self.lineEdit_33.setText(data[0][7])

            str9 = self.label_36.text()  # 审核
            self.lineEdit_30.setText(data[0][8])

            str10 = self.label_37.text()  # 办文编号
            self.lineEdit_31.setText(data[0][9])

            str11 = self.label_42.text()  # 承办处室
            self.lineEdit_34.setText(data[0][10])

            str12 = self.label_38.text()  # 承办人
            self.lineEdit_32.setText(data[0][11])

            str13 = self.label_48.text()  # 联系电话
            self.lineEdit_39.setText(data[0][12])

    # 展示收文信息,同时判断是应该录入还是修改收文
    def displayprev(self):
        # 将收文表字段复制过来
        self.dateEdit_2.setDate(self.dateEdit.date())  # 收文时间
        self.lineEdit_8.setText(self.lineEdit_6.text())  # 密级
        self.lineEdit_9.setText(self.lineEdit_7.text())  # 是否公开
        self.lineEdit_40.setText(self.lineEdit_36.text())  # 紧急程度
        self.lineEdit_43.setText(self.lineEdit_35.text())  # 文件标题
        self.lineEdit_48.setText(self.lineEdit_33.text())  # 处理结果
        self.lineEdit_49.setText(self.lineEdit_30.text())  # 审核
        self.lineEdit_44.setText(self.lineEdit_31.text())  # 办文编号
        self.lineEdit_45.setText(self.lineEdit_34.text())  # 承办处室
        self.lineEdit_46.setText(self.lineEdit_32.text())  # 承办人
        self.lineEdit_47.setText(self.lineEdit_39.text())  # 联系电话
        sql = "select 内容摘要和拟办意见,领导批示,批文来文单位,批文来文字号 from revfile where 发文字号 = \'%s\'" % self.mydata[0][2]
        data = self.executeSql(sql)
        # 批文表中有数据录入了则隐藏插入按钮
        if not (data[0][0] is None and data[0][1] is None and data[0][2] is None and data[0][3] is None):
            self.pushButton_4.hide()
            self.lineEdit_41.setText(data[0][2])  # 批文来文单位
            self.lineEdit_42.setText(data[0][3])  # 批文来文字号
            self.textEdit_6.setText(data[0][0])  # 内容摘要和拟办意见
            self.textEdit_7.setText(data[0][1])  # 领导批示

    # 插入收文表
    def insertrev(self):
        input1 = self.dateEdit.text()  # 收文时间
        input2 = self.lineEdit_6.text()  # 密级
        input3 = self.lineEdit_7.text()  # 是否公开
        input4 = self.lineEdit_36.text()  # 紧急程度
        input5 = self.lineEdit_38.text()  # 收文来文单位
        input6 = self.lineEdit_37.text()  # 收文来文字号
        input7 = self.lineEdit_35.text()  # 文件标题
        input8 = self.lineEdit_33.text()  # 处理结果
        input9 = self.lineEdit_30.text()  # 审核
        input10 = self.lineEdit_31.text()  # 办文编号
        input11 = self.lineEdit_34.text()  # 承办处室
        input12 = self.lineEdit_32.text()  # 承办人
        input13 = self.lineEdit_39.text()  # 联系电话
        # 执行插入
        sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,文件标题,处理结果,审核,发文字号,承办处室,承办人,联系电话) values('%s','%s'," \
              "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  input1, input2, input3, input4, input5, input6,
                  input7, input8, input9, input10, input11,
                  input12, input13)
        self.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

        # 录入成功后显示
        self.displayrev()

    # 更新收文表
    def updaterev(self):
        print("更新收文表")

    # 插入批文表
    def insertprev(self):
        input1 = self.lineEdit_41.text()  # 批文来文单位
        input2 = self.lineEdit_42.text()  # 批文来文字号
        input3 = self.textEdit_6.toPlainText()  # 内容摘要和拟办意见
        input4 = self.textEdit_7.toPlainText()  # 领导批示
        sql = "update revfile set 批文来文单位 = '%s',批文来文字号 = '%s',内容摘要和拟办意见 = '%s',领导批示 = '%s' where 发文字号 = '%s'" \
              % (input1, input2, input3, input4, self.mydata[0][2])
        self.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

        # 录入成功后显示
        self.displayprev()

    # 更新批文表
    def updateprev(self):
        print("更新批文表")

    # 选择整改发函文件
    def btnchoosefile1(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit.setText(p[0])

    # 选择问题表
    def btnchoosefile2(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_2.setText(p[0])

    def btnbasic(self):
        self.stackedWidget.setCurrentIndex(0)
        self.displayDetail()

    def btnpro(self):
        self.stackedWidget.setCurrentIndex(2)
        self.displayqueDetail()

    def btnimport(self):
        self.stackedWidget.setCurrentIndex(3)

    def btnelse(self):
        self.stackedWidget.setCurrentIndex(1)
        self.displayrev()

    def btnanother(self):
        self.stackedWidget.setCurrentIndex(4)
        self.displayprev()

    def btnzgfh(self):
        self.stackedWidget.setCurrentIndex(5)

    def btnzglr(self):
        self.stackedWidget.setCurrentIndex(6)
