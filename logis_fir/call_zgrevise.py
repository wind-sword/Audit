from PyQt5 import QtWidgets

from uipy_dir.zgrevise import Ui_Form


class Call_zgrevise(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)