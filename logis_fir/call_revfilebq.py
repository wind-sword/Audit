import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.revfilebq import Ui_Dialog
from logis_fir.tools import tools


class Call_revfilebq(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = key  # 收文表主键

        # 初始化页面数据
        self.displayRevfilebqDetail()

        self.pushButton_revise.clicked.connect(self.reviseRevfilebqDetail)
        self.pushButton_quit.clicked.connect(self.closeWindow)

    def displayRevfilebqDetail(self):
        sql = "select 要求时间,文件去向 from revfile where 序号 = %s" % self.xh
        data = tools.executeSql(sql)
        if data[0][0] is None:
            self.dateEdit_1.setDate(datetime.datetime.now())
        else:
            self.dateEdit_1.setDate(QDate.fromString(data[0][0], 'yyyy/MM/dd'))
        self.lineEdit_1.setText(data[0][1])

    def reviseRevfilebqDetail(self):
        input1 = self.dateEdit_1.text()
        input2 = self.lineEdit_1.text()

        sql = "update revfile set 要求时间 = '%s',文件去向 = '%s' where 序号 = %s" % (input1, input2, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(None, "提示", "修改成功！")

        self.close()

    def closeWindow(self):
        self.close()
