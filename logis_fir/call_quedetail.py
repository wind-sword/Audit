from PyQt5 import QtWidgets
from uipy_dir.quedetail import Ui_Form

class Call_quedetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton_4.clicked.connect(self.btfun1)
        self.commandLinkButton.clicked.connect(self.btfun2)
        self.commandLinkButton_2.clicked.connect(self.btfun3)
        self.commandLinkButton_3.clicked.connect(self.btfun4)

    def btfun1(self):
        self.stackedWidget.setCurrentIndex(0)

    def btfun2(self):
        self.stackedWidget.setCurrentIndex(1)

    def btfun3(self):
        self.stackedWidget.setCurrentIndex(2)

    def btfun4(self):
        self.stackedWidget.setCurrentIndex(3)


