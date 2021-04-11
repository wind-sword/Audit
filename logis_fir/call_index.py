import os
import sqlite3
import datetime

from PyQt5 import QtCore, QtWidgets

from call_lcdetail import Call_lcdetail
from uipy_dir.index import Ui_indexWindow
import sys
import qtawesome
from call_zgdetail import Call_zgdetail
import shutil


class Call_index(QtWidgets.QMainWindow, Ui_indexWindow):
    # 类成员变量
    db_path = "../db/database.db"
    project_word_path = "../project_word"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.initButton()

    def init_ui(self):
        self.bt_search.setFont(qtawesome.font('fa', 16))
        self.bt_search.setText(chr(0xf002) + ' ' + '搜索')

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.tabWidget.setTabText(0, "整改台账")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.tabWidget_lczl.setTabText(0, "流程总览")
        self.tabWidget_lczl.setTabsClosable(1)
        self.tabWidget_lczl.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget_lczl.tabCloseRequested.connect(self.mclose1)

        # 初始化显示
        self.stackedWidget.setCurrentIndex(0)
        self.showLczlTable()

    def initButton(self):
        # 页面对应关系 0：流程总览 page_lczl | 1：整改台账 page_zgtz | 2：发文办理 page_fwbl  |  3：收文办理 page_swbl | 4:收文浏览 page_tjfx
        # |5：统计分析 page_tjfx
        self.btzgtz.clicked.connect(self.zgtz)

        self.btlczl.clicked.connect(lambda: self.btjump(btname="lczl"))
        self.btfwbl.clicked.connect(lambda: self.btjump(btname="fwbl"))
        self.btswbl.clicked.connect(lambda: self.btjump(btname="swbl"))
        self.btswll.clicked.connect(lambda: self.btjump(btname="swll"))

        self.btcx.clicked.connect(self.tjfx)
        self.bttj.clicked.connect(self.tjfx)

        self.bt_search.clicked.connect(self.search)

        self.pushButton_file.clicked.connect(self.choose_file_zb)
        self.pushButton_file_3.clicked.connect(self.choose_file_gw)

        self.pushButton_addac.clicked.connect(self.add_zb)
        self.pushButton_addac_3.clicked.connect(self.add_gw)
        self.pushButton_3.clicked.connect(self.add_sw)

        self.comboBox_type.currentIndexChanged.connect(self.fwexchange)

        self.pushButton.clicked.connect(self.showRegisTable)

        self.pushButton_more.clicked.connect(self.tz_detail)

        self.btckxq.clicked.connect(self.lc_detail)
        self.btszzg.clicked.connect(self.lc_to_tz)
        self.btjrzg.clicked.connect(self.to_tz_detail)

        self.dateEdit_5.dateChanged.connect(self.autoSyn1)
        self.dateEdit_6.dateChanged.connect(self.autoSyn2)
        self.lineEdit_num.textChanged.connect(self.autoSyn3)
        self.lineEdit_18.textChanged.connect(self.autoSyn4)
        self.comboBox_2.currentIndexChanged.connect(self.autoSyn5)

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

    # 显示台账内容
    def showProjectTable(self):
        # 表格不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # sql由台账表的流程序号出发,通过多表查询获得台账所有字段
        sql = 'select bwprocess.流程开始时间,sendfile.发文标题,sendfile.发文字号,revfile.收文标题,revfile.收文字号,GROUP_CONCAT(' \
              'corfile.批文标题),GROUP_CONCAT(corfile.批文字号),standingbook.整改发函内容 from standingbook join bwprocess on ' \
              'standingbook.流程序号 = bwprocess.序号 join sendfile on bwprocess.发文序号 = sendfile.序号 join revfile on ' \
              'bwprocess.收文序号 = revfile.序号 join bw_cast_cor on bwprocess.序号 = bw_cast_cor.流程序号 join corfile on ' \
              'bw_cast_cor.批文序号 = corfile.序号 GROUP BY standingbook.序号 '
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

        self.tableWidget.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget.resizeRowsToContents()  # 根据行调整框大小

    # 显示发文流程内容
    def showLczlTable(self):
        # 表格不可编辑
        self.tableWidget_lczl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # sql查询通过多表左外连接查询获取发文流程结果.并且根据流程序号这一唯一标识分组,将批文标题和字号用逗号连接起来
        sql = "SELECT bwprocess.流程开始时间,sendfile.发文标题,sendfile.发文字号,revfile.收文标题,revfile.收文字号,GROUP_CONCAT(" \
              "corfile.批文标题),GROUP_CONCAT(corfile.批文字号),bwprocess.是否加入整改 FROM bwprocess LEFT OUTER JOIN sendfile ON " \
              "sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN revfile ON revfile.序号 = bwprocess.收文序号 LEFT OUTER JOIN " \
              "bw_cast_cor ON bw_cast_cor.流程序号 = bwprocess.序号 LEFT OUTER JOIN corfile ON corfile.序号 = " \
              "bw_cast_cor.批文序号 GROUP BY bwprocess.序号 "
        data = self.executeSql(sql)
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

    # 显示发文流程内容(未完成,需要和审计厅的人确认登记表字段来源再进行开发)
    def showRegisTable(self):
        # 表格不可编辑
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # 清空表格
        self.tableWidget_2.clear()

        # 表格不可编辑
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        type1 = self.comboBox_2.currentText()  # 种类一
        type2 = self.comboBox.currentText()  # 种类二

        sql = ""

        if type1 == "发文登记表":
            self.label_34.setText("湖北省审计厅发文登记簿 注：红色办理中，黑色办结。")
            self.tableWidget_2.setColumnCount(11)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['登记时间', '发文字号', '密级', '标识', '标题', '签发人', '份数', '公文运转情况', '批示情况', '批示办理情况', '起草处室'])
            if type2 == "委文":
                self.label_35.setText("鄂审计委文")
            elif type2 == "委发":
                self.label_35.setText("鄂审计委发")
            elif type2 == "委办文":
                self.label_35.setText("鄂审计委办文")
            elif type2 == "委办发":
                self.label_35.setText("鄂审计委办发")
            elif type2 == "委函":
                self.label_35.setText("鄂审计委函")
            elif type2 == "委办函":
                self.label_35.setText("鄂审计委办函")
            elif type2 == "委便签":
                self.label_35.setText("鄂审计委便签")
            elif type2 == "委办便签":
                self.label_35.setText("鄂审计委办便签:（无编号）")
            elif type2 == "会议纪要":
                self.label_35.setText("会议纪要")
            elif type2 == "审计专报":
                self.label_35.setText("审计专报")

            sql = ''

        elif type1 == "收文登记表":
            self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。4、蓝色：临时交办审计任务。")
            self.tableWidget_2.setColumnCount(12)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['时间', '编号', '秘级', '来文单位', '来文字号', '来文标题', '拟办意见', '厅领导签批意见', '承办处室', '办理结果', '要求时间', '文件去向'])
            if type2 == "请字":
                self.label_34.setText("请字[2021]（平级、下级报送的请示类文件）→")
            elif type2 == "情字":
                self.label_34.setText("情字[2021]（平级、下级报送的情况类文件）→")
            elif type2 == "综字":
                self.label_34.setText("综字[2021]（上级下发的各类文件）→")
            elif type2 == "会字":
                self.label_34.setText("会[2021]（各级会议通知）→")
            elif type2 == "电字":
                self.label_34.setText("电[2021]（电报文件）→")

            sql = 'select 收文时间,收文字号,秘密等级,来文单位,来文字号,收文标题,内容摘要和拟办意见,领导批示,承办处室,处理结果 from revfile'

        elif type1 == "批文登记表":
            self.label_35.setText("1、红色：件未办结。2、绿色：件已办结，事项在办。3、黑色：件与事项完全办结并共同归档。")
            self.label_34.setText("批字[2021]（省领导对审计委员会及委员会办公室文件资料的批示）")
            self.tableWidget_2.setColumnCount(15)
            self.tableWidget_2.setHorizontalHeaderLabels(
                ['时间', '发文编号', '收文编号', '办文编号', '秘级', '来文单位', '来文字号', '来文标题', '省领导批示内容', '秘书处拟办意见', '委办主任签批意见',
                 '批示任务办理要求时间', '承办处室及承办人', '办理结果', '文件去向'])

            sql = 'select corfile.收文时间,sendfile.发文字号,revfile.收文字号,corfile.批文字号,corfile.秘密等级,corfile.来文单位,' \
                  'corfile.来文字号,corfile.批文标题,corfile.领导批示,corfile.内容摘要和拟办意见,corfile.委办主任签批意见,' \
                  'corfile.批示任务办理要求时间,corfile.承办处室及承办人,corfile.办理结果,corfile.文件去向 from bwprocess join sendfile on ' \
                  'bwprocess.发文序号 = sendfile.序号 join revfile on bwprocess.收文序号 = revfile.序号 join bw_cast_cor on ' \
                  'bwprocess.序号 = bw_cast_cor.流程序号 join corfile on bw_cast_cor.批文序号 = corfile.序号 '

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

        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小

    # 同步输入框内容,1、2为公文时间同步,3、4为公文编号同步,5为办文登记表下拉框同步
    def autoSyn1(self):
        self.dateEdit_6.setDate(self.dateEdit_5.date())

    def autoSyn2(self):
        self.dateEdit_5.setDate(self.dateEdit_6.date())

    def autoSyn3(self):
        self.lineEdit_18.setText(self.lineEdit_num.text())

    def autoSyn4(self):
        self.lineEdit_num.setText(self.lineEdit_18.text())

    def autoSyn5(self):
        type1 = self.comboBox_2.currentText()
        self.comboBox.clear()
        if type1 == "发文登记表":
            self.comboBox.addItems(["委文", "委发", "委办文", "委办发", "委函", "委办函", "委便签", "委办便签", "会议纪要", "审计专报"])
        elif type1 == "收文登记表":
            self.comboBox.addItems(["请字", "情字", "综字", "会字", "电字"])
        elif type1 == "批文登记表":
            self.comboBox.addItem("批字")

    def mclose(self, index):
        self.tabWidget.removeTab(index)

    def mclose1(self, index):
        self.tabWidget_lczl.removeTab(index)

    # 整改台账按钮
    def zgtz(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.showProjectTable()  # 点击整改台账显示表内容

    # 办文流程下按钮跳转
    def btjump(self, btname):
        if btname == "lczl":
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        if btname == "fwbl":
            self.stackedWidget.setCurrentIndex(2)
        if btname == "swbl":
            self.stackedWidget.setCurrentIndex(3)
        if btname == "swll":
            self.stackedWidget.setCurrentIndex(4)

    # 统计分析按钮
    def tjfx(self):
        self.stackedWidget.setCurrentIndex(5)

    # 整改台账下的项目搜索按钮(未开发)
    def search(self):
        # 需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    # 发文办理下的选择文件夹按钮(专报)
    def choose_file_zb(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def choose_file_gw(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file_3.setText(p[0])

    # 发文办理下的项目类型切换栏
    def fwexchange(self, index):
        self.stackedWidget_new.setCurrentIndex(index)

    # 发文办理下的确认按钮(专报)
    def add_zb(self):
        input1 = self.lineEdit.text()  # 发文标题
        input2 = self.lineEdit_2.text()  # 报送范围
        input3 = self.lineEdit_3.text()  # 发文字号
        input4 = self.lineEdit_4.text()  # 紧急程度
        input5 = self.lineEdit_5.text()  # 秘密等级
        input6 = self.lineEdit_6.text()  # 是否公开
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
        input16 = os.path.split(input_file_path)[1]  # 文件名

        if input3 != "":
            # 执行插入sendfile表
            sql = "insert into sendfile(发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导," \
                  "审计办主任,办文日期,报文内容,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                  "'%s','%s','%s','%s',1);" % (input1, input2, input3, input4, input5, input6, input7, input8, input9,
                                               input10, input11, input12, input13, input14, input15, input16)
            self.executeSql(sql)

            # 找到当前发文的序号
            sql = "select 序号 from sendfile where 发文字号 = '%s'" % input3
            data = self.executeSql(sql)

            # 执行插入流程表
            curr_time = datetime.datetime.now()
            time_str = curr_time.strftime("%Y/%m/%d")
            sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,0,'%s')" % (data[0][0], time_str)
            self.executeSql(sql)

            # 导入文件
            self.copyFile(input_file_path, self.project_word_path)

            QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.critical(self, "新建失败", "发文字号不能为空!")

    # 发文办理下的确认按钮(公文)
    def add_gw(self):
        input1 = self.lineEdit_num.text()  # 发文字号
        input2 = self.lineEdit_num_3.text()  # 发文标题
        input3 = self.textEdit.toPlainText()  # 领导审核意见
        input4 = self.textEdit_2.toPlainText()  # 审计办领导审核意见
        input5 = self.textEdit_3.toPlainText()  # 办文情况说明和拟办意见
        input6 = self.dateEdit_6.text()  # 办文日期
        input_file_path = self.lineEdit_file_3.text()  # 文件路径
        input7 = os.path.split(input_file_path)[1]  # 文件名
        input8 = self.lineEdit_22.text()  # 紧急程度
        input9 = self.lineEdit_15.text()  # 保密等级
        input10 = self.lineEdit_16.text()  # 是否公开
        input11 = self.lineEdit_17.text()  # 审核
        input12 = self.lineEdit_19.text()  # 承办处室
        input13 = self.lineEdit_20.text()  # 承办人
        input14 = self.lineEdit_21.text()  # 联系电话

        if input1 != "":
            # 执行插入sendfile表
            sql = "insert into sendfile(发文字号,发文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,办文日期,报文内容,紧急程度,秘密等级,是否公开,审核,承办处室,承办人," \
                  "联系电话,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',2);" % (
                      input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12,
                      input13, input14)
            self.executeSql(sql)

            # 导入文件
            self.copyFile(input_file_path, self.project_word_path)

            # 找到当前发文的序号
            sql = "select 序号 from sendfile where 发文字号 = '%s'" % input1
            data = self.executeSql(sql)

            # 执行插入流程表
            curr_time = datetime.datetime.now()
            time_str = curr_time.strftime("%Y/%m/%d")
            sql = "insert into bwprocess(发文序号,是否加入整改,流程开始时间) VALUES(%s,0,'%s')" % (data[0][0], time_str)
            self.executeSql(sql)

            QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.critical(self, "新建失败", "发文字号不能为空!")

    # 收文办理下的录入按钮
    def add_sw(self):
        input1 = self.dateEdit_4.text()  # 收文时间
        input2 = self.lineEdit_23.text()  # 密级
        input3 = self.lineEdit_24.text()  # 是否公开
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
        if input10 != "":
            # 执行插入收文表
            sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,来文单位,来文字号,收文标题,处理结果,审核,收文字号,承办处室,承办人,联系电话) values('%s'," \
                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      input1, input2, input3, input4, input5, input6,
                      input7, input8, input9, input10, input11,
                      input12, input13)
            self.executeSql(sql)

            # 找到当前收文的序号
            sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
            data = self.executeSql(sql)

            # 执行插入流程表
            curr_time = datetime.datetime.now()
            time_str = curr_time.strftime("%Y/%m/%d")
            sql = "insert into bwprocess(收文序号,是否加入整改,流程开始时间) VALUES(%s,0,'%s')" % (data[0][0], time_str)
            self.executeSql(sql)

            QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.critical(self, "录入失败", "办文编号不能为空!")

    # 整改台账下的查看详情按钮
    def tz_detail(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择整改项目！")
        else:
            # 获取发文字号用于查询
            key = self.tableWidget.item(row, 1).text()
            tab_new = Call_zgdetail(key)
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, key)
            self.tabWidget.setCurrentIndex(tab_num)

    # 办文流程详情下的查看详情按钮
    def lc_detail(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择流程！")
        else:
            key1 = self.tableWidget_lczl.item(row, 2).text()  # 发文号
            key2 = self.tableWidget_lczl.item(row, 4).text()  # 收文号
            tab_new1 = Call_lcdetail(key1, key2)
            tab_new1.setObjectName('tab_new')
            tab_num1 = self.tabWidget_lczl.addTab(tab_new1, "流程详情")
            self.tabWidget_lczl.setCurrentIndex(tab_num1)

    # 办文流程下设置整改按钮
    def lc_to_tz(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择流程！")
        else:
            key1 = self.tableWidget_lczl.item(row, 2).text()  # 发文号
            key2 = self.tableWidget_lczl.item(row, 4).text()  # 收文号
            key3 = self.tableWidget_lczl.item(row, 6).text()  # 批文号
            key4 = self.tableWidget_lczl.item(row, 7).text()  # 是否整改

            # key1,key2,key3都不为空表示办文流程已经完成,可以设置整改了
            if key1 != "/" and key2 != "/" and key3 != "/" and key4 != "1":
                sql = "select bwprocess.序号 from bwprocess,sendfile where sendfile.序号 = bwprocess.发文序号 and " \
                      "sendfile.发文字号 = '%s'" % key1
                data = self.executeSql(sql)
                xh = data[0][0]

                # 将流程加入到台账中
                sql = "insert into standingbook(流程序号,tag) VALUES(%s,0)" % xh
                self.executeSql(sql)

                # 修改流程整改状态为1
                sql = "update bwprocess set 是否加入整改 = 1 where 序号 = %s" % xh
                self.executeSql(sql)

                QtWidgets.QMessageBox.information(self, "提示", "添加成功！")

                # 刷新流程页面
                self.showLczlTable()

            # 否则不能整改
            else:
                if key1 == "/":
                    QtWidgets.QMessageBox.warning(self, "警告", "无法设置整改！")
                elif key1 != "/" and (key2 == "/" or key3 == "/"):
                    QtWidgets.QMessageBox.warning(self, "警告", "无法设置整改！")
                elif key4 == "1":
                    QtWidgets.QMessageBox.warning(self, "警告", "已设置整改！")

    # 办文流程下进入整改按钮,调用整改台账下的查看详情(待完成)
    def to_tz_detail(self):
        print("ok")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    callindex = Call_index()
    callindex.show()
    sys.exit(app.exec_())
