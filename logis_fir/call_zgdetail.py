import os
import shutil
import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

from uipy_dir.zgdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail
import xlrd


class Call_zgdetail(QtWidgets.QWidget, Ui_Form):
    xh = -1  # 整改序号
    xh_lc = -1  # 流程序号
    xh_send = -1  # 发文序号
    send_type = -1  # 发文类型
    xh_rev = -1  # 收文序号

    pro_tag = -1  # 表示问题表是否录入
    zgfh_tag = -1  # 表示整改发函是否录入

    db_path = "../db/database.db"
    zgfh_word_path = "../zgfh_word"

    def __init__(self, key):
        super().__init__()
        self.setupUi(self)
        self.cast(key)
        self.initFunctionButton()

        self.commandLinkButton.clicked.connect(self.btnbasic)
        self.commandLinkButton_2.clicked.connect(self.btnpro)
        self.commandLinkButton_4.clicked.connect(self.btnelse)
        self.commandLinkButton_5.clicked.connect(self.btnanother)
        self.commandLinkButton_6.clicked.connect(self.btnzgfh)
        self.commandLinkButton_7.clicked.connect(self.btnzglr)

        self.tabWidget.setTabText(0, "问题浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.tableWidget.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget.resizeRowsToContents()  # 根据行调整框大小
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改
        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改

        # 初始化要展示的页面是专报还是公文
        if self.send_type == 1:
            self.stackedWidget.setCurrentIndex(6)
        elif self.send_type == 2:
            self.stackedWidget.setCurrentIndex(0)
        # 初始化展示
        self.displaySendDetail()

    def initFunctionButton(self):
        # 打开发文文件
        self.pushButton_file.clicked.connect(
            lambda: self.openfile(file_folder="project_word", file=self.lineEdit_file_3.text()))

        # 打开专报文件
        self.pushButton_file_2.clicked.connect(
            lambda: self.openfile(file_folder="project_word", file=self.lineEdit_file.text()))

        # 打开整改发函文件
        self.pushButton_4.clicked.connect(lambda: self.openfile(file_folder="zgfh_word", file=self.lineEdit.text()))

        # 问题详情查看
        self.pushButton.clicked.connect(self.questionDetail)

        # 选择发函文件
        self.pushButton_5.clicked.connect(self.btnchoosefile1)
        # 保存发函文件
        self.pushButton_6.clicked.connect(self.savezgfh)

        # 选择问题Excel表
        self.pushButton_7.clicked.connect(self.btnchoosefile2)
        # 导入问题整改情况
        self.pushButton_8.clicked.connect(self.importExcel)

    # 用发文字号初始化变量
    def cast(self, key):
        sql = "select bwprocess.序号,bwprocess.发文序号,bwprocess.收文序号 from bwprocess,sendfile where " \
              "bwprocess.发文序号 = sendfile.序号 and sendfile.发文字号 = '%s'" % key
        data = self.executeSql(sql)
        # print(data)
        self.xh_lc = data[0][0]
        self.xh_send = data[0][1]
        self.xh_rev = data[0][2]

        # 初始化整改序号
        sql = "select 序号 from standingbook where 流程序号 = %s" % self.xh_lc
        result = self.executeSql(sql)
        self.xh = result[0][0]

        # 初始化发文类型
        sql = "select projectType from sendfile where 序号 = %s" % self.xh_send
        result = self.executeSql(sql)
        self.send_type = result[0][0]

        # 初始化问题表状态
        sql = "select * from problem where 发文序号 = %s" % self.xh_send
        result = self.executeSql(sql)
        if len(result) != 0:
            self.pro_tag = 1

        # 初始化整改发函录入状态
        sql = "select 整改发函内容 from standingbook where 序号 = %s" % self.xh
        result = self.executeSql(sql)
        if result[0][0] != "":
            self.zgfh_tag = 1

        # 初始化流程状态
        self.commandLinkButton.setDescription("已完成")
        self.commandLinkButton_4.setDescription("已完成")
        self.commandLinkButton_5.setDescription("已完成")
        if self.pro_tag == 1:
            self.commandLinkButton_2.setDescription("已完成")
        if self.zgfh_tag == 1:
            self.commandLinkButton_6.setDescription("已完成")

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

    # source对应的文件复制一份到target(project_word)文件夹下,copy方法保留当前文件权限,暂未考虑同名文件
    def copyFile(self, source, target):
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())

    # 关闭tab
    def mclose(self, index):
        self.tabWidget.removeTab(index)

    # 跳转问题详情
    def questionDetail(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.tableWidget.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择问题！")
        else:
            # 主键1:序号
            key1 = self.tableWidget.item(row, 0).text()
            # 主键2:发文字号
            key2 = self.xh_send
            tab_new = Call_quedetail(key1, key2)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "问题顺序号%s详情" % key1)
            self.tabWidget.setCurrentIndex(tab_num)

    # 根据文件名打开相应文件
    def openfile(self, file_folder, file):
        # 获取文件路径
        path = os.path.dirname(os.getcwd()) + '\\' + file_folder + '\\' + file
        print(path)
        os.startfile(path)

    # 展示问题表格
    def displayqueDetail(self):
        if self.pro_tag != -1:
            # 选出该项目对应的所有问题
            sql = 'select problem.问题顺序号,problem.被审计领导干部,problem.所在地方和单位,sendfile.发文字号,problem.审计报告文号,problem.出具审计报告时间,' \
                  'problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类,' \
                  'problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况 from problem,sendfile where 发文序号 =  %s and ' \
                  'sendfile.序号 = problem.发文序号' % self.xh_send
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
                        self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                    else:
                        self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                    y = y + 1
                x = x + 1

    # 显示公文详情
    def displaySendDetail(self):
        sql = "select 发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
              "领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
              "序号 =  %s" % self.xh_send
        data = self.executeSql(sql)
        # print(data)

        # 专报类型
        if self.send_type == 1:
            self.lineEdit_3.setText(data[0][0])  # 专报标题
            self.lineEdit_4.setText(data[0][1])  # 报送范围
            self.lineEdit_5.setText(data[0][2])  # 发文字号
            self.lineEdit_13.setText(data[0][3])  # 紧急程度
            self.lineEdit_10.setText(data[0][4])  # 秘密等级
            self.lineEdit_14.setText(data[0][5])  # 是否公开
            self.lineEdit_11.setText(data[0][6])  # 拟稿人
            self.lineEdit_15.setText(data[0][7])  # 拟稿处室分管厅领导
            self.lineEdit_12.setText(data[0][8])  # 拟稿处室
            self.lineEdit_16.setText(data[0][9])  # 综合处编辑
            self.lineEdit_18.setText(data[0][10])  # 综合处审核
            self.lineEdit_19.setText(data[0][11])  # 秘书处审核
            self.lineEdit_17.setText(data[0][12])  # 综合处分管厅领导
            self.lineEdit_20.setText(data[0][13])  # 审计办主任
            self.lineEdit_file.setText(data[0][18])  # 报文内容
            self.dateEdit_3.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 办文日期

        # 公文类型
        elif self.send_type == 2:
            self.lineEdit_num.setText(data[0][2])  # 发文字号
            self.lineEdit_num_3.setText(data[0][0])  # 公文标题
            self.textEdit_2.setText(data[0][14])  # 领导审核意见
            self.textEdit_4.setText(data[0][15])  # 审计办领导审核意见
            self.textEdit_3.setText(data[0][16])  # 办文情况说明和拟办意见
            self.lineEdit_file_3.setText(data[0][18])  # 公文内容
            self.lineEdit_22.setText(data[0][4])  # 保密等级
            self.lineEdit_23.setText(data[0][5])  # 是否公开
            self.lineEdit_29.setText(data[0][3])  # 紧急程度
            self.lineEdit_24.setText(data[0][19])  # 审核
            self.lineEdit_26.setText(data[0][20])  # 承办处室
            self.lineEdit_27.setText(data[0][21])  # 承办人
            self.lineEdit_28.setText(data[0][22])  # 联系电话
            self.dateEdit_7.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 办文日期
            self.dateEdit_6.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 日期
            self.lineEdit_25.setText(data[0][2])  # 办文编号

    # 展示收文信息
    def displayRev(self):
        sql = "select 收文收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,收文标题,处理结果,审核,收文字号,收文承办处室,收文承办人,收文联系电话 from revfile where 序号 " \
              "= %s" % self.xh_rev
        data = self.executeSql(sql)
        # print(data)
        self.dateEdit.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
        self.lineEdit_6.setText(data[0][1])  # 密级
        self.lineEdit_7.setText(data[0][2])  # 是否公开
        self.lineEdit_36.setText(data[0][3])  # 紧急程度
        self.lineEdit_38.setText(data[0][4])  # 收文来文单位
        self.lineEdit_37.setText(data[0][5])  # 收文来文字号
        self.lineEdit_35.setText(data[0][6])  # 文件标题
        self.lineEdit_33.setText(data[0][7])  # 处理结果
        self.lineEdit_30.setText(data[0][8])  # 审核
        self.lineEdit_31.setText(data[0][9])  # 办文编号
        self.lineEdit_34.setText(data[0][10])  # 承办处室
        self.lineEdit_32.setText(data[0][11])  # 承办人
        self.lineEdit_39.setText(data[0][12])  # 联系电话

    # 展示批文信息
    def display2Rev(self):
        sql = "select 批文收文时间,秘密等级,是否公开,紧急程度,批文来文单位,批文来文字号,批文标题,处理结果,审核,批文字号,批文承办处室,批文承办人,批文联系电话,内容摘要和拟办意见,领导批示 from " \
              "revfile where 序号 = %s" % self.xh_rev
        data = self.executeSql(sql)
        self.dateEdit_2.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
        self.lineEdit_8.setText(data[0][1])  # 密级
        self.lineEdit_9.setText(data[0][2])  # 是否公开
        self.lineEdit_40.setText(data[0][3])  # 紧急程度
        self.lineEdit_41.setText(data[0][4])  # 批文来文单位
        self.lineEdit_42.setText(data[0][5])  # 批文来文字号
        self.lineEdit_43.setText(data[0][6])  # 文件标题
        self.lineEdit_48.setText(data[0][7])  # 处理结果
        self.lineEdit_49.setText(data[0][8])  # 审核
        self.lineEdit_44.setText(data[0][9])  # 批文编号
        self.lineEdit_45.setText(data[0][10])  # 承办处室
        self.lineEdit_46.setText(data[0][11])  # 承办人
        self.lineEdit_47.setText(data[0][12])  # 联系电话
        self.textEdit_6.setText(data[0][13])  # 内容摘要和拟办意见
        self.textEdit_7.setText(data[0][14])  # 领导批示

    # 展示整改发函页面
    def displayzgfh(self):
        # 根据整改发函是否导入展示不同功能按钮
        if self.zgfh_tag == 1:
            self.pushButton_5.hide()
            self.pushButton_6.hide()
            self.pushButton_4.show()
            sql = "select 整改发函内容 from standingbook where 序号 = %s" % self.xh
            data = self.executeSql(sql)
            self.lineEdit.setText(data[0][0])
        else:
            self.pushButton_5.show()
            self.pushButton_6.show()
            self.pushButton_4.hide()

    # 展示问题总览
    def displayqueoverview(self):
        if self.pro_tag != -1:
            sql = 'select problem.问题顺序号,problem.被审计领导干部,problem.所在地方和单位,sendfile.发文字号,problem.审计报告文号,problem.出具审计报告时间,' \
                  'problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类,' \
                  'problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况,rectification.整改责任部门,rectification.序号,' \
                  'rectification.应上报整改报告时间,rectification.实际上报整改报告时间,rectification.整改情况,rectification.已整改金额,' \
                  'rectification.追责问责人数,rectification.推动制度建设数目,rectification.推动制度建设文件,rectification.部分整改情况具体描述,' \
                  'rectification.未整改原因说明,rectification.下一步整改措施及时限,rectification.认定整改情况,rectification.认定整改金额,' \
                  'rectification.整改率 from problem,sendfile,rectification where problem.发文序号 = %s and sendfile.序号 = ' \
                  'problem.发文序号 and problem.问题顺序号 = rectification.问题顺序号 and problem.发文序号 = rectification.发文序号 order ' \
                  'by problem.问题顺序号,problem.发文序号' % self.xh_send
            data = self.executeSql(sql)

            # 打印结果
            # print(data)

            size = len(data)
            # print("项目数目为:"+str(size))
            self.tableWidget_2.setRowCount(size)

            x = 0
            for i in data:
                y = 0
                for j in i:
                    if data[x][y] is None:
                        self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                    else:
                        self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                    y = y + 1
                x = x + 1

    '''
    # 展示补全信息
    def displayinfo(self):
        if self.info_tag != -1:
            self.pushButton_2.hide()
            sql = "select 委办主任签批意见,批示任务办理要求时间,承办处室及承办人,办理结果,文件去向 from standingbook where 序号 = %s" % self.xh
            data = self.executeSql(sql)
            self.lineEdit_21.setText(data[0][0])  # 委办主任签批意见
            self.dateEdit_4.setDate(QDate.fromString(data[0][1], 'yyyy/M/d'))  # 批示任务办理要求时间
            self.lineEdit_51.setText(data[0][2])  # 审计厅承办处室及承办人
            self.lineEdit_52.setText(data[0][3])  # 办理结果
            self.lineEdit_53.setText(data[0][4])  # 文件去向
    '''

    # 选择整改发函文件
    def btnchoosefile1(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit.setText(p[0])

    # 选择问题表
    def btnchoosefile2(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_2.setText(p[0])

    # 保存整改发函文件
    def savezgfh(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        input_file_path = self.lineEdit.text()
        if input_file_path != "":
            filename = os.path.split(input_file_path)[1]  # 文件名
            sql = "update standingbook set 整改发函内容 = '%s' where 序号 = %s" % (filename, self.xh)
            self.executeSql(sql)
            # 导入文件
            self.copyFile(input_file_path, self.zgfh_word_path)

            # 更新整改发函状态
            self.zgfh_tag = 1
            self.commandLinkButton_6.setDescription("已完成")

            QtWidgets.QMessageBox.information(w, "提示", "保存成功！")

            self.displayzgfh()
        else:
            QtWidgets.QMessageBox.information(w, "提示", "请选择文件!")

    # 根据excel中的右边问题整改信息导入问题表
    def importExcel(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
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
                num = 1  # 要插入数据库中的问题序号
                celli_0 = sheet.row(i)[0].value  # 问题顺序号
                # celli_3 = sheet.row(i)[3].value  # 报送专报期号
                celli_3 = self.xh_send  # 报送专报期号,忽略excel表中发文字号这一列,直接读入发文序号
                celli_16 = sheet.row(i)[16].value  # 整改责任部门
                celli_17 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 17).value, 0).strftime("%Y/%m/%d")  # 应上报整改报告时间
                celli_18 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 18).value, 0).strftime("%Y/%m/%d")  # 实际上报整改报告时间
                celli_19 = sheet.row(i)[19].value  # 整改情况
                celli_20 = sheet.row(i)[20].value  # 已整改金额
                celli_21 = int(sheet.row(i)[21].value)  # 追责问责人数
                celli_22 = int(sheet.row(i)[22].value)  # 推动制度建设数目
                celli_23 = sheet.row(i)[23].value  # 推动制度建设文件
                celli_24 = sheet.row(i)[24].value  # 部分整改情况具体描述
                celli_25 = sheet.row(i)[25].value  # 未整改原因说明
                celli_26 = sheet.row(i)[26].value  # 下一步整改措施及时限
                celli_27 = sheet.row(i)[27].value  # 认定整改情况
                celli_28 = sheet.row(i)[28].value  # 认定整改金额
                celli_29 = sheet.row(i)[29].value  # 整改率

                sql = "select max(序号) from rectification where 问题顺序号 = %s and 发文序号 = %s and 整改责任部门 = '%s'" % (
                    celli_0, celli_3, celli_16)
                data = self.executeSql(sql)

                if data[0][0] is None:
                    num = 1
                else:
                    num = data[0][0] + 1

                sql = "insert into rectification values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s','%s','%s')" % (
                          num, celli_0, celli_3, celli_16, celli_17, celli_18, celli_19, celli_20, celli_21, celli_22,
                          celli_23, celli_24, celli_25, celli_26, celli_27, celli_28, celli_29)
                self.executeSql(sql)

            QtWidgets.QMessageBox.information(w, "提示", "录入成功!")

            self.displayqueoverview()
        else:
            QtWidgets.QMessageBox.information(w, "提示", "请选择文件!")

    '''
    def updateInfo(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常

        input1 = self.lineEdit_21.text()  # 委办主任签批意见
        input2 = self.dateEdit_4.text()  # 批示任务办理要求时间
        input3 = self.lineEdit_51.text()  # 审计厅承办处室及承办人
        input4 = self.lineEdit_52.text()  # 办理结果
        input5 = self.lineEdit_53.text()  # 文件去向
        sql = "update standingbook set 委办主任签批意见 = '%s',批示任务办理要求时间 = '%s',承办处室及承办人 = '%s',办理结果 = '%s',文件去向 = '%s'," \
              "tag = 1 where 序号 = %s" % (input1, input2, input3, input4, input5, self.xh)
        self.executeSql(sql)

        self.info_tag = 1
        self.commandLinkButton_3.setDescription("已完成")

        QtWidgets.QMessageBox.information(w, "提示", "操作成功!")

        # 重新展示补全信息详情页面
        self.displayinfo()
    '''

    def btnbasic(self):
        if self.send_type == 2:
            self.stackedWidget.setCurrentIndex(0)
        elif self.send_type == 1:
            self.stackedWidget.setCurrentIndex(6)
        self.displaySendDetail()

    def btnpro(self):
        self.stackedWidget.setCurrentIndex(2)
        self.displayqueDetail()

    def btnelse(self):
        self.stackedWidget.setCurrentIndex(1)
        self.displayRev()

    def btnanother(self):
        self.stackedWidget.setCurrentIndex(3)
        self.display2Rev()

    def btnzgfh(self):
        self.stackedWidget.setCurrentIndex(4)
        self.displayzgfh()

    def btnzglr(self):
        self.stackedWidget.setCurrentIndex(5)
        self.displayqueoverview()
