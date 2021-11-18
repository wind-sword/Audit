import traceback

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont

from uipy_dir.zgdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail
from logis_fir.call_zgrevise import Call_zgrevise
from logis_fir.tools import tools
from logis_fir.logger import Logger
import xlrd


class Call_zgdetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        # 整改流程变量
        self.xh = -1  # 整改序号
        self.xh_lc = -1  # 流程序号
        self.xh_send = -1  # 发文序号
        self.send_type = -1  # 发文类型
        self.xh_rev = -1  # 收文序号
        self.xh_cor_list = []  # 批文序号列表
        self.comboBox_dict = dict()  # 用下拉框下标映射到批文序号列表
        self.pro_tag = -1  # 表示问题表是否录入
        self.zgfh_tag = -1  # 表示整改发函是否录入(只要有一个发函录入则状态为录入)
        self.zglr_tag = -1  # 表示整改措施是否录入(只要录入一次整改措施则状态为录入)

        self.tabWidget_dict = dict()  # 记录问题详情tabWidget的映射情况:问题号 -> tabWidget对象

        self.window = None  # 整改子窗口

        # 页面上方流程跳转按钮
        self.commandLinkButton_1.clicked.connect(lambda: self.btjump(btname="1"))
        self.commandLinkButton_2.clicked.connect(lambda: self.btjump(btname="2"))
        self.commandLinkButton_3.clicked.connect(lambda: self.btjump(btname="3"))
        self.commandLinkButton_4.clicked.connect(lambda: self.btjump(btname="4"))
        self.commandLinkButton_5.clicked.connect(lambda: self.btjump(btname="5"))
        self.commandLinkButton_6.clicked.connect(lambda: self.btjump(btname="6"))

        # tab设置
        font = QFont('微软雅黑', 10, QFont.Black)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabText(0, "问题总览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.setMovable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        # 同步批文输入框的三个list高亮情况
        self.listWidget.currentRowChanged.connect(self.autoHighlight1)
        self.listWidget_2.currentRowChanged.connect(self.autoHighlight2)
        self.listWidget_3.currentRowChanged.connect(self.autoHighlight3)

        # 同步整改录入两个表的同步显示情况
        self.tableWidget_2.currentCellChanged.connect(self.autoHighlight4)
        self.tableWidget_4.currentCellChanged.connect(self.autoHighlight5)

        # 绑定按钮或其他控件功能函数
        self.initControlFunction()

        # 初始化流程变量
        self.initVar(key)

        # 初始化页面展示
        self.initView()

    # 流程跳转
    def btjump(self, btname):
        if btname == "1":
            if self.send_type == 1:
                self.stackedWidget.setCurrentIndex(0)
            elif self.send_type == 2:
                self.stackedWidget.setCurrentIndex(1)
            self.displaySendDetail()
        elif btname == "2":
            self.stackedWidget.setCurrentIndex(2)
            self.displayQuestionTable()
        elif btname == "3":
            self.stackedWidget.setCurrentIndex(3)
            self.displayRevDetail()
        elif btname == "4":
            self.stackedWidget.setCurrentIndex(4)
            self.displayCorDetail()
        elif btname == "5":
            self.stackedWidget.setCurrentIndex(5)
            self.displayZgfh()
        elif btname == "6":
            self.stackedWidget.setCurrentIndex(6)
            self.displayQuestionOverview()

    # 控件绑定功能函数
    def initControlFunction(self):
        # 发文登记
        self.pushButton_file.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file_3.text()))  # 打开公文文件
        self.pushButton_file_2.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file.text()))  # 打开专报文件

        # 问题表查看
        self.pushButton.clicked.connect(self.jumpQuestionDetail)  # 问题详情查看
        self.pushButton_3.clicked.connect(self.refreshQuestionTable)  # 问题表刷新

        # 批文查看
        self.comboBox.currentIndexChanged.connect(
            lambda: self.displayCorFileForIndex(xh_cur_cor=self.comboBox_dict[self.comboBox.currentIndex()]))  # 绑定下拉框切换

        # 整改发函
        self.pushButton_4.clicked.connect(self.openZgfh)  # 打开整改发函文件
        self.pushButton_5.clicked.connect(self.chooseFileZgfh)  # 选择发函文件
        self.pushButton_6.clicked.connect(self.saveZgfh)  # 保存发函文件
        self.pushButton_2.clicked.connect(self.deleteZgfh)  # 删除发函文件

        # 整改录入
        self.pushButton_7.clicked.connect(self.chooseQuestionExcel)  # 选择问题Excel表
        self.pushButton_8.clicked.connect(self.importExcelProblemZg)  # 导入问题整改情况
        self.pushButton_9.clicked.connect(self.deleteRecentProblemZg)  # 删除最近一次整改记录
        self.pushButton_10.clicked.connect(self.reviseZgdetail)  # 打开整改详情修改框

    # 用发文字号初始化变量
    def initVar(self, key):
        # 整改序号
        self.xh = key

        # 初始化流程序号
        sql = "select 流程序号 from zgprocess where 序号 = %s" % self.xh
        self.xh_lc = tools.executeSql(sql)[0][0]

        # 流程序号不为-1表示这是一个办文整改流程
        if self.xh_lc != -1:
            # 初始化发文序号,收文序号
            sql = "select 发文序号,收文序号 from bwprocess where 序号 = %s" % self.xh_lc
            data = tools.executeSql(sql)
            # print(data)
            self.xh_send = data[0][0]
            # 收文可能为空
            if data[0][1] is not None:
                self.xh_rev = data[0][1]

            # 初始化批文序号列表
            sql = 'select 序号 from corfile where 流程序号 = %s' % self.xh_lc
            result = tools.executeSql(sql)
            if len(result) != 0:
                for i in result:
                    for j in i:
                        self.xh_cor_list.append(j)

            # 初始化发文类型
            sql = "select projectType from sendfile where 序号 = %s" % self.xh_send
            result = tools.executeSql(sql)
            self.send_type = result[0][0]

            # 初始化问题表状态
            sql = "select * from problem where 发文序号 = %s" % self.xh_send
            result = tools.executeSql(sql)
            if len(result) != 0:
                self.pro_tag = 1

            # 初始化整改措施是否录入
            sql = "select * from problem,rectification where problem.发文序号 = %s and problem.序号 = " \
                  "rectification.问题序号" % self.xh_send
            result = tools.executeSql(sql)
            if len(result) != 0:
                self.zglr_tag = 1

        # 流程序号为-1表示这是一个经责自然资源整改流程
        elif self.xh_lc == -1:
            # 初始化问题表状态
            sql = "select * from problem_jz where 整改序号 = %s" % self.xh
            result = tools.executeSql(sql)
            if len(result) != 0:
                self.pro_tag = 1

            # 初始化整改措施是否录入
            sql = "select * from problem_jz,rectification_jz where problem_jz.整改序号 = %s and problem_jz.序号 = " \
                  "rectification_jz.问题序号" % self.xh
            result = tools.executeSql(sql)
            if len(result) != 0:
                self.zglr_tag = 1

        # 初始化整改发函状态
        sql = "select * from zgword where 整改序号 = %s" % self.xh
        result = tools.executeSql(sql)
        if len(result) != 0:
            self.zgfh_tag = 1

        # 初始化页面上方跳转按钮状态
        if self.xh_send == -1:
            self.commandLinkButton_1.setDescription("无")
            self.commandLinkButton_1.setDisabled(True)
        else:
            self.commandLinkButton_1.setDescription("已完成")

        if self.pro_tag == 1:
            self.commandLinkButton_2.setDescription("已完成")

        if self.xh_rev == -1:
            self.commandLinkButton_3.setDescription("无")
            self.commandLinkButton_3.setDisabled(True)
        else:
            self.commandLinkButton_3.setDescription("已完成")

        if len(self.xh_cor_list) == 0:
            self.commandLinkButton_4.setDescription("无")
            self.commandLinkButton_4.setDisabled(True)
        else:
            self.commandLinkButton_4.setDescription("已完成")

        if self.zgfh_tag == 1:
            self.commandLinkButton_5.setDescription("已完成")
        if self.zglr_tag == 1:
            self.commandLinkButton_6.setDescription("已完成")

    # 初始化整改界面显示
    def initView(self):
        # 经责的整改流程
        if self.xh_lc == -1:
            self.stackedWidget.setCurrentIndex(2)
            # 初始化页面展示
            self.displayQuestionTable()

        # 公文的整改流程
        else:
            if self.send_type == 1:
                self.stackedWidget.setCurrentIndex(0)
            elif self.send_type == 2:
                self.stackedWidget.setCurrentIndex(1)
            # 初始化页面展示
            self.displaySendDetail()

        # 设置文号为项目详情标题
        sql = "select 标识文号 from zgprocess where 序号 = %s" % self.xh
        data = tools.executeSql(sql)
        self.label_title.setText(data[0][0])

    """
    @关闭子页面操作函数
    @关闭tabWidget或者Window
    """

    # 关闭tab
    def closeTab(self, index):
        obj = self.tabWidget.widget(index)
        for key, value in self.tabWidget_dict.items():
            if value == obj:
                self.tabWidget_dict.pop(key)
                break
            else:
                continue
        self.tabWidget.removeTab(index)

    """
    @新增子页面操作函数
    主要是对表格某一行进行操作(修改或查看)生成新的子页面
    """

    # 跳转问题详情
    def jumpQuestionDetail(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择问题！")
        else:
            # 问题表主键,问题序号
            key = self.tableWidget.item(row, 0).text()
            # 该问题的问题顺序号
            key_num = self.tableWidget.item(row, 1).text()
            # 实例tab不存在
            if self.tabWidget_dict.get(key) is None:
                tab_new = Call_quedetail(key, self.xh_lc)
                tab_new.setObjectName('tab_new')
                tab_num = self.tabWidget.addTab(tab_new, "问题%s详情" % key_num)
                self.tabWidget.setCurrentIndex(tab_num)
                self.tabWidget_dict[key] = tab_new
            else:
                cur_tab = self.tabWidget_dict.get(key)
                cur_index = self.tabWidget.indexOf(cur_tab)
                self.tabWidget.setCurrentIndex(cur_index)

    # 打开整改详情修改框
    def reviseZgdetail(self):
        row = self.tableWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择整改措施！")
        else:
            # 整改表主键
            key = self.tableWidget_4.item(row, 0).text()
            self.window = Call_zgrevise(key, self.xh_lc)
            self.window.setWindowTitle("整改详情")
            self.window.exec()
            self.displayQuestionOverview()

    """
    @同步高亮显示
    主要是对前端多个控件之间的内容进行同步高亮显示
    """

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

    # 同步整改页面两个table高亮
    def autoHighlight4(self):
        row = self.tableWidget_2.currentRow()
        self.tableWidget_4.setCurrentCell(row, 0)

    def autoHighlight5(self):
        row = self.tableWidget_4.currentRow()
        self.tableWidget_2.setCurrentCell(row, 0)

    """
    @页面展示函数
    """

    # 展示问题表格
    def displayQuestionTable(self):
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改

        # 清空表格
        self.tableWidget.clear()

        font = QFont('Microsoft YaHei UI', 14, QFont.Black)
        font.setBold(True)
        # 设置表头字体
        self.tableWidget.horizontalHeader().setFont(font)

        if self.pro_tag != -1:
            # 公文整改项目
            if self.xh_lc != -1:
                self.tableWidget.setColumnCount(17)
                self.tableWidget.setHorizontalHeaderLabels(
                    ['序号', '问题顺序号', '被审计领导干部', '所在地方或单位', '报送专报期号', '问题源自审计报告文号', '出具审计专报时间', '审计组组长',
                     '审计组主审', '问题描述', '问题一级分类', '问题二级分类', '问题三级分类', '问题四级分类', '备注', '问题金额', '移送及处理情况'])

                # 选出该项目对应的所有问题
                sql = 'select problem.序号,problem.问题顺序号,problem.被审计领导干部,problem.所在地方或单位,sendfile.发文字号,problem.审计报告文号,' \
                      'problem.出具审计报告时间,problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,' \
                      'problem.问题三级分类,problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况 from problem,sendfile ' \
                      'where problem.发文序号 = %s and sendfile.序号 = problem.发文序号' % self.xh_send
            # 经责整改项目
            else:
                self.tableWidget.setColumnCount(20)
                self.tableWidget.setHorizontalHeaderLabels(
                    ['序号', '问题顺序号', '被审计领导干部', '所在地方或单位', '报送文号', '审计报告（意见）文号', '经责结果报告文号', '出具审计专报时间', '审计组组长',
                     '审计组主审', '问题描述', '是否在审计报告中反映', '是否在结果报告中反映', '审计对象分类', '问题类别', '问题定性', '问题表现形式', '备注',
                     '问题金额（万元）', '移送及处理情况'])

                # 选出该项目对应的所有问题
                sql = "select 序号,问题顺序号,被审计领导干部,所在地方或单位,报送文号,审计意见或报告文号,经责结果报告文号,出具审计报告时间,审计组组长,审计组主审,问题描述,是否在审计报告中反映," \
                      "是否在结果报告中反映,审计对象分类,问题类别,问题定性,问题表现形式,备注,问题金额,移送及处理情况 from problem_jz where 整改序号 = '%s'" % self.xh

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

            font = QFont('Microsoft YaHei UI', 12, QFont.Black)
            font.setBold(False)
            self.tableWidget.hideColumn(0)  # 将问题数据库主键隐藏起来
            self.tableWidget.setFont(font)  # 设置表格内容字体大小
            self.tableWidget.resizeColumnsToContents()  # 根据列调整框大小
            self.tableWidget.resizeRowsToContents()  # 根据行调整框大小
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 表格只可选中行
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # 表格只可选中单行

    # 问题表下的刷新按钮
    def refreshQuestionTable(self):
        self.displayQuestionTable()

    # 显示公文详情
    def displaySendDetail(self):
        sql = "select 发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
              "领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
              "序号 =  %s" % self.xh_send
        data = tools.executeSql(sql)
        # print(data)

        # 专报类型
        if self.send_type == 1:
            self.lineEdit_3.setReadOnly(True)  # 专报标题
            self.lineEdit_4.setReadOnly(True)  # 报送范围
            self.lineEdit_5.setReadOnly(True)  # 发文字号
            self.lineEdit_13.setReadOnly(True)  # 紧急程度
            self.lineEdit_10.setReadOnly(True)  # 秘密等级
            self.lineEdit_14.setReadOnly(True)  # 是否公开
            self.lineEdit_11.setReadOnly(True)  # 拟稿人
            self.lineEdit_15.setReadOnly(True)  # 拟稿处室分管厅领导
            self.lineEdit_12.setReadOnly(True)  # 拟稿处室
            self.lineEdit_16.setReadOnly(True)  # 综合处编辑
            self.lineEdit_18.setReadOnly(True)  # 综合处审核
            self.lineEdit_19.setReadOnly(True)  # 秘书处审核
            self.lineEdit_17.setReadOnly(True)  # 综合处分管厅领导
            self.lineEdit_20.setReadOnly(True)  # 审计办主任
            self.lineEdit_file.setReadOnly(True)  # 报文内容
            self.dateEdit_3.setReadOnly(True)  # 办文日期

            # 设置文本输入不可写
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

            # 如果报文内容为空,打开文件按钮不可点击
            if self.lineEdit_file.text() == "":
                self.pushButton_file_2.setDisabled(True)
            else:
                self.pushButton_file_2.setEnabled(True)

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

            # 设置文本输入不可写
            self.lineEdit_num.setReadOnly(True)  # 发文字号
            self.lineEdit_num_3.setReadOnly(True)  # 公文标题
            self.textEdit_2.setReadOnly(True)  # 领导审核意见
            self.textEdit_4.setReadOnly(True)  # 审计办领导审核意见
            self.textEdit_3.setReadOnly(True)  # 办文情况说明和拟办意见
            self.lineEdit_file_3.setReadOnly(True)  # 公文内容
            self.lineEdit_22.setReadOnly(True)  # 保密等级
            self.lineEdit_23.setReadOnly(True)  # 是否公开
            self.lineEdit_29.setReadOnly(True)  # 紧急程度
            self.lineEdit_24.setReadOnly(True)  # 审核
            self.lineEdit_26.setReadOnly(True)  # 承办处室
            self.lineEdit_27.setReadOnly(True)  # 承办人
            self.lineEdit_28.setReadOnly(True)  # 联系电话
            self.dateEdit_7.setReadOnly(True)  # 办文日期
            self.dateEdit_6.setReadOnly(True)  # 日期
            self.lineEdit_25.setReadOnly(True)  # 办文编号

            # 如果报文内容为空,打开文件按钮不可点击
            if self.lineEdit_file_3.text() == "":
                self.pushButton_file.setDisabled(True)
            else:
                self.pushButton_file.setEnabled(True)

    # 展示收文信息
    def displayRevDetail(self):
        sql = "select 收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,内容摘要和拟办意见,领导批示,处理结果,审核,收文字号,承办处室,承办人,联系电话 from revfile where " \
              "序号 = %s" % self.xh_rev
        data = tools.executeSql(sql)

        self.dateEdit.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
        self.lineEdit_6.setText(data[0][1])  # 密级
        self.lineEdit_7.setText(data[0][2])  # 是否公开
        self.lineEdit_36.setText(data[0][3])  # 紧急程度
        self.lineEdit_38.setText(data[0][4])  # 收文来文单位
        self.lineEdit_37.setText(data[0][5])  # 收文来文字号
        self.lineEdit_35.setText(data[0][6])  # 文件标题
        self.textEdit.setText(data[0][7])  # 内容摘要和拟办意见
        self.textEdit_5.setText(data[0][8])  # 领导批示
        self.lineEdit_33.setText(data[0][9])  # 处理结果
        self.lineEdit_30.setText(data[0][10])  # 审核
        self.lineEdit_31.setText(data[0][11])  # 办文编号
        self.lineEdit_34.setText(data[0][12])  # 承办处室
        self.lineEdit_32.setText(data[0][13])  # 承办人
        self.lineEdit_50.setText(data[0][14])  # 联系电话

        # 设置文本输入不可写
        self.dateEdit.setReadOnly(True)  # 收文时间
        self.lineEdit_6.setReadOnly(True)  # 密级
        self.lineEdit_7.setReadOnly(True)  # 是否公开
        self.lineEdit_36.setReadOnly(True)  # 紧急程度
        self.lineEdit_38.setReadOnly(True)  # 收文来文单位
        self.lineEdit_37.setReadOnly(True)  # 收文来文字号
        self.lineEdit_35.setReadOnly(True)  # 文件标题
        self.textEdit.setReadOnly(True)  # 内容摘要和拟办意见
        self.textEdit_5.setReadOnly(True)  # 领导批示
        self.lineEdit_33.setReadOnly(True)  # 处理结果
        self.lineEdit_30.setReadOnly(True)  # 审核
        self.lineEdit_31.setReadOnly(True)  # 办文编号
        self.lineEdit_34.setReadOnly(True)  # 承办处室
        self.lineEdit_32.setReadOnly(True)  # 承办人
        self.lineEdit_50.setReadOnly(True)  # 联系电话

    # 展示批文信息
    def displayCorDetail(self):
        # 设置不可修改,list默认不可修改
        self.dateEdit_2.setReadOnly(True)  # 收文时间
        self.lineEdit_8.setReadOnly(True)  # 密级
        self.lineEdit_9.setReadOnly(True)  # 是否公开
        self.lineEdit_40.setReadOnly(True)  # 紧急程度
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 批文来文单位
        self.listWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 批文来文字号
        self.lineEdit_43.setReadOnly(True)  # 文件标题
        self.listWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 省领导内容摘要和拟办意见
        self.lineEdit_21.setReadOnly(True)  # 厅领导内容摘要和拟办意见
        self.textEdit_7.setReadOnly(True)  # 领导批示
        self.lineEdit_48.setReadOnly(True)  # 处理结果
        self.lineEdit_49.setReadOnly(True)  # 审核
        self.lineEdit_44.setReadOnly(True)  # 批文编号
        self.lineEdit_45.setReadOnly(True)  # 承办处室
        self.lineEdit_46.setReadOnly(True)  # 承办人
        self.lineEdit_47.setReadOnly(True)  # 联系电话

        # 获取批文数量
        cor_num = len(self.xh_cor_list)

        # 表示收文已经完成批改,此时读取数据库
        if cor_num != 0:
            self.comboBox_dict.clear()  # 清空当前字典
            self.comboBox.disconnect()  # 先断开comboBox,防止绑定函数出错
            self.comboBox.clear()  # 清空复选框

            sql = "select 序号,批文字号 from corfile where corfile.流程序号 = %s " % self.xh_lc
            result = tools.executeSql(sql)
            index = 0
            if len(result) != 0:
                for i in result:
                    self.comboBox_dict[index] = i[0]
                    self.comboBox.addItem(i[1])
                    index = index + 1

            # print("当前下拉框字典:" + str(self.comboBox_dict))

            # 有了数据后再重新绑定
            self.comboBox.currentIndexChanged.connect(
                lambda: self.displayCorForIndex(xh_cur_cor=self.comboBox_dict[self.comboBox.currentIndex()]))

            xh_cur_cor = self.comboBox_dict[self.comboBox.currentIndex()]

            self.displayCorForIndex(xh_cur_cor)

    # 展示某一个批文页面
    def displayCorForIndex(self, xh_cur_cor):
        sql = "select 收文时间,秘密等级,是否公开,紧急程度,批文标题,处理结果,审核,批文字号,承办处室,承办人,联系电话,内容摘要和拟办意见," \
              "领导批示 from corfile where 序号 = %s" % xh_cur_cor
        data = tools.executeSql(sql)

        self.dateEdit_2.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
        self.lineEdit_8.setText(data[0][1])  # 密级
        self.lineEdit_9.setText(data[0][2])  # 是否公开
        self.lineEdit_40.setText(data[0][3])  # 紧急程度
        self.lineEdit_43.setText(data[0][4])  # 文件标题
        self.lineEdit_48.setText(data[0][5])  # 处理结果
        self.lineEdit_49.setText(data[0][6])  # 审核
        self.lineEdit_44.setText(data[0][7])  # 批文编号
        self.lineEdit_45.setText(data[0][8])  # 承办处室
        self.lineEdit_46.setText(data[0][9])  # 承办人
        self.lineEdit_47.setText(data[0][10])  # 联系电话
        self.lineEdit_21.setText(data[0][11])  # 厅领导内容摘要和拟办意见
        self.textEdit_7.setText(data[0][12])  # 领导批示

        sql = "select 领导来文单位,领导来文字号,领导内容摘要和领导批示 from instruction where 批文序号 = %s" % xh_cur_cor
        data = tools.executeSql(sql)

        # 先清空list
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        if len(data) != 0:
            for i in data:
                self.listWidget.addItem(i[0])  # 领导来文单位
                self.listWidget_2.addItem(i[1])  # 领导来文字号
                self.listWidget_3.addItem(i[2])  # 省领导内容摘要和拟办意见

    # 展示整改发函页面
    def displayZgfh(self):
        # 清空list
        self.listWidget_4.clear()

        # 整改文件输入栏不可编辑
        self.lineEdit.setReadOnly(True)

        # 将所有整改发函文件名显示在list中
        sql = "select 整改发函内容 from zgword where 整改序号 = %s" % self.xh
        data = tools.executeSql(sql)

        if len(data) == 0:
            self.zgfh_tag = -1
            self.commandLinkButton_5.setDescription("未完成")
        else:
            self.zgfh_tag = 1
            self.commandLinkButton_5.setDescription("已完成")

        for i in data:
            self.listWidget_4.addItem(i[0])

    # 展示问题总览
    def displayQuestionOverview(self):
        self.lineEdit_2.setReadOnly(True)

        font = QFont('Microsoft YaHei UI', 14, QFont.Black)
        font.setBold(True)
        # 设置表头字体
        self.tableWidget_4.horizontalHeader().setFont(font)
        self.tableWidget_4.setColumnCount(15)
        self.tableWidget_4.setHorizontalHeaderLabels(
            ['主键', '整改责任部门', '应上报整改报告时间', '实际上报整改报告时间', '整改情况', '已整改金额', '追责问责人数', '推动制度建设数目',
             '推动制度建设文件', '部分整改情况具体描述', '未整改原因说明', '下一步整改措施及时限', '认定整改情况', '认定整改金额', '整改率'])

        self.tableWidget_4.hideColumn(0)  # 隐藏整改数据库主键

        # 公文整改项目
        if self.xh_lc != -1:
            sql = "select * from problem,rectification where problem.发文序号 = %s and problem.序号 = " \
                  "rectification.问题序号" % self.xh_send
        # 经责整改项目
        else:
            sql = "select * from problem_jz,rectification_jz where problem_jz.整改序号 = %s and problem_jz.序号 = " \
                  "rectification_jz.问题序号" % self.xh
        result = tools.executeSql(sql)
        if len(result) != 0:
            self.zglr_tag = 1
            self.commandLinkButton_6.setDescription("已完成")
            self.pushButton_9.setEnabled(True)
            self.pushButton_10.setEnabled(True)
        else:
            self.zglr_tag = -1
            self.commandLinkButton_6.setDescription("未完成")
            self.pushButton_9.setDisabled(True)
            self.pushButton_10.setDisabled(True)

        # 公文整改项目
        if self.xh_lc != -1:
            font = QFont('Microsoft YaHei UI', 14, QFont.Black)
            font.setBold(True)
            # 设置表头字体
            self.tableWidget_2.horizontalHeader().setFont(font)
            self.tableWidget_2.setColumnCount(17)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['整改上报次序', '问题顺序号', '被审计领导干部', '所在地方或单位', '报送专报期号', '问题源自审计报告文号', '出具审计专报时间', '审计组组长',
                 '审计组主审', '问题描述', '问题一级分类', '问题二级分类', '问题三级分类', '问题四级分类', '备注', '问题金额', '移送及处理情况'])

            sql = 'select rectification.上报次序,problem.问题顺序号,problem.被审计领导干部,problem.所在地方或单位,sendfile.发文字号,' \
                  'problem.审计报告文号,problem.出具审计报告时间,problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,' \
                  'problem.问题二级分类,problem.问题三级分类,problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况,' \
                  'rectification.序号,rectification.整改责任部门,rectification.应上报整改报告时间,rectification.实际上报整改报告时间,' \
                  'rectification.整改情况,rectification.已整改金额,rectification.追责问责人数,rectification.推动制度建设数目,' \
                  'rectification.推动制度建设文件,rectification.部分整改情况具体描述,rectification.未整改原因说明,rectification.下一步整改措施及时限,' \
                  'rectification.认定整改情况,rectification.认定整改金额,rectification.整改率 from sendfile left outer join problem ' \
                  'on sendfile.序号 = problem.发文序号 left outer join rectification on problem.序号 = rectification.问题序号 ' \
                  'where sendfile.序号 = %s order by problem.问题顺序号 asc,rectification.上报次序 desc' % self.xh_send

        # 经责整改项目
        elif self.xh_lc == -1:
            font = QFont('Microsoft YaHei UI', 14, QFont.Black)
            font.setBold(True)
            # 设置表头字体
            self.tableWidget_2.horizontalHeader().setFont(font)
            self.tableWidget_2.setColumnCount(20)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['整改上报次序', '问题顺序号', '被审计领导干部', '所在地方或单位', '报送文号', '审计报告（意见）文号', '经责结果报告文号', '出具审计专报时间', '审计组组长',
                 '审计组主审', '问题描述', '是否在审计报告中反映', '是否在结果报告中反映', '审计对象分类', '问题类别', '问题定性', '问题表现形式', '备注',
                 '问题金额（万元）', '移送及处理情况'])

            sql = 'select rectification_jz.上报次序,problem_jz.问题顺序号,problem_jz.被审计领导干部,problem_jz.所在地方或单位,' \
                  'problem_jz.报送文号,problem_jz.审计意见或报告文号,problem_jz.经责结果报告文号,problem_jz.出具审计报告时间,problem_jz.审计组组长,' \
                  'problem_jz.审计组主审,problem_jz.问题描述,problem_jz.是否在审计报告中反映,problem_jz.是否在结果报告中反映,problem_jz.审计对象分类,' \
                  'problem_jz.问题类别,problem_jz.问题定性,problem_jz.问题表现形式,problem_jz.备注,problem_jz.问题金额,' \
                  'problem_jz.移送及处理情况,rectification_jz.序号,rectification_jz.整改责任部门,rectification_jz.应上报整改报告时间,' \
                  'rectification_jz.实际上报整改报告时间,rectification_jz.整改情况,rectification_jz.已整改金额,rectification_jz.追责问责人数,' \
                  'rectification_jz.推动制度建设数目,rectification_jz.推动制度建设文件,rectification_jz.部分整改情况具体描述,' \
                  'rectification_jz.未整改原因说明,rectification_jz.下一步整改措施及时限,rectification_jz.认定整改情况,' \
                  'rectification_jz.认定整改金额,rectification_jz.整改率 from problem_jz left outer join ' \
                  'rectification_jz on problem_jz.序号 = rectification_jz.问题序号 where problem_jz.整改序号 = %s order by ' \
                  'problem_jz.问题顺序号 asc,rectification_jz.上报次序 desc' % self.xh

        data = tools.executeSql(sql)

        # 打印结果
        # print(data)

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_2.setRowCount(size)
        self.tableWidget_4.setRowCount(size)

        # tableWidget_2和_4开始分割列数
        if self.xh_lc != -1:
            split = 17
        else:
            split = 20

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    if y < split:
                        self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                    else:
                        self.tableWidget_4.setItem(x, y - split, QtWidgets.QTableWidgetItem("/"))
                else:
                    if y < split:
                        self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                    else:
                        self.tableWidget_4.setItem(x, y - split, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改
        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 表格只可选中行
        self.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # 表格只可选中单行

        self.tableWidget_4.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改
        self.tableWidget_4.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_4.resizeRowsToContents()  # 根据行调整框大小
        self.tableWidget_4.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 表格只可选中行
        self.tableWidget_4.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # 表格只可选中单行

    """
    @文件选择按钮函数
    弹出文件系统页面,选择相应类型文件
    """

    # 选择整改发函文件
    def chooseFileZgfh(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc);;WPS(*.wps)")
        self.lineEdit.setText(p[0])

    # 选择问题表
    def chooseQuestionExcel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Excel(*.xlsx);;Excel(*.xls);;ET(*.et)")
        self.lineEdit_2.setText(p[0])

    """
    @整改发函文件操作
    增删查
    """

    # 保存整改发函文件
    def saveZgfh(self):
        input_file_path = self.lineEdit.text()
        if input_file_path != "":
            filename = tools.getFileName(input_file_path)  # 文件名
            if tools.judgeExistSameNameFile(tools.zgfh_word_path, filename):
                QtWidgets.QMessageBox.critical(None, "导入失败", "存在相同的文件名！")
            else:
                sql = "insert into zgword values(NULL,%s,'%s')" % (self.xh, filename)
                tools.executeSql(sql)
                # 导入文件
                tools.copyFile(input_file_path, tools.zgfh_word_path)

                QtWidgets.QMessageBox.information(None, "提示", "保存成功！")

                # 清空整改文件名输入栏
                self.lineEdit.clear()

                self.displayZgfh()
        else:
            QtWidgets.QMessageBox.information(None, "提示", "请选择文件！")

    # 打开选择的整改发函文件
    def openZgfh(self):
        row = self.listWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择整改发函文件！")
        else:
            filename = self.listWidget_4.currentItem().text()
            tools.openFile(file_folder="zgfh_word", file=filename)

    # 删除选择的整改发函文件
    def deleteZgfh(self):
        row = self.listWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择整改发函文件！")
        else:
            filename = self.listWidget_4.currentItem().text()
            tools.deleteFile(tools.zgfh_word_path, filename)
            sql = "delete from zgword where 整改发函内容 = '%s'" % filename
            tools.executeSql(sql)
            QtWidgets.QMessageBox.information(None, "提示", "删除成功！")

            self.displayZgfh()

    """
    @excel操作
    input&output
    """

    # 根据excel中的右边问题整改信息导入问题表
    def importExcelProblemZg(self):
        path = self.lineEdit_2.text()
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
                print('Sheet Name: %s\nSheet cols: %s\nSheet rows: %s' % (sheet_name, sheet_cols, sheet_rows))

                check_tag = 1  # excel输入合法检测标识,如果为1表示excel中所有数据合法,可以写入数据库

                # excel表格分割列数
                if self.xh_lc != -1:
                    split = 15
                else:
                    split = 18

                # 读取excel数据进行检测
                for i in range(4, sheet_rows):
                    # 判断问题顺序号是否为整数
                    if not tools.judgeInteger(sheet.row(i)[0].value):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行: 问题顺序号应为整数！" % str(i + 1))
                        break
                    # 出具审计专报时间,判断是否为合法时间
                    if isinstance(sheet.row(i)[2 + split].value, str):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：出具审计专报时间格式错误！" % str(i + 1))
                        break
                    # 实际上报整改时间,判断是否为合法时间
                    if isinstance(sheet.row(i)[3 + split].value, str):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：实际上报整改时间格式错误！" % str(i + 1))
                        break
                    # 已整改金额,判断是否为浮点数
                    if not isinstance(sheet.row(i)[5 + split].value, float):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：已整改金额应为数字！" % str(i + 1))
                        break
                    # 追责问责人数,判断是否为整数
                    if not tools.judgeInteger(sheet.row(i)[6 + split].value):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：追责问责人数应为整数！" % str(i + 1))
                        break
                    # 推动制度建设数目,判断是否为整数
                    if not tools.judgeInteger(sheet.row(i)[7 + split].value):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：推动制度建设数目应为整数！" % str(i + 1))
                        break
                    # 认定整改金额,判断是否为浮点数
                    if not isinstance(sheet.row(i)[13 + split].value, float):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：认定整改金额应为数字！" % str(i + 1))
                        break
                if sheet_rows == 4:
                    check_tag = 0
                    QtWidgets.QMessageBox.information(None, "提示", "表格数据为空！")

                if check_tag == 1:
                    flag_beforZg = 0    #设置未整改标记
                    flag_inZg = 0    #设置部分整改标记
                    flag_passZg = 0    #设置已整改标记
                    # 读取excel数据
                    for i in range(4, sheet_rows):
                        cell_problem_key1 = int(sheet.row(i)[0].value)  # 问题顺序号
                        if self.xh_lc != -1:
                            cell_problem_key2 = self.xh_send  # 发文序号,用来和问题顺序号一起唯一定位一个问题,直接读取变量,而非excel
                        else:
                            cell_problem_key2 = self.xh  # 整改序号,用来和问题顺序号一起唯一定位一个问题,直接读取变量,而非excel
                        cell_right_i_1 = sheet.row(i)[1 + split].value  # 整改责任部门
                        cell_right_i_2 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 2 + split).value, 0).strftime(
                            "%Y/%m/%d")  # 应上报整改报告时间
                        cell_right_i_3 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 3 + split).value, 0).strftime(
                            "%Y/%m/%d")  # 实际上报整改报告时间
                        cell_right_i_4 = sheet.row(i)[4 + split].value  # 整改情况
                        cell_right_i_5 = sheet.row(i)[5 + split].value  # 已整改金额
                        cell_right_i_6 = int(sheet.row(i)[6 + split].value)  # 追责问责人数
                        cell_right_i_7 = int(sheet.row(i)[7 + split].value)  # 推动制度建设数目
                        cell_right_i_8 = sheet.row(i)[8 + split].value  # 推动制度建设文件
                        cell_right_i_9 = sheet.row(i)[9 + split].value  # 部分整改情况具体描述
                        cell_right_i_10 = sheet.row(i)[10 + split].value  # 未整改原因说明
                        cell_right_i_11 = sheet.row(i)[11 + split].value  # 下一步整改措施及时限
                        cell_right_i_12 = sheet.row(i)[12 + split].value  # 认定整改情况
                        cell_right_i_13 = sheet.row(i)[13 + split].value  # 认定整改金额
                        cell_right_i_14 = sheet.row(i)[14 + split].value  # 整改率
                        #根据认定整改情况对标记值进行自增
                        if(cell_right_i_12 == "已整改"):
                            flag_passZg = flag_passZg + 1
                        elif(cell_right_i_12 == "未整改"):
                            flag_beforZg = flag_beforZg + 1
                        elif(cell_right_i_12 == "部分整改"):
                            flag_inZg = flag_inZg + 1

                        # 办文流程整改
                        if self.xh_lc != -1:
                            # 先找到问题序号,再确定整改措施对应的是哪个问题.这里的逻辑有待商榷,原因是要用用户在excel中输入的问题顺序号去寻找问题表主键
                            sql = "select 序号 from problem where 问题顺序号 = %s and 发文序号 = %s" \
                                  % (cell_problem_key1, cell_problem_key2)
                            xh_pro = tools.executeSql(sql)[0][0]

                            sql = "select max(上报次序) from rectification where 问题序号 = %s " % xh_pro
                            data = tools.executeSql(sql)

                            # 确认上报批次
                            if data[0][0] is None:
                                order = 1
                            else:
                                order = data[0][0] + 1

                            table = "rectification"

                        # 经责整改
                        else:
                            # 先找到问题序号,再确定整改措施对应的是哪个问题.这里的逻辑有待商榷,原因是要用用户在excel中输入的问题顺序号去寻找问题表主键
                            sql = "select 序号 from problem_jz where 问题顺序号 = %s and 整改序号 = %s" \
                                  % (cell_problem_key1, cell_problem_key2)
                            xh_pro = tools.executeSql(sql)[0][0]

                            sql = "select max(上报次序) from rectification_jz where 问题序号 = %s " % xh_pro
                            data = tools.executeSql(sql)

                            # 确认上报批次
                            if data[0][0] is None:
                                order = 1
                            else:
                                order = data[0][0] + 1

                            table = "rectification_jz"

                        sql = "insert into '%s' values(NULL,%s,'%s','%s','%s','%s','%s','%s','%s','%s'," \
                              "'%s','%s','%s','%s','%s','%s','%s')" % (
                                  table, xh_pro, order, cell_right_i_1, cell_right_i_2, cell_right_i_3, cell_right_i_4,
                                  cell_right_i_5, cell_right_i_6, cell_right_i_7, cell_right_i_8, cell_right_i_9,
                                  cell_right_i_10, cell_right_i_11, cell_right_i_12, cell_right_i_13,
                                  cell_right_i_14)
                        tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(None, "提示", "录入成功！")
                    #录入成功以后，进行整改总览表里面，是否整改完成字段的设置
                    print(flag_beforZg)
                    print(flag_inZg)
                    print(flag_passZg)
                    print(self.xh_send)

                    sql = "select sendfile.发文字号 from sendfile where 序号 = %s" % (self.xh_send)   #根据发文序号找到发文字号
                    data = tools.executeSql(sql)
                    send_file_name = data[0][0]

                    if(flag_inZg != 0):
                        sql = "update zgprocess set 整改状态 = '部分整改' where 标识文号 = '%s'" % (send_file_name)
                        tools.executeSql(sql)
                    if((flag_beforZg != 0) and (flag_passZg != 0)):
                        sql = "update zgprocess set 整改状态 = '部分整改' where 标识文号 = '%s'" % (send_file_name)
                        tools.executeSql(sql)
                    if((flag_beforZg == 0) and (flag_inZg == 0)):
                        sql = "update zgprocess set 整改状态 = '已整改' where 标识文号 = '%s'" % (send_file_name)
                        tools.executeSql(sql)
                    if((flag_inZg == 0) and (flag_passZg == 0)):
                        sql = "update zgprocess set 整改状态 = '未整改' where 标识文号 = '%s'" % (send_file_name)
                        tools.executeSql(sql)

                    self.lineEdit_2.clear()

                    self.displayQuestionOverview()
                else:
                    QtWidgets.QMessageBox.critical(None, "错误", "导入失败！")
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())
        else:
            QtWidgets.QMessageBox.information(None, "提示", "请选择文件！")

    """
    @其他功能
    """
    def deleteRecentProblemZg(self):
        reply = QtWidgets.QMessageBox.question(None, '询问', '是否确认删除最近一次整改上报？', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)  # 询问是否确认删除
        if reply == QtWidgets.QMessageBox.Yes:  # 如果确认删除
            # 公文整改
            if self.xh_lc != -1:
                sql = "select max(rectification.上报次序) from sendfile,problem,rectification where sendfile.序号 = " \
                      "problem.发文序号 and problem.序号 = rectification.问题序号 and sendfile.序号 = %s" % self.xh_send
                max_num = tools.executeSql(sql)[0][0]
                sql = "delete from rectification where 序号 in (select rectification.序号 from sendfile,problem," \
                      "rectification where sendfile.序号 = problem.发文序号 and problem.序号 = rectification.问题序号 and " \
                      "sendfile.序号 = %s) and 上报次序 = %s" % (self.xh_send, max_num)
            # 经责整改
            else:
                sql = "select max(rectification_jz.上报次序) from problem_jz,rectification_jz where problem_jz.序号 = " \
                      "rectification_jz.问题序号 and problem_jz.整改序号 = %s" % self.xh
                max_num = tools.executeSql(sql)[0][0]
                sql = "delete from rectification_jz where 序号 in (select rectification_jz.序号 from problem_jz," \
                      "rectification_jz where problem_jz.序号 = rectification_jz.问题序号 and problem_jz.整改序号 = %s) and " \
                      "上报次序 = %s" % (self.xh, max_num)

            tools.executeSql(sql)
            QtWidgets.QMessageBox.information(None, "提示", "删除成功！")

            # 修改流程总览页面是否完成整改字段
            sql = "select sendfile.发文字号 from sendfile where sendfile.序号 = %s" % (self.xh_send)  # 根据发文序号找到发文字号
            data = tools.executeSql(sql)
            send_file_name = data[0][0]

            sql_findProblemId = "select problem.序号 from problem where problem.发文序号 = '%s'" % (self.xh_send)    #根据发文序号找到所有问题序号
            data = tools.executeSql(sql_findProblemId)
            problemId = data[0][0]

            sql_len = "select rectification.序号 from rectification where rectification.问题序号 = '%s'" %(problemId) #根据问题序号找对应的整改序号有多少个
            data = tools.executeSql(sql_len)
            size = len(data)

            if (size == 0): #如果问题序号没有对应的整改序号，说明整改上报已被删除干净，设置为未整改
                sql = "update zgprocess set 整改状态 = '未整改' where 标识文号 = '%s'" % (send_file_name)
                tools.executeSql(sql)
                print("设置为未整改")
            else:
                sql_finMaxId = "select max(rectification.上报次序) from rectification where rectification.问题序号 = '%s'" % (
                    problemId)  # 根据问题序号找到最大上报次序
                data = tools.executeSql(sql_finMaxId)
                maxId = data[0][0]
                print(maxId)

                sql_findProblemId = "select problem.序号 from problem where problem.发文序号 = '%s'" % (self.xh_send)  # 根据发文序号找到所有问题序号
                data = tools.executeSql(sql_findProblemId)
                leng = len(data)
                print(data)
                flag_passZg = 0     #已整改流程计数
                flag_beforZg = 0    #未整改流程计数
                flag_inZg = 0       #部分整改流程计数
                for i in range(leng):
                    sql = "select rectification.认定整改情况 from rectification where rectification.问题序号 = '%s' and rectification.上报次序 = '%s'" % (
                    data[i][0], maxId)
                    data_status = tools.executeSql(sql)
                    # 根据认定整改情况对标记值进行自增
                    if (data_status[0][0] == "已整改"):
                        flag_passZg = flag_passZg + 1
                    elif (data_status[0][0] == "未整改"):
                        flag_beforZg = flag_beforZg + 1
                    elif (data_status[0][0] == "部分整改"):
                        flag_inZg = flag_inZg + 1

                if (flag_inZg != 0):
                    sql = "update zgprocess set 整改状态 = '部分整改' where 标识文号 = '%s'" % (send_file_name)
                    tools.executeSql(sql)
                if ((flag_beforZg != 0) and (flag_passZg != 0)):
                    sql = "update zgprocess set 整改状态 = '部分整改' where 标识文号 = '%s'" % (send_file_name)
                    tools.executeSql(sql)
                if ((flag_beforZg == 0) and (flag_inZg == 0)):
                    sql = "update zgprocess set 整改状态 = '已整改' where 标识文号 = '%s'" % (send_file_name)
                    tools.executeSql(sql)
                if ((flag_inZg == 0) and (flag_passZg == 0)):
                    sql = "update zgprocess set 整改状态 = '未整改' where 标识文号 = '%s'" % (send_file_name)
                    tools.executeSql(sql)

            self.displayQuestionOverview()


