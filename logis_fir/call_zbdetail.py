from PyQt5 import QtCore, QtWidgets
from uipy_dir.zbdetail import Ui_Form

class Call_zbdetail(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        