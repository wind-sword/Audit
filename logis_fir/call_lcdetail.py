from PyQt5 import QtWidgets

from uipy_dir.lcdetail import Ui_Form

class Call_lcdetail(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(lambda:self.btjump(btname="0"))
        self.commandLinkButton_2.clicked.connect(lambda:self.btjump(btname="2"))
        self.commandLinkButton_3.clicked.connect(lambda:self.btjump(btname="3"))

    # 按钮跳转
    def btjump(self, btname):
        if btname == "0":
            self.stackedWidget.setCurrentIndex(0)
        if btname == "1":
            self.stackedWidget.setCurrentIndex(2)
        if btname == "2":
            self.stackedWidget.setCurrentIndex(3)
