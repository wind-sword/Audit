from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

from uipy_dir.zgdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail
from logis_fir.call_zgrevise import Call_zgrevise
from tools import tools
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

        self.window = None  # 整改子窗口

        # 页面上方流程跳转按钮
        self.commandLinkButton_1.clicked.connect(lambda: self.btjump(btname="1"))
        self.commandLinkButton_2.clicked.connect(lambda: self.btjump(btname="2"))
        self.commandLinkButton_3.clicked.connect(lambda: self.btjump(btname="3"))
        self.commandLinkButton_4.clicked.connect(lambda: self.btjump(btname="4"))
        self.commandLinkButton_5.clicked.connect(lambda: self.btjump(btname="5"))
        self.commandLinkButton_6.clicked.connect(lambda: self.btjump(btname="6"))

        # tab设置
        self.tabWidget.setTabText(0, "问题浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)

        # 绑定按钮或其他控件功能函数
        self.initControlFunction()

        # 同步批文输入框的三个list高亮情况
        self.listWidget.currentRowChanged.connect(self.autoHighlight1)
        self.listWidget_2.currentRowChanged.connect(self.autoHighlight2)
        self.listWidget_3.currentRowChanged.connect(self.autoHighlight3)

        # 同步整改录入两个表的同步显示情况
        self.tableWidget_2.currentCellChanged.connect(self.autoHighlight4)
        self.tableWidget_4.currentCellChanged.connect(self.autoHighlight5)

        # 初始化流程变量
        self.initVar(key)

        # 初始化页面展示
        self.initView()

        # 初始化页面数据
        self.displaySendDetail()

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

    # 关闭tab
    def closeTab(self, index):
        self.tabWidget.removeTab(index)

    # 控件绑定功能函数
    def initControlFunction(self):
        # 打开公文文件
        self.pushButton_file.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file_3.text()))

        # 打开专报文件
        self.pushButton_file_2.clicked.connect(
            lambda: tools.openFile(file_folder="project_word", file=self.lineEdit_file.text()))

        # 问题详情查看
        self.pushButton.clicked.connect(self.jumpQuestionDetail)

        # 打开整改详情修改框
        self.pushButton_10.clicked.connect(self.reviseZgdetail)

        # 打开整改发函文件
        self.pushButton_4.clicked.connect(self.openZgfh)
        # 选择发函文件
        self.pushButton_5.clicked.connect(self.chooseFileZgfh)
        # 保存发函文件
        self.pushButton_6.clicked.connect(self.saveZgfh)
        # 删除发函文件
        self.pushButton_2.clicked.connect(self.deleteZgfh)

        # 选择问题Excel表
        self.pushButton_7.clicked.connect(self.chooseQuestionExcel)
        # 导入问题整改情况
        self.pushButton_8.clicked.connect(self.importExcel)

        # 绑定下拉框切换
        self.comboBox.currentIndexChanged.connect(
            lambda: self.displayCorFileForIndex(xh_cur_cor=self.comboBox_dict[self.comboBox.currentIndex()]))

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

    # 用发文字号初始化变量
    def initVar(self, key):
        # 整改序号
        self.xh = key
        # 初始化流程序号,发文序号,收文序号
        sql = "select bwprocess.序号,bwprocess.发文序号,bwprocess.收文序号 from bwprocess,standingbook where " \
              "bwprocess.序号 = standingbook.流程序号 and standingbook.序号 = %s" % key
        data = tools.executeSql(sql)
        # print(data)
        self.xh_lc = data[0][0]
        self.xh_send = data[0][1]
        self.xh_rev = data[0][2]

        # 初始化批文序号列表
        sql = 'select bw_cast_cor.批文序号 from bw_cast_cor where bw_cast_cor.流程序号 = %s' % self.xh_lc
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

        # 初始化整改发函状态
        sql = "select * from zgword where 整改序号 = %s" % self.xh
        result = tools.executeSql(sql)
        if len(result) != 0:
            self.zgfh_tag = 1

        # 初始化整改措施是否录入
        sql = "select * from problem,rectification where problem.发文序号 = %s and problem.序号 = rectification.问题序号" % self.xh_send
        result = tools.executeSql(sql)
        if len(result) != 0:
            self.zglr_tag = 1

        # 初始化流程状态
        self.commandLinkButton_1.setDescription("已完成")
        self.commandLinkButton_3.setDescription("已完成")
        self.commandLinkButton_4.setDescription("已完成")
        if self.pro_tag == 1:
            self.commandLinkButton_2.setDescription("已完成")
        if self.zgfh_tag == 1:
            self.commandLinkButton_5.setDescription("已完成")
        if self.zglr_tag == 1:
            self.commandLinkButton_6.setDescription("已完成")

    # 初始化整改界面显示
    def initView(self):
        if self.send_type == 1:
            self.stackedWidget.setCurrentIndex(0)
        elif self.send_type == 2:
            self.stackedWidget.setCurrentIndex(1)

        # 设置整改流程标题为发文标题
        sql = "select 发文标题 from sendfile where 序号 = %s" % self.xh_send
        data = tools.executeSql(sql)
        self.label_title.setText(data[0][0])

    # 跳转问题详情
    def jumpQuestionDetail(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.tableWidget.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择问题！")
        else:
            # 问题表主键,问题序号
            key = self.tableWidget.item(row, 0).text()
            tab_new = Call_quedetail(key)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "问题详情")
            self.tabWidget.setCurrentIndex(tab_num)

    # 打开整改详情修改框
    def reviseZgdetail(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.tableWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择整改措施！")
        else:
            # 整改表主键
            key = self.tableWidget_4.item(row, 0).text()
            self.window = Call_zgrevise(key)
            self.window.setWindowTitle("整改详情")
            self.window.exec()

    # 展示问题表格
    def displayQuestionTable(self):
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改

        self.tableWidget.hideColumn(0)  # 将问题数据库主键隐藏起来

        if self.pro_tag != -1:
            # 选出该项目对应的所有问题
            sql = 'select problem.序号,problem.问题顺序号,problem.被审计领导干部,problem.所在地方或单位,sendfile.发文字号,problem.审计报告文号,' \
                  'problem.出具审计报告时间,problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,' \
                  'problem.问题三级分类,problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况 from problem,sendfile where ' \
                  'problem.发文序号 = %s and sendfile.序号 = problem.发文序号' % self.xh_send
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
            self.tableWidget.resizeRowsToContents()  # 根据行调整框大小
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 表格只可选中行
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # 表格只可选中单行

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
        self.lineEdit_39.setText(data[0][14])  # 联系电话

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
        self.lineEdit_39.setReadOnly(True)  # 联系电话

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

            sql = "select corfile.序号,corfile.批文字号 from corfile,bw_cast_cor where bw_cast_cor.流程序号 = %s and corfile.序号 " \
                  "= bw_cast_cor.批文序号" % self.xh_lc
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

        self.tableWidget_4.hideColumn(0)  # 隐藏整改数据库主键

        # 初始化整改措施是否录入
        sql = "select * from problem,rectification where problem.发文序号 = %s and problem.序号 = rectification.问题序号" % self.xh_send
        result = tools.executeSql(sql)
        if len(result) != 0:
            self.zglr_tag = 1
            self.commandLinkButton_6.setDescription("已完成")
        else:
            self.zglr_tag = -1
            self.commandLinkButton_6.setDescription("未完成")

        if self.pro_tag != -1:
            sql = 'select rectification.上报次序,problem.问题顺序号,problem.被审计领导干部,problem.所在地方或单位,sendfile.发文字号,' \
                  'problem.审计报告文号,problem.出具审计报告时间,problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,' \
                  'problem.问题二级分类,problem.问题三级分类,problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况,' \
                  'rectification.序号,rectification.整改责任部门,rectification.应上报整改报告时间,rectification.实际上报整改报告时间,' \
                  'rectification.整改情况,rectification.已整改金额,rectification.追责问责人数,rectification.推动制度建设数目,' \
                  'rectification.推动制度建设文件,rectification.部分整改情况具体描述,rectification.未整改原因说明,rectification.下一步整改措施及时限,' \
                  'rectification.认定整改情况,rectification.认定整改金额,rectification.整改率 from sendfile left outer join problem ' \
                  'on sendfile.序号 = problem.发文序号 left outer join rectification on problem.序号 = rectification.问题序号 ' \
                  'where sendfile.序号 = %s order by rectification.上报次序 desc,problem.问题顺序号 asc' % self.xh_send
            data = tools.executeSql(sql)

            # 打印结果
            # print(data)

            size = len(data)
            # print("项目数目为:"+str(size))
            self.tableWidget_2.setRowCount(size)
            self.tableWidget_4.setRowCount(size)

            x = 0
            for i in data:
                y = 0
                for j in i:
                    if data[x][y] is None:
                        if y < 17:
                            self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                        else:
                            self.tableWidget_4.setItem(x, y - 17, QtWidgets.QTableWidgetItem("/"))
                    else:
                        if y < 17:
                            self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                        else:
                            self.tableWidget_4.setItem(x, y - 17, QtWidgets.QTableWidgetItem(str(data[x][y])))
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

    # 选择整改发函文件
    def chooseFileZgfh(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit.setText(p[0])

    # 选择问题表
    def chooseQuestionExcel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_2.setText(p[0])

    # 保存整改发函文件
    def saveZgfh(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        input_file_path = self.lineEdit.text()
        if input_file_path != "":
            filename = tools.getFileName(input_file_path)  # 文件名
            sql = "insert into zgword values(NULL,%s,'%s')" % (self.xh, filename)
            tools.executeSql(sql)
            # 导入文件
            tools.copyFile(input_file_path, tools.zgfh_word_path)

            QtWidgets.QMessageBox.information(w, "提示", "保存成功！")

            # 清空整改文件名输入栏
            self.lineEdit.clear()

            self.displayZgfh()
        else:
            QtWidgets.QMessageBox.information(w, "提示", "请选择文件!")

    # 打开选择的整改发函文件
    def openZgfh(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.listWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择整改发函文件！")
        else:
            filename = self.listWidget_4.currentItem().text()
            tools.openFile(file_folder="zgfh_word", file=filename)

    # 删除选择的整改发函文件
    def deleteZgfh(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        row = self.listWidget_4.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(w, "提示", "请选择整改发函文件！")
        else:
            filename = self.listWidget_4.currentItem().text()
            tools.deleteFile(tools.zgfh_word_path, filename)
            sql = "delete from zgword where 整改发函内容 = '%s'" % filename
            tools.executeSql(sql)
            QtWidgets.QMessageBox.information(w, "提示", "删除成功！")

            self.displayZgfh()

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
            sheet_rows = sheet.nrows  # 获得行数
            print('Sheet Name: %s\nSheet cols: %s\nSheet rows: %s' % (sheet_name, sheet_cols, sheet_rows))

            # 读取excel数据
            for i in range(4, sheet_rows):
                cell_i_0 = sheet.row(i)[0].value  # 问题顺序号
                # cell_i_3 = sheet.row(i)[3].value  # 报送专报期号
                cell_i_3 = self.xh_send  # 报送专报期号,忽略excel表中发文字号这一列,直接读入发文序号
                cell_i_16 = sheet.row(i)[16].value  # 整改责任部门
                cell_i_17 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 17).value, 0).strftime("%Y/%m/%d")  # 应上报整改报告时间
                cell_i_18 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 18).value, 0).strftime("%Y/%m/%d")  #
                # 实际上报整改报告时间
                cell_i_19 = sheet.row(i)[19].value  # 整改情况
                cell_i_20 = sheet.row(i)[20].value  # 已整改金额
                cell_i_21 = int(sheet.row(i)[21].value)  # 追责问责人数
                cell_i_22 = int(sheet.row(i)[22].value)  # 推动制度建设数目
                cell_i_23 = sheet.row(i)[23].value  # 推动制度建设文件
                cell_i_24 = sheet.row(i)[24].value  # 部分整改情况具体描述
                cell_i_25 = sheet.row(i)[25].value  # 未整改原因说明
                cell_i_26 = sheet.row(i)[26].value  # 下一步整改措施及时限
                cell_i_27 = sheet.row(i)[27].value  # 认定整改情况
                cell_i_28 = sheet.row(i)[28].value  # 认定整改金额
                cell_i_29 = sheet.row(i)[29].value  # 整改率

                # 先找到问题序号,再确定整改措施对应的是哪个问题.这里的逻辑有待商榷,原因是要用用户在excel中输入的问题顺序号去寻找问题表主键
                sql = "select 序号 from problem where 问题顺序号 = %s and 发文序号 = %s" % (int(cell_i_0), cell_i_3)
                xh_pro = tools.executeSql(sql)[0][0]

                sql = "select max(上报次序) from rectification where 问题序号 = %s " % xh_pro
                data = tools.executeSql(sql)

                if data[0][0] is None:
                    num = 1
                else:
                    num = data[0][0] + 1

                sql = "insert into rectification values(NULL,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s','%s','%s')" % (
                          xh_pro, num, cell_i_16, cell_i_17, cell_i_18, cell_i_19, cell_i_20, cell_i_21, cell_i_22,
                          cell_i_23, cell_i_24, cell_i_25, cell_i_26, cell_i_27, cell_i_28, cell_i_29)
                tools.executeSql(sql)

            QtWidgets.QMessageBox.information(w, "提示", "录入成功!")

            self.displayQuestionOverview()
        else:
            QtWidgets.QMessageBox.information(w, "提示", "请选择文件!")
