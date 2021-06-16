import datetime
import traceback

import xlrd
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from qtpy import QtCore

from uipy_dir.lcdetail import Ui_Form
from logis_fir.tools import tools
from logis_fir.logger import Logger


class Call_lcdetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        # 成员变量
        self.xh = -1  # 流程序号
        self.xh_send = -1  # 发文序号
        self.xh_rev = -1  # 收文序号
        self.xh_cor_list = []  # 批文序号列表,元素为(批文序号,批文字号)
        self.send_type = -1  # 发文类型
        self.pro_tag = -1  # 问题表是否导入

        # 页面上方流程按钮跳转
        self.commandLinkButton_1.clicked.connect(lambda: self.btjump(btname="1"))
        self.commandLinkButton_2.clicked.connect(lambda: self.btjump(btname="2"))
        self.commandLinkButton_3.clicked.connect(lambda: self.btjump(btname="3"))
        self.commandLinkButton_4.clicked.connect(lambda: self.btjump(btname="4"))

        # 控件功能绑定相应功能函数
        self.initControlFunction()

        # 同步公文页面输入框:日期和办文编号
        self.dateEdit_6.dateChanged.connect(self.autoSyn1)
        self.dateEdit_7.dateChanged.connect(self.autoSyn2)
        self.spinBox_2.valueChanged.connect(self.autoSyn3)
        self.spinBox_3.valueChanged.connect(self.autoSyn3)

        # 同步批文输入框的三个list高亮情况
        self.listWidget.currentRowChanged.connect(self.autoHighlight1)
        self.listWidget_2.currentRowChanged.connect(self.autoHighlight2)
        self.listWidget_3.currentRowChanged.connect(self.autoHighlight3)

        # 初始化流程变量
        self.initVar(key)

        # 初始化页面展示情况
        self.initView()

        # 初始化页面数据
        if self.xh_send != -1:
            self.displaySendFile()
        elif self.xh_send == -1 and self.xh_rev != -1:
            self.displayRevFile()

        print("当前流程序号:%s" % self.xh)
        print("当前发文序号:%s" % self.xh_send)
        print("当前收文序号:%s" % self.xh_rev)
        print("当前批文序号列表:%s" % self.xh_cor_list)
        print("当前发文类型:%s" % self.send_type)
        print("当前问题表导入情况:%s\n" % self.pro_tag)

    # 页面上方流程按钮跳转,同时刷新页面
    def btjump(self, btname):
        if btname == "1":
            '''
            # 将选择stackedWidget的逻辑写在display中,可以解决一些初始化显示的问题
            if self.send_type == 1:
                self.stackedWidget.setCurrentIndex(0)
            elif self.send_type == 2:
                self.stackedWidget.setCurrentIndex(1)
            '''
            self.displaySendFile()
        elif btname == "2":
            # self.stackedWidget.setCurrentIndex(2)
            self.displayQuestionDetail()
        elif btname == "3":
            # self.stackedWidget.setCurrentIndex(3)
            self.displayRevFile()
        elif btname == "4":
            # self.stackedWidget.setCurrentIndex(4)
            self.displayCorFile()

    # 控件绑定功能函数
    def initControlFunction(self):
        # 专报/公文下按钮绑定增删改查功能
        self.pushButton_2.clicked.connect(lambda: self.reviseSendFile(btname="gw"))
        self.pushButton_5.clicked.connect(lambda: self.reviseSendFile(btname="zb"))

        self.pushButton_8.clicked.connect(lambda: self.updateSendFile(btname="gw"))
        self.pushButton.clicked.connect(lambda: self.updateSendFile(btname="zb"))

        self.pushButton_9.clicked.connect(lambda: self.cancelSendFile(btname="gw"))
        self.pushButton_10.clicked.connect(lambda: self.cancelSendFile(btname="zb"))

        # 收文下按钮绑定增删改查功能
        self.pushButton_3.clicked.connect(self.insertRevFile)
        self.pushButton_6.clicked.connect(self.reviseRevFile)
        self.pushButton_11.clicked.connect(self.updateRevFile)
        self.pushButton_12.clicked.connect(self.cancelRevFile)

        # 批文下按钮绑定增删改查功能
        self.pushButton_4.clicked.connect(self.insertCorFile)
        self.pushButton_7.clicked.connect(self.reviseCorFile)
        self.pushButton_13.clicked.connect(self.insertOrUpdateCorFile)
        self.pushButton_14.clicked.connect(self.cancelCorFile)

        # 批文下的list增加删除条目功能
        self.pushButton_add.clicked.connect(self.addTerm)
        self.pushButton_sub.clicked.connect(self.subTerm)

        # 绑定下拉框切换
        self.comboBox.currentIndexChanged.connect(
            lambda: self.displayCorFileForIndex(xh_cur_cor=self.xh_cor_list[self.comboBox.currentIndex()][0]))

        # 选择问题Excel表
        self.pushButton_quechoose.clicked.connect(self.chooseProblemTable)

        # 导入问题表
        self.pushButton_queimport.clicked.connect(self.importExcelProblem)

        # 打开公文文件
        self.pushButton_opfile.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file_3.text()))

        # 打开专报文件
        self.pushButton_opfile_2.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file.text()))

        # 选择公文文件
        self.pushButton_file.clicked.connect(self.choose_file_gw)

        # 选择专报文件
        self.pushButton_file_2.clicked.connect(self.choose_file_zb)

    # 同步公文输入框内容
    def autoSyn1(self):
        self.dateEdit_7.setDate(self.dateEdit_6.date())

    def autoSyn2(self):
        self.dateEdit_6.setDate(self.dateEdit_7.date())

    def autoSyn3(self):
        cur = self.comboBox_10.currentText() + '[' + self.spinBox_2.text() + ']' + self.spinBox_3.text() + \
              self.label_51.text()
        self.lineEdit_25.setText(cur)

    # 同步批文页面list高亮
    def autoHighlight1(self):
        index = self.listWidget.currentRow()
        self.listWidget_2.setCurrentRow(index)
        self.listWidget_3.setCurrentRow(index)

    def autoHighlight2(self):
        index = self.listWidget_2.currentRow()
        self.listWidget.setCurrentRow(index)
        self.listWidget_3.setCurrentRow(index)

    def autoHighlight3(self):
        index = self.listWidget_3.currentRow()
        self.listWidget.setCurrentRow(index)
        self.listWidget_2.setCurrentRow(index)

    # 用流程表中的序号初始化各变量
    def initVar(self, key):
        self.xh = key
        sql = "select 发文序号,收文序号 from bwprocess where 序号 = %s" % self.xh
        data = tools.executeSql(sql)
        # 表明发文字号不为空,对各状态变量初始化
        if data[0][0] is not None:
            self.xh_send = data[0][0]

            # 初始化发文类型
            sql = "select projectType from sendfile where 序号 = %s" % self.xh_send
            result = tools.executeSql(sql)
            self.send_type = result[0][0]

            # 初始化问题表状态
            sql = "select * from problem where 发文序号 = %s" % self.xh_send
            result = tools.executeSql(sql)
            if len(result) != 0:
                self.pro_tag = 1

        # 判断收文序号是否存在
        if data[0][1] is not None:
            # 初始化收文序号
            self.xh_rev = data[0][1]

        # 初始化批文序号列表
        sql = 'select bw_cast_cor.批文序号,corfile.批文字号 from bw_cast_cor,corfile where bw_cast_cor.流程序号 = %s and ' \
              'bw_cast_cor.批文序号 = corfile.序号' % self.xh
        result = tools.executeSql(sql)
        # 如果有批文序号,那么初始化批文序号列表
        if len(result) != 0:
            self.xh_cor_list = result

    # 从初始化的变量情况判断要展示的页面
    def initView(self):
        # 没有发文流程
        if self.xh_send == -1:
            self.commandLinkButton_1.hide()
            self.commandLinkButton_2.hide()
            self.stackedWidget.setCurrentIndex(3)
        # 有发文流程
        else:
            # 专报类型
            if self.send_type == 1:
                self.stackedWidget.setCurrentIndex(0)
            # 公文类型
            elif self.send_type == 2:
                self.stackedWidget.setCurrentIndex(1)

    # 展示问题表格
    def displayQuestionDetail(self):
        # 表格不可修改
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 文件路径不可编辑
        self.lineEdit_3.setReadOnly(True)
        # 问题已导入时,隐藏相关信息
        if self.pro_tag != -1:
            self.pushButton_quechoose.hide()
            self.pushButton_queimport.hide()
            self.lineEdit_3.hide()
            self.label_23.hide()
        # 选出该项目对应的所有问题
        sql = 'select problem.问题顺序号,problem.被审计领导干部,problem.所在地方或单位,sendfile.发文字号,problem.审计报告文号,problem.出具审计报告时间,' \
              'problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类,problem.问题四级分类,' \
              'problem.备注,problem.问题金额,problem.移送及处理情况 from problem,sendfile where problem.发文序号 = %s and sendfile.序号 ' \
              '= problem.发文序号' % self.xh_send
        data = tools.executeSql(sql)
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

        self.tableWidget.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget.resizeRowsToContents()  # 根据内容调整框大小

        self.stackedWidget.setCurrentIndex(2)

    # 展示发文页面
    def displaySendFile(self):
        if self.xh_send != -1:
            sql = "select 发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
                  "领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
                  "序号 =  %s" % self.xh_send
            data = tools.executeSql(sql)
            # print(data)
            # 专报类型
            if self.send_type == 1:
                # 隐藏确认按钮,取消按钮,替换文件按钮
                self.pushButton.hide()
                self.pushButton_10.hide()
                self.pushButton_file_2.hide()

                # 显示修改按钮,打开文件按钮
                self.pushButton_5.show()
                self.pushButton_opfile_2.show()

                self.lineEdit.setText(data[0][0])  # 发文标题
                self.lineEdit_2.setText(data[0][1])  # 报送范围
                self.spinBox.setValue(int(tools.getIntegerFromString(data[0][2])[0]))  # 发文字号
                self.comboBox_2.setCurrentText(data[0][3])  # 紧急程度
                self.lineEdit_5.setText(data[0][4])  # 秘密等级
                self.comboBox_3.setCurrentText(data[0][5])  # 是否公开
                self.lineEdit_10.setText(data[0][6])  # 拟稿人
                self.lineEdit_15.setText(data[0][7])  # 拟稿处室分管厅领导
                self.lineEdit_11.setText(data[0][8])  # 拟稿处室
                self.lineEdit_12.setText(data[0][9])  # 综合处编辑
                self.lineEdit_17.setText(data[0][10])  # 综合处审核
                self.lineEdit_18.setText(data[0][11])  # 秘书处审核
                self.lineEdit_16.setText(data[0][12])  # 综合处分管厅领导
                self.lineEdit_19.setText(data[0][13])  # 审计办主任
                self.lineEdit_file.setText(data[0][18])  # 报文内容
                self.dateEdit_3.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 办文日期

                # 如果报文内容为空,打开文件按钮不可点击
                if self.lineEdit_file.text() == "":
                    self.pushButton_opfile_2.setDisabled(True)
                else:
                    self.pushButton_opfile_2.setEnabled(True)

                # 设置只读
                self.lineEdit.setReadOnly(True)
                self.lineEdit_2.setReadOnly(True)
                self.spinBox.setReadOnly(True)
                self.comboBox_2.setDisabled(True)
                self.lineEdit_5.setReadOnly(True)
                self.comboBox_3.setDisabled(True)
                self.lineEdit_10.setReadOnly(True)
                self.lineEdit_15.setReadOnly(True)
                self.lineEdit_11.setReadOnly(True)
                self.lineEdit_12.setReadOnly(True)
                self.lineEdit_17.setReadOnly(True)
                self.lineEdit_18.setReadOnly(True)
                self.lineEdit_16.setReadOnly(True)
                self.lineEdit_19.setReadOnly(True)
                self.lineEdit_file.setReadOnly(True)
                self.dateEdit_3.setReadOnly(True)

            # 公文类型
            elif self.send_type == 2:
                # 隐藏确认取消按钮,替换文件按钮
                self.pushButton_8.hide()
                self.pushButton_9.hide()
                self.pushButton_file.hide()

                # 显示修改按钮,打开文件按钮
                self.pushButton_2.show()
                self.pushButton_opfile.show()

                self.lineEdit_num_3.setText(data[0][0])  # 发文标题
                self.comboBox_10.setCurrentText(tools.getTypeFromString(data[0][2]))  # 发文字号[类型]
                self.spinBox_2.setValue(int(tools.getIntegerFromString(data[0][2])[0]))  # 发文字号[年]
                self.spinBox_3.setValue(int(tools.getIntegerFromString(data[0][2])[1]))  # 发文字号[编号]
                self.lineEdit_25.setText(data[0][2])  # 办文编号
                self.comboBox_4.setCurrentText(data[0][3])  # 紧急程度
                self.lineEdit_22.setText(data[0][4])  # 保密等级
                self.comboBox_5.setCurrentText(data[0][5])  # 是否公开
                self.textEdit_2.setText(data[0][14])  # 领导审核意见
                self.textEdit_4.setText(data[0][15])  # 审计办领导审核意见
                self.textEdit_3.setText(data[0][16])  # 办文情况说明和拟办意见
                self.lineEdit_file_3.setText(data[0][18])  # 公文内容
                self.lineEdit_24.setText(data[0][19])  # 审核
                self.lineEdit_26.setText(data[0][20])  # 承办处室
                self.lineEdit_27.setText(data[0][21])  # 承办人
                self.lineEdit_28.setText(data[0][22])  # 联系电话
                self.dateEdit_7.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 办文日期
                self.dateEdit_6.setDate(QDate.fromString(data[0][23], 'yyyy/M/d'))  # 日期

                # 如果报文内容为空,打开文件按钮不可点击
                if self.lineEdit_file_3.text() == "":
                    self.pushButton_opfile.setDisabled(True)
                else:
                    self.pushButton_opfile.setEnabled(True)

                # 设置只读
                self.comboBox_10.setDisabled(True)
                self.spinBox_2.setReadOnly(True)
                self.spinBox_3.setReadOnly(True)
                self.lineEdit_num_3.setReadOnly(True)
                self.textEdit_2.setReadOnly(True)
                self.textEdit_4.setReadOnly(True)
                self.textEdit_3.setReadOnly(True)
                self.lineEdit_file_3.setReadOnly(True)
                self.lineEdit_22.setReadOnly(True)
                self.comboBox_5.setDisabled(True)
                self.comboBox_4.setDisabled(True)
                self.lineEdit_24.setReadOnly(True)
                self.lineEdit_26.setReadOnly(True)
                self.lineEdit_27.setReadOnly(True)
                self.lineEdit_28.setReadOnly(True)
                self.dateEdit_7.setReadOnly(True)
                self.dateEdit_6.setReadOnly(True)
                self.lineEdit_25.setReadOnly(True)
        if self.send_type == 1:
            self.stackedWidget.setCurrentIndex(0)
        elif self.send_type == 2:
            self.stackedWidget.setCurrentIndex(1)

    # 展示收文页面
    def displayRevFile(self):
        # 隐藏确认和取消按钮
        self.pushButton_11.hide()
        self.pushButton_12.hide()

        # 收文表本来就存在,此时读数据库,隐藏新增收文按钮,展示修改按钮,设置文本输入只读模式
        if self.xh_rev != -1:
            sql = "select 收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,内容摘要和拟办意见,领导批示,处理结果,审核,收文字号,承办处室,承办人,联系电话 from revfile " \
                  "where 序号 = %s" % self.xh_rev
            data = tools.executeSql(sql)

            self.pushButton_3.hide()
            self.pushButton_6.show()

            self.dateEdit_5.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
            self.lineEdit_14.setText(data[0][1])  # 密级
            self.comboBox_6.setCurrentText(data[0][2])  # 是否公开
            self.comboBox_7.setCurrentText(data[0][3])  # 紧急程度
            self.lineEdit_66.setText(data[0][4])  # 收文来文单位
            self.lineEdit_67.setText(data[0][5])  # 收文来文字号
            self.lineEdit_68.setText(data[0][6])  # 文件标题
            self.textEdit_10.setText(data[0][7])  # 内容摘要和拟办意见
            self.textEdit_11.setText(data[0][8])  # 领导批示
            self.lineEdit_64.setText(data[0][9])  # 处理结果
            self.lineEdit_65.setText(data[0][10])  # 审核
            self.comboBox_11.setCurrentText(tools.getTypeFromString(data[0][11]))  # 收文编号:类型
            self.spinBox_4.setValue(int(tools.getIntegerFromString(data[0][11])[0]))  # 收文编号:[年]
            self.spinBox_5.setValue(int(tools.getIntegerFromString(data[0][11])[1]))  # 收文编号:编号
            self.lineEdit_61.setText(data[0][12])  # 承办处室
            self.lineEdit_62.setText(data[0][13])  # 承办人
            self.lineEdit_63.setText(data[0][14])  # 联系电话

            self.dateEdit_5.setReadOnly(True)
            self.lineEdit_14.setReadOnly(True)
            self.comboBox_6.setDisabled(True)
            self.comboBox_7.setDisabled(True)
            self.lineEdit_66.setReadOnly(True)
            self.lineEdit_67.setReadOnly(True)
            self.lineEdit_68.setReadOnly(True)
            self.lineEdit_64.setReadOnly(True)
            self.lineEdit_65.setReadOnly(True)
            self.comboBox_11.setDisabled(True)
            self.spinBox_4.setReadOnly(True)
            self.spinBox_5.setReadOnly(True)
            self.lineEdit_61.setReadOnly(True)
            self.lineEdit_62.setReadOnly(True)
            self.lineEdit_63.setReadOnly(True)
            self.textEdit_10.setReadOnly(True)
            self.textEdit_11.setReadOnly(True)

        # 收文表本来不存在,但是发文表存在,此时应该继承发文表中已有内容,隐藏修改收文按钮,展示新增收文按钮
        elif self.xh_rev == -1 and self.xh_send != -1:
            # 继承专报字段,此处重新查询发文字段是为了防止:用户如果修改发文界面输入文本而没有保存此次修改的话,收文表字段会错误继承用户修改的字段内容,因为此时数据库中并没有提交修改
            sql = "select 发文标题,发文字号,紧急程度,秘密等级,是否公开 from sendfile where 序号 = %s" % self.xh_send
            data = tools.executeSql(sql)
            self.pushButton_3.show()
            self.pushButton_6.hide()

            self.lineEdit_14.setText(data[0][3])  # 密级
            self.comboBox_6.setCurrentText(data[0][4])  # 是否公开
            self.lineEdit_68.setText(data[0][0])  # 文件标题
            self.comboBox_7.setCurrentText(data[0][2])  # 紧急程度
            self.lineEdit_67.setText(data[0][1])  # 来文字号
            self.dateEdit_5.setDate(datetime.datetime.now())  # 初始化时间时间默认值为当前时间
            self.comboBox_11.setCurrentIndex(0)  # 初始化收文类型
            self.spinBox_4.setValue(datetime.datetime.now().year)  # 初始化时间为当前系统时间
            self.spinBox_5.setValue(1)  # 初始化编号为1

            # 继承而来的字段不可改变
            self.lineEdit_14.setReadOnly(True)
            self.comboBox_6.setDisabled(True)
            self.lineEdit_68.setReadOnly(True)
            self.comboBox_7.setDisabled(True)
            self.lineEdit_67.setReadOnly(True)

        self.stackedWidget.setCurrentIndex(3)

    # 展示所有批文页面
    def displayCorFile(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常

        # 设置不可修改,list默认不能修改
        self.dateEdit_4.setReadOnly(True)  # 收文时间
        self.lineEdit_13.setText("")
        self.lineEdit_13.setReadOnly(True)  # 密级
        self.comboBox_8.setCurrentText("是")
        self.comboBox_8.setDisabled(True)  # 是否公开
        self.comboBox_9.setCurrentText("无")
        self.comboBox_9.setDisabled(True)  # 紧急程度
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 批文来文单位
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 批文来文字号
        self.lineEdit_59.setReadOnly(True)  # 文件标题
        self.listWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 省领导内容摘要和拟办意见
        self.textEdit_9.setReadOnly(True)  # 领导批示
        self.lineEdit_6.setReadOnly(True)  # 厅领导内容摘要和拟办意见
        self.lineEdit_55.setReadOnly(True)  # 处理结果
        self.lineEdit_56.setReadOnly(True)  # 审核
        self.spinBox_6.setValue(0)
        self.spinBox_7.setValue(0)
        self.spinBox_6.setReadOnly(True)  # 批文编号:[年]
        self.spinBox_7.setReadOnly(True)  # 批文编号:[编号]
        self.lineEdit_52.setReadOnly(True)  # 承办处室
        self.lineEdit_53.setReadOnly(True)  # 承办人
        self.lineEdit_54.setReadOnly(True)  # 联系电话

        # 表示收文还没有录入,此时不允许录入批文,跳转到收文录入页面
        if self.xh_rev == -1:
            QtWidgets.QMessageBox.critical(w, "错误", "收文未录入！")
            self.stackedWidget.setCurrentIndex(3)
            self.displayRevFile()
            return

        # 获取批文数量
        cor_num = len(self.xh_cor_list)

        # 隐藏确认和取消按钮,当批文数量不为0的时候显示修改按钮
        self.pushButton_4.show()
        if cor_num != 0:
            self.pushButton_7.show()
        else:
            self.pushButton_7.hide()
        self.pushButton_13.hide()
        self.pushButton_14.hide()

        # 展示下拉框和标签
        self.label_25.show()
        self.comboBox.show()
        self.comboBox.setEnabled(True)

        # 隐藏+和-号
        self.pushButton_add.hide()
        self.pushButton_sub.hide()

        # 表示收文已经完成批改,此时读取批文列表,显示新增和修改按钮
        if cor_num != 0:
            self.comboBox.disconnect()  # 先断开comboBox,防止绑定函数出错
            self.comboBox.clear()  # 清空复选框

            if len(self.xh_cor_list) != 0:
                for i in self.xh_cor_list:
                    self.comboBox.addItem(i[1])

            # 有了数据后再重新绑定
            self.comboBox.currentIndexChanged.connect(
                lambda: self.displayCorFileForIndex(xh_cur_cor=self.xh_cor_list[self.comboBox.currentIndex()][0]))

            xh_cur_cor = self.xh_cor_list[self.comboBox.currentIndex()][0]

            self.displayCorFileForIndex(xh_cur_cor)

        else:
            self.dateEdit_4.setDate(QDate.currentDate())  # 收文时间
            self.listWidget.clear()  # 批文来文单位
            self.listWidget_2.clear()  # 批文来文字号
            self.lineEdit_59.clear()  # 文件标题
            self.lineEdit_55.clear()  # 处理结果
            self.lineEdit_56.clear()  # 审核
            self.spinBox_6.setValue(datetime.datetime.now().year)  # 批文编号:[年]
            self.spinBox_7.setValue(1)  # 批文编号:编号
            self.lineEdit_52.clear()  # 承办处室
            self.lineEdit_53.clear()  # 承办人
            self.lineEdit_54.clear()  # 联系电话
            self.listWidget_3.clear()  # 省领导内容摘要和拟办意见
            self.lineEdit_6.clear()  # 厅领导内容摘要和拟办意见
            self.textEdit_9.clear()  # 领导批示

        self.stackedWidget.setCurrentIndex(4)

    # 展示某一个批文页面
    def displayCorFileForIndex(self, xh_cur_cor):
        sql = "select 收文时间,秘密等级,是否公开,紧急程度,批文标题,处理结果,审核,批文字号,承办处室,承办人,联系电话,内容摘要和拟办意见," \
              "领导批示 from corfile where 序号 = %s" % xh_cur_cor
        data = tools.executeSql(sql)

        self.dateEdit_4.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
        self.lineEdit_13.setText(data[0][1])  # 密级
        self.comboBox_8.setCurrentText(data[0][2])  # 是否公开
        self.comboBox_9.setCurrentText(data[0][3])  # 紧急程度
        # self.lineEdit_57.setText(data[0][4])  # 批文来文单位
        # self.lineEdit_58.setText(data[0][5])  # 批文来文字号
        self.lineEdit_59.setText(data[0][4])  # 文件标题
        self.lineEdit_55.setText(data[0][5])  # 处理结果
        self.lineEdit_56.setText(data[0][6])  # 审核
        self.spinBox_6.setValue(int(tools.getIntegerFromString(data[0][7])[0]))  # 批文编号:[年]
        self.spinBox_7.setValue(int(tools.getIntegerFromString(data[0][7])[1]))  # 批文编号:编号
        self.lineEdit_52.setText(data[0][8])  # 承办处室
        self.lineEdit_53.setText(data[0][9])  # 承办人
        self.lineEdit_54.setText(data[0][10])  # 联系电话
        self.lineEdit_6.setText(data[0][11])  # 厅领导内容摘要和拟办意见
        self.textEdit_9.setText(data[0][12])  # 领导批示

        sql = "select 领导来文单位,领导来文字号,领导内容摘要和领导批示 from instruction where 批文序号 = %s" % xh_cur_cor
        data = tools.executeSql(sql)

        # 先清空list
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        if len(data) != 0:
            for i in data:
                self.listWidget.addItem(i[0])  # 来文单位
                self.listWidget_2.addItem(i[1])  # 来文字号
                self.listWidget_3.addItem(i[2])  # 省领导内容摘要和拟办意见

    # 修改发文按钮
    def reviseSendFile(self, btname):
        # 设置可写,确认和取消按钮可见,修改按钮不可见,替换文件按钮可见,打开文件按钮不可见
        if btname == "zb":
            self.pushButton.show()
            self.pushButton_10.show()
            self.pushButton_5.hide()
            self.pushButton_file_2.show()
            self.pushButton_opfile_2.hide()

            self.lineEdit.setReadOnly(False)
            self.lineEdit_2.setReadOnly(False)
            self.spinBox.setReadOnly(False)
            self.comboBox_2.setEnabled(True)
            self.lineEdit_5.setReadOnly(False)
            self.comboBox_3.setEnabled(True)
            self.lineEdit_10.setReadOnly(False)
            self.lineEdit_15.setReadOnly(False)
            self.lineEdit_11.setReadOnly(False)
            self.lineEdit_12.setReadOnly(False)
            self.lineEdit_17.setReadOnly(False)
            self.lineEdit_18.setReadOnly(False)
            self.lineEdit_16.setReadOnly(False)
            self.lineEdit_19.setReadOnly(False)
            # self.lineEdit_file.setReadOnly(False)
            self.dateEdit_3.setReadOnly(False)

        elif btname == "gw":
            self.pushButton_8.show()
            self.pushButton_9.show()
            self.pushButton_2.hide()
            self.pushButton_file.show()
            self.pushButton_opfile.hide()

            self.comboBox_10.setEnabled(True)
            self.spinBox_2.setReadOnly(False)
            self.spinBox_3.setReadOnly(False)
            self.lineEdit_num_3.setReadOnly(False)
            self.textEdit_2.setReadOnly(False)
            self.textEdit_4.setReadOnly(False)
            self.textEdit_3.setReadOnly(False)
            # self.lineEdit_file_3.setReadOnly(False)
            self.lineEdit_22.setReadOnly(False)
            self.comboBox_5.setEnabled(True)
            self.comboBox_4.setEnabled(True)
            self.lineEdit_24.setReadOnly(False)
            self.lineEdit_26.setReadOnly(False)
            self.lineEdit_27.setReadOnly(False)
            self.lineEdit_28.setReadOnly(False)
            self.dateEdit_7.setReadOnly(False)
            self.dateEdit_6.setReadOnly(False)
            # self.lineEdit_25.setReadOnly(False)

    # 提交修改发文
    def updateSendFile(self, btname):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        if btname == "zb":
            input1 = self.lineEdit.text()  # 发文标题
            input2 = self.lineEdit_2.text()  # 报送范围
            input3 = self.label_11.text() + self.spinBox.text() + self.label_12.text()  # 发文字号
            input4 = self.comboBox_2.currentText()  # 紧急程度
            input5 = self.lineEdit_5.text()  # 秘密等级
            input6 = self.comboBox_3.currentText()  # 是否公开
            input7 = self.lineEdit_10.text()  # 拟稿人
            input8 = self.lineEdit_15.text()  # 拟稿处室分管厅领导
            input9 = self.lineEdit_11.text()  # 拟稿处室
            input10 = self.lineEdit_12.text()  # 综合处编辑
            input11 = self.lineEdit_17.text()  # 综合处审核
            input12 = self.lineEdit_18.text()  # 秘书处审核
            input13 = self.lineEdit_16.text()  # 综合处分管厅领导
            input14 = self.lineEdit_19.text()  # 审计办主任
            input15 = self.lineEdit_file.text()  # 报文内容
            input16 = self.dateEdit_3.text()  # 办文日期

            if input1 != "":
                sql = "select 发文字号 from sendfile where 发文字号 = '%s'" % input3
                data = tools.executeSql(sql)
                sql = "select 发文字号 from sendfile where 序号 = %s" % self.xh_send
                result = tools.executeSql(sql)[0][0]
                # 数据库中发文字号是否存在,不允许重复的发文字号输入
                if len(data) != 0 and result != input3:
                    QtWidgets.QMessageBox.critical(w, "修改失败", "发文字号已经存在!")
                else:
                    # 替换文件
                    sql = "select 报文内容 from sendfile where 序号 = %s" % self.xh_send
                    old_file_name = tools.executeSql(sql)[0][0]
                    # 表示替换了新文件
                    if old_file_name != input15:
                        input_file_path = input15  # 存储文件路径
                        input15 = tools.getFileName(input15)  # 获取新的文件名,作为数据库更新字段
                        tools.replaceFile(input_file_path, old_file_name, tools.project_word_path)

                    sql = "update sendfile set 发文标题 = '%s',报送范围 = '%s',发文字号 = '%s',紧急程度 = '%s',秘密等级 = '%s',是否公开 = '%s'," \
                          "拟稿人 = '%s',拟稿处室分管厅领导 = '%s',拟稿处室审核 = '%s',综合处编辑 = '%s',综合处审核 = '%s',秘书处审核 = '%s',综合处分管厅领导= " \
                          "'%s',审计办主任 = '%s',报文内容 = '%s',办文日期 = '%s' where 序号 = %s" % (
                              input1, input2, input3, input4, input5, input6, input7, input8, input9,
                              input10, input11, input12, input13, input14, input15, input16, self.xh_send)
                    tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

                    self.displaySendFile()
            else:
                QtWidgets.QMessageBox.critical(w, "修改失败", "发文标题不能为空!")

        elif btname == "gw":
            input1 = self.comboBox_10.currentText() + '[' + self.spinBox_2.text() + ']' + self.spinBox_3.text() \
                     + self.label_51.text()  # 发文字号
            input2 = self.lineEdit_num_3.text()  # 发文标题
            input3 = self.textEdit_2.toPlainText()  # 领导审核意见
            input4 = self.textEdit_4.toPlainText()  # 审计办领导审核意见
            input5 = self.textEdit_3.toPlainText()  # 办文情况说明和拟办意见
            input6 = self.lineEdit_file_3.text()  # 公文内容
            input7 = self.lineEdit_22.text()  # 秘密等级
            input8 = self.comboBox_5.currentText()  # 是否公开
            input9 = self.comboBox_4.currentText()  # 紧急程度
            input10 = self.lineEdit_24.text()  # 审核
            input11 = self.lineEdit_26.text()  # 承办处室
            input12 = self.lineEdit_27.text()  # 承办人
            input13 = self.lineEdit_28.text()  # 联系电话
            input14 = self.dateEdit_7.text()  # 办文日期
            # input15 = self.dateEdit_6.text()  # 日期
            # input16 = self.lineEdit_25.text()  # 办文编号

            if input2 != "":
                sql = "select 发文字号 from sendfile where 发文字号 = '%s'" % input1
                data = tools.executeSql(sql)
                sql = "select 发文字号 from sendfile where 序号 = %s" % self.xh_send
                result = tools.executeSql(sql)[0][0]
                # 数据库中发文字号是否存在,不允许重复的发文字号输入
                if len(data) != 0 and input1 != result:
                    QtWidgets.QMessageBox.critical(w, "修改失败", "发文字号已经存在!")
                else:
                    # 替换文件
                    sql = "select 报文内容 from sendfile where 序号 = %s" % self.xh_send
                    old_file_name = tools.executeSql(sql)[0][0]
                    # 表示替换了新文件
                    if old_file_name != input6:
                        input_file_path = input6  # 存储文件路径
                        input6 = tools.getFileName(input6)  # 获取新的文件名,作为数据库更新字段
                        tools.replaceFile(input_file_path, old_file_name, tools.project_word_path)

                    sql = "update sendfile set 发文字号 = '%s',发文标题 = '%s',领导审核意见 = '%s',审计办领导审核意见 = '%s',办文情况说明和拟办意见 = " \
                          "'%s',报文内容 = '%s',秘密等级 = '%s',是否公开 = '%s',紧急程度 = '%s',审核 = '%s',承办处室 = '%s',承办人 = '%s'," \
                          "联系电话 = '%s',办文日期 = '%s' where 序号 = %s" % (
                              input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                              input12, input13, input14, self.xh_send)
                    tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

                    self.displaySendFile()
            else:
                QtWidgets.QMessageBox.critical(w, "修改失败", "发文标题不能为空!")

    # 取消修改发文
    def cancelSendFile(self, btname):
        # 回到展示页面
        self.displaySendFile()

    # 录入收文
    def insertRevFile(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常

        input1 = self.dateEdit_5.text()  # 收文时间
        input2 = self.lineEdit_14.text()  # 密级
        input3 = self.comboBox_6.currentText()  # 是否公开
        input4 = self.comboBox_7.currentText()  # 紧急程度
        input5 = self.lineEdit_66.text()  # 收文来文单位
        input6 = self.lineEdit_67.text()  # 收文来文字号
        input7 = self.lineEdit_68.text()  # 文件标题
        input8 = self.textEdit_10.toPlainText()  # 内容摘要和拟办意见
        input9 = self.textEdit_11.toPlainText()  # 领导批示
        input10 = self.lineEdit_64.text()  # 处理结果
        input11 = self.lineEdit_65.text()  # 审核
        input12 = self.comboBox_11.currentText() + '[' + self.spinBox_4.text() + ']' + self.spinBox_5.text() + self.label_52.text()  # 收文编号
        input13 = self.lineEdit_61.text()  # 承办处室
        input14 = self.lineEdit_62.text()  # 承办人
        input15 = self.lineEdit_63.text()  # 联系电话

        if input7 != "":
            sql = "select 收文字号 from revfile where 收文字号 = '%s'" % input12
            data = tools.executeSql(sql)
            # 数据库中收文字号是否存在,不允许重复的收文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(w, "录入失败", "收文字号已经存在!")
            else:
                # 执行插入收文表
                sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,内容摘要和拟办意见,领导批示,处理结果,审核,收文字号,承办处室,承办人," \
                      "联系电话) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                          input1, input2, input3, input4, input5, input6,
                          input7, input8, input9, input10, input11,
                          input12, input13, input14, input15)
                tools.executeSql(sql)

                # 找到当前收文的序号
                sql = "select 序号 from revfile where 收文字号 = '%s'" % input12
                data = tools.executeSql(sql)

                # 更新流程表,根据流程序号更新收文序号
                sql = "update bwprocess set 收文序号 = %s where 序号 = %s" % (data[0][0], self.xh)
                tools.executeSql(sql)

                # 更新状态变量
                self.xh_rev = data[0][0]

                QtWidgets.QMessageBox.information(w, "提示", "录入成功！")

            # 重新展示收文界面
            self.displayRevFile()

        else:
            QtWidgets.QMessageBox.critical(w, "录入失败", "收文标题不能为空!")

    # 修改收文按钮
    def reviseRevFile(self):
        # 隐藏修改按钮,展示确认和取消按钮
        self.pushButton_6.hide()
        self.pushButton_11.show()
        self.pushButton_12.show()

        # 设置可写
        self.dateEdit_5.setReadOnly(False)
        self.lineEdit_14.setReadOnly(False)
        self.comboBox_6.setEnabled(True)
        self.comboBox_7.setEnabled(True)
        self.lineEdit_66.setReadOnly(False)
        self.lineEdit_67.setReadOnly(False)
        self.lineEdit_68.setReadOnly(False)
        self.lineEdit_64.setReadOnly(False)
        self.lineEdit_65.setReadOnly(False)
        self.comboBox_11.setEnabled(True)
        self.spinBox_4.setReadOnly(False)
        self.spinBox_5.setReadOnly(False)
        self.lineEdit_61.setReadOnly(False)
        self.lineEdit_62.setReadOnly(False)
        self.lineEdit_63.setReadOnly(False)
        self.textEdit_10.setReadOnly(False)
        self.textEdit_11.setReadOnly(False)

    # 确认修改收文
    def updateRevFile(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常

        input1 = self.dateEdit_5.text()  # 收文时间
        input2 = self.lineEdit_14.text()  # 密级
        input3 = self.comboBox_6.currentText()  # 是否公开
        input4 = self.comboBox_7.currentText()  # 紧急程度
        input5 = self.lineEdit_66.text()  # 收文来文单位
        input6 = self.lineEdit_67.text()  # 收文来文字号
        input7 = self.lineEdit_68.text()  # 文件标题
        input8 = self.textEdit_10.toPlainText()  # 内容摘要和拟办意见
        input9 = self.textEdit_11.toPlainText()  # 领导批示
        input10 = self.lineEdit_64.text()  # 处理结果
        input11 = self.lineEdit_65.text()  # 审核
        input12 = self.comboBox_11.currentText() + '[' + self.spinBox_4.text() + ']' + self.spinBox_5.text() + self.label_52.text()  # 办文编号
        input13 = self.lineEdit_61.text()  # 承办处室
        input14 = self.lineEdit_62.text()  # 承办人
        input15 = self.lineEdit_63.text()  # 联系电话

        if input7 != "":
            sql = "select 收文字号 from revfile where 收文字号 = '%s'" % input12
            data = tools.executeSql(sql)
            sql = "select 收文字号 from revfile where 序号 = %s" % self.xh_rev
            result = tools.executeSql(sql)[0][0]
            # 数据库中收文字号是否存在,不允许重复的收文字号输入
            if len(data) != 0 and result != input12:
                QtWidgets.QMessageBox.critical(w, "修改失败", "收文字号已经存在!")
            else:
                # 执行更新收文表
                sql = "update revfile set 收文时间 = '%s',秘密等级 = '%s',是否公开 = '%s',紧急程度 = '%s',来文单位 = '%s',来文字号 = '%s'," \
                      "收文标题 = '%s',内容摘要和拟办意见 = '%s',领导批示 = '%s',处理结果 = '%s',审核 = '%s',收文字号 = '%s',承办处室 = '%s'," \
                      "承办人 = '%s',联系电话 = '%s' where 序号 = %s" % (
                          input1, input2, input3, input4, input5, input6,
                          input7, input8, input9, input10, input11,
                          input12, input13, input14, input15, self.xh_rev)

                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

                self.displayRevFile()

        else:
            QtWidgets.QMessageBox.critical(w, "修改错误", "收文标题不能为空!")

    # 取消修改收文
    def cancelRevFile(self):
        self.displayRevFile()

    # 新增批文
    def insertCorFile(self):
        # 显示确认和取消按钮,用确认按钮的name判断是新增还是修改
        self.pushButton_4.hide()
        self.pushButton_7.hide()
        self.pushButton_13.show()
        self.pushButton_14.show()

        # 隐藏下拉选择框和标签
        self.label_25.hide()
        self.comboBox.hide()

        # 显示add和sub选项
        self.pushButton_add.show()
        self.pushButton_sub.show()

        self.pushButton_13.setText("确认新增")

        # 设置继承字段,从收文表中继承
        sql = "select 秘密等级,是否公开,紧急程度 from revfile where 序号 = %s" % self.xh_rev
        data = tools.executeSql(sql)
        self.lineEdit_13.setText(data[0][0])  # 密级
        self.comboBox_8.setCurrentText(data[0][1])  # 是否公开
        self.comboBox_9.setCurrentText(data[0][2])  # 紧急程度

        self.dateEdit_4.setDate(QDate.currentDate())  # 收文时间
        self.listWidget.clear()  # 批文来文单位
        self.listWidget_2.clear()  # 批文来文字号
        self.lineEdit_59.clear()  # 文件标题
        self.lineEdit_55.clear()  # 处理结果
        self.lineEdit_56.clear()  # 审核
        self.spinBox_6.setValue(datetime.datetime.now().year)  # 批文编号:[年]
        self.spinBox_7.setValue(1)  # 批文编号:编号
        self.lineEdit_52.clear()  # 承办处室
        self.lineEdit_53.clear()  # 承办人
        self.lineEdit_54.clear()  # 联系电话
        self.listWidget_3.clear()  # 省领导内容摘要和拟办意见
        self.lineEdit_6.clear()  # 厅领导内容摘要和拟办意见
        self.textEdit_9.clear()  # 领导批示

        # self.lineEdit_13.setReadOnly(False)  # 密级
        # self.comboBox_8.setEnabled(True)  # 是否公开
        # self.comboBox_9.setEnabled(True)  # 紧急程度
        self.dateEdit_4.setReadOnly(False)  # 收文时间
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 批文来文单位
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 批文来文字号
        self.lineEdit_59.setReadOnly(False)  # 文件标题
        self.listWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 省领导内容摘要和拟办意见
        self.lineEdit_6.setReadOnly(False)  # 厅内容摘要和拟办意见
        self.textEdit_9.setReadOnly(False)  # 领导批示
        self.lineEdit_55.setReadOnly(False)  # 处理结果
        self.lineEdit_56.setReadOnly(False)  # 审核
        self.spinBox_6.setReadOnly(False)  # 批文编号:[年]
        self.spinBox_7.setReadOnly(False)  # 批文编号:编号
        self.lineEdit_52.setReadOnly(False)  # 承办处室
        self.lineEdit_53.setReadOnly(False)  # 承办人
        self.lineEdit_54.setReadOnly(False)  # 联系电话

    # 修改批文按钮
    def reviseCorFile(self):
        # 显示确认和取消按钮,用确认按钮的name判断是新增还是修改;显示+和-号
        self.pushButton_4.hide()
        self.pushButton_7.hide()
        self.pushButton_13.show()
        self.pushButton_14.show()

        self.pushButton_add.show()
        self.pushButton_sub.show()

        self.pushButton_13.setText("确认修改")

        # 下拉框不可切换
        self.comboBox.setDisabled(True)

        # 设置item可编辑
        for index in range(self.listWidget.count()):
            self.listWidget.item(index).setFlags(self.listWidget.item(index).flags() | QtCore.Qt.ItemIsEditable)
        for index in range(self.listWidget_2.count()):
            self.listWidget_2.item(index).setFlags(self.listWidget_2.item(index).flags() | QtCore.Qt.ItemIsEditable)
        for index in range(self.listWidget_3.count()):
            self.listWidget_3.item(index).setFlags(self.listWidget_3.item(index).flags() | QtCore.Qt.ItemIsEditable)

        self.dateEdit_4.setReadOnly(False)  # 收文时间
        self.lineEdit_13.setReadOnly(False)  # 密级
        self.comboBox_8.setEnabled(True)  # 是否公开
        self.comboBox_9.setEnabled(True)  # 紧急程度
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 批文来文单位
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 批文来文字号
        self.lineEdit_59.setReadOnly(False)  # 文件标题
        self.listWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # 省领导内容摘要和拟办意见
        self.lineEdit_6.setReadOnly(False)  # 厅内容摘要和拟办意见
        self.textEdit_9.setReadOnly(False)  # 领导批示
        self.lineEdit_55.setReadOnly(False)  # 处理结果
        self.lineEdit_56.setReadOnly(False)  # 审核
        self.spinBox_6.setReadOnly(False)  # 批文编号:[年]
        self.spinBox_7.setReadOnly(False)  # 批文编号:编号
        self.lineEdit_52.setReadOnly(False)  # 承办处室
        self.lineEdit_53.setReadOnly(False)  # 承办人
        self.lineEdit_54.setReadOnly(False)  # 联系电话

    # 确认新增/修改批文
    def insertOrUpdateCorFile(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        input1 = self.dateEdit_4.text()  # 收文时间
        input2 = self.lineEdit_13.text()  # 密级
        input3 = self.comboBox_8.currentText()  # 是否公开
        input4 = self.comboBox_9.currentText()  # 紧急程度
        input5 = self.lineEdit_59.text()  # 批文标题
        input6 = self.comboBox_12.currentText() + '[' + self.spinBox_6.text() + ']' + self.spinBox_7.text() + self.label_53.text()  # 批文编号
        input7 = self.lineEdit_6.text()  # 厅领导内容摘要和拟办意见
        input8 = self.textEdit_9.toPlainText()  # 领导批示
        input9 = self.lineEdit_55.text()  # 处理结果
        input10 = self.lineEdit_56.text()  # 审核
        input11 = self.lineEdit_52.text()  # 承办处室
        input12 = self.lineEdit_53.text()  # 承办人
        input13 = self.lineEdit_54.text()  # 联系电话

        if self.pushButton_13.text() == "确认新增":
            if input5 != "":
                sql = "select 批文字号 from corfile where 批文字号 = '%s'" % input6
                data = tools.executeSql(sql)
                # 数据库中批文字号是否存在,不允许重复的批文字号输入
                if len(data) != 0:
                    QtWidgets.QMessageBox.critical(w, "录入失败", "批文字号已经存在!")
                else:
                    # 插入corfile表中
                    sql = "insert into corfile(收文时间,秘密等级,是否公开,紧急程度,批文标题,批文字号,内容摘要和拟办意见,领导批示,处理结果,审核,承办处室,承办人," \
                          "联系电话) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                              input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                              input12, input13)
                    tools.executeSql(sql)

                    # 获取批文序号
                    sql = "select 序号 from corfile where 批文字号 = '%s'" % input6
                    data = tools.executeSql(sql)

                    # 插入instruction中
                    for index in range(self.listWidget.count()):
                        input14 = self.listWidget.item(index).text()  # 领导来文单位
                        input15 = self.listWidget_2.item(index).text()  # 领导来文字号
                        input16 = self.listWidget_3.item(index).text()  # 领导内容摘要和领导批示
                        sql = "insert into instruction(批文序号,领导来文单位,领导来文字号,领导内容摘要和领导批示) VALUES(%s,'%s','%s','%s')" % (
                            data[0][0], input14, input15, input16)
                        tools.executeSql(sql)

                    # 插入映射表中
                    sql = "insert into bw_cast_cor(流程序号,批文序号) VALUES(%s,%s)" % (self.xh, data[0][0])
                    tools.executeSql(sql)

                    # 向xh_cor_list中插入新的元组
                    self.xh_cor_list.append((data[0][0], input6))

                    QtWidgets.QMessageBox.information(w, "提示", "录入成功！")
            else:
                QtWidgets.QMessageBox.critical(w, "录入失败", "批文标题不能为空!")

        elif self.pushButton_13.text() == "确认修改":
            if input5 != "":
                sql = "select 批文字号 from corfile where 批文字号 = '%s'" % input6
                data = tools.executeSql(sql)
                sql = "select 批文字号 from corfile where 序号 = %s" % self.xh_cor_list[self.comboBox.currentIndex()][0]
                result = tools.executeSql(sql)[0][0]
                # 数据库中批文字号是否存在,不允许重复的批文字号输入
                if len(data) != 0 and result != input6:
                    QtWidgets.QMessageBox.critical(w, "修改失败", "批文字号已经存在!")
                else:
                    # 更新corfile表
                    sql = "update corfile set 收文时间 = '%s',秘密等级 = '%s',是否公开 = '%s',紧急程度 = '%s',批文标题 = '%s'," \
                          "批文字号 = '%s',内容摘要和拟办意见 = '%s',领导批示 = '%s',处理结果 = '%s',审核 = '%s',承办处室 = '%s'," \
                          "承办人 = '%s',联系电话 = '%s' where 序号 = %s" % (
                              input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                              input12, input13, self.xh_cor_list[self.comboBox.currentIndex()][0])
                    tools.executeSql(sql)

                    # 删除instruction表中所有序号为self.xh_cor_list[self.comboBox.currentIndex()][0]的条目
                    sql = "delete from instruction where 批文序号 = %s" % self.xh_cor_list[self.comboBox.currentIndex()][0]
                    tools.executeSql(sql)

                    # 重新插入instruction表
                    for index in range(self.listWidget.count()):
                        input14 = self.listWidget.item(index).text()  # 领导来文单位
                        input15 = self.listWidget_2.item(index).text()  # 领导来文字号
                        input16 = self.listWidget_3.item(index).text()  # 领导内容摘要和领导批示
                        sql = "insert into instruction(批文序号,领导来文单位,领导来文字号,领导内容摘要和领导批示) VALUES(%s,'%s','%s','%s')" % (
                            self.xh_cor_list[self.comboBox.currentIndex()][0], input14, input15, input16)
                        tools.executeSql(sql)

                    # xh_cor_list修改元组的批文字号,元组不能直接修改,先删除,再增加
                    xh_cor_temp = self.xh_cor_list[self.comboBox.currentIndex()][0]
                    del self.xh_cor_list[self.comboBox.currentIndex()]
                    self.xh_cor_list.insert(self.comboBox.currentIndex(), (xh_cor_temp, input6))

                    QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

            else:
                QtWidgets.QMessageBox.critical(w, "修改失败", "批文标题不能为空!")

        # 重新展示批文界面
        self.displayCorFile()

    # 取消新增/修改批文
    def cancelCorFile(self):
        self.displayCorFile()

    # 批文界面下的add和sub按钮,用于增加和删除条目
    def addTerm(self):
        item1 = QListWidgetItem("请输入领导来文单位")
        item1.setFlags(item1.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget.addItem(item1)
        item2 = QListWidgetItem("请输入领导来文字号")
        item2.setFlags(item2.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_2.addItem(item2)
        item3 = QListWidgetItem("请输入领导批示")
        item3.setFlags(item3.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_3.addItem(item3)

    def subTerm(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.listWidget.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择要删除的条目")
        else:
            self.listWidget.takeItem(row)
            self.listWidget_2.takeItem(row)
            self.listWidget_3.takeItem(row)

    # 选择问题表
    def chooseProblemTable(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "All Files(*);;Excel(*.xls);;Excel(*.xlsx)")
        self.lineEdit_3.setText(p[0])

    # 发文办理下的选择文件夹按钮(专报)
    def choose_file_zb(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        if p[0] != "":
            self.lineEdit_file.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def choose_file_gw(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        if p[0] != "":
            self.lineEdit_file_3.setText(p[0])

    # 根据excel中的左边问题基本信息导入问题表
    def importExcelProblem(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        # 文件路径
        path = self.lineEdit_3.text()
        path.replace('/', '\\\\')

        # 判断用户是否选择文件
        if path != "":
            try:
                # 获取excel文件
                data = xlrd.open_workbook(path)
                print('All sheets: %s' % data.sheet_names())

                # 获取excel第一个sheet,也就是问题表所在sheet
                sheet = data.sheets()[0]

                sheet_name = sheet.name  # 获得名称
                sheet_cols = sheet.ncols  # 获得列数
                sheet_rows = sheet.nrows  # 获得行数
                print('Sheet Name: %s\nSheet cols: %s\nSheet rows: %s\n' % (sheet_name, sheet_cols, sheet_rows))
            except:

                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())

            check_tag = 1  # excel输入合法检测标识,如果为1表示excel中所有数据合法,可以写入数据库

            # 检测excel某些输入是否合法
            try:
                # 读取excel数据进行检测
                for i in range(4, sheet_rows):
                    # 问题顺序号,判断是否为整数
                    if not tools.judgeInteger(sheet.row(i)[0].value):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(w, "提示", "excel表格第%s行: 问题顺序号应为整数" % str(i + 1))
                        break
                    # 出具审计专报时间,判断是否为合法时间
                    if isinstance(sheet.row(i)[5].value, str):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(w, "提示", "excel表格第%s行: 出具审计专报时间格式错误" % str(i + 1))
                        break
                    # 认定整改金额,判断是否为浮点数
                    if not isinstance(sheet.row(i)[14].value, float):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(w, "提示", "excel表格第%s行: 问题金额应为数字" % str(i + 1))
                        break
                if sheet_rows == 4:
                    check_tag = 0
                    QtWidgets.QMessageBox.information(w, "提示", "表格数据为空")
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())

            if check_tag == 1:
                # 写入数据库
                try:
                    for i in range(4, sheet_rows):
                        cell_i_0 = int(sheet.row(i)[0].value)  # 问题顺序号
                        cell_i_1 = sheet.row(i)[1].value  # 被审计对象
                        cell_i_2 = sheet.row(i)[2].value  # 所在地方或单位
                        # cell_i_3 = sheet.row(i)[3].value  # 报送专报期号
                        cell_i_3 = self.xh_send  # 报送专报期号,忽略excel表中发文字号这一列,直接读入发文序号
                        cell_i_4 = sheet.row(i)[4].value  # 审计报告（意见）文号
                        cell_i_5 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 5).value, 0).strftime(
                            "%Y/%m/%d")  # 出具审计专报时间 Year/Month/Day
                        cell_i_6 = sheet.row(i)[6].value  # 审计组组长
                        cell_i_7 = sheet.row(i)[7].value  # 审计组主审
                        cell_i_8 = sheet.row(i)[8].value  # 问题描述
                        cell_i_9 = sheet.row(i)[9].value  # 问题一级分类
                        cell_i_10 = sheet.row(i)[10].value  # 问题二级分类
                        cell_i_11 = sheet.row(i)[11].value  # 问题三级分类
                        cell_i_12 = sheet.row(i)[12].value  # 问题四级分类
                        cell_i_13 = sheet.row(i)[13].value  # 备注（不在前列问题类型中的，简单描述）
                        cell_i_14 = sheet.row(i)[14].value  # 问题金额（万元）
                        cell_i_15 = sheet.row(i)[15].value  # 移送及处理情况

                        sql = "insert into problem values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                              "'%s','%s','%s','%s','%s')" % (
                                  cell_i_0, cell_i_1, cell_i_2, cell_i_3, cell_i_4, cell_i_5, cell_i_6, cell_i_7,
                                  cell_i_8, cell_i_9, cell_i_10, cell_i_11, cell_i_12, cell_i_13, cell_i_14, cell_i_15)
                        tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(w, "提示", "导入完成")

                    # 更新问题表状态
                    self.pro_tag = 1

                    # 导入完成后更新表格
                    self.displayQuestionDetail()
                except:
                    log = Logger('./log/logfile.log', level='error')
                    log.logger.error("错误:%s", traceback.format_exc())
            else:
                QtWidgets.QMessageBox.critical(w, "错误", "导入失败")
        else:
            QtWidgets.QMessageBox.information(w, "提示", "请选择文件!")
