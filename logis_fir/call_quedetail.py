from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.quedetail import Ui_Form

class Call_quedetail(QtWidgets.QWidget, Ui_Form):
    mydata = []
    def __init__(self,data):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton_4.clicked.connect(self.btfun1)
        self.commandLinkButton.clicked.connect(self.btfun2)
        self.commandLinkButton_2.clicked.connect(self.btfun3)
        self.commandLinkButton_3.clicked.connect(self.btfun4)
        self.mydata = data
        self.displayquedetail()

    def displayquedetail(self):
        # 被审计领导干部
        str1 = self.label_3.text()
        self.lineEdit.setText(self.mydata[0][0])

        # 所在地方或单位
        str2 = self.label_4.text()
        self.lineEdit_2.setText(self.mydata[0][1])

        # 出具审计报告时间
        str3 = self.label_8.text()
        self.dateEdit_2.setDate(QDate.fromString(self.mydata[0][2], 'yyyy/M/d'))

        # 审计组主审
        str4 = self.label_10.text()
        self.lineEdit_8.setText(self.mydata[0][3])

        # 审计组组长
        str5 = self.label_9.text()
        self.lineEdit_7.setText(self.mydata[0][4])

        # 发文字号
        str6 = self.label_5.text()
        self.lineEdit_3.setText(self.mydata[0][5])

        # 审计报告文号
        str7 = self.label_6.text()
        self.lineEdit_4.setText(self.mydata[0][6])

        # 问题描述
        str8 = self.label_11.text()
        self.lineEdit_9.setText(self.mydata[0][7])

    def btfun1(self):
        self.stackedWidget.setCurrentIndex(0)

    def btfun2(self):
        self.stackedWidget.setCurrentIndex(1)

    def btfun3(self):
        self.stackedWidget.setCurrentIndex(2)

    def btfun4(self):
        self.stackedWidget.setCurrentIndex(3)


