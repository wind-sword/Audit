import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

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
        self.cast(k1, k2)

        # 初始化页面展示
        self.screenView()
        # 初始化页面数据
        if self.xh_send != -1:
            self.displaySendfile()
        elif self.xh_send == -1 and self.xh_rev != -1:
            self.displayRevfile()

        print("当前流程序号:%s" % self.xh)
        print("当前发文序号:%s" % self.xh_send)
        print("当前收文序号:%s" % self.xh_rev)
        print("当前发文类型:%s" % self.send_type)
        print("当前收文批改情况:%s\n" % self.rev_tag)

        self.insertOrUpdate()

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
            self.displaySendfile()
        if btname == "2":
            self.stackedWidget.setCurrentIndex(2)
            self.displayRevfile()
        if btname == "3":
            self.stackedWidget.setCurrentIndex(3)
            self.displayRev2file()

    # 绑定添加修改按钮
    def insertOrUpdate(self):
        self.pushButton_3.clicked.connect(self.insertRevFile)
        self.pushButton_4.clicked.connect(self.insertRev2File)

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
    def displaySendfile(self):
        if self.xh_send != -1:
            sql = "select 专报标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
                  "公文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
                  "序号 =  %s" % self.xh_send
            data = self.executeSql(sql)
            # print(data)
            # 专报类型
            if self.send_type == 1:
                self.lineEdit.setText(data[0][0])  # 专报标题
                self.lineEdit_2.setText(data[0][1])  # 报送范围
                self.lineEdit_4.setText(data[0][2])  # 发文字号
                self.lineEdit_13.setText(data[0][3])  # 紧急程度
                self.lineEdit_5.setText(data[0][4])  # 秘密等级
                self.lineEdit_14.setText(data[0][5])  # 是否公开
                self.lineEdit_8.setText(data[0][6])  # 拟稿人
                self.lineEdit_15.setText(data[0][7])  # 拟稿处室分管厅领导
                self.lineEdit_9.setText(data[0][8])  # 拟稿处室
                self.lineEdit_10.setText(data[0][9])  # 综合处编辑
                self.lineEdit_11.setText(data[0][10])  # 综合处审核
                self.lineEdit_12.setText(data[0][11])  # 秘书处审核
                self.lineEdit_16.setText(data[0][12])  # 综合处分管厅领导
                self.lineEdit_17.setText(data[0][13])  # 审计办主任
                self.lineEdit_file.setText(data[0][19])  # 报文内容
                self.dateEdit.setDate(QDate.fromString(data[0][24], 'yyyy/M/d'))  # 办文日期

            # 公文类型
            elif self.send_type == 2:
                self.lineEdit_num.setText(data[0][2])  # 发文字号
                self.lineEdit_num_3.setText(data[0][14])  # 公文标题
                self.textEdit_2.setText(data[0][15])  # 领导审核意见
                self.textEdit_4.setText(data[0][16])  # 审计办领导审核意见
                self.textEdit_3.setText(data[0][17])  # 办文情况说明和拟办意见
                self.lineEdit_file_3.setText(data[0][19])  # 公文内容
                self.lineEdit_22.setText(data[0][4])  # 保密等级
                self.lineEdit_23.setText(data[0][5])  # 是否公开
                self.lineEdit_29.setText(data[0][3])  # 紧急程度
                self.lineEdit_24.setText(data[0][20])  # 审核
                self.lineEdit_26.setText(data[0][21])  # 承办处室
                self.lineEdit_27.setText(data[0][22])  # 承办人
                self.lineEdit_28.setText(data[0][23])  # 联系电话
                self.dateEdit_7.setDate(QDate.fromString(data[0][24], 'yyyy/M/d'))  # 办文日期
                self.dateEdit_6.setDate(QDate.fromString(data[0][24], 'yyyy/M/d'))  # 日期
                self.lineEdit_25.setText(data[0][2])  # 办文编号

    # 展示收文页面
    def displayRevfile(self):
        # 收文表本来就存在,此时读数据库,隐藏新增收文按钮,修改按钮暂未实现
        if self.xh_rev != -1:
            sql = "select 收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,文件标题,处理结果,审核,收文字号,承办处室,承办人,联系电话 from revfile where 序号 = %s" % self.xh_rev
            data = self.executeSql(sql)
            self.pushButton_3.hide()
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

        # 收文表本来不存在,但是发文表存在,此时应该继承发文表中已有内容
        elif self.xh_rev == -1 and self.xh_send != -1:
            # 继承专报字段,此处重新查询发文字段是为了防止:用户如果修改发文界面输入文本而没有保存此次修改的话,收文表字段会错误继承用户修改的字段内容,因为此时数据库中并没有提交修改
            sql = "select 专报标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任," \
                  "公文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,projectType,报文内容,审核,承办处室,承办人,联系电话,办文日期 from sendfile where " \
                  "序号 =  %s" % self.xh_send
            data = self.executeSql(sql)
            if self.send_type == 1:
                self.lineEdit_6.setText(data[0][4])  # 密级
                self.lineEdit_7.setText(data[0][5])  # 是否公开
                self.lineEdit_36.setText(data[0][3])  # 紧急程度
                self.lineEdit_37.setText(data[0][2])  # 来文字号
                self.lineEdit_35.setText(data[0][0])  # 文件标题
            # 继承公文字段
            elif self.send_type == 2:
                self.lineEdit_6.setText(data[0][4])  # 密级
                self.lineEdit_7.setText(data[0][5])  # 是否公开
                self.lineEdit_36.setText(data[0][3])  # 紧急程度
                self.lineEdit_35.setText(data[0][14])  # 公文标题
                self.lineEdit_37.setText(data[0][2])  # 来文字号
                self.lineEdit_34.setText(data[0][21])  # 承办处室
                self.lineEdit_32.setText(data[0][22])  # 承办人
                self.lineEdit_39.setText(data[0][23])  # 联系电话

    # 展示批文页面
    def displayRev2file(self):
        # 表示收文还没有录入,此时展示空页面
        if self.rev_tag == -1:
            pass
        # 表示收文还没有批示,此时继承收文的必要字段,按照收文继承发文的逻辑,应该读数据库,而不是复制收文前端的输入文本框
        elif self.rev_tag == 0:
            sql = "select 收文时间,秘密等级,是否公开,紧急程度,文件标题,处理结果,审核,承办处室,承办人,联系电话 from revfile where 序号 = %s" % self.xh_rev
            data = self.executeSql(sql)
            self.dateEdit_2.setDate(QDate.fromString(data[0][0], 'yyyy/M/d'))  # 收文时间
            self.lineEdit_8.setText(data[0][1])  # 密级
            self.lineEdit_9.setText(data[0][2])  # 是否公开
            self.lineEdit_40.setText(data[0][3])  # 紧急程度
            self.lineEdit_43.setText(data[0][4])  # 文件标题
            self.lineEdit_48.setText(data[0][5])  # 处理结果
            self.lineEdit_49.setText(data[0][6])  # 审核
            self.lineEdit_45.setText(data[0][7])  # 承办处室
            self.lineEdit_46.setText(data[0][8])  # 承办人
            self.lineEdit_47.setText(data[0][9])  # 联系电话

        # 表示收文已经完成批改,此时读取数据库,隐藏录入按钮
        elif self.rev_tag == 1:
            self.pushButton_4.hide()
            sql = "select 收文时间,秘密等级,是否公开,紧急程度,批文来文单位,批文来文字号,文件标题,处理结果,审核,批文字号,承办处室,承办人,联系电话,内容摘要和拟办意见,领导批示 from " \
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

    # 录入收文
    def insertRevFile(self):
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
            sql = "insert into revfile(收文时间,秘密等级,是否公开,紧急程度,收文来文单位,收文来文字号,文件标题,处理结果,审核,收文字号,承办处室,承办人,联系电话,tag) values(" \
                  "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      input1, input2, input3, input4, input5, input6,
                      input7, input8, input9, input10, input11,
                      input12, input13, 0)
            self.executeSql(sql)

            # 找到当前收文的序号
            sql = "select 序号 from revfile where 收文字号 = '%s'" % input10
            data = self.executeSql(sql)

            # 更新流程表,根据流程序号更新收文序号
            sql = "update bwprocess set 收文序号 = '%s' where 序号 = '%s'" % (data[0][0], self.xh)
            self.executeSql(sql)

            # 更新变量
            self.xh_rev = data[0][0]
            self.rev_tag = 0

            QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

            # 重新展示收文界面
            self.displayRevfile()

        else:
            QtWidgets.QMessageBox.information(self, "提示", "办文编号不能为空!")

    # 录入批文
    def insertRev2File(self):
        input1 = self.lineEdit_41.text()  # 批文来文单位
        input2 = self.lineEdit_42.text()  # 批文来文字号
        input3 = self.lineEdit_44.text()  # 批文编号
        input4 = self.textEdit_6.toPlainText()  # 内容摘要和拟办意见
        input5 = self.textEdit_7.toPlainText()  # 领导批示
        if input3 != "":
            sql = "update revfile set 批文来文单位 = '%s',批文来文字号 = '%s',批文字号 = '%s',内容摘要和拟办意见 = '%s',领导批示 = '%s',tag = 1 " \
                  "where 序号 = %s" % (input1, input2, input3, input4, input5, self.xh_rev)
            self.executeSql(sql)

            # 更新变量
            self.rev_tag = 1

            QtWidgets.QMessageBox.information(self, "提示", "录入成功！")

            # 重新展示批文界面
            self.displayRevfile()

        else:
            QtWidgets.QMessageBox.information(self, "提示", "办文编号不能为空!")
