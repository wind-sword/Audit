import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.instbq import Ui_Dialog
from logis_fir.tools import tools


class Call_instbq(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = key  # 整改表主键

        # 初始化页面数据
        self.displayInstbqDetail()

        self.pushButton_revise.clicked.connect(self.reviseInstbqDetail)
        self.pushButton_quit.clicked.connect(self.closeWindow)

    def displayInstbqDetail(self):
        sql = "select 领导姓名,领导职务,批示时间 from instruction where 序号 = %s" % self.xh
        data = tools.executeSql(sql)

        self.lineEdit_1.setText(data[0][0])  # 领导姓名
        self.lineEdit_2.setText(data[0][1])  # 领导职务
        if data[0][2] is None:
            self.dateEdit.setDate(datetime.datetime.now())
        else:
            self.dateEdit.setDate(QDate.fromString(data[0][2], 'yyyy/MM/dd'))  # 批示时间

    def reviseInstbqDetail(self):
        input1 = self.lineEdit_1.text()  # 领导姓名
        input2 = self.lineEdit_2.text()  # 领导职务
        input3 = self.dateEdit.text()  # 批示时间

        sql = "update instruction set 领导姓名 = '%s',领导职务 = '%s',批示时间 = '%s' where 序号 = %s" % (
            input1, input2, input3, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(None, "提示", "修改成功！")

        self.close()

    def closeWindow(self):
        self.close()
