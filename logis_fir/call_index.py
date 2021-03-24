import os
import sqlite3

from PyQt5 import QtCore, QtWidgets

from call_lcdetail import Call_lcdetail
from uipy_dir.index import Ui_indexWindow
import sys
import qtawesome
from call_zbdetail import Call_zbdetail
from call_gwdetail import Call_gwdetail
import shutil


class Call_index(QtWidgets.QMainWindow, Ui_indexWindow):
    db_path = "../db/database.db"
    project_word_path = "../project_word"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.logi()

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

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()  # 根据内容调整框大小

        self.showLczlTable()  # 初始化显示

    def logi(self):
        # 页面对应关系 0：流程总览 page_lczl | 1：整改台账 page_zgtz | 2：发文办理 page_fwbl  |  3：收文办理 page_swbl | 4:收文浏览 page_tjfx
        # |5：统计分析 page_tjfx
        self.btzgtz.clicked.connect(self.btfun1)

        self.btlczl.clicked.connect(lambda: self.btjump(btname="lczl"))
        self.btfwbl.clicked.connect(lambda: self.btjump(btname="fwbl"))
        self.btswbl.clicked.connect(lambda: self.btjump(btname="swbl"))
        self.btswll.clicked.connect(lambda: self.btjump(btname="swll"))

        self.btcx.clicked.connect(self.btfun3)
        self.bttj.clicked.connect(self.btfun3)
        self.bt_search.clicked.connect(self.btfun4)
        self.pushButton_file.clicked.connect(self.btfun5)
        self.pushButton_file_3.clicked.connect(self.btfun5_1)
        self.pushButton_addac.clicked.connect(self.btfun6)
        self.pushButton_addac_3.clicked.connect(self.btfun6_1)
        self.comboBox_type.currentIndexChanged.connect(self.btfun7)
        self.pushButton_more.clicked.connect(self.btfun8)
        self.btckxq.clicked.connect(self.btfun9)
        self.pushButton_3.clicked.connect(self.btfun10)

        self.dateEdit_5.dateChanged.connect(self.autoSyn1)
        self.dateEdit_6.dateChanged.connect(self.autoSyn2)
        self.lineEdit_num.textChanged.connect(self.autoSyn3)
        self.lineEdit_18.textChanged.connect(self.autoSyn4)

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
        # 导致表头消失 self.tableWidget.clear()
        sql = 'select 时间,发文字号,收文字号,办文字号,秘密等级,来文单位,来文字号,来文标题,省领导批示内容,秘书处拟办意见,委办主任签批意见,批示任务办理要求时间,承办处室及承办人,办理结果,' \
              '文件去向 from standingbook'
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

    # 显示发文流程内容
    def showLczlTable(self):
        # 导致表头消失 self.tableWidget.clear()

        # sql查询通过三表左外连接查询获取发文流程结果
        sql = "SELECT sendfile.发文字号,revfile.收文字号,revfile.批文字号,bwprocess.是否加入整改 from bwprocess LEFT OUTER JOIN " \
              "sendfile on sendfile.序号 = bwprocess.发文序号 LEFT OUTER JOIN revfile on revfile.序号 = bwprocess.收文序号 "
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

    # 同步输入框内容
    def autoSyn1(self):
        self.dateEdit_6.setDate(self.dateEdit_5.date())

    def autoSyn2(self):
        self.dateEdit_5.setDate(self.dateEdit_6.date())

    def autoSyn3(self):
        self.lineEdit_18.setText(self.lineEdit_num.text())

    def autoSyn4(self):
        self.lineEdit_num.setText(self.lineEdit_18.text())

    def mclose(self, index):
        self.tabWidget.removeTab(index)

    def mclose1(self, index):
        self.tabWidget_lczl.removeTab(index)

    # 整改台账按钮
    def btfun1(self):
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
    def btfun3(self):
        self.stackedWidget.setCurrentIndex(5)

    # 整改台账下的项目搜索按钮(未开发)
    def btfun4(self):
        # 需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    # 发文办理下的选择文件夹按钮(专报)
    def btfun5(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file.setText(p[0])

    # 发文办理下的选择文件夹按钮(公文)
    def btfun5_1(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file_3.setText(p[0])

    # 发文办理下的确认按钮(专报)
    def btfun6(self):
        str1 = self.label.text()  # 专报标题
        input1 = self.lineEdit.text()

        str2 = self.label_2.text()  # 报送范围
        input2 = self.lineEdit_2.text()

        str3 = self.label_3.text()  # 发文字号
        input3 = self.lineEdit_3.text()

        str4 = self.label_4.text()  # 紧急程度
        input4 = self.lineEdit_4.text()

        str5 = self.label_5.text()  # 秘密等级
        input5 = self.lineEdit_5.text()

        str6 = self.label_6.text()  # 是否公开
        input6 = self.lineEdit_6.text()

        str7 = self.label_7.text()  # 拟稿人
        input7 = self.lineEdit_7.text()

        str8 = self.label_8.text()  # 拟稿处室分管厅领导
        input8 = self.lineEdit_12.text()

        str9 = self.label_9.text()  # 拟稿处室审核
        input9 = self.lineEdit_8.text()

        str10 = self.label_10.text()  # 综合处编辑
        input10 = self.lineEdit_9.text()

        str11 = self.label_11.text()  # 综合处审核
        input11 = self.lineEdit_10.text()

        str12 = self.label_12.text()  # 秘书处审核
        input12 = self.lineEdit_11.text()

        str13 = self.label_13.text()  # 综合处分管厅领导
        input13 = self.lineEdit_13.text()

        str14 = self.label_14.text()  # 审计办主任
        input14 = self.lineEdit_14.text()

        str15 = self.label_time.text()  # 办文日期
        input15 = self.dateEdit_3.text()

        str16 = self.label_file.text()  # 报文内容
        input_file_path = self.lineEdit_file.text()  # 文件路径
        input16 = os.path.split(input_file_path)[1]  # 文件名

        if input3 != "":
            # 执行插入sendfile表
            sql = "insert into sendfile(专报标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导," \
                  "审计办主任,办文日期,报文内容,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                  "'%s','%s','%s','%s',1);" % (input1, input2, input3, input4, input5, input6, input7, input8, input9,
                                               input10, input11, input12, input13, input14, input15, input16)
            self.executeSql(sql)

            # 找到当前发文的序号
            sql = "select 序号 from sendfile where 发文字号 = '%s'" % input3
            data = self.executeSql(sql)

            # 执行插入流程表
            sql = "insert into bwprocess(发文序号,是否加入整改) VALUES('%s',0)" % data[0][0]
            self.executeSql(sql)

            # 导入文件
            self.copyFile(input_file_path, self.project_word_path)

            QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "发文字号不能为空!")

    # 发文办理下的确认按钮(公文)
    def btfun6_1(self):
        str1 = self.label_num.text()  # 发文字号
        input1 = self.lineEdit_num.text()

        str2 = self.label_num_3.text()  # 公文标题
        input2 = self.lineEdit_num_3.text()

        str3 = self.label_num_4.text()  # 领导审核意见
        input3 = self.textEdit.toPlainText()

        str4 = self.label_num_5.text()  # 审计办领导审核意见
        input4 = self.textEdit_2.toPlainText()

        str5 = self.label_num_6.text()  # 办文情况说明和拟办意见
        input5 = self.textEdit_3.toPlainText()

        str6 = self.label_23.text()  # 办文日期
        input6 = self.dateEdit_6.text()

        str7 = self.label_file_3.text()  # 公文内容
        input_file_path = self.lineEdit_file_3.text()  # 文件路径
        input7 = os.path.split(input_file_path)[1]  # 文件名

        str8 = self.label_24.text()  # 紧急程度
        input8 = self.lineEdit_22.text()

        str9 = self.label_15.text()  # 保密等级
        input9 = self.lineEdit_15.text()

        str10 = self.label_16.text()  # 是否公开
        input10 = self.lineEdit_16.text()

        str11 = self.label_17.text()  # 审核
        input11 = self.lineEdit_17.text()

        str12 = self.label_20.text()  # 承办处室
        input12 = self.lineEdit_19.text()

        str13 = self.label_21.text()  # 承办人
        input13 = self.lineEdit_20.text()

        str14 = self.label_22.text()  # 联系电话
        input14 = self.lineEdit_21.text()

        if input1 != "":
            # 执行插入sendfile表
            sql = "insert into sendfile(发文字号,公文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,办文日期,报文内容,紧急程度,秘密等级,是否公开,审核,承办处室,承办人," \
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
            sql = "insert into bwprocess(发文序号,是否加入整改) VALUES('%s',0)" % data[0][0]
            self.executeSql(sql)

            QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "发文字号不能为空!")

    # 发文办理下的项目类型切换栏
    def btfun7(self, index):
        self.stackedWidget_new.setCurrentIndex(index)

    # 整改台账下的查看详情按钮(台账详情需要大修改,暂时未完成,先完成发文流程,此处逻辑为旧逻辑)
    def btfun8(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择项目！")
        else:
            # 获取发文字号用于查询
            key = self.tableWidget.item(row, 1).text()
            sql = 'select sendfile.专报标题,sendfile.报送范围,sendfile.发文字号,sendfile.紧急程度,sendfile.秘密等级,sendfile.是否公开,' \
                  'sendfile.拟稿人,sendfile.拟稿处室分管厅领导,sendfile.拟稿处室审核,sendfile.综合处编辑,sendfile.综合处审核,sendfile.秘书处审核,' \
                  'sendfile.综合处分管厅领导,sendfile.审计办主任,sendfile.公文标题,sendfile.领导审核意见,sendfile.审计办领导审核意见,' \
                  'sendfile.办文情况说明和拟办意见,sendfile.projectType,sendfile.报文内容,sendfile.审核,sendfile.承办处室,sendfile.承办人,' \
                  'sendfile.联系电话,sendfile.办文日期 from sendfile where 发文字号 =  \'%s\'' % key
            data = self.executeSql(sql)
            # 判断项目类型
            if data[0][18] == 1:
                tab_new = Call_zbdetail(data)
                tab_new.setObjectName('tab_new')
                tab_num = self.tabWidget.addTab(tab_new, "专报%s详情" % key)
                self.tabWidget.setCurrentIndex(tab_num)
            elif data[0][18] == 2:
                tab_new = Call_gwdetail(data)
                tab_new.setObjectName('tab_new')
                tab_num = self.tabWidget.addTab(tab_new, "公文%s详情" % key)
                self.tabWidget.setCurrentIndex(tab_num)

    # 办文流程详情下的查看详情按钮
    def btfun9(self):
        row = self.tableWidget_lczl.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择流程！")
        else:
            key1 = self.tableWidget_lczl.item(row, 0).text()  # 发文号
            key2 = self.tableWidget_lczl.item(row, 1).text()  # 收文号
            tab_new1 = Call_lcdetail(key1, key2)
            tab_new1.setObjectName('tab_new')
            tab_num1 = self.tabWidget_lczl.addTab(tab_new1, "流程详情")
            self.tabWidget_lczl.setCurrentIndex(tab_num1)

    # 收文办理下的录入按钮
    def btfun10(self):
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
            sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,文件标题,处理结果,审核,收文字号,承办处室,承办人,联系电话,tag) values(" \
                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      input1, input2, input3, input4, input5, input6,
                      input7, input8, input9, input10, input11,
                      input12, input13, 0)
            self.executeSql(sql)

            # 找到当前收文的序号
            sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
            data = self.executeSql(sql)

            # 执行插入流程表
            sql = "insert into bwprocess(收文序号,是否加入整改) VALUES('%s',0)" % data[0][0]
            self.executeSql(sql)

            QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

            # 返回显示页面,重新加载流程内容
            self.stackedWidget.setCurrentIndex(0)
            self.showLczlTable()
        else:
            QtWidgets.QMessageBox.information(self, "提示", "办文编号不能为空!")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    callindex = Call_index()
    callindex.show()
    sys.exit(app.exec_())
