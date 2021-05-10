import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.corfilebq import Ui_Dialog
from logis_fir.tools import tools


class Call_corfilebq(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = key  # 批文表主键

        # 初始化页面数据
        self.displayCorfilebqDetail()

        self.pushButton_revise.clicked.connect(self.reviseCorfilebqDetail)
        self.pushButton_quit.clicked.connect(self.closeWindow)

    def displayCorfilebqDetail(self):
        sql = "select 委办主任签批意见,批示任务办理要求时间,审计厅承办处室及承办人,办理结果,文件去向,起草处室 from corfile where 序号 = %s" % self.xh
        data = tools.executeSql(sql)
        self.lineEdit_1.setText(data[0][0])  # 委办主任签批意见
        if data[0][1] is None:
            self.dateEdit_1.setDate(datetime.datetime.now())
        else:
            self.dateEdit_1.setDate(QDate.fromString(data[0][1], 'yyyy/M/d'))  # 批示任务办理要求时间
        self.lineEdit_2.setText(data[0][2])  # 审计厅承办处室及承办人
        self.lineEdit_3.setText(data[0][3])  # 办理结果
        self.lineEdit_4.setText(data[0][4])  # 文件去向
        self.lineEdit_5.setText(data[0][5])  # 起草处室

    def reviseCorfilebqDetail(self):
        input1 = self.lineEdit_1.text()  # 委办主任签批意见
        input2 = self.dateEdit_1.text()  # 批示任务办理要求时间
        input3 = self.lineEdit_2.text()  # 审计厅承办处室及承办人
        input4 = self.lineEdit_3.text()  # 办理结果
        input5 = self.lineEdit_4.text()  # 文件去向
        input6 = self.lineEdit_5.text()  # 起草处室

        sql = "update corfile set 委办主任签批意见 = '%s',批示任务办理要求时间 = '%s',审计厅承办处室及承办人 = '%s',办理结果 = '%s',文件去向 = '%s'," \
              "起草处室 = '%s' where 序号 = %s" % (input1, input2, input3, input4, input5, input6, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "修改成功！")

        self.close()

    def closeWindow(self):
        self.close()
