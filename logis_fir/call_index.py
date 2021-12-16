import datetime
import traceback
import sys

import xlrd
import xlwt

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import QAbstractItemView, QListWidgetItem
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from uipy_dir.index import Ui_indexWindow
from logis_fir.call_lcdetail import Call_lcdetail
from logis_fir.call_zgdetail import Call_zgdetail
from logis_fir.call_sendfilebq import Call_sendfilebq
from logis_fir.call_revfilebq import Call_revfilebq
from logis_fir.call_corfilebq import Call_corfilebq
from logis_fir.call_instbq import Call_instbq
from logis_fir.tools import tools
from logis_fir.logger import Logger

from screen_shot import WScreenShot


class Call_index(QtWidgets.QMainWindow, Ui_indexWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.window = None  # 补全子窗口
        self.resType1 = ""  # 办文登记表当前type1
        self.resType2 = ""  # 办文登记表当前type2

        self.tabWidget_lczl_dict = dict()  # 记录流程总览tabWidget的映射情况:流程号 -> tabWidget对象
        self.tabWidget_zgzl_dict = dict()  # 记录整改总览tabWidget的映射情况:整改号 -> tabWidget对象

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 页面对应关系 0:流程总览 page_lczl | 1:流程总览 page_fwbl | 2:收文办理 page_swbl | 3:批文办理 page_pwbl | 4:办文浏览 page_bwll |
        # 5:经责问题表录入 page_jzwtlr | 6:经责文件录入 page_jzwjlr | 7:整改总览 page_zgzl | 8:统计分析 page_tjfx(未开发)
        self.btlczl.clicked.connect(lambda: self.btjump(btname="lczl"))
        self.btfwbl.clicked.connect(lambda: self.btjump(btname="fwbl"))
        self.btswbl.clicked.connect(lambda: self.btjump(btname="swbl"))
        self.btpwbl.clicked.connect(lambda: self.btjump(btname="pwbl"))
        self.btjzwtlr.clicked.connect(lambda: self.btjump(btname="jzwtlr"))
        self.btjzwjlr.clicked.connect(lambda: self.btjump(btname="jzwjlr"))
        self.btjzzl.clicked.connect(lambda: self.btjump(btname="jzzl"))
        self.btswll.clicked.connect(lambda: self.btjump(btname="swll"))
        self.btzgzl.clicked.connect(lambda: self.btjump(btname="zgtz"))
        self.btcx.clicked.connect(lambda: self.btjump(btname="wtcx"))
        self.btpstj.clicked.connect(lambda: self.btjump(btname="pstj"))
        self.btbwtj.clicked.connect(lambda: self.btjump(btname="bwtj"))
        self.btwttj.clicked.connect(lambda: self.btjump(btname="wttj"))

        # 整改总览tab
        font = QFont('Microsoft YaHei UI', 10, QFont.Black)
        self.tabWidget_zgzl.setFont(font)
        self.tabWidget_zgzl.setTabText(0, "整改总览")
        self.tabWidget_zgzl.setTabsClosable(1)
        self.tabWidget_zgzl.setMovable(1)
        self.tabWidget_zgzl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_zgzl.tabCloseRequested.connect(self.closeTab1)

        # 流程总览tab
        self.tabWidget_lczl.setFont(font)
        self.tabWidget_lczl.setTabText(0, "流程总览")
        self.tabWidget_lczl.setTabsClosable(1)
        self.tabWidget_lczl.setMovable(1)
        self.tabWidget_lczl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_lczl.tabCloseRequested.connect(self.closeTab2)

        # 绑定按钮或其他控件功能函数
        self.initControlFunction()

        # 初始化显示
        self.stackedWidget.setCurrentIndex(0)  # 初始显示为办文流程总览界面
        self.setPushButton_backGround("lczl")  # 设置导航栏按钮背景状态

        # 初始化页面数据
        self.initData()

    # 主页左侧按钮跳转
    def btjump(self, btname):
        self.setPushButton_backGround(btname)  # 设置导航栏按钮背景状态
        if btname == "lczl":
            self.stackedWidget.setCurrentIndex(0)
            # self.tabWidget_lczl.setCurrentIndex(0)
        elif btname == "fwbl":
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_new.setCurrentIndex(self.comboBox_type_fw.currentIndex())  # 初始化发文办理页面
        elif btname == "swbl":
            self.stackedWidget.setCurrentIndex(2)
        elif btname == "pwbl":
            self.stackedWidget.setCurrentIndex(3)
        elif btname == "swll":
            self.stackedWidget.setCurrentIndex(4)
            self.lineEdit_44.setText("请在此输入表格名")
        elif btname == "jzwtlr":
            self.stackedWidget.setCurrentIndex(5)
        elif btname == "jzwjlr":
            self.stackedWidget.setCurrentIndex(6)
        elif btname == "jzzl":
            self.stackedWidget.setCurrentIndex(7)
            # 没有刷新按钮
            self.displayFileJzPage()
        elif btname == "zgtz":
            self.stackedWidget.setCurrentIndex(8)
        elif btname == "pstj":
            self.stackedWidget.setCurrentIndex(9)
        elif btname == "wtcx":
            self.stackedWidget.setCurrentIndex(10)
            self.lineEdit_45.setText("请在此输入表格名")
        elif btname == "bwtj":
            self.stackedWidget.setCurrentIndex(11)
        elif btname == "wttj":
            self.stackedWidget.setCurrentIndex(12)
        elif btname == "lctj":
            self.stackedWidget.setCurrentIndex(13)

    # 设置导航栏按钮背景
    def setPushButton_backGround(self, btname):
        type_1 = "QPushButton{border: 1px solid #00557f;border-left:4px solid rgb(0, 85, " \
                 "127);font-weight:700;font-size:20px;} "
        type_2 = "QPushButton{border: 1px solid #00557f;border-left:4px solid rgb(0, 85, " \
                 "127);font-weight:700;font-size:25px;background-color:rgb(14 , 135 , 228);} "
        btDict = {
            "lczl": self.btlczl,
            "swll": self.btswll,
            "fwbl": self.btfwbl,
            "swbl": self.btswbl,
            "pwbl": self.btpwbl,
            "jzwtlr": self.btjzwtlr,
            "jzwjlr": self.btjzwjlr,
            "jzzl": self.btjzzl,
            "zgtz": self.btzgzl,
            "wtcx": self.btcx,
            "pstj": self.btpstj,
            "bwtj": self.btbwtj,
            "wttj": self.btwttj,
        }
        for button in btDict.values():
            button.setStyleSheet(type_1)
        btDict.get(btname).setStyleSheet(type_2)

    # 初始化数据
    def initData(self):
        # 流程总览页面初始化显示
        self.refreshBwprocessTable()

        # 公文页面初始化显示
        self.lineEdit_file_3.setReadOnly(True)
        self.lineEdit_18.setReadOnly(True)
        self.lineEdit_19.setText("秘书处")
        self.spinBox_2.setValue(datetime.datetime.now().year)
        self.spinBox_3.setValue(1)
        self.comboBox_9.setCurrentIndex(0)
        self.dateEdit_6.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

        # 专报页面初始化显示
        self.lineEdit_file_zb.setReadOnly(True)
        self.spinBox_6.setValue(datetime.datetime.now().year)  # 专报年号:[年]
        self.spinBox.setValue(1)  # 专报编号:[编号]
        self.dateEdit_zb.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

        # 收文办理初始化显示
        self.lineEdit_34.setText("秘书处")
        self.comboBox_10.setCurrentIndex(0)  # 收文编号:[收文类型]
        self.spinBox_4.setValue(datetime.datetime.now().year)  # 收文编号:[年]
        self.spinBox_5.setValue(1)  # 收文编号:[编号]
        self.dateEdit_4.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

        # 批文办理初始化显示
        self.lineEdit_62.setText("秘书处")
        self.comboBox_25.setCurrentIndex(0)  # 批文编号:[收文类型]
        self.spinBox_8.setValue(datetime.datetime.now().year)  # 批文编号:[年]
        self.spinBox_9.setValue(1)  # 批文编号:[编号]
        self.dateEdit_14.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间

        # 初始化经责模块显示
        self.displayProblemJzPage()
        self.displayJzFileInsertPage()
        self.displayFileJzPage()

        # 整改总览初始化显示
        self.refreshZgprocessTable()

        # 统计分析初始化显示
        self.showProblemSearchTable()
        self.showRectificationTable()
        self.showBwChart()
        self.showProblemStatistics()

    # 控件绑定功能函数
    def initControlFunction(self):
        # 流程总览的按钮功能
        self.btlcxq.clicked.connect(self.lc_detail)
        self.btlczg.clicked.connect(self.lc_to_zg)
        self.pushButton_refresh_lczl.clicked.connect(self.refreshBwprocessTable)
        self.pushButton_type_search.clicked.connect(self.searchForLc)  # 办文流程搜索按钮
        self.comboBox_12.currentIndexChanged.connect(self.sortForLc)  # 排序方法
        self.pushButton_type_search_2.clicked.connect(self.selectForLc)  # 筛选的搜索按钮
        self.checkBox.clicked.connect(self.tip_lc)  # 设置时间按钮提示
        self.btdellc.clicked.connect(self.deleteLc)  # 删除流程
        self.bt_excel_output_lc.clicked.connect(self.lcExcelOutput)  # 导出至Excel表格
        self.comboBox_13.currentIndexChanged.connect(self.autoSyn7)
        self.dateEdit_8.dateChanged.connect(lambda: self.autoSynCancelTimeCheckBox(self.checkBox))
        self.dateEdit_10.dateChanged.connect(lambda: self.autoSynCancelTimeCheckBox(self.checkBox))

        # 发文办理页面专报/公文按钮功能
        self.pushButton_choose_zb.clicked.connect(self.choose_file_zb)
        self.pushButton_choose_gw.clicked.connect(self.choose_file_gw)
        self.pushButton_add_zb.clicked.connect(self.add_zb)
        self.pushButton_add_gw.clicked.connect(self.add_gw)
        self.dateEdit_5.dateChanged.connect(self.autoSyn1)
        self.dateEdit_6.dateChanged.connect(self.autoSyn2)
        self.spinBox_2.valueChanged.connect(self.autoSyn3)
        self.spinBox_3.valueChanged.connect(self.autoSyn3)
        self.comboBox_9.currentIndexChanged.connect(self.autoSyn3)
        self.comboBox_type_fw.currentIndexChanged.connect(
            lambda: self.autoSynSendfileType(index=self.comboBox_type_fw.currentIndex()))

        # 收文办理页面按钮功能
        self.pushButton_add_sw.clicked.connect(self.add_rev)

        # 批文办理页面按钮功能
        self.pushButton_add_pw.clicked.connect(self.add_cor)
        self.pushButton_add_item.clicked.connect(self.addTerm)
        self.pushButton_sub_item.clicked.connect(self.subTerm)
        self.listWidget_4.currentRowChanged.connect(lambda: self.autoSyn5(clickedListWidget=self.listWidget_4))
        self.listWidget_5.currentRowChanged.connect(lambda: self.autoSyn5(clickedListWidget=self.listWidget_5))
        self.listWidget_6.currentRowChanged.connect(lambda: self.autoSyn5(clickedListWidget=self.listWidget_6))

        # 办文登记表页面的按钮功能
        self.comboBox_19.currentIndexChanged.connect(self.autoSyn4)  # 设置两个comboBox同步
        self.pushButton_type_search_3.clicked.connect(lambda: self.showRegisTable(type1=self.comboBox_19.currentText(),
                                                                                  type2=self.comboBox_20.currentText()))  # 筛选办文
        self.pushButton_supply_bw.clicked.connect(self.supplyRegisTable)
        self.pushButton_color.clicked.connect(self.setRegisTableRowStatus)
        self.bt_excel_output_lc_2.clicked.connect(self.bwExcelOutput)

        # 经责问题总表录入页面按钮功能
        self.bt_search_jz.clicked.connect(self.searchForJzProblem)
        self.pushButton_que_choose.clicked.connect(self.chooseProblemJzTable)
        self.pushButton_que_import.clicked.connect(
            lambda: self.importExcelProblemJz(path=self.lineEdit_que_jz.text(), keyword="multiple",
                                              keyword2="multiple"))
        self.listWidget_sjwh.currentRowChanged.connect(lambda: self.autoSyn6(clickedListWidget=self.listWidget_sjwh))
        self.listWidget_sjyj.currentRowChanged.connect(lambda: self.autoSyn6(clickedListWidget=self.listWidget_sjyj))
        self.listWidget_sjbg.currentRowChanged.connect(lambda: self.autoSyn6(clickedListWidget=self.listWidget_sjbg))
        self.listWidget_sjjg.currentRowChanged.connect(lambda: self.autoSyn6(clickedListWidget=self.listWidget_sjjg))
        self.listWidget_excel.currentRowChanged.connect(lambda: self.autoSyn6(clickedListWidget=self.listWidget_excel))

        # 经责文件录入页面按钮功能
        self.pushButton_choose_excel.clicked.connect(self.choose_file_jz_excel)
        self.pushButton_choose_excel_2.clicked.connect(self.choose_file_jz_excel2)
        self.pushButton_choose_sjyj.clicked.connect(self.choose_file_sjyj)
        self.pushButton_choose_sjbg.clicked.connect(self.choose_file_sjbg)
        self.pushButton_choose_sjjg.clicked.connect(self.choose_file_sjjg)

        self.pushButton_add_sjyj.clicked.connect(self.add_sjyj)
        self.pushButton_add_sjbg.clicked.connect(self.add_sjbg)

        # 经责文件总览页面按钮功能
        self.pushButton_open_sjyj.clicked.connect(lambda: self.openSjFile(listType="sjyj"))
        self.pushButton_open_sjbg.clicked.connect(lambda: self.openSjFile(listType="sjbg"))
        self.pushButton_open_sjjg.clicked.connect(lambda: self.openSjFile(listType="sjjg"))
        self.pushButton_del_sjyj.clicked.connect(lambda: self.delSjFile(listType="sjyj"))
        self.pushButton_del_sjbg.clicked.connect(lambda: self.delSjFile(listType="sjbg"))
        self.pushButton_del_sjjg.clicked.connect(lambda: self.delSjFile(listType="sjjg"))

        # 整改总览下的按钮功能
        self.pushButton_zg_detail.clicked.connect(self.zg_detail)
        self.comboBox_15.currentIndexChanged.connect(self.sortForZg)  # 排序方法
        self.checkBox_3.clicked.connect(self.tip_zg)  # 设置时间按钮提示
        self.pushButton_type_search_5.clicked.connect(self.selectForZg)  # 条件筛选
        self.pushButton_refresh_lczl_2.clicked.connect(self.refreshZgprocessTable)
        self.comboBox_28.currentIndexChanged.connect(self.autoSyn9)  # 设置复选框同步
        self.pushButton_type_search_4.clicked.connect(self.searchForZg)  # 搜索指定流程
        self.btlczg_3.clicked.connect(self.zgExcelOutput)  # 导出至Excel表格
        self.comboBox_16.currentIndexChanged.connect(self.autoSyn8)
        self.dateEdit_7.dateChanged.connect(lambda: self.autoSynCancelTimeCheckBox(self.checkBox_3))
        self.dateEdit_9.dateChanged.connect(lambda: self.autoSynCancelTimeCheckBox(self.checkBox_3))

        # 领导批示统计下的按钮及其他功能绑定
        self.pushButton_refresh_lczl_5.clicked.connect(self.refreshRectificationTable)
        self.bt_excel_output_lc_4.clicked.connect(self.searchForRectification)  # 按条件查询

        # 问题查询下的按钮及其他功能绑定
        self.pushButton_refresh_lczl_13.clicked.connect(self.refreshProblemSearchTable)  # 刷新显示表格内容
        self.pushButton_add_item_3.clicked.connect(self.addCondition)  # 添加搜索条件
        self.pushButton_sub_item_3.clicked.connect(self.subCondition)  # 添加搜索条件
        self.part_search_wtcx.clicked.connect(self.searchForProblem)  # 按条件进行多维查询
        self.comboBox_27.currentIndexChanged.connect(self.autoSyn11)  # 两个comboBox同步
        self.comboBox_18.currentIndexChanged.connect(self.sortForProblem)  # 排序
        self.sort_wtcx_2.clicked.connect(self.cxExcelOutput)  # 导出至Excel表格
        self.listWidget_9.currentRowChanged.connect(lambda: self.autoSyn10(clickedListWidget=self.listWidget_9))
        self.listWidget_10.currentRowChanged.connect(lambda: self.autoSyn10(clickedListWidget=self.listWidget_10))

        # 办文统计下的按钮及其他功能绑定
        self.comboBox_35.currentIndexChanged.connect(self.showBwChart)  # 按条件显示图形
        self.pushButton_12.clicked.connect(self.screen_shot)

        # 问题统计下的按钮及其他功能绑定
        self.pushButton_part_search_lc_7.clicked.connect(self.showProblemStatistics)  # 显示问题统计图像
        self.pushButton_6.clicked.connect(self.screen_shot_wttj)  # 截屏功能

    """
    @同步前端显示函数
    主要是对前端多个控件之间的内容进行逻辑同步
    """

    # 同步输入框内容,autoSyn1、2为公文时间输入同步,3为公文编号输入同步,4为办文登记表两个下拉框内容同步
    def autoSyn1(self):
        self.dateEdit_6.setDate(self.dateEdit_5.date())

    def autoSyn2(self):
        self.dateEdit_5.setDate(self.dateEdit_6.date())

    def autoSyn3(self):
        cur = self.comboBox_9.currentText() + '〔' + self.spinBox_2.text() + '〕' + self.spinBox_3.text() \
              + '号'
        self.lineEdit_18.setText(cur)

    def autoSyn4(self):
        type1 = self.comboBox_19.currentText()
        self.comboBox_20.clear()
        if type1 == "发文登记表":
            self.comboBox_20.addItems(["不限制", "委文", "委发", "委办文", "委办发", "委函", "委办函", "委便签", "委办便签", "会议纪要", "审计专报"])
        elif type1 == "收文登记表":
            self.comboBox_20.addItems(["请字", "情字", "综字", "会字", "电字"])
        elif type1 == "批文登记表":
            self.comboBox_20.addItems(["批字", "批示"])

    # 批文页面listWidget高亮内容同步
    def autoSyn5(self, clickedListWidget):
        listWidgetSet = {self.listWidget_4, self.listWidget_5, self.listWidget_6}
        listWidgetSet.remove(clickedListWidget)
        for listWidget in listWidgetSet:
            listWidget.setCurrentRow(clickedListWidget.currentRow())

    # 经责文件总览listWidget高亮内容同步
    def autoSyn6(self, clickedListWidget):
        listWidgetSet = {self.listWidget_sjwh, self.listWidget_sjyj, self.listWidget_sjbg, self.listWidget_sjjg,
                         self.listWidget_excel}
        listWidgetSet.remove(clickedListWidget)
        for listWidget in listWidgetSet:
            listWidget.setCurrentRow(clickedListWidget.currentRow())

    # 办文流程筛选栏同步
    def autoSyn7(self):
        type_1 = self.comboBox_13.currentText()
        self.comboBox_14.clear()
        if type_1 == "发文类型":
            self.comboBox_14.addItems(["委文", "委发", "委办文", "委办发", "委函", "委办函", "委便签", "委办便签", "会议纪要", "审计专报"])
        elif type_1 == "收文类型":
            self.comboBox_14.addItems(["请字", "情字", "综字", "会字", "电字"])
        elif type_1 == "是否加入整改":
            self.comboBox_14.addItems(["否", "是"])
        elif type_1 == "不限制":
            self.comboBox_14.addItems(["不限制"])

    # 整改流程筛选栏同步
    def autoSyn8(self):
        type_1 = self.comboBox_16.currentText()
        self.comboBox_17.clear()
        if type_1 == "发文类型":
            self.comboBox_17.addItems(["委文", "委发", "委办文", "委办发", "委函", "委办函", "委便签", "委办便签", "会议纪要", "审计专报"])
        elif type_1 == "收文类型":
            self.comboBox_17.addItems(["请字", "情字", "综字", "会字", "电字"])
        elif type_1 == "不限制":
            self.comboBox_17.addItems(["不限制"])
        elif type_1 == "整改状态":
            self.comboBox_17.addItems(["未整改", "部分整改", "已整改"])

    # 整改流程搜索栏同步
    def autoSyn9(self):
        nowText = self.comboBox_28.currentText()
        self.comboBox_23.clear()
        if nowText == "普通流程":
            self.comboBox_23.addItems(["发文编号", "发文标题", "收文编号", "收文标题", "批文编号", "批文标题", "整改状态"])
        else:
            self.comboBox_23.addItems(["整改状态"])

    # 批文页面listWidget高亮内容同步
    def autoSyn10(self, clickedListWidget):
        listWidgetSet = {self.listWidget_9, self.listWidget_10}
        listWidgetSet.remove(clickedListWidget)
        for listWidget in listWidgetSet:
            listWidget.setCurrentRow(clickedListWidget.currentRow())

    # 问题查询页面排序栏同步
    def autoSyn11(self):
        nowText = self.comboBox_27.currentText()
        self.comboBox_18.clear()
        if nowText == "按出具审计报告时间" or nowText == "按应上报整改报告时间" or nowText == "按实际上报整改报告时间":
            self.comboBox_18.addItems(["由近及远排序", "由远及近排序"])
        elif nowText == "按整改率":
            self.comboBox_18.addItems(["由高至低排序", "由低至高排序"])
        elif nowText == "按上报次序":
            self.comboBox_18.addItems(["由大到小排序", "由小到大排序"])
        else:
            self.comboBox_18.addItems(["由多到少排序", "由少到多排序"])

    # 发文办理下的公文类型同步
    def autoSynSendfileType(self, index):
        self.stackedWidget_new.setCurrentIndex(index)

    # 日期有变动就取消checkBox的选中
    def autoSynCancelTimeCheckBox(self, checkBox):
        checkBox.setChecked(False)

    """
    @关闭子页面操作函数
    @关闭tabWidget或者Window
    """

    def closeTab1(self, index):
        obj = self.tabWidget_zgzl.widget(index)
        for key, value in self.tabWidget_zgzl_dict.items():
            if value == obj:
                self.tabWidget_zgzl_dict.pop(key)
                break
            else:
                continue
        self.tabWidget_zgzl.removeTab(index)

    def closeTab2(self, index):
        obj = self.tabWidget_lczl.widget(index)
        for key, value in self.tabWidget_lczl_dict.items():
            if value == obj:
                self.tabWidget_lczl_dict.pop(key)
                break
            else:
                continue
        self.tabWidget_lczl.removeTab(index)

    """
    @新增子页面操作函数
    主要是对表格某一行进行操作(修改或查看)生成新的子页面
    """

    # 整改总览下的查看详情按钮
    def zg_detail(self):
        row = self.tableWidget_zgzl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择整改项目！")
        else:
            # 获取整改序号
            key = self.tableWidget_zgzl.item(row, 0).text()
            # 实例tab不存在
            if self.tabWidget_zgzl_dict.get(key) is None:
                tab_new = Call_zgdetail(key)
                tab_new.setObjectName('tab_new')
                tab_index = self.tabWidget_zgzl.addTab(tab_new, self.tableWidget_zgzl.item(row, 2).text())
                self.tabWidget_zgzl.setCurrentIndex(tab_index)
                self.tabWidget_zgzl_dict[key] = tab_new
            # 实例tab已经存在
            else:
                cur_tab = self.tabWidget_zgzl_dict.get(key)
                cur_index = self.tabWidget_zgzl.indexOf(cur_tab)
                self.tabWidget_zgzl.setCurrentIndex(cur_index)

    # 办文流程详情下的查看详情按钮
    def lc_detail(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择流程！")
        else:
            key = self.tableWidget_lczl.item(row, 0).text()  # 流程序号
            # 实例tab不存在
            if self.tabWidget_lczl_dict.get(key) is None:
                tab_new = Call_lcdetail(key)
                tab_new.setObjectName('tab_new')
                # 设置tab标题,有发文标题设置为发文编号,没有发文设置有收文设置为收文编号,没有发文没有收文设置为批文标题
                if self.tableWidget_lczl.item(row, 2).text() != '/':
                    tab_index = self.tabWidget_lczl.addTab(tab_new, self.tableWidget_lczl.item(row, 2).text())
                elif self.tableWidget_lczl.item(row, 5).text() != '/':
                    tab_index = self.tabWidget_lczl.addTab(tab_new, self.tableWidget_lczl.item(row, 5).text())
                else:
                    tab_index = self.tabWidget_lczl.addTab(tab_new,
                                                           self.tableWidget_lczl.item(row, 7).text().replace("\n", ","))
                self.tabWidget_lczl.setCurrentIndex(tab_index)
                self.tabWidget_lczl_dict[key] = tab_new
            # 实例tab已经存在
            else:
                cur_tab = self.tabWidget_lczl_dict.get(key)
                cur_index = self.tabWidget_lczl.indexOf(cur_tab)
                self.tabWidget_lczl.setCurrentIndex(cur_index)

    # 补充发文登记表
    def supplyRegisTable(self):
        row = self.tableWidget_bwzl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择表格中的一行！")
        else:
            key = self.tableWidget_bwzl.item(row, 0).text()
            if self.resType1 == "发文登记表":
                self.window = Call_sendfilebq(key)
                self.window.setWindowTitle("发文补充")

            elif self.resType1 == "收文登记表":
                self.window = Call_revfilebq(key)
                self.window.setWindowTitle("收文补充")

            elif self.resType1 == "批文登记表":
                if self.resType2 == "批字":
                    self.window = Call_corfilebq(key)
                    self.window.setWindowTitle("批文补充")
                elif self.resType2 == "批示":
                    self.window = Call_instbq(key)
                    self.window.setWindowTitle("批示补充")
            self.window.exec()

            # 重新展示
            self.showRegisTable(type1=self.resType1, type2=self.resType2)

    """
    @页面展示函数
    @页面初始化函数
    @页面刷新功能
    """

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
        sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号)," \
              "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n'),REPLACE(GROUP_CONCAT(" \
              "distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改 FROM bwprocess LEFT OUTER JOIN sendfile ON " \
              "sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = problem.发文序号 LEFT OUTER JOIN " \
              "revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile ON bwprocess.序号 = corfile.流程序号 GROUP BY " \
              "bwprocess.序号 "
        data = tools.executeSql(sql)

        # 打印结果
        size = len(data)
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
        # 清空表格
        self.tableWidget_bwzl.clear()
        # 表格不可编辑
        self.tableWidget_bwzl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 表格只可选中行
        self.tableWidget_bwzl.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 表格只可选中单行
        self.tableWidget_bwzl.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置字体
        self.tableWidget_bwzl.horizontalHeader().setFont(QFont('Microsoft YaHei UI', 14, QFont.Black))

        self.resType1 = type1  # 标识当前访问的登记表类型1
        self.resType2 = type2  # 标识当前访问的登记表类型2
        # 设置状态按钮可用
        self.pushButton_color.setEnabled(True)
        self.radioButton_red.setEnabled(True)
        self.radioButton_green.setEnabled(True)
        self.radioButton_black.setEnabled(True)
        self.pushButton_supply_bw.setEnabled(True)

        data = []
        if type1 == "发文登记表":
            self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。")
            self.tableWidget_bwzl.setColumnCount(12)
            self.tableWidget_bwzl.setHorizontalHeaderLabels(
                ['主键', '登记时间', '发文字号', '密级', '标识', '标题', '签发人', '份数', '公文运转情况', '批示情况', '批示办理情况', '起草处室'])
            rear = ""
            if type2 == "委文":
                self.label_34.setText("鄂审计委文")
                rear = " having sendfile.发文字号 like '鄂审计委文%' "
            elif type2 == "委发":
                self.label_34.setText("鄂审计委发")
                rear = " having sendfile.发文字号 like '鄂审计委发%' "
            elif type2 == "委办文":
                self.label_34.setText("鄂审计委办文")
                rear = " having sendfile.发文字号 like '鄂审计委办文%' "
            elif type2 == "委办发":
                self.label_34.setText("鄂审计委办发")
                rear = " having sendfile.发文字号 like '鄂审计委办发%' "
            elif type2 == "委函":
                self.label_34.setText("鄂审计委函")
                rear = " having sendfile.发文字号 like '鄂审计委函%' "
            elif type2 == "委办函":
                self.label_34.setText("鄂审计委办函")
                rear = " having sendfile.发文字号 like '鄂审计委办函%' "
            elif type2 == "委便签":
                self.label_34.setText("鄂审计委便签")
                rear = " having sendfile.发文字号 like '鄂审计委便签%' "
            elif type2 == "委办便签":
                self.label_34.setText("鄂审计委办便签:（无编号）")
                rear = " having sendfile.发文字号 like '鄂审计委办便签%' "
            elif type2 == "会议纪要":
                self.label_34.setText("会议纪要")
                rear = " having sendfile.发文字号 like '会议纪要%' "
            elif type2 == "审计专报":
                self.label_34.setText("审计专报")
                rear = " having sendfile.发文字号 like '审计专报%' "

            sql = "select sendfile.序号,sendfile.办文日期,sendfile.发文字号,sendfile.秘密等级,sendfile.标识,sendfile.发文标题," \
                  "sendfile.签发人,sendfile.份数,sendfile.公文运转情况,GROUP_CONCAT(instruction.领导内容摘要和领导批示,'\n')," \
                  "sendfile.批示办理情况,sendfile.起草处室,sendfile.状态 from sendfile left outer join bwprocess on " \
                  "sendfile.序号 = bwprocess.发文序号 left outer join corfile on corfile.流程序号 = bwprocess.序号 left outer " \
                  "join instruction on instruction.批文序号 = corfile.序号 group by sendfile.序号" + rear
            data = tools.executeSql(sql)

            data = tools.sortByKey(data, 2, 2)

        elif type1 == "收文登记表":
            self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。")
            self.tableWidget_bwzl.setColumnCount(13)
            self.tableWidget_bwzl.setHorizontalHeaderLabels(
                ['主键', '时间', '编号', '秘级', '来文单位', '来文字号', '来文标题', '拟办意见', '要求时间', '厅领导签批意见', '承办处室', '办理结果',
                 '文件去向'])
            rear = ""
            if type2 == "请字":
                self.label_34.setText("请字（平级、下级报送的请示类文件）→")
                rear = " where 收文字号 like '请字%' "
            elif type2 == "情字":
                self.label_34.setText("情字（平级、下级报送的情况类文件）→")
                rear = " where 收文字号 like '情字%' "
            elif type2 == "综字":
                self.label_34.setText("综字（上级下发的各类文件）→")
                rear = " where 收文字号 like '综字%' "
            elif type2 == "会字":
                self.label_34.setText("会字（各级会议通知）→")
                rear = " where 收文字号 like '会字%' "
            elif type2 == "电字":
                self.label_34.setText("电字（电报文件）→")
                rear = " where 收文字号 like '电字%' "

            sql = "select 序号,收文时间,收文字号,秘密等级,来文单位,来文字号,收文标题,内容摘要和拟办意见,要求时间,领导批示,承办处室,处理结果,文件去向,状态 from revfile" + rear
            data = tools.executeSql(sql)

            # 按照收文字号排序
            data = tools.sortByKey(data, 2, 2)

        elif type1 == "批文登记表":
            # 按照一条批文为单位生成登记表
            if type2 == "批字":
                self.label_34.setText("批字（省领导对审计委员会及委员会办公室文件资料的批示）")
                self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。")
                self.tableWidget_bwzl.setColumnCount(16)
                self.tableWidget_bwzl.setHorizontalHeaderLabels(
                    ['主键', '时间', '发文编号', '收文编号', '办文编号', '秘级', '来文单位', '来文字号', '来文标题', '省领导批示内容', '秘书处拟办意见', '委办主任签批意见',
                     '批示任务办理要求时间', '审计厅承办处室及承办人', '办理结果', '文件去向'])

                sql = "select corfile.序号,corfile.收文时间,sendfile.发文字号,revfile.收文字号,corfile.批文字号,corfile.秘密等级," \
                      "GROUP_CONCAT(instruction.领导来文单位,'\n'),GROUP_CONCAT(instruction.领导来文字号,'\n'),corfile.批文标题," \
                      "GROUP_CONCAT(instruction.领导内容摘要和领导批示,'\n'),corfile.内容摘要和拟办意见,corfile.领导批示,corfile.批示任务办理要求时间," \
                      "corfile.审计厅承办处室及承办人,corfile.办理结果,corfile.文件去向,corfile.状态 from corfile left outer join " \
                      "instruction on corfile.序号 = instruction.批文序号 left outer join bwprocess on bwprocess.序号 = " \
                      "corfile.流程序号 left outer join sendfile on bwprocess.发文序号 = sendfile.序号 left outer join revfile " \
                      "on bwprocess.收文序号 = revfile.序号 group by corfile.序号 "
                data = tools.executeSql(sql)

                # 按照批文字号排序
                data = tools.sortByKey(data, 4, 2)

            # 按照一条批示为单位生成登记表
            elif type2 == "批示":
                # 设置状态按钮不可用
                self.pushButton_color.setDisabled(True)
                self.radioButton_red.setDisabled(True)
                self.radioButton_green.setDisabled(True)
                self.radioButton_black.setDisabled(True)

                self.label_34.setText("批字（省领导对审计委员会及委员会办公室文件资料的批示详情）")
                self.label_35.setText("一位省领导的一条批示作为一条记录。")
                self.tableWidget_bwzl.setColumnCount(13)
                self.tableWidget_bwzl.setHorizontalHeaderLabels(
                    ['主键', '办文编号', '密级', '报送载体', '报送标题', '来文字号', '来文标题', '来文单位', '批示载体', '批示人',
                     '批示人职务', '批示时间', '批示内容'])

                sql = "select instruction.序号,corfile.批文字号,corfile.秘密等级,sendfile.发文字号,sendfile.发文标题," \
                      "instruction.领导来文字号,corfile.批文标题,instruction.领导来文单位,revfile.收文字号,instruction.领导姓名," \
                      "instruction.领导职务,instruction.批示时间,instruction.领导内容摘要和领导批示 from instruction left outer join " \
                      "corfile on instruction.批文序号 = corfile.序号 left outer join bwprocess on bwprocess.序号 = " \
                      "corfile.流程序号 left outer join sendfile on bwprocess.发文序号 = sendfile.序号 left outer join revfile " \
                      "on bwprocess.收文序号 = revfile.序号 "
                data = tools.executeSql(sql)

                # 按照批文字号排序
                data = tools.sortByKey(data, 1, 2)

        # 打印结果
        # print(data)

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_bwzl.setRowCount(size)

        x = 0
        for i in data:
            # 批示不属于公文,无状态,status为公文状态
            if type2 != "批示":
                length = len(i) - 1
                status = i[length]
            else:
                length = len(i)
                status = ""
            for y in range(0, length):
                if data[x][y] is None:
                    self.tableWidget_bwzl.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_bwzl.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                if status == "red":
                    self.tableWidget_bwzl.item(x, y).setForeground(QBrush(QColor(255, 0, 0)))
                elif status == "green":
                    self.tableWidget_bwzl.item(x, y).setForeground(QBrush(QColor(0, 170, 0)))
                elif status == "black":
                    self.tableWidget_bwzl.item(x, y).setForeground(QBrush(QColor(0, 0, 0)))
            x = x + 1

        self.tableWidget_bwzl.hideColumn(0)  # 将发文、收文、批文、批示数据库主键隐藏起来,作为传参
        self.tableWidget_bwzl.setFont(QFont('Times', 14, QFont.Black))
        self.tableWidget_bwzl.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_bwzl.resizeRowsToContents()  # 根据行调整框大小

    # 初始化经责问题总表页面
    def displayProblemJzPage(self):
        # 表格不可编辑
        self.tableWidget_jz_pro.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        sql = "select 序号,问题顺序号,被审计领导干部,所在地方或单位,报送文号,审计意见或报告文号,经责结果报告文号,出具审计报告时间,审计组组长,审计组主审,问题描述,是否在审计报告中反映," \
              "是否在结果报告中反映,审计对象分类,问题类别,问题定性,问题表现形式,备注,问题金额,移送及处理情况 from problem_jz "
        data = tools.executeSql(sql)

        size = len(data)

        # 对data按照文号排序
        data = tools.sortByKey(data, 5, 2)

        # 已经完成录入
        if size != 0:
            # 搜索按钮可点击
            self.bt_search_jz.setEnabled(True)

            self.tableWidget_jz_pro.setRowCount(size)

            x = 0
            for i in data:
                y = 0
                for j in i:
                    if data[x][y] is None:
                        self.tableWidget_jz_pro.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                    else:
                        self.tableWidget_jz_pro.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                    y = y + 1
                x = x + 1

            # 下拉栏自动收集文号作为查询条件
            keywords_temp = []
            for i in data:
                # 审计意见(报告)文号必定不为空
                if i[5] != "":
                    keywords_temp.append(i[5])

            keywords = list(set(keywords_temp))
            keywords.sort(key=keywords_temp.index)

            self.comboBox_11.clear()
            for i in keywords:
                self.comboBox_11.addItem(i)

        else:
            # 清空表格
            self.tableWidget_jz_pro.setRowCount(0)

            # 清空搜索栏可选项
            self.comboBox_11.clear()

            # 搜索按钮不可点击
            self.bt_search_jz.setDisabled(True)

        self.tableWidget_jz_pro.hideColumn(0)  # 将经责问题表主键隐藏起来
        self.tableWidget_jz_pro.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_jz_pro.resizeRowsToContents()  # 根据行调整框大小

    # 初始化经责文件导入界面
    def displayJzFileInsertPage(self):
        # 初始化文号控件
        self.spinBox_sjyj_year.setValue(datetime.datetime.now().year)
        self.spinBox_sjbg_year.setValue(datetime.datetime.now().year)
        self.spinBox_sjjg_year.setValue(datetime.datetime.now().year)

        self.spinBox_sjyj_num.setValue(1)
        self.spinBox_sjbg_num.setValue(1)
        self.spinBox_sjjg_num.setValue(1)

        # 文件输入栏不可编辑
        self.lineEdit_file_sjyj.setReadOnly(True)
        self.lineEdit_file_sjbg.setReadOnly(True)
        self.lineEdit_file_sjjg.setReadOnly(True)
        self.lineEdit_file_excel.setReadOnly(True)
        self.lineEdit_file_excel_2.setReadOnly(True)
        self.lineEdit_que_jz.setReadOnly(True)

        # 清空文件输入栏
        self.lineEdit_file_sjyj.clear()
        self.lineEdit_file_sjbg.clear()
        self.lineEdit_file_sjjg.clear()
        self.lineEdit_file_excel.clear()
        self.lineEdit_file_excel_2.clear()
        self.lineEdit_que_jz.clear()

    # 展示经责文件总览界面
    def displayFileJzPage(self):
        # 清空list
        self.listWidget_sjyj.clear()
        self.listWidget_sjbg.clear()
        self.listWidget_sjjg.clear()
        self.listWidget_sjwh.clear()
        self.listWidget_excel.clear()

        # 查找审计意见文件信息和相关问题个数
        sql = "select sjyjword.审计意见文号,sjyjword.审计意见内容,count(problem_jz.审计意见或报告文号) from sjyjword left join problem_jz " \
              "on sjyjword.审计意见文号 = problem_jz.审计意见或报告文号 group by sjyjword.审计意见文号 "
        data = tools.executeSql(sql)
        result = []
        for i in data:
            tempTuple = (i[0], i[1], '/', '/', i[2])
            result.append(tempTuple)

        # 查找审计报告文件信息以及审计结果报告文件信息和相关问题个数
        sql = "select sjbgword.审计报告文号,sjbgword.审计报告内容,sjbgword.审计结果内容,count(problem_jz.审计意见或报告文号) from sjbgword left " \
              "join problem_jz on sjbgword.审计报告文号 = problem_jz.审计意见或报告文号 group by sjbgword.审计报告文号 "
        data = tools.executeSql(sql)
        for i in data:
            tempTuple = (i[0], '/', i[1], i[2], i[3])
            result.append(tempTuple)

        # print(result)
        for i in result:
            self.listWidget_sjwh.addItem(i[0])
            self.listWidget_sjyj.addItem(i[1])
            self.listWidget_sjbg.addItem(i[2])
            self.listWidget_sjjg.addItem(i[3])
            self.listWidget_excel.addItem(str(i[4]))

    # 显示整改内容
    def showZgTable(self):
        # 表格不可编辑
        self.tableWidget_zgzl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget_zgzl.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget_zgzl.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableWidget_zgzl.hideColumn(0)  # 将流程数据库主键隐藏起来,作为传参,此处主键为整改序号

        # sql由整改表的流程序号出发,通过多表查询获得办文流程类型整改的所有字段
        sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
              "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess join " \
              "bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 left outer " \
              "join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = corfile.流程序号 GROUP BY " \
              "zgprocess.序号 "
        data1 = tools.executeSql(sql)

        # sql由整改表的流程序号出发,通过多表查询获得经责项目类型整改的所有字段
        sql = "select zgprocess.序号,problem_jz.出具审计报告时间,problem_jz.审计意见或报告文号,zgprocess.整改状态 from zgprocess join " \
              "problem_jz on zgprocess.序号 = problem_jz.整改序号 group by zgprocess.序号"
        temp_data2 = tools.executeSql(sql)
        data2 = []

        # 对temp_data2进行数据处理,使得data1和data2可以合并
        for i in temp_data2:
            temp_tuple = (i[0], i[1], i[2], None, None, None, None, None, i[3])
            data2.append(temp_tuple)

        # 合并两个列表
        data = data1 + data2

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_zgzl.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.tableWidget_zgzl.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_zgzl.resizeRowsToContents()  # 根据行调整框大小

        self.tableWidget_zgzl.sortItems(1, Qt.DescendingOrder)  # 按照流程建立时间排序

    # 显示问题查询内容
    def showProblemSearchTable(self):
        # 表格不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 表格只可选中行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 表格只可选中单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        sql = "SELECT sendfile.发文字号,problem.被审计领导干部,problem.所在地方或单位,problem.审计报告文号,problem.出具审计报告时间," \
              "problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类," \
              "problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况,rectification.上报次序,rectification." \
              "整改责任部门,rectification.应上报整改报告时间,rectification.实际上报整改报告时间,rectification.整改情况,rectification." \
              "已整改金额,rectification.追责问责人数,rectification.推动制度建设数目,rectification.推动制度建设文件,rectification." \
              "部分整改情况具体描述,rectification.未整改原因说明,rectification.下一步整改措施及时限,rectification.认定整改情况," \
              "rectification.认定整改金额,rectification.整改率 FROM problem LEFT OUTER JOIN rectification ON rectification." \
              "问题序号 = problem.序号 LEFT OUTER JOIN sendfile ON sendfile.序号 = problem.发文序号"
        data = tools.executeSql(sql)

        # 打印结果
        size = len(data)
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

    # 显示所有领导批示
    def showRectificationTable(self):
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
        self.tableWidget_2.setColumnCount(13)
        self.tableWidget_2.horizontalHeader().setStyleSheet("QHeaderView::section{background:lightyellow;}")
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['主键', '办文编号', '密级', '报送载体', '报送标题', '来文字号', '来文标题', '来文单位', '批示载体', '批示人',
             '批示人职务', '批示时间', '批示内容'])

        sql = "select instruction.序号,corfile.批文字号,corfile.秘密等级,sendfile.发文字号,sendfile.发文标题," \
              "instruction.领导来文字号,corfile.批文标题,instruction.领导来文单位,revfile.收文字号,instruction.领导姓名," \
              "instruction.领导职务,instruction.批示时间,instruction.领导内容摘要和领导批示 from instruction left outer join " \
              "corfile on instruction.批文序号 = corfile.序号 left outer join bwprocess on bwprocess.序号 = " \
              "corfile.流程序号 left outer join sendfile on bwprocess.发文序号 = sendfile.序号 left outer join revfile " \
              "on bwprocess.收文序号 = revfile.序号 "
        data = tools.executeSql(sql)
        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_2.setRowCount(size)

        x = 0
        for i in data:
            for y in range(0, 13):
                if data[x][y] is None:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
            x = x + 1

        self.tableWidget_2.setFont(QFont('Times', 14, QFont.Black))
        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小

        self.tableWidget_2.hideColumn(0)

    # 显示办文流程饼状图统计
    def showBwChart(self):
        nowText = self.comboBox_35.currentText()
        # 设置绘图区域
        figure = pyplot.figure()  # 新建绘图区域
        canvas = FigureCanvas(figure)  # 绘图区域放到图层canvas之中
        self.gridLayout_15.addWidget(canvas, 1, 0, 2, 2)  # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）
        self.label_78.setText("%s情况的数量及比例如下：" % nowText)
        pyplot.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
        # 发文条目
        sql_send = "select * from sendfile"

        # 收文条目
        sql_rev = "select * from revfile"

        # 批文条目
        sql_cor = "select * from corfile"
        if nowText == "办文类型":
            # 发文条目
            size_send = len(tools.executeSql(sql_send))

            # 收文条目
            size_rev = len(tools.executeSql(sql_rev))

            # 批文条目
            size_cor = len(tools.executeSql(sql_cor))

            lab_1 = '发文登记表（' + str(size_send) + '）'
            lab_2 = '收文登记表（' + str(size_rev) + '）'
            lab_3 = '批文登记表（' + str(size_cor) + '）'
            labels = [lab_1, lab_2, lab_3]
            sizes = [size_send, size_rev, size_cor]
            colors = ['yellowGreen', 'Gold', 'lightSkyBlue']
            explode = 0, 0, 0
        elif nowText == "是否公开":

            sql_send_pub = sql_send + " where sendfile.是否公开 = '是'"
            len_send_pub = len(tools.executeSql(sql_send_pub))
            sql_rev_pub = sql_rev + " where revfile.是否公开 = '是'"
            len_rev_pub = len(tools.executeSql(sql_rev_pub))
            sql_cor_pub = sql_cor + " where corfile.是否公开 = '是'"
            len_cor_pub = len(tools.executeSql(sql_cor_pub))
            size_pub = len_send_pub + len_rev_pub + len_cor_pub

            sql_send_not_pub = sql_send + " where sendfile.是否公开 = '否'"
            len_send_not_pub = len(tools.executeSql(sql_send_not_pub))
            sql_rev_not_pub = sql_rev + " where revfile.是否公开 = '否'"
            len_rev_not_pub = len(tools.executeSql(sql_rev_not_pub))
            sql_cor_not_pub = sql_cor + " where corfile.是否公开 = '否'"
            len_cor_not_pub = len(tools.executeSql(sql_cor_not_pub))
            size_not_pub = len_send_not_pub + len_rev_not_pub + len_cor_not_pub

            lab_1 = '公开办文（' + str(size_pub) + '）'
            lab_2 = '不公开办文（' + str(size_not_pub) + '）'
            labels = [lab_1, lab_2]
            sizes = [size_pub, size_not_pub]
            colors = ['yellowGreen', 'Gold']
            explode = 0, 0

        elif nowText == "秘密等级":
            sql_send_pub = sql_send + " where sendfile.秘密等级 = '' or sendfile.秘密等级 = '不加密' or sendfile.秘密等级 = '公开'"
            len_send_pub = len(tools.executeSql(sql_send_pub))
            sql_rev_pub = sql_rev + " where revfile.秘密等级 = '' or revfile.秘密等级 = '不加密' or revfile.秘密等级 = '公开'"
            len_rev_pub = len(tools.executeSql(sql_rev_pub))
            sql_cor_pub = sql_cor + " where corfile.秘密等级 = '' or corfile.秘密等级 = '不加密' or corfile.秘密等级 = '公开'"
            len_cor_pub = len(tools.executeSql(sql_cor_pub))
            size_pub = len_send_pub + len_rev_pub + len_cor_pub

            sql_send_mm = sql_send + " where sendfile.秘密等级 like '%秘密%'"
            len_send_mm = len(tools.executeSql(sql_send_mm))
            sql_rev_mm = sql_rev + " where revfile.秘密等级 like '%秘密%'"
            len_rev_mm = len(tools.executeSql(sql_rev_mm))
            sql_cor_mm = sql_cor + " where corfile.秘密等级 like '%秘密%'"
            len_cor_mm = len(tools.executeSql(sql_cor_mm))
            size_mm = len_send_mm + len_rev_mm + len_cor_mm

            sql_send_jm = sql_send + " where sendfile.秘密等级 like '%机密%'"
            len_send_jm = len(tools.executeSql(sql_send_jm))
            sql_rev_jm = sql_rev + " where revfile.秘密等级 like '%机密%'"
            len_rev_jm = len(tools.executeSql(sql_rev_jm))
            sql_cor_jm = sql_cor + " where corfile.秘密等级 like '%机密%'"
            len_cor_jm = len(tools.executeSql(sql_cor_jm))
            size_jm = len_send_jm + len_rev_jm + len_cor_jm

            sql_send_juem = sql_send + " where sendfile.秘密等级 like '%绝密%'"
            len_send_juem = len(tools.executeSql(sql_send_juem))
            sql_rev_juem = sql_rev + " where revfile.秘密等级 like '%绝密%'"
            len_rev_juem = len(tools.executeSql(sql_rev_juem))
            sql_cor_juem = sql_cor + " where corfile.秘密等级 like '%绝密%'"
            len_cor_juem = len(tools.executeSql(sql_cor_juem))
            size_juem = len_send_juem + len_rev_juem + len_cor_juem

            lab_1 = '不加密（' + str(size_pub) + '）'
            lab_2 = '秘密（' + str(size_mm) + '）'
            lab_3 = '机密（' + str(size_jm) + '）'
            lab_4 = '绝密（' + str(size_juem) + '）'
            labels = [lab_1, lab_2, lab_3, lab_4]
            sizes = [size_pub, size_mm, size_jm, size_juem]
            colors = ['yellowGreen', 'Gold', 'Pink', 'lightSkyBlue']
            explode = 0, 0, 0, 0

        elif nowText == "紧急程度":

            sql_send_pt = sql_send + " where sendfile.紧急程度 = '' or sendfile.紧急程度 = '无'"
            len_send_pt = len(tools.executeSql(sql_send_pt))
            sql_rev_pt = sql_rev + " where revfile.紧急程度 = '' or revfile.紧急程度 = '无'"
            len_rev_pt = len(tools.executeSql(sql_rev_pt))
            sql_cor_pt = sql_cor + " where corfile.紧急程度 = '' or corfile.紧急程度 = '无'"
            len_cor_pt = len(tools.executeSql(sql_cor_pt))
            size_pt = len_send_pt + len_rev_pt + len_cor_pt

            sql_send_jj = sql_send + " where sendfile.紧急程度 like '%加急%'"
            len_send_jj = len(tools.executeSql(sql_send_jj))
            sql_rev_jj = sql_rev + " where revfile.紧急程度 like '%加急%'"
            len_rev_jj = len(tools.executeSql(sql_rev_jj))
            sql_cor_jj = sql_cor + " where corfile.紧急程度 like '%加急%'"
            len_cor_jj = len(tools.executeSql(sql_cor_jj))
            size_jj = len_send_jj + len_rev_jj + len_cor_jj

            sql_send_tj = sql_send + " where sendfile.紧急程度 like '%特急%'"
            len_send_tj = len(tools.executeSql(sql_send_tj))
            sql_rev_tj = sql_rev + " where revfile.紧急程度 like '%特急%'"
            len_rev_tj = len(tools.executeSql(sql_rev_tj))
            sql_cor_tj = sql_cor + " where corfile.紧急程度 like '%特急%'"
            len_cor_tj = len(tools.executeSql(sql_cor_tj))
            size_tj = len_send_tj + len_rev_tj + len_cor_tj

            lab_1 = '普通（' + str(size_pt) + '）'
            lab_2 = '加急（' + str(size_jj) + '）'
            lab_3 = '特急（' + str(size_tj) + '）'
            labels = [lab_1, lab_2, lab_3]
            sizes = [size_pt, size_jj, size_tj]
            colors = ['yellowGreen', 'Gold', 'Pink']
            explode = 0, 0, 0

        elif nowText == "办文状态":

            sql_send_jwbj = sql_send + " where sendfile.状态 = 'red'"
            len_send_jwbj = len(tools.executeSql(sql_send_jwbj))
            sql_rev_jwbj = sql_rev + " where revfile.状态 = 'red'"
            len_rev_jwbj = len(tools.executeSql(sql_rev_jwbj))
            sql_cor_jwbj = sql_cor + " where corfile.状态 = 'red'"
            len_cor_jwbj = len(tools.executeSql(sql_cor_jwbj))
            size_jwbj = len_send_jwbj + len_rev_jwbj + len_cor_jwbj

            sql_send_sxzb = sql_send + " where sendfile.状态 = 'green'"
            len_send_sxzb = len(tools.executeSql(sql_send_sxzb))
            sql_rev_sxzb = sql_rev + " where revfile.状态 = 'green'"
            len_rev_sxzb = len(tools.executeSql(sql_rev_sxzb))
            sql_cor_sxzb = sql_cor + " where corfile.状态 = 'green'"
            len_cor_sxzb = len(tools.executeSql(sql_cor_sxzb))
            size_sxzb = len_send_sxzb + len_rev_sxzb + len_cor_sxzb

            sql_send_wqbj = sql_send + " where sendfile.状态 = 'black'"
            len_send_wqbj = len(tools.executeSql(sql_send_wqbj))
            sql_rev_wqbj = sql_rev + " where revfile.状态 = 'black'"
            len_rev_wqbj = len(tools.executeSql(sql_rev_wqbj))
            sql_cor_wqbj = sql_cor + " where corfile.状态 = 'black'"
            len_cor_wqbj = len(tools.executeSql(sql_cor_wqbj))
            size_wqbj = len_send_wqbj + len_rev_wqbj + len_cor_wqbj

            lab_1 = '件未办结（' + str(size_jwbj) + '）'
            lab_2 = '件已办结，事项在办（' + str(size_sxzb) + '）'
            lab_3 = '件与事项完全办结并共同归档（' + str(size_wqbj) + '）'
            labels = [lab_1, lab_2, lab_3]
            sizes = [size_jwbj, size_sxzb, size_wqbj]
            colors = ['yellowGreen', 'Gold', 'Pink']
            explode = 0, 0, 0

        patches, l_text, p_text = pyplot.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                                             shadow=True,
                                             startangle=50)  # startangle表示饼图的起始角度
        # pie函数返回值中，l_text代表饼状图外的文本，p_text代表饼状图内的文本
        for t in l_text:
            t.set_size(20)
        for t in p_text:
            t.set_size(15)

    # 显示问题整改柱状图统计
    def showProblemStatistics(self):
        Dict = {
            "问题金额统计": "SUM(problem.问题金额)",
            "认定整改金额统计": "SUM(rectification.认定整改金额)",
            "问题数量统计": "COUNT(problem.序号)",
            "认定整改情况": "rectification.认定整改情况",
            "上报整改情况": "rectification.整改情况",
            "审计组组长": "problem.审计组组长",
            "审计组主审": "problem.审计组主审",
        }
        tongjiliang = self.comboBox_37.currentText()
        tongjiweidu = self.comboBox_36.currentText()
        text_27 = "以" + tongjiweidu + "为维度进行" + tongjiliang
        self.label_27.setText(text_27)
        # 设置绘图区域
        figure = pyplot.figure()  # 新建绘图区域
        canvas = FigureCanvas(figure)  # 绘图区域放到图层canvas之中
        self.gridLayout_3.addWidget(canvas, 1, 0, 2, 2)  # 图层放到pyqt布局之中（这个布局替代了之前设计时使用的graphicView）

        aim = self.comboBox_37.currentText()  # 统计量
        dim = self.comboBox_36.currentText()  # 统计维度

        # 此处不需要左外连接,因为没有整改的问题不加入统计,选定最后一次上报数据作为分析数据
        # 内层select用于过滤数据只保留最近一次上报的记录,外层用select用于对问题进行统计分析
        sql = "select %s,%s,problem.序号,rectification.上报次序 from problem join rectification on problem.序号 = " \
              "rectification.问题序号 where (problem.序号,rectification.上报次序) in (select problem.序号,MAX(rectification.上报次序) " \
              "from problem join rectification on problem.序号 = rectification.问题序号 group by problem.序号) group by %s " \
              % (Dict.get(dim), Dict.get(aim), Dict.get(dim))

        # 得到绘图数据
        data = tools.executeSql(sql)
        print(data)

        # 绘制图形
        pyplot.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
        bar_width = 0.1
        x_name = []
        y = []
        for Tuple in data:
            x_name.append(Tuple[0])
            y.append(Tuple[1])

        x = list(range(len(x_name)))  # 设置x轴的节点数
        x_address = [i for i in x]  # 循环遍历，得到指定的节点数
        pyplot.xticks(x_address, x_name)  # 绘制x轴
        pyplot.xticks(fontsize=15)  # 设置x轴字体大小
        pyplot.yticks(fontsize=15)  # 设置y轴字体大小
        pyplot.bar(x, y, width=bar_width)  # 三个柱子颜色
        canvas.draw()  # 这是关键

    # 刷新发文流程页面
    def refreshBwprocessTable(self):
        # 刷新控件
        self.lineEdit_global.clear()
        self.comboBox_13.clear()
        self.comboBox_13.addItems(["不限制", "发文类型", "收文类型", "是否加入整改"])
        self.comboBox_14.clear()
        self.comboBox_14.addItem("不限制")
        self.checkBox.setChecked(False)
        self.lineEdit_4.setText("请在此输入表格名")
        self.comboBox_12.clear()
        self.comboBox_12.addItems(['按流程开始时间由近及远排序', '按流程开始时间由远及近排序', '按问题个数排序'])
        self.comboBox_21.clear()
        self.comboBox_21.addItems(['发文标题', '发文号', '收文标题', '收文号', '批文标题', '批文号'])
        self.dateEdit_8.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        self.dateEdit_10.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        # 刷新显示tableWidget
        self.showBwprocessTable()

    # 刷新整改流程页面
    def refreshZgprocessTable(self):
        # 刷新控件
        self.comboBox_15.clear()
        self.comboBox_15.addItems(["按流程开始时间由近及远排序", "按流程开始时间由远及近排序"])
        self.comboBox_28.clear()
        self.comboBox_28.addItems(["普通流程", "经责流程"])
        self.comboBox_23.clear()
        self.comboBox_23.addItems(["发文编号", "发文标题", "收文编号", "收文标题", "批文编号", "批文标题", "整改状态"])
        self.comboBox_16.clear()
        self.comboBox_16.addItems(["不限制", "发文类型", "收文类型"])
        self.comboBox_17.clear()
        self.comboBox_17.addItem("不限制")
        self.checkBox_3.setChecked(False)
        self.lineEdit_6.setText("请在此输入表格名")
        self.dateEdit_7.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        self.dateEdit_9.setDate(datetime.datetime.now())  # 初始化时间为当前系统时间
        # 刷新显示tableWidget
        self.showZgTable()

    # 刷新显示问题查询页面
    def refreshProblemSearchTable(self):
        self.comboBox_27.clear()
        self.comboBox_27.addItems(["按出具审计报告时间", "按应上报整改报告时间", "按实际上报整改报告时间", "按问题金额", "按上报次序",
                                   "按已整改金额", "按追责问责人数", "按推动制度建设数目", "按认定整改金额", "按整改率"])
        self.comboBox_18.clear()
        self.comboBox_18.addItems(["由近及远排序", "由远及近排序"])
        self.listWidget_9.clear()
        self.listWidget_10.clear()
        self.comboBox_22.clear()
        self.comboBox_22.addItems(["选择查询类型", "对应发文号", "被审计领导干部", "所在地方单位", "审计报告文号", "审计组组长",
                                   "审计组主审", "问题描述", "问题一级分类", "问题二级分类", "问题三级分类",
                                   "问题四级分类", "问题金额", "移送及处理情况", "整改责任部门", "整改情况",
                                   "已整改金额", "追责问责人数", "推动制度建设数目", "推动制度建设文件", "认定整改情况",
                                   "认定整改金额", "整改率"])
        self.lineEdit_43.setText("请输入表格名")
        self.showProblemSearchTable()

    # 刷新显示批示统计
    def refreshRectificationTable(self):
        self.lineEdit_28.clear()
        self.comboBox_32.clear()
        self.comboBox_32.addItems(["办文编号", "报送载体", "报送标题", "来文字号", "来文标题", "来文单位", "批示载体", "批示人", "批示人职务"])
        self.showRectificationTable()

    """
    @公文录入操作函数
    @word文档录入操作函数
    """

    # 发文办理下的确认按钮(专报)
    def add_zb(self):
        input1 = self.lineEdit.text()  # 发文标题
        input2 = self.lineEdit_2.text()  # 报送范围
        input3 = "审计专报" + '〔' + self.spinBox_6.text() + '〕' + self.spinBox.text() + "号"  # 发文字号
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
                QtWidgets.QMessageBox.critical(None, "新建失败", "发文字号已经存在！")
            elif tools.judgeExistSameNameFile(tools.project_word_path, input16):
                QtWidgets.QMessageBox.critical(None, "新建失败", "存在相同的文件名！")
            else:
                # 导入文件
                tools.copyFile(input_file_path, tools.project_word_path)

                # 执行插入sendfile表
                sql = "insert into sendfile(发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核," \
                      "综合处分管厅领导,审计办主任,办文日期,报文内容,projectType,状态) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s','%s','%s','%s','%s','%s',1,'red')" % (
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

                QtWidgets.QMessageBox.information(None, "提示", "新建成功！")

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()

                # 录入完成后清空所有输入,时间重置,发文字号重置
                self.lineEdit.clear()  # 发文标题
                self.lineEdit_2.clear()  # 报送范围
                self.spinBox_6.setValue(datetime.datetime.now().year)  # 发文字号:年
                self.spinBox.setValue(1)  # 发文字号:编号
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
        else:
            QtWidgets.QMessageBox.critical(None, "新建失败", "发文标题不能为空！")

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
                QtWidgets.QMessageBox.critical(None, "新建失败", "发文字号已经存在！")
            elif tools.judgeExistSameNameFile(tools.project_word_path, input7):
                QtWidgets.QMessageBox.critical(None, "新建失败", "存在相同的文件名！")
            else:
                # 导入文件
                tools.copyFile(input_file_path, tools.project_word_path)

                # 执行插入sendfile表
                sql = "insert into sendfile(发文字号,发文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,办文日期,报文内容,紧急程度,秘密等级,是否公开,审核,承办处室," \
                      "承办人,联系电话,projectType,状态) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'%s','%s',2,'red')" % (
                          input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                          input12, input13, input14)
                tools.executeSql(sql)

                # 找到当前发文的序号
                sql = "select 序号 from sendfile where 发文字号 = '%s'" % input1
                data = tools.executeSql(sql)

                # 执行插入流程表
                # curr_time = datetime.datetime.now()
                # time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], input6)
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(None, "提示", "新建成功！")

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()

                # 录入完成后清空显示页面,发文字号重置
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
                self.lineEdit_19.setText("秘书处")  # 承办处室
                self.lineEdit_20.clear()  # 承办人
                self.lineEdit_21.clear()  # 联系电话
        else:
            QtWidgets.QMessageBox.critical(None, "新建失败", "发文标题不能为空！")

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
                QtWidgets.QMessageBox.critical(None, "新建失败", "收文字号已经存在！")
            else:
                # 执行插入收文表
                sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,处理结果,审核,收文字号,承办处室,承办人,联系电话,内容摘要和拟办意见," \
                      "领导批示,状态) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                      "'red')" % (input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                                  input11, input12, input13, input14, input15)
                tools.executeSql(sql)

                # 找到当前收文的序号
                sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
                data = tools.executeSql(sql)

                # 执行插入流程表
                # curr_time = datetime.datetime.now()
                # time_str = curr_time.strftime("%Y/%m/%d")
                sql = "insert into bwprocess(收文序号,是否加入整改,流程开始时间) VALUES(%s,'否','%s')" % (data[0][0], input1)
                tools.executeSql(sql)

                QtWidgets.QMessageBox.information(None, "提示", "录入成功！")

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()

                # 录入完成后清空显示页面
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
                self.lineEdit_34.setText("秘书处")  # 承办处室
                self.lineEdit_32.clear()  # 承办人
                self.lineEdit_39.clear()  # 联系电话
                self.textEdit_4.clear()  # 内容摘要和拟办意见
                self.textEdit_5.clear()  # 领导批示

        else:
            QtWidgets.QMessageBox.critical(None, "录入失败", "收文标题不能为空！")

    # 批文办理下的录入按钮
    def add_cor(self):
        input1 = self.dateEdit_14.text()  # 收文时间
        input2 = self.lineEdit_31.text()  # 密级
        input3 = self.comboBox_24.currentText()  # 是否公开
        input4 = self.comboBox_26.currentText()  # 紧急程度
        input5 = self.lineEdit_61.text()  # 批文标题
        input6 = self.comboBox_25.currentText() + '〔' + self.spinBox_8.text() + '〕' + self.spinBox_9.text() \
                 + '号'  # 批文编号
        input7 = self.lineEdit_29.text()  # 厅领导内容摘要和拟办意见
        input8 = self.textEdit_10.toPlainText()  # 领导批示
        input9 = self.lineEdit_58.text()  # 处理结果
        input10 = self.lineEdit_60.text()  # 审核
        input11 = self.lineEdit_62.text()  # 承办处室
        input12 = self.lineEdit_57.text()  # 承办人
        input13 = self.lineEdit_63.text()  # 联系电话

        if input5 != "":
            sql = "select 批文字号 from corfile where 批文字号 = '%s'" % input6
            data = tools.executeSql(sql)
            # 数据库中批文字号是否存在,不允许重复的批文字号输入
            if len(data) != 0:
                QtWidgets.QMessageBox.critical(None, "录入失败", "批文字号已经存在！")
            else:
                # 创建一个新的空的流程
                sql = "insert into bwprocess(流程开始时间, 是否加入整改) VALUES('%s','否')" % input1
                tools.executeSql(sql)

                # 找到新创建流程的序号,依据是发文,收文,批文都为空
                sql = "select bwprocess.序号 from bwprocess left outer join corfile on bwprocess.序号 = corfile.流程序号 " \
                      "where bwprocess.发文序号 IS NULL and bwprocess.收文序号 IS NULL and corfile.序号 is NULL"
                xh_lc = tools.executeSql(sql)[0][0]

                # 插入corfile表中
                sql = "insert into corfile(流程序号,收文时间,秘密等级,是否公开,紧急程度,批文标题,批文字号,内容摘要和拟办意见,领导批示,处理结果,审核,承办处室,承办人," \
                      "联系电话,状态) VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','red')" % (
                          xh_lc, input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                          input11, input12, input13)
                tools.executeSql(sql)

                # 获取批文序号
                sql = "select 序号 from corfile where 批文字号 = '%s'" % input6
                xh_cor = tools.executeSql(sql)[0][0]

                # 插入instruction中
                for index in range(self.listWidget_5.count()):
                    input14 = self.listWidget_5.item(index).text()  # 领导来文单位
                    input15 = self.listWidget_6.item(index).text()  # 领导来文字号
                    input16 = self.listWidget_4.item(index).text()  # 领导内容摘要和领导批示
                    sql = "insert into instruction(批文序号,领导来文单位,领导来文字号,领导内容摘要和领导批示) VALUES(%s,'%s','%s','%s')" % (
                        xh_cor, input14, input15, input16)
                    tools.executeSql(sql)

                QtWidgets.QMessageBox.information(None, "提示", "录入成功！")

                # 返回显示页面,重新加载流程内容
                self.stackedWidget.setCurrentIndex(0)
                self.showBwprocessTable()

                # 录入完成后清空显示页面
                self.dateEdit_14.setDate(datetime.datetime.now())  # 批文时间
                self.lineEdit_31.clear()  # 密级
                self.comboBox_24.setCurrentIndex(0)  # 是否公开
                self.comboBox_26.setCurrentIndex(0)  # 紧急程度
                self.lineEdit_61.clear()  # 批文标题
                self.comboBox_25.setCurrentIndex(0)  # 批文编号:[批文类型]
                self.spinBox_8.setValue(datetime.datetime.now().year)  # 批文编号:[年]
                self.spinBox_9.setValue(1)  # 批文编号:[编号]
                self.lineEdit_29.clear()  # 厅领导内容摘要和拟办意见
                self.textEdit_10.clear()  # 领导批示
                self.lineEdit_58.clear()  # 处理结果
                self.lineEdit_60.clear()  # 审核
                self.lineEdit_62.setText("秘书处")  # 承办处室
                self.lineEdit_57.clear()  # 承办人
                self.lineEdit_63.clear()  # 联系电话

                self.listWidget_5.clear()  # 领导来文单位
                self.listWidget_6.clear()  # 领导来文字号
                self.listWidget_4.clear()  # 领导内容摘要和领导批示
        else:
            QtWidgets.QMessageBox.critical(None, "录入失败", "批文标题不能为空！")

    # 导入审计意见或问题表
    def add_sjyj(self):
        input_file_path_sjyj = self.lineEdit_file_sjyj.text()
        input_file_path_excel = self.lineEdit_file_excel.text()
        keyword = self.comboBox_sjyj.currentText() + '〔' + self.spinBox_sjyj_year.text() + '〕' + self.spinBox_sjyj_num.text() \
                  + '号'  # 审计意见文号
        if input_file_path_sjyj == "" and input_file_path_excel == "":
            QtWidgets.QMessageBox.information(None, "提示", "请选择文件！")
        else:
            if input_file_path_sjyj != "":
                filename = tools.getFileName(input_file_path_sjyj)  # 审计意见文件名
                if tools.judgeExistSameNameFile(tools.sjyj_word_path, filename):
                    QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计意见文件名！")
                else:
                    sql = "select * from sjyjword where 审计意见文号 = '%s'" % keyword
                    data = tools.executeSql(sql)
                    if len(data) != 0:
                        QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计意见文号！")
                    else:
                        sql = "insert into sjyjword values(NULL,'%s','%s')" % (keyword, filename)
                        tools.executeSql(sql)

                        # 导入文件
                        tools.copyFile(input_file_path_sjyj, tools.sjyj_word_path)

                        QtWidgets.QMessageBox.information(None, "提示", "审计意见导入成功！")

                        # 清空文件名输入栏
                        self.lineEdit_file_sjyj.clear()

            if input_file_path_excel != "":
                # 导入问题分表
                self.importExcelProblemJz(input_file_path_excel, keyword, "")

    # 导入审计报告和审计结果或问题表
    def add_sjbg(self):
        input_file_path_sjbg = self.lineEdit_file_sjbg.text()
        input_file_path_sjjg = self.lineEdit_file_sjjg.text()
        input_file_path_excel = self.lineEdit_file_excel_2.text()
        keyword_sjbg = self.comboBox_sjbg.currentText() + '〔' + self.spinBox_sjbg_year.text() + '〕' \
                       + self.spinBox_sjbg_num.text() + '号'  # 审计报告文号
        keyword_sjjg = self.comboBox_sjjg.currentText() + '〔' + self.spinBox_sjjg_year.text() + '〕' \
                       + self.spinBox_sjjg_num.text() + '号'  # 审计结果文号
        if input_file_path_sjbg == "" and input_file_path_sjjg == "" and input_file_path_excel == "":
            QtWidgets.QMessageBox.information(None, "提示", "请选择文件！")
        else:
            if input_file_path_sjbg != "" and input_file_path_sjjg != "":
                filename1 = tools.getFileName(input_file_path_sjbg)  # 审计报告文件名
                filename2 = tools.getFileName(input_file_path_sjjg)  # 经责审计结果报告文件名
                if tools.judgeExistSameNameFile(tools.sjbg_word_path, filename1):
                    QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计报告文件名！")
                elif tools.judgeExistSameNameFile(tools.sjjg_word_path, filename2):
                    QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计结果报告文件名！")
                else:
                    sql = "select * from sjbgword where 审计报告文号 = '%s'" % keyword_sjbg
                    data1 = tools.executeSql(sql)
                    sql = "select * from sjbgword where 审计结果文号 = '%s'" % keyword_sjjg
                    data2 = tools.executeSql(sql)
                    if len(data1) != 0:
                        QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计报告文号！")
                    elif len(data2) != 0:
                        QtWidgets.QMessageBox.critical(None, "Word导入失败", "存在相同的审计结果报告文号！")
                    else:
                        sql = "insert into sjbgword values(NULL,'%s','%s','%s','%s')" % (
                            keyword_sjbg, filename1, keyword_sjjg, filename2)
                        tools.executeSql(sql)

                        # 导入文件
                        tools.copyFile(input_file_path_sjbg, tools.sjbg_word_path)
                        tools.copyFile(input_file_path_sjjg, tools.sjjg_word_path)

                        QtWidgets.QMessageBox.information(None, "提示", "审计报告和结果导入成功！")

                        # 清空文件名输入栏
                        self.lineEdit_file_sjbg.clear()
                        self.lineEdit_file_sjjg.clear()

            elif input_file_path_sjbg != "" or input_file_path_sjjg != "":
                QtWidgets.QMessageBox.critical(None, "word导入失败", "审计报告和审计结果报告必须同时录入！")

            if input_file_path_excel != "":
                self.importExcelProblemJz(input_file_path_excel, keyword_sjbg, keyword_sjjg)

    """
    @tableWidget表格统一搜索检索排序功能栏
    @表格搜索功能函数
    @表格筛选功能函数
    @表格排序功能函数
    """

    # 办文流程搜索按钮
    def searchForLc(self):
        if self.lineEdit_global.text() == "":
            QtWidgets.QMessageBox.warning(None, "提示", "输入不可为空！")
            return
        dic = {
            "发文标题": "sendfile.发文标题",
            '发文号': 'sendfile.发文字号',
            '收文标题': 'revfile.收文标题',
            '收文号': 'revfile.收文字号',
            '批文标题': "corfile.批文标题",
            '批文号': "corfile.批文字号"
        }
        nowText = '%' + self.lineEdit_global.text() + '%'
        sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号)," \
              "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n'),REPLACE(GROUP_CONCAT(" \
              "distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改 FROM bwprocess LEFT OUTER JOIN sendfile ON " \
              "sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = problem.发文序号 LEFT OUTER JOIN " \
              "revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile ON bwprocess.序号 = corfile.流程序号  WHERE " \
              "%s LIKE '%s' GROUP BY bwprocess.序号 " % (dic.get(self.comboBox_21.currentText()), nowText)
        # 打印显示
        data = tools.executeSql(sql)
        size = len(data)
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

        self.sortForLc()

    # 经责问题表中的搜索按钮
    def searchForJzProblem(self):
        keyword = self.comboBox_11.currentText()
        sql = "select 序号,问题顺序号,被审计领导干部,所在地方或单位,报送文号,审计意见或报告文号,经责结果报告文号,出具审计报告时间,审计组组长,审计组主审,问题描述,是否在审计报告中反映," \
              "是否在结果报告中反映,审计对象分类,问题类别,问题定性,问题表现形式,备注,问题金额,移送及处理情况 from problem_jz where 审计意见或报告文号 = '%s' " % keyword
        data = tools.executeSql(sql)

        data = tools.sortByKey(data, 5, 2)

        size = len(data)
        self.tableWidget_jz_pro.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_jz_pro.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_jz_pro.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

    # 整改流程搜索按钮
    def searchForZg(self):
        if self.lineEdit_global_2.text() == "":
            QtWidgets.QMessageBox.warning(None, "提示", "输入不可为空！")
            return
        nowText = '%' + self.lineEdit_global_2.text() + '%'
        if self.comboBox_28.currentText() == "普通流程":
            dic = {
                "发文编号": 'sendfile.发文字号',
                '发文标题': 'sendfile.发文标题',
                '收文标题': 'revfile.收文标题',
                '收文编号': 'revfile.收文字号',
                '批文标题': "corfile.批文标题",
                '批文编号': "corfile.批文字号",
                '整改状态': 'zgprocess.整改状态'
            }
            sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
                  "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess join " \
                  "bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 left outer " \
                  "join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = corfile.流程序号 WHERE %s " \
                  "LIKE '%s' GROUP BY zgprocess.序号" % (dic.get(self.comboBox_23.currentText()), nowText)
            data = tools.executeSql(sql)
        else:
            dic = {
                '整改状态': 'zgprocess.整改状态'
            }
            # sql由整改表的流程序号出发,通过多表查询获得经责项目类型整改的所有字段
            sql = "select zgprocess.序号,problem_jz.出具审计报告时间,problem_jz.审计意见或报告文号,zgprocess.整改状态 from zgprocess join " \
                  "problem_jz on zgprocess.序号 = problem_jz.整改序号 WHERE %s LIKE '%s' group by zgprocess.序号 " % (
                      dic.get(self.comboBox_23.currentText()), nowText)
            temp_data = tools.executeSql(sql)
            data = []
            # 对temp_data2进行数据处理,使得data1和data2可以合并
            for i in temp_data:
                temp_tuple = (i[0], i[1], i[2], None, None, None, None, None, i[3])
                data.append(temp_tuple)

        size = len(data)  # 行数
        self.tableWidget_zgzl.setRowCount(size)
        # 打印显示
        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.sortForZg()

    # 问题表分析搜索按钮
    def searchForProblem(self):
        condition_dict = {
            "对应发文号": "sendfile.发文字号",
            "被审计领导干部": "problem.被审计领导干部",
            "所在地方单位": "problem.所在地方或单位",
            "审计报告文号": "problem.审计报告文号",
            "审计组组长": "problem.审计组组长",
            "审计组主审": "problem.审计组主审",
            "问题描述": "problem.问题描述",
            "问题一级分类": "problem.问题一级分类",
            "问题二级分类": "problem.问题二级分类",
            "问题三级分类": "problem.问题三级分类",
            "问题四级分类": "problem.问题四级分类",
            "问题金额": "problem.问题金额",
            "移送及处理情况": "problem.移送及处理情况",
            "整改责任部门": "rectification.整改责任部门",
            "整改情况": "rectification.整改情况",
            "已整改金额": "rectification.已整改金额",
            "追责问责人数": "rectification.追责问责人数",
            "推动制度建设数目": "rectification.推动制度建设数目",
            "推动制度建设文件": "rectification.推动制度建设文件",
            "认定整改情况": "rectification.认定整改情况",
            "认定整改金额": "rectification.认定整改金额",
            "整改率": "rectification.整改率"
        }
        numeric_condition_dict = {
            "问题金额": "problem.问题金额",
            "已整改金额": "rectification.已整改金额",
            "追责问责人数": "rectification.追责问责人数",
            "推动制度建设数目": "rectification.推动制度建设数目",
            "认定整改金额": "rectification.认定整改金额",
            "整改率": "rectification.整改率"
        }

        sql = "SELECT sendfile.发文字号,problem.被审计领导干部,problem.所在地方或单位,problem.审计报告文号,problem.出具审计报告时间," \
              "problem.审计组组长,problem.审计组主审,problem.问题描述,problem.问题一级分类,problem.问题二级分类,problem.问题三级分类," \
              "problem.问题四级分类,problem.备注,problem.问题金额,problem.移送及处理情况,rectification.上报次序,rectification." \
              "整改责任部门,rectification.应上报整改报告时间,rectification.实际上报整改报告时间,rectification.整改情况,rectification." \
              "已整改金额,rectification.追责问责人数,rectification.推动制度建设数目,rectification.推动制度建设文件,rectification." \
              "部分整改情况具体描述,rectification.未整改原因说明,rectification.下一步整改措施及时限,rectification.认定整改情况," \
              "rectification.认定整改金额,rectification.整改率 FROM problem LEFT OUTER JOIN rectification ON rectification." \
              "问题序号 = problem.序号 LEFT OUTER JOIN sendfile ON sendfile.序号 = problem.发文序号"

        rowCount = self.listWidget_9.count()

        # 形成多维查询sql语句
        for i in range(rowCount):
            if i == 0:
                sql = sql + " where"
            else:
                sql = sql + " and"
            key = self.listWidget_9.item(i).text()
            value = condition_dict.get(key)
            if key in numeric_condition_dict.keys():
                # 数值查询
                item = self.listWidget_10.item(i)  # 获取条目对象
                item_object = self.listWidget_10.itemWidget(item)  # 根据条目获取窗口对象
                lineEdit = item_object.findChildren(QtWidgets.QLineEdit)  # 获取窗口对象包含的所有lineEdit
                second_condition_before = lineEdit[0].text()
                second_condition_behind = lineEdit[1].text()
                if(second_condition_before == "请输入数额" or second_condition_before == ""):
                    second_condition_before = 0
                if (second_condition_behind == "请输入数额" or second_condition_behind == ""):
                    second_condition_behind = sys.maxsize
                add_condition = " %s between '%s' and '%s'" % (value, second_condition_before, second_condition_behind)
            else:
                # 文字查询
                second_condition = '%' + self.listWidget_10.item(i).text() + '%'
                add_condition = " %s like '%s'" % (value, second_condition)
            sql = sql + add_condition

        # 打印结果
        data = tools.executeSql(sql)
        size = len(data)
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

        self.sortForProblem()

    # 领导批示统计分析按钮
    def searchForRectification(self):
        dic = {
            "办文编号": "corfile.批文字号",
            '报送载体': 'sendfile.发文字号',
            '报送标题': 'sendfile.发文字号',
            '来文字号': 'instruction.领导来文字号',
            '来文标题': "corfile.批文标题",
            '来文单位': "instruction.领导来文单位",
            '批示载体': "revfile.收文字号",
            '批示人': "instruction.领导姓名",
            '批示人职务': "instruction.领导职务"
        }
        nowText = '%' + self.lineEdit_28.text() + '%'
        sql = "select instruction.序号,corfile.批文字号,corfile.秘密等级,sendfile.发文字号,sendfile.发文标题," \
              "instruction.领导来文字号,corfile.批文标题,instruction.领导来文单位,revfile.收文字号,instruction.领导姓名," \
              "instruction.领导职务,instruction.批示时间,instruction.领导内容摘要和领导批示 from instruction left outer join " \
              "corfile on instruction.批文序号 = corfile.序号 left outer join bwprocess on bwprocess.序号 = " \
              "corfile.流程序号 left outer join sendfile on bwprocess.发文序号 = sendfile.序号 left outer join revfile " \
              "on bwprocess.收文序号 = revfile.序号 WHERE %s LIKE '%s'" % (dic.get(self.comboBox_32.currentText()), nowText)
        data = tools.executeSql(sql)
        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_2.setRowCount(size)

        x = 0
        for i in data:
            for y in range(0, 13):
                if data[x][y] is None:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
            x = x + 1

    # 办文流程排序功能
    def sortForLc(self):
        now = self.comboBox_12.currentText()
        if now == "按流程开始时间由近及远排序":
            self.tableWidget_lczl.sortItems(1, Qt.DescendingOrder)  # 按照流程建立时间由近及远排序
        elif now == "按流程开始时间由远及近排序":
            self.tableWidget_lczl.sortItems(1, Qt.AscendingOrder)  # 按照流程建立时间由近及远排序
        else:
            self.tableWidget_lczl.sortItems(4, Qt.AscendingOrder)  # 按照问题个数排序

    # 整改流程排序功能
    def sortForZg(self):
        now = self.comboBox_15.currentText()
        if now == "按流程开始时间由近及远排序":
            self.tableWidget_zgzl.sortItems(1, Qt.DescendingOrder)  # 按照流程建立时间由近及远排序
        elif now == "按流程开始时间由远及近排序":
            self.tableWidget_zgzl.sortItems(1, Qt.AscendingOrder)  # 按照流程建立时间由近及远排序

    # 问题表分析排序功能
    def sortForProblem(self):
        sort_type = self.comboBox_27.currentText()
        sort_style = self.comboBox_18.currentText()
        if sort_type == "按出具审计报告时间":
            if sort_style == "由近及远排序":
                self.tableWidget.sortItems(5, Qt.DescendingOrder)
            elif sort_style == "由远及近排序":
                self.tableWidget.sortItems(5, Qt.AscendingOrder)
        elif sort_type == "按应上报整改报告时间":
            if sort_style == "由近及远排序":
                self.tableWidget.sortItems(18, Qt.DescendingOrder)
            elif sort_style == "由远及近排序":
                self.tableWidget.sortItems(18, Qt.AscendingOrder)
        elif sort_type == "按实际报整改报告时间":
            if sort_style == "由近及远排序":
                self.tableWidget.sortItems(19, Qt.DescendingOrder)
            elif sort_style == "由远及近排序":
                self.tableWidget.sortItems(19, Qt.AscendingOrder)
        elif sort_type == "按问题金额":
            if sort_style == "由多到少排序":
                self.tableWidget.sortItems(14, Qt.DescendingOrder)
            elif sort_style == "由少到多排序":
                self.tableWidget.sortItems(14, Qt.AscendingOrder)
        elif sort_type == "按上报次序":
            if sort_style == "由大到小排序":
                self.tableWidget.sortItems(16, Qt.DescendingOrder)
            elif sort_style == "由小到大排序":
                self.tableWidget.sortItems(16, Qt.AscendingOrder)
        elif sort_type == "按已整改金额":
            if sort_style == "由多到少排序":
                self.tableWidget.sortItems(21, Qt.DescendingOrder)
            elif sort_style == "由少到多排序":
                self.tableWidget.sortItems(21, Qt.AscendingOrder)
        elif sort_type == "按追责问责人数":
            if sort_style == "由多到少排序":
                self.tableWidget.sortItems(22, Qt.DescendingOrder)
            elif sort_style == "由少到多排序":
                self.tableWidget.sortItems(22, Qt.AscendingOrder)
        elif sort_type == "按推动制度建设数目":
            if sort_style == "由多到少排序":
                self.tableWidget.sortItems(23, Qt.DescendingOrder)
            elif sort_style == "由少到多排序":
                self.tableWidget.sortItems(23, Qt.AscendingOrder)
        elif sort_type == "按认定整改金额":
            if sort_style == "由多到少排序":
                self.tableWidget.sortItems(29, Qt.DescendingOrder)
            elif sort_style == "由少到多排序":
                self.tableWidget.sortItems(29, Qt.AscendingOrder)
        elif sort_type == "按整改率":
            if sort_style == "由高至低排序":
                self.tableWidget.sortItems(0, Qt.DescendingOrder)
            elif sort_style == "由低至高排序":
                self.tableWidget.sortItems(0, Qt.AscendingOrder)

    # 办文流程按照条件筛选
    def selectForLc(self):
        firstNeed = self.comboBox_13.currentText()  # 第一个条件
        secondNeed = '%' + self.comboBox_14.currentText() + '%'  # 第二个条件
        condition_dict = {"发文类型": "sendfile.发文字号", "收文类型": "revfile.收文字号", "是否加入整改": "bwprocess.是否加入整改"}
        if self.checkBox.property("checked"):  # 当设置时间时
            frontTime = self.dateEdit_8.text()
            behindTime = self.dateEdit_10.text()
            if firstNeed == "不限制":
                sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号)," \
                      "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n')," \
                      "REPLACE(GROUP_CONCAT(distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改 FROM bwprocess LEFT " \
                      "OUTER JOIN sendfile ON sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = " \
                      "problem.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile " \
                      "ON bwprocess.序号 = corfile.流程序号 WHERE  bwprocess.流程开始时间 BETWEEN '%s' AND '%s' GROUP BY " \
                      "bwprocess.序号 " % (frontTime, behindTime)
            else:
                sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号)," \
                      "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n')," \
                      "REPLACE(GROUP_CONCAT(distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改 FROM bwprocess LEFT " \
                      "OUTER JOIN sendfile ON sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = " \
                      "problem.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile " \
                      "ON bwprocess.序号 = corfile.流程序号 WHERE %s LIKE '%s' and bwprocess.流程开始时间 BETWEEN '%s' AND '%s' " \
                      "GROUP BY bwprocess.序号 " % (condition_dict.get(firstNeed), secondNeed, frontTime, behindTime)

        else:  # 当未设置时间
            if firstNeed == "不限制":
                sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号)," \
                      "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n')," \
                      "REPLACE(GROUP_CONCAT(distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改 FROM bwprocess LEFT " \
                      "OUTER JOIN sendfile ON sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = " \
                      "problem.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile " \
                      "ON bwprocess.序号 = corfile.流程序号 GROUP BY bwprocess.序号 "
            else:
                sql = "SELECT bwprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,count(distinct problem.序号), " \
                      "revfile.收文字号,revfile.收文标题,REPLACE(GROUP_CONCAT(distinct corfile.批文字号),',','\n')," \
                      "REPLACE(GROUP_CONCAT(distinct corfile.批文标题),',','\n'),bwprocess.是否加入整改  FROM bwprocess LEFT " \
                      "OUTER JOIN sendfile ON sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN problem ON sendfile.序号 = " \
                      "problem.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN corfile " \
                      "ON bwprocess.序号 = corfile.流程序号 WHERE %s LIKE '%s' GROUP BY bwprocess.序号 " % \
                      (condition_dict.get(firstNeed), secondNeed)
        # 打印显示
        data = tools.executeSql(sql)
        size = len(data)
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

        self.sortForLc()

    # 整改流程按照条件筛选
    def selectForZg(self):
        firstNeed = self.comboBox_16.currentText()  # 第一个条件
        secondNeed = '%' + self.comboBox_17.currentText() + '%'  # 第二个条件
        condition_dict = {"发文类型": "sendfile.发文字号", "收文类型": "revfile.收文字号", "整改状态": "zgprocess.整改状态"}
        if self.checkBox_3.property("checked"):  # 当设置时间时
            frontTime = self.dateEdit_7.text()
            behindTime = self.dateEdit_9.text()
            if firstNeed == "不限制":
                sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
                      "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess " \
                      "join bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 " \
                      "left outer join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = " \
                      "corfile.流程序号 WHERE bwprocess.流程开始时间 BETWEEN '%s' AND '%s' GROUP BY zgprocess.序号 " % (frontTime,
                                                                                                            behindTime)
            else:
                sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
                      "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess " \
                      "join bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 " \
                      "left outer join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = " \
                      "corfile.流程序号 WHERE %s LIKE '%s' and bwprocess.流程开始时间 BETWEEN '%s' AND '%s' GROUP BY " \
                      "zgprocess.序号 " % (condition_dict.get(firstNeed), secondNeed, frontTime, behindTime)
        else:  # 当未设置时间
            if firstNeed == "不限制":
                sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
                      "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess " \
                      "join bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 " \
                      "left outer join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = " \
                      "corfile.流程序号 GROUP BY zgprocess.序号 "
            else:
                sql = "select zgprocess.序号,bwprocess.流程开始时间,sendfile.发文字号,sendfile.发文标题,revfile.收文字号,revfile.收文标题," \
                      "GROUP_CONCAT(corfile.批文字号,'\n'),GROUP_CONCAT(corfile.批文标题,'\n'),zgprocess.整改状态 from zgprocess " \
                      "join bwprocess on zgprocess.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 " \
                      "left outer join revfile on bwprocess.收文序号 = revfile.序号 join corfile on bwprocess.序号 = " \
                      "corfile.流程序号 WHERE %s LIKE '%s' GROUP BY zgprocess.序号 " % (condition_dict.get(firstNeed),
                                                                                  secondNeed)
        # 打印显示
        data = tools.executeSql(sql)
        size = len(data)
        self.tableWidget_zgzl.setRowCount(size)
        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_zgzl.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.sortForZg()

    """
    @excel操作
    input&output
    """

    # 根据excel中的左边问题基本信息导入经责问题表
    # @param path 文件路径
    # @param keyword 审计意见(报告)文号
    # @param keyword2 审计结果报告
    def importExcelProblemJz(self, path, keyword, keyword2):
        # 文件路径
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

                check_tag = 1  # excel输入合法检测标识,如果为1表示excel中所有数据合法,可以写入数据库

                # 检测excel某些输入是否合法
                for i in range(4, sheet_rows):
                    # 问题顺序号,判断是否为整数
                    if not tools.judgeInteger(sheet.row(i)[0].value):
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：问题顺序号应为整数！" % str(i + 1))
                        break
                    # 导入的是问题分表(对应审计意见)时,检测审计意见(报告)文号,判断是否与当前keyword一致(强约束)
                    if keyword != "multiple" and keyword2 == "":
                        if sheet.row(i)[4].value != keyword:
                            check_tag = 0
                            QtWidgets.QMessageBox.information(None, "提示",
                                                              "excel表格第%s行：审计意见(报告)文号与输入文号不一致！" % str(i + 1))
                            break
                    # 导入的是问题分表(对应审计报告)时,检测审计意见(报告)文号,检测审计结果报告文号,判断是否与当前keyword,keyword2一致(强约束)
                    elif keyword != "multiple" and keyword2 != "":
                        if sheet.row(i)[4].value != keyword:
                            check_tag = 0
                            QtWidgets.QMessageBox.information(None, "提示",
                                                              "excel表格第%s行：审计意见(报告)文号与输入文号不一致！" % str(i + 1))
                            break
                        if sheet.row(i)[5].value != keyword2:
                            check_tag = 0
                            QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：审计结果报告文号与输入文号不一致！" % str(i + 1))
                            break
                    # 导入的是问题总表时,检测审计意见(报告)文号,判断是否为空(弱约束,以后可以考虑用文号的格式进行正则匹配约束输入)
                    elif keyword == "multiple" and keyword2 == "multiple":
                        if sheet.row(i)[4].value == "":
                            check_tag = 0
                            QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：审计意见(报告)文号为空！" % str(i + 1))
                            break
                    # 出具审计专报时间,判断是否为合法时间,可以为空
                    if isinstance(sheet.row(i)[6].value, str) and sheet.row(i)[6].value != "":
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：出具审计专报时间格式错误！" % str(i + 1))
                        break
                    # 问题金额,判断是否为浮点数,可以为空
                    if not isinstance(sheet.row(i)[17].value, float) and sheet.row(i)[17].value != "":
                        check_tag = 0
                        QtWidgets.QMessageBox.information(None, "提示", "excel表格第%s行：问题金额应为数字！" % str(i + 1))
                        break
                if sheet_rows == 4:
                    check_tag = 0
                    QtWidgets.QMessageBox.information(None, "提示", "表格数据为空！")

                # 写入经责问题表数据库
                if check_tag == 1:
                    # 表示导入的是问题分表,表中所有问题对应同一个审计意见(报告)文号,导入问题的同时还要对该文号对应的单个项目设置整改
                    if keyword != "multiple":
                        # 首先创建一个整改流程
                        sql = "insert into zgprocess(序号,流程序号,标识文号,整改状态) values(NULL,-1,'%s','未整改')" % keyword
                        tools.executeSql(sql)

                        # 其次用标识文号查出刚刚创建的整改流程主键
                        sql = "select 序号 from zgprocess where 标识文号 = '%s'" % keyword
                        xh_zg = tools.executeSql(sql)[0][0]

                        # 最后写入经责问题表数据库,将xh_zg作为经责问题表的外键,从而建立关联
                        for i in range(4, sheet_rows):
                            cell_i_0 = int(sheet.row(i)[0].value)  # 问题顺序号
                            cell_i_1 = sheet.row(i)[1].value  # 被审计领导干部
                            cell_i_2 = sheet.row(i)[2].value  # 所在地方或单位
                            cell_i_3 = sheet.row(i)[3].value  # 报送专报期号,直接读取excel中的输入
                            cell_i_4 = sheet.row(i)[4].value  # 审计报告（意见）文号
                            cell_i_5 = sheet.row(i)[5].value  # 经责结果报告文号
                            if sheet.cell(i, 6).value != "":
                                cell_i_6 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 6).value, 0).strftime(
                                    "%Y/%m/%d")  # 出具审计专报时间 Year/Month/Day
                            else:
                                cell_i_6 = ""
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

                            sql = "insert into problem_jz values(NULL,%s, %s,'%s','%s','%s','%s','%s','%s','%s','%s'," \
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                      xh_zg, cell_i_0, cell_i_1, cell_i_2, cell_i_3, cell_i_4, cell_i_5, cell_i_6,
                                      cell_i_7, cell_i_8, cell_i_9, cell_i_10, cell_i_11, cell_i_12, cell_i_13,
                                      cell_i_14, cell_i_15, cell_i_16, cell_i_17, cell_i_18)
                            tools.executeSql(sql)

                    # 表示导入的是问题总表,表中所有问题对应不同的审计意见(报告)文号,导入问题的同时还要对多文号对应的多个项目设置整改
                    elif keyword == "multiple":
                        # 首先从excel中解析出所有文号,放入keywords中存储
                        keywords = set()
                        for i in range(4, sheet_rows):
                            keywords.add(sheet.row(i)[4].value)  # 审计报告（意见）文号

                        # 其次对于keywords中的每一个文号,都要建立一个整改流程
                        for i in keywords:
                            sql = "insert into zgprocess(序号,流程序号,标识文号,整改状态) values(NULL,-1,'%s','未整改')" % i
                            tools.executeSql(sql)

                        # 最后写入经责问题表数据库,将xh_zg作为经责问题表的外键,从而建立关联
                        for i in range(4, sheet_rows):
                            cell_i_0 = int(sheet.row(i)[0].value)  # 问题顺序号
                            cell_i_1 = sheet.row(i)[1].value  # 被审计领导干部
                            cell_i_2 = sheet.row(i)[2].value  # 所在地方或单位
                            cell_i_3 = sheet.row(i)[3].value  # 报送专报期号,直接读取excel中的输入
                            cell_i_4 = sheet.row(i)[4].value  # 审计报告（意见）文号
                            cell_i_5 = sheet.row(i)[5].value  # 经责结果报告文号
                            if sheet.cell(i, 6).value != "":
                                cell_i_6 = xlrd.xldate.xldate_as_datetime(sheet.cell(i, 6).value, 0).strftime(
                                    "%Y/%m/%d")  # 出具审计专报时间 Year/Month/Day
                            else:
                                cell_i_6 = ""
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

                            # 用该问题的文号找出整改序号
                            sql = "select 序号 from zgprocess where 标识文号 = '%s'" % cell_i_4
                            xh_zg = tools.executeSql(sql)[0][0]

                            sql = "insert into problem_jz values(NULL,%s, %s,'%s','%s','%s','%s','%s','%s','%s','%s'," \
                                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                      xh_zg, cell_i_0, cell_i_1, cell_i_2, cell_i_3, cell_i_4, cell_i_5, cell_i_6,
                                      cell_i_7, cell_i_8, cell_i_9, cell_i_10, cell_i_11, cell_i_12, cell_i_13,
                                      cell_i_14, cell_i_15, cell_i_16, cell_i_17, cell_i_18)
                            tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(None, "提示", "问题表导入完成！")

                    # 导入完成后更新经责表录入界面
                    self.displayProblemJzPage()
                else:
                    QtWidgets.QMessageBox.critical(None, "错误", "问题表导入失败！")

                # 清空输入栏
                if keyword != "multiple" and keyword2 == "":
                    self.lineEdit_file_excel.clear()
                elif keyword != "multiple" and keyword2 != "":
                    self.lineEdit_file_excel_2.clear()
                elif keyword == "multiple" and keyword2 == "multiple":
                    self.lineEdit_que_jz.clear()

            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())
        else:
            QtWidgets.QMessageBox.information(None, "提示", "请选择文件！")

    # 导出Excel表格
    def lcExcelOutput(self):
        nowText = self.lineEdit_4.text()
        if nowText == "":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入表格名")
        # 当没有输入表格名时提示并选中
        elif nowText == "请在此输入表格名":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入表格名")
            self.lineEdit_4.selectAll()
            self.lineEdit_4.setFocus()
        else:
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

            work_book = xlwt.Workbook(encoding='utf-8')
            sheet = work_book.add_sheet(nowText, cell_overwrite_ok=True)

            # 设置单元格宽度
            time = sheet.col(0)  # 流程开始时间
            time.width = 256 * 13
            send_number = sheet.col(1)  # 发文号
            send_number.width = 256 * 30
            send_name = sheet.col(2)  # 发文标题
            send_name.width = 256 * 100
            q_number = sheet.col(3)  # 问题个数
            q_number.width = 256 * 10
            receive_number = sheet.col(4)  # 收文号
            receive_number.width = 256 * 30
            receive_name = sheet.col(5)  # 收文标题
            receive_name.width = 256 * 100
            instruction_number = sheet.col(6)  # 批文号
            instruction_number.width = 256 * 30
            instruction_name = sheet.col(7)  # 批文标题
            instruction_name.width = 256 * 100
            if_change = sheet.col(8)  # 是否设置整改
            if_change.width = 256 * 13

            # 设置输出内容单元格高度
            out_high_style = xlwt.easyxf('font:height 300')

            # 设置列名,从流程开始时间这一列开始,序号不用显示
            sheet.write(0, 0, '流程开始时间', style_head)
            sheet.write(0, 1, '发文号', style_head)
            sheet.write(0, 2, '发文标题', style_head)
            sheet.write(0, 3, '问题个数', style_head)
            sheet.write(0, 4, '收文号', style_head)
            sheet.write(0, 5, '收文标题', style_head)
            sheet.write(0, 6, '批文号', style_head)
            sheet.write(0, 7, '批文标题', style_head)
            sheet.write(0, 8, '是否设置整改', style_head)

            rows = self.tableWidget_lczl.rowCount()
            for i in range(rows):
                # 因为是边读边写，所以每次写完后，要把上次存储的数据清空，存储下一行读取的数据
                mainList = []
                # tableWidget一共有9列,去掉序号列
                for j in range(0, 9):
                    mainList.append(self.tableWidget_lczl.item(i, j + 1).text())  # 添加到数组
                    # 把mainList中的数据写入表格
                    sheet.write(i + 1, j, mainList[j], style)
                    # 设置当前列的高度
                    sheet.row(i + 1).set_style(out_high_style)
            # 设置表头单元格高度
            head_high_style = xlwt.easyxf('font:height 400')
            sheet.row(0).set_style(head_high_style)
            # 保存
            try:
                work_book.save('/home/user/桌面/' + nowText + '.xls')
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())
            else:
                QtWidgets.QMessageBox.information(None, "提示", "导出成功")

    # 将办文表导出至Excel
    def bwExcelOutput(self):
        print(2)

    def zgExcelOutput(self):
        nowText = self.lineEdit_6.text()
        if nowText == "":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入表格名")
        # 当没有输入表格名时提示并选中
        elif nowText == "请在此输入表格名":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入表格名")
            self.lineEdit_6.selectAll()
            self.lineEdit_6.setFocus()
        else:
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

            work_book = xlwt.Workbook(encoding='utf-8')
            sheet = work_book.add_sheet(nowText, cell_overwrite_ok=True)

            # 设置单元格宽度
            time = sheet.col(0)  # 流程开始时间
            time.width = 256 * 13
            send_number = sheet.col(1)  # 发文号
            send_number.width = 256 * 30
            send_name = sheet.col(2)  # 发文标题
            send_name.width = 256 * 100
            receive_number = sheet.col(3)  # 收文号
            receive_number.width = 256 * 30
            receive_name = sheet.col(4)  # 收文标题
            receive_name.width = 256 * 100
            instruction_number = sheet.col(5)  # 批文号
            instruction_number.width = 256 * 30
            instruction_name = sheet.col(6)  # 批文标题
            instruction_name.width = 256 * 100
            if_change = sheet.col(7)  # 是否设置整改
            if_change.width = 256 * 13

            # 设置输出内容单元格高度
            out_high_style = xlwt.easyxf('font:height 300')

            # 设置列名,从流程开始时间这一列开始,序号不用显示
            sheet.write(0, 0, '流程开始时间', style_head)
            sheet.write(0, 1, '发文号', style_head)
            sheet.write(0, 2, '发文标题', style_head)
            sheet.write(0, 3, '收文号', style_head)
            sheet.write(0, 4, '收文标题', style_head)
            sheet.write(0, 5, '批文号', style_head)
            sheet.write(0, 6, '批文标题', style_head)
            sheet.write(0, 7, '是否完成整改', style_head)
            rows = self.tableWidget_zgzl.rowCount()
            for i in range(rows):
                # 因为是边读边写，所以每次写完后，要把上次存储的数据清空，存储下一行读取的数据
                mainList = []
                # tableWidget一共有8列,去掉序号列
                for j in range(0, 8):
                    mainList.append(self.tableWidget_zgzl.item(i, j + 1).text())  # 添加到数组
                    # 把mainList中的数据写入表格
                    sheet.write(i + 1, j, mainList[j], style)
                    # 设置当前列的高度
                    sheet.row(i + 1).set_style(out_high_style)
            # 设置表头单元格高度
            head_high_style = xlwt.easyxf('font:height 400')
            sheet.row(0).set_style(head_high_style)
            # 保存
            try:
                work_book.save('/home/user/桌面/' + nowText + '.xls')
            except:
                log = Logger('./log/logfile.log', level='error')
                log.logger.error("错误:%s", traceback.format_exc())
            else:
                QtWidgets.QMessageBox.information(None, "提示", "导出成功")

    def cxExcelOutput(self):
        print(23)

    def screen_shot(self):
        name = self.lineEdit_46.text()
        if name == "请输入图片名":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入图片名")
        else:
            win = WScreenShot(name=name)
            win.run(name=name)

    def screen_shot_wttj(self):
        name = self.lineEdit_47.text()
        if name == "请输入图片名":
            QtWidgets.QMessageBox.warning(None, "提示", "请输入图片名")
        else:
            win = WScreenShot(name=name)
            win.run(name=name)

    """
    @文件选择按钮函数
    弹出文件系统页面,选择相应类型文件
    """

    # 发文办理下的选择文件夹按钮(专报)
    def choose_file_zb(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Doc(*.doc);;Docx(*.docx);;WPS(*.wps)")
        self.lineEdit_file_zb.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def choose_file_gw(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Doc(*.doc);;Docx(*.docx);;WPS(*.wps)")
        self.lineEdit_file_3.setText(p[0])

    # 选择审计意见
    def choose_file_sjyj(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Doc(*.doc);;Docx(*.docx);;WPS(*.wps)")
        self.lineEdit_file_sjyj.setText(p[0])

    # 选择审计报告
    def choose_file_sjbg(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Doc(*.doc);;Docx(*.docx);;WPS(*.wps)")
        self.lineEdit_file_sjbg.setText(p[0])

    # 选择审计结果报告
    def choose_file_sjjg(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "Doc(*.doc);;Docx(*.docx);;WPS(*.wps)")
        self.lineEdit_file_sjjg.setText(p[0])

    # 选择经责问题表
    def chooseProblemJzTable(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "xls(*.xls);;xlsx(*.xlsx);;ET(*.et)")
        self.lineEdit_que_jz.setText(p[0])

    # 选择审计意见问题分表
    def choose_file_jz_excel(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "xls(*.xls);;xlsx(*.xlsx);;ET(*.et)")
        self.lineEdit_file_excel.setText(p[0])

    # 选择审计报告问题分表
    def choose_file_jz_excel2(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/", "xls(*.xls);;xlsx(*.xlsx);;ET(*.et)")
        self.lineEdit_file_excel_2.setText(p[0])

    """
    @其他功能控件实现
    """

    # 办文流程下设置整改按钮
    def lc_to_zg(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择流程！")
        else:
            key = self.tableWidget_lczl.item(row, 0).text()  # 流程序号
            key_zg = self.tableWidget_lczl.item(row, 9).text()  # 是否整改

            sql = "select 发文序号,收文序号 from bwprocess where 序号 = %s" % key
            xh_send = tools.executeSql(sql)[0][0]

            sql = "select 序号 from corfile where 流程序号 = %s" % key
            xh_cor = tools.executeSql(sql)

            # 获取问题
            if xh_send is not None:
                sql = "select count(*) from problem where 发文序号 = %s" % xh_send
                pro_num = tools.executeSql(sql)[0][0]

            # 发文号批文号都不为空&&问题个数不为0&&办文流程没有设置整改;则表示办文流程可以设置整改了
            if xh_send is not None and len(xh_cor) != 0 and pro_num != 0 and key_zg == "否":
                reply = QtWidgets.QMessageBox.question(None, '询问', '是否确认设置整改？', QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)  # 询问是否确认设置整改
                if reply == QtWidgets.QMessageBox.Yes:  # 如果确认设置整改
                    sql = "select 发文字号 from sendfile where 序号 = %s" % xh_send
                    doc_num_send = tools.executeSql(sql)[0][0]

                    # 将流程加入到整改中
                    sql = "insert into zgprocess(序号,流程序号,标识文号,整改状态) VALUES(NULL,%s,'%s','未整改')" % (key, doc_num_send)
                    tools.executeSql(sql)

                    # 修改流程为需要整改
                    sql = "update bwprocess set 是否加入整改 = '是' where 序号 = %s" % key
                    tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(None, "提示", "添加成功！")

                    # 更新tab映射情况,重新加载tab
                    obj = self.tabWidget_lczl_dict.get(key)
                    if obj is not None:
                        index = self.tabWidget_lczl.indexOf(obj)
                        self.tabWidget_lczl.removeTab(index)
                        tab_new = Call_lcdetail(key)
                        tab_new.setObjectName('tab_new')
                        self.tabWidget_lczl.addTab(tab_new, doc_num_send)
                        self.tabWidget_lczl_dict[key] = tab_new

                    # 刷新流程页面
                    self.showBwprocessTable()

            # 否则不能整改
            else:
                QtWidgets.QMessageBox.warning(None, "设置失败", "无法设置整改！")

    # 设置时间提示
    def tip_lc(self):
        if self.checkBox.property("checked"):
            front = self.dateEdit_8.date()
            behind = self.dateEdit_10.date()
            if front > behind:
                QtWidgets.QMessageBox.warning(None, "提示", "设置时间不合法")
                self.checkBox.setChecked(False)

    def tip_zg(self):
        if self.checkBox_3.property("checked"):
            front = self.dateEdit_7.date()
            behind = self.dateEdit_9.date()
            if front > behind:
                QtWidgets.QMessageBox.warning(None, "提示", "设置时间不合法")
                self.checkBox_3.setChecked(False)

    # 设置办文登记表中办文的办理状态
    def setRegisTableRowStatus(self):
        row = self.tableWidget_bwzl.currentRow()
        status = ""
        if self.radioButton_red.isChecked():
            status = "red"
        elif self.radioButton_green.isChecked():
            status = "green"
        elif self.radioButton_black.isChecked():
            status = "black"
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择表格中的一行！")
        else:
            key = self.tableWidget_bwzl.item(row, 0).text()
            table = ""
            if self.resType1 == "发文登记表":
                table = "sendfile"
            elif self.resType1 == "收文登记表":
                table = "revfile"
            elif self.resType1 == "批文登记表":
                table = "corfile"
            sql = "update '%s' set 状态 = '%s' where 序号 = %s" % (table, status, key)
            tools.executeSql(sql)

            QtWidgets.QMessageBox.information(None, "提示", "修改成功！")

            # 重新显示
            self.showRegisTable(type1=self.resType1, type2=self.resType2)

    # 打开选择的经责文件
    def openSjFile(self, listType):
        row = self.listWidget_sjwh.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择对应文件！")
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
            if filename == '/':
                QtWidgets.QMessageBox.information(None, "提示", "不存在对应文件！")
            else:
                tools.openFile(file_folder=file_folder, file=filename)

    # 删除相关文件
    def delSjFile(self, listType):
        row = self.listWidget_sjwh.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择对应文件！")
        else:
            keyword = self.listWidget_sjwh.currentItem().text()
            filename = ""
            file_folder = ""
            file_folder_sjjg = ""
            filename_sjjg = ""
            sql = ""

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
            if filename == '/':
                QtWidgets.QMessageBox.information(None, "提示", "不存在对应文件！")
            else:
                tools.executeSql(sql)
                tools.deleteFile(file_folder, filename)

                # 如果是删除审计报告或者审计结报,那么需要同时删除两个文件
                if listType == "sjbg" or listType == "sjjg":
                    tools.deleteFile(file_folder_sjjg, filename_sjjg)

                QtWidgets.QMessageBox.information(None, "提示", "删除成功！")
                self.displayFileJzPage()

    # 删除流程
    def deleteLc(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择流程！")
        else:
            key = self.tableWidget_lczl.item(row, 0).text()  # 流程序号
            key_zg = self.tableWidget_lczl.item(row, 9).text()  # 是否整改

            sql = "select 发文序号,收文序号 from bwprocess where 序号 = %s" % key
            xh_send = tools.executeSql(sql)[0][0]
            xh_rev = tools.executeSql(sql)[0][1]

            sql = "select 序号 from corfile where 流程序号 = %s" % key
            xh_cor = tools.executeSql(sql)

            if key_zg == "是":
                QtWidgets.QMessageBox.warning(None, "删除失败", "请先撤销整改！")
            else:
                reply = QtWidgets.QMessageBox.question(None, '询问', '是否确认删除流程？', QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)  # 询问是否确认删除
                if reply == QtWidgets.QMessageBox.Yes:  # 如果确认删除
                    # 批文不为空,首先删除流程对应批文和所有批示
                    if len(xh_cor) != 0:
                        # 删除批示
                        sql = "delete from instruction where 序号 in (select instruction.序号 from instruction,corfile " \
                              "where instruction.批文序号 = corfile.序号 and corfile.流程序号 = %s)" % key
                        tools.executeSql(sql)
                        # 删除批文
                        sql = "delete from corfile where 流程序号 = %s " % key
                        tools.executeSql(sql)

                    # 删除流程
                    sql = "delete from bwprocess where 序号 = %s" % key
                    tools.executeSql(sql)

                    # 删除收文
                    if xh_rev is not None:
                        sql = "delete from revfile where 序号 = %s" % xh_rev
                        tools.executeSql(sql)

                    # 删除发文和问题表
                    if xh_send is not None:
                        # 删除问题表
                        sql = "delete from problem where problem.发文序号 = %s" % xh_send
                        tools.executeSql(sql)

                        # 删除发文绑定文件
                        sql = "select 报文内容 from sendfile where 序号 = %s" % xh_send
                        filename = tools.executeSql(sql)[0][0]
                        tools.deleteFile(tools.project_word_path, filename)

                        # 删除发文
                        sql = "delete from sendfile where 序号 = %s" % xh_send
                        tools.executeSql(sql)

                    QtWidgets.QMessageBox.information(None, "提示", "删除成功！")

                    # 删除映射和tab
                    obj = self.tabWidget_lczl_dict.get(key)
                    if obj is not None:
                        index = self.tabWidget_lczl.indexOf(obj)
                        self.tabWidget_lczl.removeTab(index)
                        self.tabWidget_lczl_dict.pop(key)

                    # 更新流程表
                    self.showBwprocessTable()

    # 批文界面下的add和sub按钮,用于增加和删除条目
    def addTerm(self):
        item1 = QListWidgetItem("请输入领导来文单位")
        item1.setFlags(item1.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_5.addItem(item1)
        item2 = QListWidgetItem("请输入领导来文字号")
        item2.setFlags(item2.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_6.addItem(item2)
        item3 = QListWidgetItem("请输入领导批示")
        item3.setFlags(item3.flags() | QtCore.Qt.ItemIsEditable)
        self.listWidget_4.addItem(item3)

    def subTerm(self):
        row = self.listWidget_5.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择要删除的条目！")
        else:
            self.listWidget_5.takeItem(row)
            self.listWidget_6.takeItem(row)
            self.listWidget_4.takeItem(row)

    # 问题查询增加删除条件
    def addCondition(self):
        nowText = self.comboBox_22.currentText()
        nowIndex = self.comboBox_22.currentIndex()
        numeric_condition_dict = {
            "问题金额": "problem.问题金额",
            "已整改金额": "rectification.已整改金额",
            "追责问责人数": "rectification.追责问责人数",
            "推动制度建设数目": "rectification.推动制度建设数目",
            "认定整改金额": "rectification.认定整改金额",
            "整改率": "rectification.整改率"
        }
        if nowText == "选择查询类型":
            QtWidgets.QMessageBox.warning(None, "提示", "请选择查询类型！")
            return
        else:
            item1 = QListWidgetItem(nowText)
            item1.setSizeHint(QtCore.QSize(60, 60))
            self.listWidget_9.addItem(item1)
            self.listWidget_9.setCurrentItem(item1)
            self.comboBox_22.removeItem(nowIndex)  # 从comboBox_22中移除所选条目
            if nowText in numeric_condition_dict.keys():
                widget2 = QtWidgets.QWidget()
                edit1 = QtWidgets.QLineEdit("请输入数额")
                label = QtWidgets.QLabel("至")
                label.setEnabled(False)
                edit2 = QtWidgets.QLineEdit("请输入数额")
                grid = QtWidgets.QGridLayout()
                grid.addWidget(edit1, 0, 1)
                grid.addWidget(label, 0, 2)
                grid.addWidget(edit2, 0, 3)
                widget2.setLayout(grid)
                listWidgetItem = QtWidgets.QListWidgetItem()
                listWidgetItem.setSizeHint(QtCore.QSize(60, 60))
                self.listWidget_10.addItem(listWidgetItem)
                self.listWidget_10.setItemWidget(listWidgetItem, widget2)
            else:
                item2 = QListWidgetItem("请输入查询条件")
                item2.setSizeHint(QtCore.QSize(60, 60))
                item2.setFlags(item1.flags() | QtCore.Qt.ItemIsEditable)
                self.listWidget_10.addItem(item2)

    def subCondition(self):
        row = self.listWidget_9.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(None, "提示", "请选择要删除的条目！")
        else:
            item = self.listWidget_9.currentItem()
            nowText = item.text()
            self.comboBox_22.addItem(nowText)  # 把删除的条目重新加入comboBox_22

            self.listWidget_9.takeItem(row)
            self.listWidget_10.takeItem(row)
