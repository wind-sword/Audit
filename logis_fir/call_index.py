import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView

from uipy_dir.index import Ui_indexWindow
from logis_fir.call_lcdetail import Call_lcdetail
from logis_fir.call_zgdetail import Call_zgdetail
from logis_fir.call_sendfilebq import Call_sendfilebq
from logis_fir.call_revfilebq import Call_revfilebq
from logis_fir.call_corfilebq import Call_corfilebq
from logis_fir.call_instbq import Call_instbq
from logis_fir.tools import tools


class Call_index(QtWidgets.QMainWindow, Ui_indexWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.window = None  # 补全子窗口
        self.resType1 = ""  # 办文登记表当前type1
        self.resType2 = ""  # 办文登记表当前type2

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 页面对应关系 0：流程总览 page_lczl | 1：整改台账 page_zgtz | 2：发文办理 page_fwbl  |  3：收文办理 page_swbl | 4:收文浏览 page_tjfx
        # |5：统计分析 page_tjfx
        self.btlczl.clicked.connect(lambda: self.btjump(btname="lczl"))
        self.btfwbl.clicked.connect(lambda: self.btjump(btname="fwbl"))
        self.btswbl.clicked.connect(lambda: self.btjump(btname="swbl"))
        self.btswll.clicked.connect(lambda: self.btjump(btname="swll"))
        self.btzgtz.clicked.connect(lambda: self.btjump(btname="zgtz"))
        self.btcx.clicked.connect(lambda: self.btjump(btname="tjfx"))
        self.bttj.clicked.connect(lambda: self.btjump(btname="tjfx"))

        # 整改台账tab
        self.tabWidget.setTabText(0, "整改台账")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.closeTab1)

        # 流程总览tab
        self.tabWidget_lczl.setTabText(0, "流程总览")
        self.tabWidget_lczl.setTabsClosable(1)
        self.tabWidget_lczl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_lczl.tabCloseRequested.connect(self.closeTab2)

        # 公文页面日期和办文编号同步;登记表页面下拉框内容同步
        self.dateEdit_5.dateChanged.connect(self.autoSyn1)
        self.dateEdit_6.dateChanged.connect(self.autoSyn2)
        self.spinBox_2.valueChanged.connect(self.autoSyn3)
        self.spinBox_3.valueChanged.connect(self.autoSyn3)
        self.comboBox_9.currentIndexChanged.connect(self.autoSyn4)
        self.comboBox_2.currentIndexChanged.connect(self.autoSyn5)

        # 绑定按钮或其他控件功能函数
        self.initControlFunction()

        # 初始化显示
        self.stackedWidget.setCurrentIndex(0)
        self.showBwprocessTable()

    # 主页左侧按钮跳转
    def btjump(self, btname):
        if btname == "zgtz":
            self.stackedWidget.setCurrentIndex(1)
            self.tabWidget.setCurrentIndex(0)
            # 初始化显示
            self.showProjectTable()
        elif btname == "lczl":
            self.stackedWidget.setCurrentIndex(0)
            self.tabWidget_lczl.setCurrentIndex(0)
            # 初始化显示
            self.showBwprocessTable()
        elif btname == "fwbl":
            self.stackedWidget.setCurrentIndex(2)
            self.stackedWidget_new.setCurrentIndex(self.comboBox_type.currentIndex())  # 初始化发文办理页面
            # 公文页面初始化显示
            self.lineEdit_file_3.setReadOnly(True)
            self.lineEdit_18.setReadOnly(True)
            self.spinBox_2.setValue(datetime.datetime.now().year)
            self.spinBox_3.setValue(1)
            self.comboBox_9.setCurrentIndex(0)
            self.dateEdit_6.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

            # 专报页面初始化显示
            self.lineEdit_file.setReadOnly(True)
            self.spinBox.setValue(1)
            self.dateEdit_3.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        elif btname == "swbl":
            self.stackedWidget.setCurrentIndex(3)
            # 初始化显示
            self.comboBox_10.setCurrentIndex(0)  # 收文编号:[收文类型]
            self.spinBox_4.setValue(datetime.datetime.now().year)  # 收文编号:[年]
            self.spinBox_5.setValue(1)  # 收文编号:[编号]
            self.dateEdit_4.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        elif btname == "swll":
            self.stackedWidget.setCurrentIndex(4)
        elif btname == "tjfx":
            self.stackedWidget.setCurrentIndex(5)

    # 关闭tab
    def closeTab1(self, index):
        self.tabWidget.removeTab(index)

    def closeTab2(self, index):
        self.tabWidget_lczl.removeTab(index)

    # 同步输入框内容,autoSyn1、2为公文时间同步,3、4、5为公文编号同步,6为办文登记表两个下拉框内容同步
    def autoSyn1(self):
        self.dateEdit_6.setDate(self.dateEdit_5.date())

    def autoSyn2(self):
        self.dateEdit_5.setDate(self.dateEdit_6.date())

    def autoSyn3(self):
        cur = self.comboBox_9.currentText() + '[' + self.spinBox_2.text() + ']' + self.spinBox_3.text() + \
              self.label_51.text()
        self.lineEdit_18.setText(cur)

    def autoSyn4(self):
        cur = self.comboBox_9.currentText() + '[' + self.spinBox_2.text() + ']' + self.spinBox_3.text() + \
              self.label_51.text()
        self.lineEdit_18.setText(cur)

    def autoSyn5(self):
        type1 = self.comboBox_2.currentText()
        self.comboBox.clear()
        if type1 == "发文登记表":
            self.comboBox.addItems(["委文", "委发", "委办文", "委办发", "委函", "委办函", "委便签", "委办便签", "会议纪要", "审计专报"])
        elif type1 == "收文登记表":
            self.comboBox.addItems(["请字", "情字", "综字", "会字", "电字"])
        elif type1 == "批文登记表":
            self.comboBox.addItems(["批字", "批示"])

    # 控件绑定功能函数
    def initControlFunction(self):
        self.bt_search.clicked.connect(self.search)

        self.pushButton_file.clicked.connect(self.choose_file_zb)
        self.pushButton_file_3.clicked.connect(self.choose_file_gw)

        self.pushButton_addac.clicked.connect(self.add_zb)
        self.pushButton_addac_3.clicked.connect(self.add_gw)
        self.pushButton_3.clicked.connect(self.add_rev)

        self.comboBox_type.currentIndexChanged.connect(
            lambda: self.chooseSendfileType(index=self.comboBox_type.currentIndex()))

        self.pushButton.clicked.connect(
            lambda: self.showRegisTable(type1=self.comboBox_2.currentText(), type2=self.comboBox.currentText()))

        self.pushButton_more.clicked.connect(self.tz_detail)

        self.btckxq.clicked.connect(self.lc_detail)
        self.btszzg.clicked.connect(self.lc_to_tz)
        self.pushButton_4.clicked.connect(self.refreshBwprocessTable)

        self.pushButton_2.clicked.connect(self.supplyRegisTable)

    # 显示台账内容
    def showProjectTable(self):
        # 表格不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableWidget.hideColumn(0)  # 将流程数据库主键隐藏起来,作为传参,此处主键为整改序号

        # sql由台账表的流程序号出发,通过多表查询获得台账所有字段
        sql = "select standingbook.序号,bwprocess.流程开始时间,sendfile.发文标题,sendfile.发文字号,revfile.收文标题,revfile.收文字号," \
              "GROUP_CONCAT(corfile.批文标题,'\n'),GROUP_CONCAT(corfile.批文字号,'\n') from standingbook join bwprocess on " \
              "standingbook.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 join revfile on " \
              "bwprocess.收文序号 = revfile.序号 join bw_cast_cor on bwprocess.序号 = bw_cast_cor.流程序号 join corfile on " \
              "bw_cast_cor.批文序号 = corfile.序号 GROUP BY standingbook.序号 "
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

        self.tableWidget.sortItems(1, Qt.DescendingOrder)  # 按照流程建立时间排序

    # 显示发文流程内容
    def showBwprocessTable(self):
        # 表格不可编辑
        self.tableWidget_lczl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget_lczl.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget_lczl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableWidget_lczl.hideColumn(0)  # 将流程数据库主键隐藏起来,作为传参,此处主键为流程序号

        # sql查询通过多表左外连接查询获取发文流程结果.并且根据流程序号这一唯一标识分组,将批文标题和字号用逗号连接起来
        sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文标题,sendfile.发文字号,revfile.收文标题,revfile.收文字号," \
              "GROUP_CONCAT(corfile.批文标题,'\n'),GROUP_CONCAT(corfile.批文字号,'\n'),bwprocess.是否加入整改 FROM bwprocess LEFT " \
              "OUTER JOIN sendfile ON sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = " \
              "bwprocess.收文序号 LEFT OUTER JOIN bw_cast_cor ON bw_cast_cor.流程序号 = bwprocess.序号 LEFT OUTER JOIN corfile " \
              "ON corfile.序号 = bw_cast_cor.批文序号 GROUP BY bwprocess.序号 "
        data = tools.executeSql(sql)
        # 打印结果
        # print(data)

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_lczl.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_lczl.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_lczl.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.tableWidget_lczl.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_lczl.resizeRowsToContents()  # 根据行调整框大小

        self.tableWidget_lczl.sortItems(1, Qt.DescendingOrder)  # 按照流程建立时间排序

    # 显示各种类型登记表总览
    def showRegisTable(self, type1, type2):
        # 表格不可编辑
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)

        # 清空表格
        self.tableWidget_2.clear()

        # 设置字体
        self.tableWidget_2.horizontalHeader().setFont(QFont('Times', 14, QFont.Black))

        self.resType1 = type1  # 标识当前访问的登记表类型1
        self.resType2 = type2  # 标识当前访问的登记表类型2

        data = []

        if type1 == "发文登记表":
            self.label_35.setText("注：红色办理中，黑色办结。")
            self.tableWidget_2.setColumnCount(12)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['主键', '登记时间', '发文字号', '密级', '标识', '标题', '签发人', '份数', '公文运转情况', '批示情况', '批示办理情况', '起草处室'])
            rear = ""
            if type2 == "委文":
                self.label_34.setText("鄂审计委文[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委文%' "
            elif type2 == "委发":
                self.label_34.setText("鄂审计委发[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委发%' "
            elif type2 == "委办文":
                self.label_34.setText("鄂审计委办文[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委办文%' "
            elif type2 == "委办发":
                self.label_34.setText("鄂审计委办文[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委办发%' "
            elif type2 == "委函":
                self.label_34.setText("鄂审计委函[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委函%' "
            elif type2 == "委办函":
                self.label_34.setText("鄂审计委办函[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委办函%' "
            elif type2 == "委便签":
                self.label_34.setText("鄂审计委便签[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委便签%' "
            elif type2 == "委办便签":
                self.label_34.setText("鄂审计委办便签:（无编号）[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '鄂审计委办便签%' "
            elif type2 == "会议纪要":
                self.label_34.setText("会议纪要[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '会议纪要%' "
            elif type2 == "审计专报":
                self.label_34.setText("审计专报[%s]" % datetime.datetime.now().year)
                rear = " having sendfile.发文字号 like '审计专报%' "

            sql = "select sendfile.序号,sendfile.办文日期,sendfile.发文字号,sendfile.秘密等级,sendfile.标识,sendfile.发文标题," \
                  "sendfile.签发人,sendfile.份数,sendfile.公文运转情况,GROUP_CONCAT(instruction.领导内容摘要和领导批示,'\n')," \
                  "sendfile.批示办理情况,sendfile.起草处室 from sendfile left outer join bwprocess on sendfile.序号 = " \
                  "bwprocess.发文序号 left outer join bw_cast_cor on bw_cast_cor.流程序号 = bwprocess.序号 left outer join " \
                  "corfile on corfile.序号 = bw_cast_cor.批文序号 left outer join instruction on instruction.批文序号 = " \
                  "corfile.序号 group by sendfile.序号" + rear
            data = tools.executeSql(sql)

            if type2 == "审计专报":
                # 按照发文字号排序,审计专报字号
                data = tools.sortByKey(data, 2, 0)
            else:
                # 按照发文字号排序,其他发文字号
                data = tools.sortByKey(data, 2, 1)

        elif type1 == "收文登记表":
            self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。4、蓝色：临时交办审计任务。")
            self.tableWidget_2.setColumnCount(13)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['主键', '时间', '编号', '秘级', '来文单位', '来文字号', '来文标题', '拟办意见', '要求时间', '厅领导签批意见', '承办处室', '办理结果',
                 '文件去向'])
            rear = ""
            if type2 == "请字":
                self.label_34.setText("请字[%s]（平级、下级报送的请示类文件）→" % datetime.datetime.now().year)
                rear = " where 收文字号 like '请字%' "
            elif type2 == "情字":
                self.label_34.setText("情字[%s]（平级、下级报送的情况类文件）→" % datetime.datetime.now().year)
                rear = " where 收文字号 like '情字%' "
            elif type2 == "综字":
                self.label_34.setText("综字[%s]（上级下发的各类文件）→" % datetime.datetime.now().year)
                rear = " where 收文字号 like '综字%' "
            elif type2 == "会字":
                self.label_34.setText("会[%s]（各级会议通知）→" % datetime.datetime.now().year)
                rear = " where 收文字号 like '会字%' "
            elif type2 == "电字":
                self.label_34.setText("电[%s]（电报文件）→" % datetime.datetime.now().year)
                rear = " where 收文字号 like '电字%' "

            sql = "select 序号,收文时间,收文字号,秘密等级,来文单位,来文字号,收文标题,内容摘要和拟办意见,要求时间,领导批示,承办处室,处理结果,文件去向 from revfile" + rear
            data = tools.executeSql(sql)

            # 按照收文字号排序
            data = tools.sortByKey(data, 2, 1)

        elif type1 == "批文登记表":
            # 按照一条批文为单位生成登记表
            if type2 == "批字":
                self.label_34.setText("批字[%s]（省领导对审计委员会及委员会办公室文件资料的批示）" % datetime.datetime.now().year)
                self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。")
                self.tableWidget_2.setColumnCount(16)
                self.tableWidget_2.setHorizontalHeaderLabels(
                    ['主键', '时间', '发文编号', '收文编号', '办文编号', '秘级', '来文单位', '来文字号', '来文标题', '省领导批示内容', '秘书处拟办意见', '委办主任签批意见',
                     '批示任务办理要求时间', '审计厅承办处室及承办人', '办理结果', '文件去向'])

                sql = "select corfile.序号,corfile.收文时间,sendfile.发文字号,revfile.收文字号,corfile.批文字号,corfile.秘密等级," \
                      "GROUP_CONCAT(instruction.领导来文单位,'\n'),GROUP_CONCAT(instruction.领导来文字号,'\n'),corfile.批文标题," \
                      "GROUP_CONCAT(instruction.领导内容摘要和领导批示,'\n'),corfile.领导批示,corfile.委办主任签批意见,corfile.批示任务办理要求时间," \
                      "corfile.审计厅承办处室及承办人,corfile.办理结果,corfile.文件去向 from corfile left outer join instruction on " \
                      "corfile.序号 = instruction.批文序号 left outer join bw_cast_cor on bw_cast_cor.批文序号 = corfile.序号 " \
                      "left outer join bwprocess on bwprocess.序号 = bw_cast_cor.流程序号 left outer join sendfile on " \
                      "bwprocess.发文序号 = sendfile.序号 left outer join revfile on bwprocess.收文序号 = revfile.序号 group by " \
                      "corfile.序号 "
                data = tools.executeSql(sql)

                # 按照批文字号排序
                data = tools.sortByKey(data, 4, 1)

            # 按照一条批示为单位生成登记表
            elif type2 == "批示":
                self.label_34.setText("批字[%s]（省领导对审计委员会及委员会办公室文件资料的批示详情）" % datetime.datetime.now().year)
                self.label_35.setText("一位省领导的一条批示作为一条记录。")
                self.tableWidget_2.setColumnCount(14)
                self.tableWidget_2.setHorizontalHeaderLabels(
                    ['主键', '办文编号', '密级', '起草处室', '报送载体', '报送标题', '来文字号', '来文标题', '来文单位', '批示载体', '批示人',
                     '批示人职务', '批示时间', '批示内容'])

                sql = "select instruction.序号,corfile.批文字号,corfile.秘密等级,corfile.起草处室,sendfile.发文字号,sendfile.发文标题," \
                      "instruction.领导来文字号,corfile.批文标题,instruction.领导来文单位,revfile.收文字号,instruction.领导姓名," \
                      "instruction.领导职务,instruction.批示时间,instruction.领导内容摘要和领导批示 from instruction left outer join " \
                      "corfile on instruction.批文序号 = corfile.序号 left outer join bw_cast_cor on corfile.序号 = " \
                      "bw_cast_cor.批文序号 left outer join bwprocess on bw_cast_cor.流程序号 = bwprocess.序号 left outer join " \
                      "sendfile on bwprocess.发文序号 = sendfile.序号 left outer join revfile on bwprocess.收文序号 = revfile.序号 "
                data = tools.executeSql(sql)

                # 按照批文字号排序
                data = tools.sortByKey(data, 1, 1)

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

        self.tableWidget_2.hideColumn(0)  # 将发文、收文、批文、批示数据库主键隐藏起来,作为传参
        self.tableWidget_2.setFont(QFont('Times', 14, QFont.Black))
        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小

    # 发文办理下的确认按钮(专报)
    def add_zb(self):
        input1 = self.lineEdit.text()  # 发文标题
        input2 = self.lineEdit_2.text()  # 报送范围
        input3 = self.label_49.text() + self.spinBox.text() + self.label_50.text()  # 发文字号
        input4 = self.comboBox_4.currentText()  # 紧急程度
        input5 = self.lineEdit_5.text()  # 秘密等级
        input6 = self.comboBox_3.currentText()  # 是否公开
        input7 = self.lineEdit_7.text()  # 拟稿人
        input8 = self.lineEdit_12.text()  # 拟稿处室分管厅领导
        input9 = self.lineEdit_8.text()  # 拟稿处室审核
        input10 = self.lineEdit_9.text()  # 综合处编辑
        input11 = self.lineEdit_10.text()  # 综合处审核
        input12 = self.lineEdit_11.text()  # 秘书处审核
        input13 = self.lineEdit_13.text()  # 综合处分管厅领导
        input14 = self.lineEdit_14.text()  # 审计办主任
        input15 = self.dateEdit_3.text()  # 办文日期
        input_file_path = self.lineEdit_file.text()  # 文件路径
        input16 = tools.getFileName(input_file_path)  # 文件名

        if input1 != "":
            sql = "select 发文字号 from sendfile where 发文字号 = '%s'" % input3
            data = tools.executeSql(sql)
            # 数据库中发文字号是否存在,不允许重复的发文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(self, "新建失败", "发文字号已经存在!")
            else:
                # 导入文件
                tools.copyFile(input_file_path, tools.project_word_path)

                # 执行插入sendfile表
                sql = "insert into sendfile(发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核," \
                      "综合处分管厅领导,审计办主任,办文日期,报文内容,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s','%s','%s','%s','%s',1)" % (
                          input1, input2, input3, input4, input5, input6, input7, input8, input9,
                          input10, input11, input12, input13, input14, input15, input16)
                tools.executeSql(sql)

                # 找到当前发文的序号
                sql = "select 序号 from sendfile where 发文字号 = '%s'" % input3
                data = tools.executeSql(sql)

                # 执行插入流程表
                curr_time = datetime.datetime.now()
                time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], time_str)
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

                # 插入完成后清空所有输入,时间重置,发文字号重置
                self.lineEdit.clear()  # 发文标题
                self.lineEdit_2.clear()  # 报送范围
                self.spinBox.setValue(1)  # 发文字号
                self.comboBox_4.setCurrentIndex(0)  # 紧急程度
                self.lineEdit_5.clear()  # 秘密等级
                self.comboBox_3.setCurrentIndex(0)  # 是否公开
                self.lineEdit_7.clear()  # 拟稿人
                self.lineEdit_12.clear()  # 拟稿处室分管厅领导
                self.lineEdit_8.clear()  # 拟稿处室审核
                self.lineEdit_9.clear()  # 综合处编辑
                self.lineEdit_10.clear()  # 综合处审核
                self.lineEdit_11.clear()  # 秘书处审核
                self.lineEdit_13.clear()  # 综合处分管厅领导
                self.lineEdit_14.clear()  # 审计办主任
                self.dateEdit_3.setDate(datetime.datetime.now())  # 办文日期
                self.lineEdit_file.clear()  # 文件路径

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()
        else:
            QtWidgets.QMessageBox.critical(self, "新建失败", "发文标题不能为空!")

    # 发文办理下的确认按钮(公文)
    def add_gw(self):
        input1 = self.comboBox_9.currentText() + '[' + self.spinBox_2.text() + ']' + self.spinBox_3.text() \
                 + self.label_51.text()  # 发文字号
        input2 = self.lineEdit_num_3.text()  # 发文标题
        input3 = self.textEdit.toPlainText()  # 领导审核意见
        input4 = self.textEdit_2.toPlainText()  # 审计办领导审核意见
        input5 = self.textEdit_3.toPlainText()  # 办文情况说明和拟办意见
        input6 = self.dateEdit_6.text()  # 办文日期
        input_file_path = self.lineEdit_file_3.text()  # 文件路径
        input7 = tools.getFileName(input_file_path)  # 文件名
        input8 = self.comboBox_5.currentText()  # 紧急程度
        input9 = self.lineEdit_15.text()  # 保密等级
        input10 = self.comboBox_6.currentText()  # 是否公开
        input11 = self.lineEdit_17.text()  # 审核
        input12 = self.lineEdit_19.text()  # 承办处室
        input13 = self.lineEdit_20.text()  # 承办人
        input14 = self.lineEdit_21.text()  # 联系电话

        if input2 != "":
            sql = "select 发文字号 from sendfile where 发文字号 = '%s'" % input1
            data = tools.executeSql(sql)
            # 数据库中发文字号是否存在,不允许重复的发文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(self, "新建失败", "发文字号已经存在!")
            else:
                # 导入文件
                tools.copyFile(input_file_path, tools.project_word_path)

                # 执行插入sendfile表
                sql = "insert into sendfile(发文字号,发文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,办文日期,报文内容,紧急程度,秘密等级,是否公开,审核,承办处室," \
                      "承办人,联系电话,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s',2)" % (
                          input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                          input12,
                          input13, input14)
                tools.executeSql(sql)

                # 找到当前发文的序号
                sql = "select 序号 from sendfile where 发文字号 = '%s'" % input1
                data = tools.executeSql(sql)

                # 执行插入流程表
                curr_time = datetime.datetime.now()
                time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], time_str)
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

                # 插入完成后清空显示页面,发文字号重置
                self.comboBox_9.setCurrentIndex(0)  # 发文字号:编号
                self.spinBox_2.setValue(datetime.datetime.now().year)  # 发文字号:[年]
                self.spinBox_3.setValue(1)  # 发文字号:编号
                self.lineEdit_num_3.clear()  # 发文标题
                self.textEdit.clear()  # 领导审核意见
                self.textEdit_2.clear()  # 审计办领导审核意见
                self.textEdit_3.clear()  # 办文情况说明和拟办意见
                self.dateEdit_6.setDate(datetime.datetime.now())  # 办文日期
                self.lineEdit_file_3.clear()  # 文件路径
                self.comboBox_5.setCurrentIndex(0)  # 紧急程度
                self.lineEdit_15.clear()  # 保密等级
                self.comboBox_6.setCurrentIndex(0)  # 是否公开
                self.lineEdit_17.clear()  # 审核
                self.lineEdit_19.clear()  # 承办处室
                self.lineEdit_20.clear()  # 承办人
                self.lineEdit_21.clear()  # 联系电话

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()
        else:
            QtWidgets.QMessageBox.critical(self, "新建失败", "发文标题不能为空!")

    # 收文办理下的录入按钮
    def add_rev(self):
        input1 = self.dateEdit_4.text()  # 收文时间
        input2 = self.lineEdit_23.text()  # 密级
        input3 = self.comboBox_8.currentText()  # 是否公开
        input4 = self.comboBox_7.currentText()  # 紧急程度
        input5 = self.lineEdit_38.text()  # 收文来文单位
        input6 = self.lineEdit_37.text()  # 收文来文字号
        input7 = self.lineEdit_35.text()  # 文件标题
        input8 = self.lineEdit_33.text()  # 处理结果
        input9 = self.lineEdit_30.text()  # 审核
        input10 = self.comboBox_10.currentText() + '[' + self.spinBox_4.text() + ']' + self.spinBox_5.text() + self.label_52.text()  # 办文编号
        input11 = self.lineEdit_34.text()  # 承办处室
        input12 = self.lineEdit_32.text()  # 承办人
        input13 = self.lineEdit_39.text()  # 联系电话
        input14 = self.textEdit_4.toPlainText()  # 内容摘要和拟办意见
        input15 = self.textEdit_5.toPlainText()  # 领导批示

        if input7 != "":
            sql = "select 收文字号 from revfile where 收文字号 = '%s'" % input10
            data = tools.executeSql(sql)
            # 数据库中收文字号是否存在,不允许重复的收文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(self, "新建失败", "收文字号已经存在!")
            else:
                # 执行插入收文表
                sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,处理结果,审核,收文字号,承办处室,承办人,联系电话,内容摘要和拟办意见," \
                      "领导批示) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                          input1, input2, input3, input4, input5, input6,
                          input7, input8, input9, input10, input11,
                          input12, input13, input14, input15)
                tools.executeSql(sql)

                # 找到当前收文的序号
                sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
                data = tools.executeSql(sql)

                # 执行插入流程表
                curr_time = datetime.datetime.now()
                time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(收文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], time_str)
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()

                # 插入完成后清空显示页面
                self.dateEdit_4.setDate(datetime.datetime.now())  # 收文时间
                self.lineEdit_23.clear()  # 密级
                self.comboBox_8.setCurrentIndex(0)  # 是否公开
                self.comboBox_7.setCurrentIndex(0)  # 紧急程度
                self.lineEdit_38.clear()  # 收文来文单位
                self.lineEdit_37.clear()  # 收文来文字号
                self.lineEdit_35.clear()  # 文件标题
                self.lineEdit_33.clear()  # 处理结果
                self.lineEdit_30.clear()  # 审核
                self.comboBox_10.setCurrentIndex(0)  # 收文编号:[收文类型]
                self.spinBox_4.setValue(datetime.datetime.now().year)  # 收文编号:[年]
                self.spinBox_5.setValue(1)  # 收文编号:[编号]
                self.lineEdit_34.clear()  # 承办处室
                self.lineEdit_32.clear()  # 承办人
                self.lineEdit_39.clear()  # 联系电话
                self.textEdit_4.clear()  # 内容摘要和拟办意见
                self.textEdit_5.clear()  # 领导批示

        else:
            QtWidgets.QMessageBox.critical(self, "录入失败", "收文标题不能为空!")

    # 整改台账下的查看详情按钮
    def tz_detail(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择整改项目！")
        else:
            # 获取整改序号
            key = self.tableWidget.item(row, 0).text()
            tab_new = Call_zgdetail(key)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, self.tableWidget.item(row, 3).text())
            self.tabWidget.setCurrentIndex(tab_num)

    # 办文流程详情下的查看详情按钮
    def lc_detail(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择流程！")
        else:
            key = self.tableWidget_lczl.item(row, 0).text()  # 流程序号
            tab_new1 = Call_lcdetail(key)
            tab_new1.setObjectName('tab_new')
            # 设置tab标题,有发文标题设置为发文编号,没有发文设置为收文编号
            if self.tableWidget_lczl.item(row, 3).text() != '/':
                tab_num1 = self.tabWidget_lczl.addTab(tab_new1, self.tableWidget_lczl.item(row, 3).text())
            else:
                tab_num1 = self.tabWidget_lczl.addTab(tab_new1, self.tableWidget_lczl.item(row, 5).text())
            self.tabWidget_lczl.setCurrentIndex(tab_num1)

    # 办文流程下设置整改按钮
    def lc_to_tz(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择流程！")
        else:
            key1 = self.tableWidget_lczl.item(row, 3).text()  # 发文号
            key2 = self.tableWidget_lczl.item(row, 5).text()  # 收文号
            key3 = self.tableWidget_lczl.item(row, 7).text()  # 批文号
            key4 = self.tableWidget_lczl.item(row, 8).text()  # 是否整改

            # key1,key2,key3都不为空表示办文流程已经完成,可以设置整改了
            if key1 != "/" and key2 != "/" and key3 != "/" and key4 != "是":
                sql = "select bwprocess.序号 from bwprocess,sendfile where sendfile.序号 = bwprocess.发文序号 and " \
                      "sendfile.发文字号 = '%s'" % key1
                data = tools.executeSql(sql)
                xh = data[0][0]

                # 将流程加入到台账中
                sql = "insert into standingbook(流程序号) VALUES(%s)" % xh
                tools.executeSql(sql)

                # 修改流程整改状态为1
                sql = "update bwprocess set 是否加入整改 = '是' where 序号 = %s" % xh
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(self, "提示", "添加成功！")

                # 刷新流程页面
                self.showBwprocessTable()

            # 否则不能整改
            else:
                if key1 == "/":
                    QtWidgets.QMessageBox.warning(self, "警告", "无法设置整改！")
                elif key1 != "/" and (key2 == "/" or key3 == "/"):
                    QtWidgets.QMessageBox.warning(self, "警告", "无法设置整改！")
                elif key4 == "是":
                    QtWidgets.QMessageBox.warning(self, "警告", "已设置整改！")

    # 刷新发文流程页面
    def refreshBwprocessTable(self):
        self.showBwprocessTable()

    # 补充发文登记表
    def supplyRegisTable(self):
        row = self.tableWidget_2.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择表格中的一行！")
        else:
            if self.resType1 == "发文登记表":
                key = self.tableWidget_2.item(row, 0).text()
                self.window = Call_sendfilebq(key)
                self.window.setWindowTitle("发文补充")
                self.window.exec()

            elif self.resType1 == "收文登记表":
                key = self.tableWidget_2.item(row, 0).text()
                self.window = Call_revfilebq(key)
                self.window.setWindowTitle("收文补充")
                self.window.exec()

            elif self.resType1 == "批文登记表":
                if self.resType2 == "批字":
                    key = self.tableWidget_2.item(row, 0).text()
                    self.window = Call_corfilebq(key)
                    self.window.setWindowTitle("批文补充")
                    self.window.exec()
                elif self.resType2 == "批示":
                    key = self.tableWidget_2.item(row, 0).text()
                    self.window = Call_instbq(key)
                    self.window.setWindowTitle("批示补充")
                    self.window.exec()

            # 重新展示
            self.showRegisTable(type1=self.resType1, type2=self.resType2)

    # 整改台账下的项目搜索按钮(未开发)
    def search(self):
        # 需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    # 发文办理下的公文类型切换栏
    def chooseSendfileType(self, index):
        self.stackedWidget_new.setCurrentIndex(index)

    # 发文办理下的选择文件夹按钮(专报)
    def choose_file_zb(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def choose_file_gw(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file_3.setText(p[0])
