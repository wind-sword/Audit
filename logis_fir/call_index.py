import datetime
import traceback

import xlrd
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
from logis_fir.logger import Logger


class Call_index(QtWidgets.QMainWindow, Ui_indexWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.window = None  # 补全子窗口
        self.resType1 = ""  # 办文登记表当前type1
        self.resType2 = ""  # 办文登记表当前type2

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 页面对应关系 0:流程总览 page_lczl | 1:流程总览 page_fwbl | 2:收文办理 page_swbl | 3:办文浏览 page_bwll | 4:经责问题表录入 page_jzwtlr
        # | 5:经责文件录入 page_jzwjlr | 6:整改总览 page_zgzl | 7:统计分析 page_tjfx(未开发)
        self.btlczl.clicked.connect(lambda: self.btjump(btname="lczl"))
        self.btfwbl.clicked.connect(lambda: self.btjump(btname="fwbl"))
        self.btswbl.clicked.connect(lambda: self.btjump(btname="swbl"))
        self.btjzwtlr.clicked.connect(lambda: self.btjump(btname="jzwtlr"))
        self.btjzwjlr.clicked.connect(lambda: self.btjump(btname="jzwjlr"))
        self.btjzzl.clicked.connect(lambda: self.btjump(btname="jzzl"))
        self.btswll.clicked.connect(lambda: self.btjump(btname="swll"))
        self.btzgzl.clicked.connect(lambda: self.btjump(btname="zgtz"))
        self.btcx.clicked.connect(lambda: self.btjump(btname="tjfx"))
        self.bttj.clicked.connect(lambda: self.btjump(btname="tjfx"))

        # 整改总览tab
        self.tabWidget_zgzl.setTabText(0, "整改总览")
        self.tabWidget_zgzl.setTabsClosable(1)
        self.tabWidget_zgzl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_zgzl.tabCloseRequested.connect(self.closeTab1)

        # 流程总览tab
        self.tabWidget_lczl.setTabText(0, "流程总览")
        self.tabWidget_lczl.setTabsClosable(1)
        self.tabWidget_lczl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_lczl.tabCloseRequested.connect(self.closeTab2)

        # 公文页面日期和办文编号同步;登记表页面下拉框内容同步;经责文件录入页面listWidget高亮同步;发文类型与页面同步
        self.dateEdit_5.dateChanged.connect(self.autoSyn1)
        self.dateEdit_6.dateChanged.connect(self.autoSyn2)
        self.spinBox_2.valueChanged.connect(self.autoSyn3)
        self.spinBox_3.valueChanged.connect(self.autoSyn3)
        self.comboBox_9.currentIndexChanged.connect(self.autoSyn4)
        self.comboBox_2.currentIndexChanged.connect(self.autoSyn5)
        self.listWidget_sjwh.currentRowChanged.connect(self.autoSyn6)
        self.listWidget_sjyj.currentRowChanged.connect(self.autoSyn7)
        self.listWidget_sjbg.currentRowChanged.connect(self.autoSyn8)
        self.listWidget_sjjg.currentRowChanged.connect(self.autoSyn9)
        self.listWidget_excel.currentRowChanged.connect(self.autoSyn10)
        self.comboBox_type_fw.currentIndexChanged.connect(
            lambda: self.autoSynSendfileType(index=self.comboBox_type_fw.currentIndex()))

        # 绑定按钮或其他控件功能函数
        self.initControlFunction()

        # 初始化显示
        self.stackedWidget.setCurrentIndex(0)
        self.showBwprocessTable()

    # 主页左侧按钮跳转
    def btjump(self, btname):
        if btname == "lczl":
            self.stackedWidget.setCurrentIndex(0)
            self.tabWidget_lczl.setCurrentIndex(0)
            # 初始化显示
            self.showBwprocessTable()
        elif btname == "fwbl":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_new.setCurrentIndex(self.comboBox_type_fw.currentIndex())  # 初始化发文办理页面
            # 公文页面初始化显示
            self.lineEdit_file_3.setReadOnly(True)
            self.lineEdit_18.setReadOnly(True)
            self.spinBox_2.setValue(datetime.datetime.now().year)
            self.spinBox_3.setValue(1)
            self.comboBox_9.setCurrentIndex(0)
            self.dateEdit_6.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

            # 专报页面初始化显示
            self.lineEdit_file_zb.setReadOnly(True)
            self.spinBox.setValue(1)
            self.dateEdit_zb.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        elif btname == "swbl":
            self.stackedWidget.setCurrentIndex(2)
            # 初始化显示
            self.comboBox_10.setCurrentIndex(0)  # 收文编号:[收文类型]
            self.spinBox_4.setValue(datetime.datetime.now().year)  # 收文编号:[年]
            self.spinBox_5.setValue(1)  # 收文编号:[编号]
            self.dateEdit_4.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        elif btname == "swll":
            self.stackedWidget.setCurrentIndex(3)
        elif btname == "jzwtlr":
            self.stackedWidget.setCurrentIndex(4)
            # 初始化显示
            self.initProblemJzPage()
        elif btname == "jzwjlr":
            self.stackedWidget.setCurrentIndex(5)
            # 初始化显示
            self.initJzFileInsertPage()
        elif btname == "jzzl":
            self.stackedWidget.setCurrentIndex(6)
            # 初始化显示
            self.displayFileJzPage()
        elif btname == "zgtz":
            self.stackedWidget.setCurrentIndex(7)
            self.tabWidget_zgzl.setCurrentIndex(0)
            # 初始化显示
            self.showProjectTable()
        elif btname == "tjfx":
            self.stackedWidget.setCurrentIndex(8)

    # 关闭tab
    def closeTab1(self, index):
        self.tabWidget_zgzl.removeTab(index)

    def closeTab2(self, index):
        self.tabWidget_lczl.removeTab(index)

    # 同步输入框内容,autoSyn1、2为公文时间同步,3、4为公文编号同步,5为办文登记表两个下拉框内容同步
    def autoSyn1(self):
        self.dateEdit_6.setDate(self.dateEdit_5.date())

    def autoSyn2(self):
        self.dateEdit_5.setDate(self.dateEdit_6.date())

    def autoSyn3(self):
        cur = self.comboBox_9.currentText() + '〔' + self.spinBox_2.text() + '〕' + self.spinBox_3.text() \
              + '号'
        self.lineEdit_18.setText(cur)

    def autoSyn4(self):
        cur = self.comboBox_9.currentText() + '〔' + self.spinBox_2.text() + '〕' + self.spinBox_3.text() \
              + '号'
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

    # listWidget高亮内容同步
    def autoSyn6(self):
        self.listWidget_sjyj.setCurrentRow(self.listWidget_sjwh.currentRow())
        self.listWidget_sjbg.setCurrentRow(self.listWidget_sjwh.currentRow())
        self.listWidget_sjjg.setCurrentRow(self.listWidget_sjwh.currentRow())
        self.listWidget_excel.setCurrentRow(self.listWidget_sjwh.currentRow())

    def autoSyn7(self):
        self.listWidget_sjwh.setCurrentRow(self.listWidget_sjyj.currentRow())
        self.listWidget_sjbg.setCurrentRow(self.listWidget_sjyj.currentRow())
        self.listWidget_sjjg.setCurrentRow(self.listWidget_sjyj.currentRow())
        self.listWidget_excel.setCurrentRow(self.listWidget_sjyj.currentRow())

    def autoSyn8(self):
        self.listWidget_sjwh.setCurrentRow(self.listWidget_sjbg.currentRow())
        self.listWidget_sjyj.setCurrentRow(self.listWidget_sjbg.currentRow())
        self.listWidget_sjjg.setCurrentRow(self.listWidget_sjbg.currentRow())
        self.listWidget_excel.setCurrentRow(self.listWidget_sjbg.currentRow())

    def autoSyn9(self):
        self.listWidget_sjwh.setCurrentRow(self.listWidget_sjjg.currentRow())
        self.listWidget_sjyj.setCurrentRow(self.listWidget_sjjg.currentRow())
        self.listWidget_sjbg.setCurrentRow(self.listWidget_sjjg.currentRow())
        self.listWidget_excel.setCurrentRow(self.listWidget_sjjg.currentRow())

    def autoSyn10(self):
        self.listWidget_sjwh.setCurrentRow(self.listWidget_excel.currentRow())
        self.listWidget_sjyj.setCurrentRow(self.listWidget_excel.currentRow())
        self.listWidget_sjbg.setCurrentRow(self.listWidget_excel.currentRow())
        self.listWidget_sjjg.setCurrentRow(self.listWidget_excel.currentRow())

    # 发文办理下的公文类型同步
    def autoSynSendfileType(self, index):
        self.stackedWidget_new.setCurrentIndex(index)

    # 控件绑定功能函数
    def initControlFunction(self):
        # 流程总览的按钮功能
        self.btlcxq.clicked.connect(self.lc_detail)
        self.btlczg.clicked.connect(self.lc_to_zg)
        self.pushButton_refresh_lczl.clicked.connect(self.refreshBwprocessTable)

        # 发文办理页面专报/公文按钮功能
        self.pushButton_choose_zb.clicked.connect(self.choose_file_zb)
        self.pushButton_choose_gw.clicked.connect(self.choose_file_gw)
        self.pushButton_add_zb.clicked.connect(self.add_zb)
        self.pushButton_add_gw.clicked.connect(self.add_gw)

        # 收文办理页面按钮功能
        self.pushButton_add_sw.clicked.connect(self.add_rev)

        # 办文登记表页面的按钮功能
        self.pushButton_browse_bw.clicked.connect(
            lambda: self.showRegisTable(type1=self.comboBox_2.currentText(), type2=self.comboBox.currentText()))
        self.pushButton_supply_bw.clicked.connect(self.supplyRegisTable)

        # 经责问题总表录入页面按钮功能
        self.bt_search_jz.clicked.connect(self.searchJzProject)
        self.pushButton_que_choose.clicked.connect(self.chooseProblemJzTable)
        self.pushButton_que_import.clicked.connect(self.importExcelProblemJz)

        # 经责文件录入页面按钮功能
        self.pushButton_choose_excel.clicked.connect(self.choose_file_jz_excel)
        self.pushButton_choose_sjyj.clicked.connect(self.choose_file_sjyj)
        self.pushButton_choose_sjbg.clicked.connect(self.choose_file_sjbg)
        self.pushButton_choose_sjjg.clicked.connect(self.choose_file_sjjg)

        self.pushButton_add_excel.clicked.connect(self.add_jz_excel)
        self.pushButton_add_sjyj.clicked.connect(self.add_sjyj)
        self.pushButton_add_sjbg.clicked.connect(self.add_sjbg)

        # 经责文件总览页面按钮功能
        self.pushButton_open_sjyj.clicked.connect(lambda: self.openSjFile(listType="sjyj"))
        self.pushButton_open_sjbg.clicked.connect(lambda: self.openSjFile(listType="sjbg"))
        self.pushButton_open_sjjg.clicked.connect(lambda: self.openSjFile(listType="sjjg"))
        self.pushButton_open_excel.clicked.connect(lambda: self.openSjFile(listType="jzexcel"))
        self.pushButton_del_sjyj.clicked.connect(lambda: self.delSjFile(listType="sjyj"))
        self.pushButton_del_sjbg.clicked.connect(lambda: self.delSjFile(listType="sjbg"))
        self.pushButton_del_sjjg.clicked.connect(lambda: self.delSjFile(listType="sjjg"))
        self.pushButton_del_excel.clicked.connect(lambda: self.delSjFile(listType="jzexcel"))

        # 整改总览下的按钮功能
        self.pushButton_zg_detail.clicked.connect(self.zg_detail)
        self.bt_search_zgzl.clicked.connect(self.searchZgProject)

    # 显示整改内容
    def showProjectTable(self):
        # 表格不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableWidget.hideColumn(0)  # 将流程数据库主键隐藏起来,作为传参,此处主键为整改序号

        # sql由整改表的流程序号出发,通过多表查询获得整改所有字段
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

    # 初始化经责问题总表录入页面
    def initProblemJzPage(self):
        # 隐藏设置整改按钮
        self.btszjzzg.hide()

        # 表格不可编辑
        self.tableWidget_3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        sql = "select 序号,问题顺序号,被审计领导干部,所在地方或单位,报送文号,审计报告文号,经责结果报告文号,出具审计报告时间,审计组组长,审计组主审,问题描述,是否在审计报告中反映,是否在结果报告中反映," \
              "审计对象分类,问题类别,问题定性,问题表现形式,备注,问题金额,移送及处理情况 from problem_jz"
        data = tools.executeSql(sql)

        size = len(data)
        # 已经完成录入
        if size != 0:
            # 隐藏录入控件栏
            self.label_58.hide()
            self.lineEdit_que_jz.hide()
            self.pushButton_que_import.hide()
            self.pushButton_que_choose.hide()

            # 显示查询条件栏
            self.label_55.show()
            self.label_56.show()
            self.comboBox_11.show()
            self.bt_search_jz.show()

            self.tableWidget_3.setRowCount(size)

            x = 0
            for i in data:
                y = 0
                for j in i:
                    if data[x][y] is None:
                        self.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                    else:
                        self.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                    y = y + 1
                x = x + 1

            # 下拉栏自动收集文号作为查询条件
            keywords = set()
            for i in data:
                # 审计意见(报告)文号必定不为空
                if i[5] != "":
                    keywords.add(i[5])
            self.comboBox_11.clear()
            for i in keywords:
                self.comboBox_11.addItem(i)

        else:
            # 显示录入控件栏
            self.label_58.show()
            self.lineEdit_que_jz.show()
            self.lineEdit_que_jz.setReadOnly(True)
            self.pushButton_que_import.show()
            self.pushButton_que_choose.show()

            # 清空表格
            self.tableWidget_3.setRowCount(0)

            # 清空文件路径输入栏
            self.lineEdit_que_jz.clear()

            # 隐藏查询控件栏
            self.label_55.hide()
            self.label_56.hide()
            self.comboBox_11.hide()
            self.bt_search_jz.hide()

        self.tableWidget_3.hideColumn(0)  # 将经责问题表主键隐藏起来
        self.tableWidget_3.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_3.resizeRowsToContents()  # 根据行调整框大小

    # 初始化经责文件导入界面
    def initJzFileInsertPage(self):
        # 初始化文号控件
        self.spinBox_sjyj_year.setValue(datetime.datetime.now().year)
        self.spinBox_sjbg_year.setValue(datetime.datetime.now().year)
        self.spinBox_excel_year.setValue(datetime.datetime.now().year)
        self.spinBox_sjyj_num.setValue(1)
        self.spinBox_sjbg_num.setValue(1)
        self.spinBox_excel_num.setValue(1)

        # 文件输入栏不可编辑
        self.lineEdit_file_sjyj.setReadOnly(True)
        self.lineEdit_file_sjbg.setReadOnly(True)
        self.lineEdit_file_sjjg.setReadOnly(True)
        self.lineEdit_file_excel.setReadOnly(True)

        # 清空文件输入栏
        self.lineEdit_file_sjyj.clear()
        self.lineEdit_file_sjbg.clear()
        self.lineEdit_file_sjjg.clear()

    # 展示经责文件总览界面
    def displayFileJzPage(self):
        # 清空list
        self.listWidget_sjyj.clear()
        self.listWidget_sjbg.clear()
        self.listWidget_sjjg.clear()
        self.listWidget_sjwh.clear()
        self.listWidget_excel.clear()

        # 将所有文件信息和文号显示在list中,此处展示了如何运用sql嵌套查询的例子,等待后人优化此处sql查询
        # 连接查询:找出满足既在sjyjword中存在又在jzexcel中存在的文号对应记录
        sql = "select sjyjword.审计意见文号,sjyjword.审计意见内容,jzexcel.经责分问题表名 from sjyjword,jzexcel where sjyjword.审计意见文号 = " \
              "jzexcel.审计意见或报告文号 "
        data = tools.executeSql(sql)
        result = []
        for i in data:
            tempTuple = (i[0], i[1], '/', '/', i[2])
            result.append(tempTuple)
        print(result)

        # 不相关字查询:找出满足在sjyjword中存在但不在jzexcel中存在的文号对应记录
        sql = "select 审计意见文号,审计意见内容 from sjyjword where 审计意见文号 not in (select " \
              "审计意见或报告文号 from jzexcel) "
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], i[1], '/', '/', '/')
            result.append(tempTuple)
        print(result)

        # 不相关字查询:找出满足在jzexcel中存在但不在sjyjword中存在的文号对应记录,且文号必须是鄂审资环意
        sql = "select 审计意见或报告文号,经责分问题表名 from jzexcel where 审计意见或报告文号 not in (select " \
              "审计意见文号 from sjyjword) and 审计意见或报告文号 like '鄂审资环意%'"
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], '/', '/', '/', i[1])
            result.append(tempTuple)
        print(result)

        # 连接查询:找出满足既在sjbgword中存在又在jzexcel中存在的文号对应记录
        sql = "select sjbgword.审计报告文号,sjbgword.审计报告内容,sjbgword.审计结果内容,jzexcel.经责分问题表名 from sjbgword,jzexcel where " \
              "sjbgword.审计报告文号 = jzexcel.审计意见或报告文号 "
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], '/', i[1], i[2], i[3])
            result.append(tempTuple)
        print(result)

        # 不相关字查询:找出满足在sjbgword中存在但不在jzexcel中存在的文号对应记录
        sql = "select 审计报告文号,审计报告内容,审计结果内容 from sjbgword where 审计报告文号 not in (select 审计意见或报告文号 from jzexcel) "
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], '/', i[1], i[2], '/')
            result.append(tempTuple)
        print(result)

        # 不相关字查询:找出满足在jzexcel中存在但不在sjbgword中存在的文号对应记录,且文号必须是鄂审经责报
        sql = "select 审计意见或报告文号,经责分问题表名 from jzexcel where 审计意见或报告文号 not in (select " \
              "审计报告文号 from sjbgword) and 审计意见或报告文号 like '鄂审经责报%'"
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], '/', '/', '/', i[1])
            result.append(tempTuple)
        print(result)

        for i in result:
            self.listWidget_sjwh.addItem(i[0])
            self.listWidget_sjyj.addItem(i[1])
            self.listWidget_sjbg.addItem(i[2])
            self.listWidget_sjjg.addItem(i[3])
            self.listWidget_excel.addItem(i[4])

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
        input15 = self.dateEdit_zb.text()  # 办文日期
        input_file_path = self.lineEdit_file_zb.text()  # 文件路径
        input16 = tools.getFileName(input_file_path)  # 文件名

        if input1 != "":
            sql = "select 发文字号 from sendfile where 发文字号 = '%s'" % input3
            data = tools.executeSql(sql)
            # 数据库中发文字号是否存在,不允许重复的发文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(self, "新建失败", "发文字号已经存在!")
            elif tools.judgeExistSameNameFile(tools.project_word_path, input16):
                QtWidgets.QMessageBox.critical(self, "新建失败", "存在相同的文件名!")
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
                # curr_time = datetime.datetime.now()
                # time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], input15)
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
                self.dateEdit_zb.setDate(datetime.datetime.now())  # 办文日期
                self.lineEdit_file_zb.clear()  # 文件路径

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()
        else:
            QtWidgets.QMessageBox.critical(self, "新建失败", "发文标题不能为空!")

    # 发文办理下的确认按钮(公文)
    def add_gw(self):
        input1 = self.comboBox_9.currentText() + '〔' + self.spinBox_2.text() + '〕' + self.spinBox_3.text() \
                 + '号'  # 发文字号
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
            elif tools.judgeExistSameNameFile(tools.project_word_path, input7):
                QtWidgets.QMessageBox.critical(self, "新建失败", "存在相同的文件名!")
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
                # curr_time = datetime.datetime.now()
                # time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], input6)
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
        input10 = self.comboBox_10.currentText() + '〔' + self.spinBox_4.text() + '〕' + self.spinBox_5.text() \
                  + '号'  # 办文编号
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
                # curr_time = datetime.datetime.now()
                # time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(收文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], input1)
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

    # 整改总览下的查看详情按钮
    def zg_detail(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择整改项目！")
        else:
            # 获取整改序号
            key = self.tableWidget.item(row, 0).text()
            tab_new = Call_zgdetail(key)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget_zgzl.addTab(tab_new, self.tableWidget.item(row, 3).text())
            self.tabWidget_zgzl.setCurrentIndex(tab_num)

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
    def lc_to_zg(self):
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

                # 将流程加入到整改中
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

    # 经责问题表中的搜索按钮
    def searchJzProject(self):
        keyword = self.comboBox_11.currentText()
        sql = "select * from problem_jz where 审计报告文号 = '%s' or 经责结果报告文号 = '%s'" % (keyword, keyword)
        data = tools.executeSql(sql)

        size = len(data)
        self.tableWidget_3.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        # 显示设置整改按钮
        self.btszjzzg.show()

    # 整改总览下的项目搜索按钮(未开发)
    def searchZgProject(self):
        # 需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    # 发文办理下的选择文件夹按钮(专报)
    def choose_file_zb(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc)")
        self.lineEdit_file_zb.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def choose_file_gw(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc)")
        self.lineEdit_file_3.setText(p[0])

    # 选择审计意见
    def choose_file_sjyj(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc)")
        self.lineEdit_file_sjyj.setText(p[0])

    # 选择审计报告
    def choose_file_sjbg(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc)")
        self.lineEdit_file_sjbg.setText(p[0])

    # 选择审计结果报告
    def choose_file_sjjg(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Word(*.docx);;Word(*.doc)")
        self.lineEdit_file_sjjg.setText(p[0])

    # 选择经责问题表
    def chooseProblemJzTable(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Excel(*.xlsx);;Excel(*.xls)")
        self.lineEdit_que_jz.setText(p[0])

    # 选择经责问题分表
    def choose_file_jz_excel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Excel(*.xlsx);;Excel(*.xls)")
        self.lineEdit_file_excel.setText(p[0])

    # 导入审计意见
    def add_sjyj(self):
        input_file_path = self.lineEdit_file_sjyj.text()
        if input_file_path != "":
            filename = tools.getFileName(input_file_path)  # 审计意见文件名
            keyword = self.comboBox_sjyj.currentText() + '〔' + self.spinBox_sjyj_year.text() + '〕' + self.spinBox_sjyj_num.text() \
                      + '号'  # 审计意见文号
            if tools.judgeExistSameNameFile(tools.sjyj_word_path, filename):
                QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文件名!")
            else:
                sql = "select * from sjyjword where 审计意见文号 = '%s'" % keyword
                data = tools.executeSql(sql)
                if len(data) != 0:
                    QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文号!")
                else:
                    sql = "insert into sjyjword values(NULL,'%s','%s')" % (keyword, filename)
                    tools.executeSql(sql)

                    # 导入文件
                    tools.copyFile(input_file_path, tools.sjyj_word_path)

                    QtWidgets.QMessageBox.information(self, "提示", "添加成功!")

                    # 清空文件名输入栏
                    self.lineEdit_file_sjyj.clear()

                    # 跳转到总览页面
                    self.stackedWidget.setCurrentIndex(6)
                    self.displayFileJzPage()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请选择文件!")

    # 导入审计报告和审计结果
    def add_sjbg(self):
        input_file_path1 = self.lineEdit_file_sjbg.text()
        input_file_path2 = self.lineEdit_file_sjjg.text()
        if input_file_path1 != "" and input_file_path2 != "":
            keyword = self.comboBox_sjbg.currentText() + '〔' + self.spinBox_sjbg_year.text() + '〕' + self.spinBox_sjbg_num.text() \
                      + '号'  # 审计报告文号
            filename1 = tools.getFileName(input_file_path1)  # 审计报告文件名
            filename2 = tools.getFileName(input_file_path2)  # 经责审计结果报告文件名
            if tools.judgeExistSameNameFile(tools.sjbg_word_path, filename1) or tools.judgeExistSameNameFile(tools.sjjg_word_path, filename2):
                QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文件名!")
            else:
                sql = "select * from sjbgword where 审计报告文号 = '%s'" % keyword
                data = tools.executeSql(sql)
                if len(data) != 0:
                    QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文号!")
                else:
                    sql = "insert into sjbgword values(NULL,'%s','%s','%s')" % (keyword, filename1, filename2)
                    tools.executeSql(sql)

                    # 导入文件
                    tools.copyFile(input_file_path1, tools.sjbg_word_path)
                    tools.copyFile(input_file_path2, tools.sjjg_word_path)

                    QtWidgets.QMessageBox.information(self, "提示", "添加成功!")

                    # 清空文件名输入栏
                    self.lineEdit_file_sjbg.clear()
                    self.lineEdit_file_sjjg.clear()

                    # 跳转到总览页面
                    self.stackedWidget.setCurrentIndex(6)
                    self.displayFileJzPage()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "两个文件必须都选择!")

    # 导入经责分问题表excel
    def add_jz_excel(self):
        input_file_path = self.lineEdit_file_excel.text()
        if input_file_path != "":
            filename = tools.getFileName(input_file_path)  # 分问题表文件名
            keyword = self.comboBox_excel.currentText() + '〔' + self.spinBox_excel_year.text() + '〕' + self.spinBox_excel_num.text() \
                      + '号'  # 审计意见(报告)文号
            if tools.judgeExistSameNameFile(tools.jz_excel_path, filename):
                QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文件名!")
            else:
                sql = "select * from jzexcel where 审计意见或报告文号 = '%s'" % keyword
                data = tools.executeSql(sql)
                if len(data) != 0:
                    QtWidgets.QMessageBox.critical(self, "导入失败", "存在相同的文号!")
                else:
                    sql = "insert into jzexcel values(NULL,'%s','%s')" % (keyword, filename)
                    tools.executeSql(sql)

                    # 导入文件
                    tools.copyFile(input_file_path, tools.jz_excel_path)

                    QtWidgets.QMessageBox.information(self, "提示", "添加成功!")

                    # 清空文件名输入栏
                    self.lineEdit_file_excel.clear()

                    # 跳转到总览页面
                    self.stackedWidget.setCurrentIndex(6)
                    self.displayFileJzPage()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请选择文件!")

    # 打开选择的经责文件或者excel文件
    def openSjFile(self, listType):
        row = self.listWidget_sjwh.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择对应文件!")
        else:
            filename = ""
            file_folder = ""
            if listType == "sjyj":
                filename = self.listWidget_sjyj.currentItem().text()
                file_folder = "sjyj_word"
            elif listType == "sjbg":
                filename = self.listWidget_sjbg.currentItem().text()
                file_folder = "sjbg_word"
            elif listType == "sjjg":
                filename = self.listWidget_sjjg.currentItem().text()
                file_folder = "sjjg_word"
            elif listType == "jzexcel":
                filename = self.listWidget_excel.currentItem().text()
                file_folder = "jz_excel"
            if filename == '/':
                QtWidgets.QMessageBox.information(self, "提示", "不存在对应文件!")
            else:
                tools.openFile(file_folder=file_folder, file=filename)

    # 删除相关文件
    def delSjFile(self, listType):
        row = self.listWidget_sjwh.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择对应文件!")
        else:
            filename = ""
            filename_sjjg = ""
            file_folder = ""
            sql = ""
            keyword = self.listWidget_sjwh.currentItem().text()
            if listType == "sjyj":
                filename = self.listWidget_sjyj.currentItem().text()
                file_folder = tools.sjyj_word_path
                sql = "delete from sjyjword where 审计意见文号 = '%s'" % keyword
            elif listType == "sjbg" or listType == "sjjg":
                filename = self.listWidget_sjbg.currentItem().text()
                file_folder = tools.sjbg_word_path
                filename_sjjg = self.listWidget_sjjg.currentItem().text()
                file_folder_sjjg = tools.sjjg_word_path
                sql = "delete from sjbgword where 审计报告文号 = '%s'" % keyword
            elif listType == "jzexcel":
                filename = self.listWidget_excel.currentItem().text()
                file_folder = tools.jz_excel_path
                sql = "delete from jzexcel where 审计意见或报告文号 = '%s'" % keyword
            if filename == '/':
                QtWidgets.QMessageBox.information(self, "提示", "不存在对应文件!")
            else:
                tools.executeSql(sql)
                tools.deleteFile(file_folder, filename)
                if filename_sjjg != "":
                    tools.deleteFile(file_folder_sjjg, filename_sjjg)
                QtWidgets.QMessageBox.information(self, "提示", "删除成功!")
                self.displayFileJzPage()

    # 根据excel中的左边问题基本信息导入经责问题表
    def importExcelProblemJz(self):
        # 文件路径
        path = self.lineEdit_que_jz.text()
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
                        QtWidgets.QMessageBox.information(self, "提示", "excel表格第%s行: 问题顺序号应为整数" % str(i + 1))
                        break
                    # 审计意见(报告)文号,判断是否为空(后续还需要判断是否符合格式要求)
                    if sheet.row(i)[4].value == "":
                        check_tag = 0
                        QtWidgets.QMessageBox.information(self, "提示", "excel表格第%s行: 审计意见(报告)文号错误!!" % str(i + 1))
                        break
                    # 出具审计专报时间,判断是否为合法时间
                    if isinstance(sheet.row(i)[6].value, str):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(self, "提示", "excel表格第%s行: 出具审计专报时间格式错误" % str(i + 1))
                        break
                    # 问题金额,判断是否为浮点数
                    if not isinstance(sheet.row(i)[17].value, float):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(self, "提示", "excel表格第%s行: 问题金额应为数字" % str(i + 1))
                        break
                if sheet_rows == 4:
                    check_tag = 0
                    QtWidgets.QMessageBox.information(self, "提示", "表格数据为空")

            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())

            if check_tag == 1:
                # 写入数据库
                try:
                    for i in range(4, sheet_rows):
                        cell_i_0 = int(sheet.row(i)[0].value)  # 问题顺序号
                        cell_i_1 = sheet.row(i)[1].value  # 被审计领导干部
                        cell_i_2 = sheet.row(i)[2].value  # 所在地方或单位
                        cell_i_3 = sheet.row(i)[3].value  # 报送专报期号,直接读取excel中的输入
                        cell_i_4 = sheet.row(i)[4].value  # 审计报告（意见）文号
                        cell_i_5 = sheet.row(i)[5].value  # 经责结果报告文号
                        cell_i_6 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 6).value, 0).strftime(
                            "%Y/%m/%d")  # 出具审计专报时间 Year/Month/Day
                        cell_i_7 = sheet.row(i)[7].value  # 审计组组长
                        cell_i_8 = sheet.row(i)[8].value  # 审计组主审
                        cell_i_9 = sheet.row(i)[9].value  # 问题描述
                        cell_i_10 = sheet.row(i)[10].value  # 是否在审计报告中反映
                        cell_i_11 = sheet.row(i)[11].value  # 是否在结果报告中反映
                        cell_i_12 = sheet.row(i)[12].value  # 审计对象分类
                        cell_i_13 = sheet.row(i)[13].value  # 问题类别
                        cell_i_14 = sheet.row(i)[14].value  # 问题定性
                        cell_i_15 = sheet.row(i)[15].value  # 问题表现形式
                        cell_i_16 = sheet.row(i)[16].value  # 备注
                        cell_i_17 = sheet.row(i)[17].value  # 问题金额
                        cell_i_18 = sheet.row(i)[18].value  # 移送及处理情况

                        sql = "insert into problem_jz values(NULL,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                              "'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                  cell_i_0, cell_i_1, cell_i_2, cell_i_3, cell_i_4, cell_i_5, cell_i_6, cell_i_7,
                                  cell_i_8, cell_i_9, cell_i_10, cell_i_11, cell_i_12, cell_i_13, cell_i_14, cell_i_15,
                                  cell_i_16, cell_i_17, cell_i_18)
                        tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(self, "提示", "导入完成")

                    # 导入完成后更新经责表录入界面
                    self.initProblemJzPage()

                except:
                    log = Logger('./log/logfile.log', level='error')
                    log.logger.error("错误:%s", traceback.format_exc())
            else:
                QtWidgets.QMessageBox.critical(self, "错误", "导入失败")
        else:
            QtWidgets.QMessageBox.information(self, "提示", "请选择文件!")
