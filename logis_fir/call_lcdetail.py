import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

from uipy_dir.lcdetail import Ui_Form


class Call_lcdetail(QtWidgets.QWidget, Ui_Form):
    xh = -1  # 流程序号
    xh_send = -1  # 发文序号
    send_type = -1  # 发文类型
    xh_rev = -1  # 收文序号
    rev_tag = -1  # 是否批改
    db_path = "../db/database.db"

    def __init__(self, k1, k2):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(lambda: self.btjump(btname="0"))
        self.commandLinkButton_2.clicked.connect(lambda: self.btjump(btname="2"))
        self.commandLinkButton_3.clicked.connect(lambda: self.btjump(btname="3"))

        self.dateEdit_6.dateChanged.connect(self.autoSyn1)
        self.dateEdit_7.dateChanged.connect(self.autoSyn2)
        self.lineEdit_num.textChanged.connect(self.autoSyn3)
        self.lineEdit_25.textChanged.connect(self.autoSyn4)

        self.cast(k1, k2)

        # 初始化页面展示
        self.screenView()
        # 初始化页面数据
        if self.xh_send != -1:
            self.displaySendFile()
        elif self.xh_send == -1 and self.xh_rev != -1:
            self.displayRevFile()

        print("当前流程序号:%s" % self.xh)
        print("当前发文序号:%s" % self.xh_send)
        print("当前收文序号:%s" % self.xh_rev)
        print("当前发文类型:%s" % self.send_type)
        print("当前收文批改情况:%s\n" % self.rev_tag)

        self.insertOrUpdate()

    # 同步公文输入框内容
    def autoSyn1(self):
        self.dateEdit_7.setDate(self.dateEdit_6.date())

    def autoSyn2(self):
        self.dateEdit_6.setDate(self.dateEdit_7.date())

    def autoSyn3(self):
        self.lineEdit_25.setText(self.lineEdit_num.text())

    def autoSyn4(self):
        self.lineEdit_num.setText(self.lineEdit_25.text())

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

    # 将发文字号和收文字号映射为流程表中的序号,并且初始化发文种类变量,是否批示变量
    def cast(self, k1, k2):
        # 表明发文字号不为空,对各状态变量初始化
        if k1 != "/":
            sql = "select bwprocess.序号,bwprocess.发文序号,bwprocess.收文序号 from bwprocess,sendfile where " \
                  "bwprocess.发文序号=sendfile.序号 and sendfile.发文字号='%s'" % k1
            data = self.executeSql(sql)
            # print(data)
            self.xh = data[0][0]
            self.xh_send = data[0][1]

            # 初始化发文类型
            sql = "select projectType from sendfile where 序号=%s" % self.xh_send
            result = self.executeSql(sql)
            self.send_type = result[0][0]

            if data[0][2] is not None:
                self.xh_rev = data[0][2]
                # 初始化收文是否批改
                sql = "select tag from revfile where 序号=%s" % self.xh_rev
                result = self.executeSql(sql)
                self.rev_tag = result[0][0]

        # 表明发文字号为空,对各状态变量初始化
        elif k1 == "/" and k2 != "/":
            sql = "select bwprocess.序号,bwprocess.发文序号,bwprocess.收文序号 from bwprocess,revfile where " \
                  "bwprocess.收文序号=revfile.序号 and revfile.收文字号='%s'" % k2
            data = self.executeSql(sql)
            # print(data)
            self.xh = data[0][0]
            if data[0][1] is not None:
                self.xh_send = data[0][1]
                # 初始化发文类型
                sql = "select projectType from sendfile where 序号=%s" % self.xh_send
                result = self.executeSql(sql)
                self.send_type = result[0][0]
            self.xh_rev = data[0][2]

            # 初始化收文是否批改
            sql = "select tag from revfile where 序号=%s" % self.xh_rev
            result = self.executeSql(sql)
            self.rev_tag = result[0][0]

    # 按钮跳转,同时刷新页面
    def btjump(self, btname):
        if btname == "0":
            if self.send_type == 2:
                self.stackedWidget.setCurrentIndex(0)
            elif self.send_type == 1:
                self.stackedWidget.setCurrentIndex(1)
            self.displaySendFile()
        if btname == "2":
            self.stackedWidget.setCurrentIndex(2)
            self.displayRevFile()
        if btname == "3":
            self.stackedWidget.setCurrentIndex(3)
            self.displayRev2File()

    # 绑定添加修改按钮
    def insertOrUpdate(self):
        self.pushButton_3.clicked.connect(self.insertRevFile)
        self.pushButton_4.clicked.connect(self.insertRev2File)
        self.pushButton_2.clicked.connect(lambda: self.updateSendFile(btname="gw"))
        self.pushButton_5.clicked.connect(lambda: self.updateSendFile(btname="zb"))
        self.pushButton_6.clicked.connect(self.updateRevFile)
        self.pushButton_7.clicked.connect(self.updateRev2File)

    # 从初始化的序号中判断要展示的页面
    def screenView(self):
        # 没有发文流程
        if self.xh_send == -1:
            self.commandLinkButton.hide()
            self.stackedWidget.setCurrentIndex(2)
        # 有发文流程
        else:
            # 专报类型
            if self.send_type == 1:
                self.stackedWidget.setCurrentIndex(1)
            # 公文类型
            elif self.send_type == 2:
                self.stackedWidget.setCurrentIndex(0)

    # 展示发文页面
    def displaySendFile(self):
        if self.xh_send != -1:
            sql = "select 发文标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
                  "领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
                  "序号 =  %s" % self.xh_send
            data = self.executeSql(sql)
            # print(data)
            # 专报类型
            if self.send_type == 1:
                self.lineEdit.setText(data[0][0])  # 发文标题
                self.lineEdit_2.setText(data[0][1])  # 报送范围
                self.lineEdit_4.setText(data[0][2])  # 发文字号
                self.lineEdit_13.setText(data[0][3])  # 紧急程度
                self.lineEdit_5.setText(data[0][4])  # 秘密等级
                self.lineEdit_14.setText(data[0][5])  # 是否公开
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

            # 公文类型
            elif self.send_type == 2:
                self.lineEdit_num.setText(data[0][2])  # 发文字号
                self.lineEdit_num_3.setText(data[0][0])  # 发文标题
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
                # self.dateEdit_6.setDate(QDate.fromString(data[0][24], 'yyyy/M/d'))  # 日期
                # self.lineEdit_25.setText(data[0][2])  # 办文编号

    # 展示收文页面
    def displayRevFile(self):
        # 收文表本来就存在,此时读数据库,隐藏新增收文按钮,展示修改按钮
        if self.xh_rev != -1:
            sql = "select 收文收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,收文标题,处理结果,审核,收文字号,收文承办处室,收文承办人,收文联系电话 from revfile " \
                  "where 序号 = %s" % self.xh_rev
            data = self.executeSql(sql)
            self.pushButton_3.hide()
            self.pushButton_6.show()
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

        # 收文表本来不存在,但是发文表存在,此时应该继承发文表中已有内容,隐藏修改收文按钮,展示新增收文按钮
        elif self.xh_rev == -1 and self.xh_send != -1:
            # 继承专报字段,此处重新查询发文字段是为了防止:用户如果修改发文界面输入文本而没有保存此次修改的话,收文表字段会错误继承用户修改的字段内容,因为此时数据库中并没有提交修改
            sql = "select 发文标题,发文字号,紧急程度,秘密等级,是否公开 from sendfile where 序号 = %s" % self.xh_send
            data = self.executeSql(sql)
            self.pushButton_3.show()
            self.pushButton_6.hide()

            self.lineEdit_6.setText(data[0][3])  # 密级
            self.lineEdit_7.setText(data[0][4])  # 是否公开
            self.lineEdit_35.setText(data[0][0])  # 文件标题
            self.lineEdit_36.setText(data[0][2])  # 紧急程度
            self.lineEdit_37.setText(data[0][1])  # 来文字号

    # 展示批文页面
    def displayRev2File(self):
        # 表示收文还没有录入,此时展示空页面
        if self.rev_tag == -1:
            pass
        # 表示收文还没有批示,此时继承收文的必要字段,按照收文继承发文的逻辑,应该读数据库,而不是复制收文前端的输入文本框
        elif self.rev_tag == 0:
            self.pushButton_4.show()
            self.pushButton_7.hide()
            sql = "select 秘密等级,是否公开,紧急程度,处理结果,审核 from revfile where 序号 = %s" % self.xh_rev
            data = self.executeSql(sql)
            self.lineEdit_8.setText(data[0][0])  # 密级
            self.lineEdit_9.setText(data[0][1])  # 是否公开
            self.lineEdit_40.setText(data[0][2])  # 紧急程度
            self.lineEdit_48.setText(data[0][3])  # 处理结果
            self.lineEdit_49.setText(data[0][4])  # 审核

        # 表示收文已经完成批改,此时读取数据库,隐藏录入按钮
        elif self.rev_tag == 1:
            self.pushButton_4.hide()
            self.pushButton_7.show()
            sql = "select 批文收文时间,秘密等级,是否公开,紧急程度,批文来文单位,批文来文字号,批文标题,处理结果,审核,批文字号,批文承办处室,批文承办人,批文联系电话,内容摘要和拟办意见," \
                  "领导批示 from revfile where 序号 = %s" % self.xh_rev
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

    # 录入收文
    def insertRevFile(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
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

        if input10 != "":
            # 执行插入收文表
            sql = "insert into revfile(收文收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,收文标题,处理结果,审核,收文字号,收文承办处室,收文承办人,收文联系电话," \
                  "tag) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      input1, input2, input3, input4, input5, input6,
                      input7, input8, input9, input10, input11,
                      input12, input13, 0)
            self.executeSql(sql)

            # 找到当前收文的序号
            sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
            data = self.executeSql(sql)

            # 更新流程表,根据流程序号更新收文序号
            sql = "update bwprocess set 收文序号 = %s where 序号 = %s" % (data[0][0], self.xh)
            self.executeSql(sql)

            # 更新变量
            self.xh_rev = data[0][0]
            self.rev_tag = 0

            QtWidgets.QMessageBox.information(w, "提示", "录入成功！")

            # 重新展示收文界面
            self.displayRevFile()

        else:
            QtWidgets.QMessageBox.critical(w, "录入错误", "办文编号不能为空!")

    # 录入批文
    def insertRev2File(self):
        print("ok")
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        input1 = self.dateEdit_2.text()  # 批文收文时间
        input2 = self.lineEdit_41.text()  # 批文来文单位
        input3 = self.lineEdit_42.text()  # 批文来文字号
        input4 = self.lineEdit_43.text()  # 批文标题
        input5 = self.lineEdit_44.text()  # 批文编号
        input6 = self.textEdit_6.toPlainText()  # 内容摘要和拟办意见
        input7 = self.textEdit_7.toPlainText()  # 领导批示
        input8 = self.lineEdit_45.text()  # 批文承办处室
        input9 = self.lineEdit_46.text()  # 批文承办人
        input10 = self.lineEdit_47.text()  # 批文联系电话
        if input5 != "":
            sql = "update revfile set 批文收文时间 = '%s',批文来文单位 = '%s',批文来文字号 = '%s',批文标题 = '%s',批文字号 = '%s',内容摘要和拟办意见 = " \
                  "'%s',领导批示 = '%s',批文承办处室 = '%s',批文承办人 = '%s',批文联系电话 = '%s',tag = 1 where 序号 = %s" % (
                      input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, self.xh_rev)
            self.executeSql(sql)

            # 更新变量
            self.rev_tag = 1

            QtWidgets.QMessageBox.information(w, "提示", "录入成功！")

            # 重新展示批文界面
            self.displayRev2File()

        else:
            QtWidgets.QMessageBox.critical(w, "录入错误", "办文编号不能为空!")

    # 修改发文
    def updateSendFile(self, btname):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常
        if btname == "zb":
            input1 = self.lineEdit.text()  # 发文标题
            input2 = self.lineEdit_2.text()  # 报送范围
            input3 = self.lineEdit_4.text()  # 发文字号
            input4 = self.lineEdit_13.text()  # 紧急程度
            input5 = self.lineEdit_5.text()  # 秘密等级
            input6 = self.lineEdit_14.text()  # 是否公开
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

            if input3 != "":
                sql = "update sendfile set 发文标题 = '%s',报送范围 = '%s',发文字号 = '%s',紧急程度 = '%s',秘密等级 = '%s',是否公开 = '%s'," \
                      "拟稿人 = '%s',拟稿处室分管厅领导 = '%s',拟稿处室审核 = '%s',综合处编辑 = '%s',综合处审核 = '%s',秘书处审核 = '%s',综合处分管厅领导= '%s'," \
                      "审计办主任 = '%s',报文内容 = '%s',办文日期 = '%s' where 序号 = %s" % (
                          input1, input2, input3, input4, input5, input6, input7, input8, input9,
                          input10, input11, input12, input13, input14, input15, input16, self.xh_send)
                self.executeSql(sql)

                QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

                self.displaySendFile()
            else:
                QtWidgets.QMessageBox.critical(w, "修改错误", "发文字号不能为空!")

        elif btname == "gw":
            input1 = self.lineEdit_num.text()  # 发文字号
            input2 = self.lineEdit_num_3.text()  # 发文标题
            input3 = self.textEdit_2.toPlainText()  # 领导审核意见
            input4 = self.textEdit_4.toPlainText()  # 审计办领导审核意见
            input5 = self.textEdit_3.toPlainText()  # 办文情况说明和拟办意见
            input6 = self.lineEdit_file_3.text()  # 公文内容
            input7 = self.lineEdit_22.text()  # 秘密等级
            input8 = self.lineEdit_23.text()  # 是否公开
            input9 = self.lineEdit_29.text()  # 紧急程度
            input10 = self.lineEdit_24.text()  # 审核
            input11 = self.lineEdit_26.text()  # 承办处室
            input12 = self.lineEdit_27.text()  # 承办人
            input13 = self.lineEdit_28.text()  # 联系电话
            input14 = self.dateEdit_7.text()  # 办文日期
            # input15 = self.dateEdit_6.text()  # 日期
            # input16 = self.lineEdit_25.text()  # 办文编号

            if input1 != "":
                sql = "update sendfile set 发文字号 = '%s',发文标题 = '%s',领导审核意见 = '%s',审计办领导审核意见 = '%s',办文情况说明和拟办意见 = '%s'," \
                      "报文内容 = '%s',秘密等级 = '%s',是否公开 = '%s',紧急程度 = '%s',审核 = '%s',承办处室 = '%s',承办人 = '%s',联系电话 = '%s'," \
                      "办文日期 = '%s' where 序号 = %s" % (
                          input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11,
                          input12, input13, input14, self.xh_send)
                self.executeSql(sql)

                QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

                self.displaySendFile()
            else:
                QtWidgets.QMessageBox.critical(w, "修改错误", "发文字号不能为空!")

    # 修改收文
    def updateRevFile(self):
        print("暂未开发")

    # 修改批文
    def updateRev2File(self):
        print("暂未开发")
