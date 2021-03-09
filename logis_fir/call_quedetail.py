from PyQt5 import QtCore, QtWidgets
from uipy_dir.quedetail import Ui_Form

class Call_quedetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

