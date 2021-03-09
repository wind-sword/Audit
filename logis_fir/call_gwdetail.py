from PyQt5 import QtCore, QtWidgets
from uipy_dir.gwdetail import Ui_Form
from logis_fir.call_quedetail import Call_quedetail

class Call_gwdetail(QtWidgets.QWidget, Ui_Form):
    mydata = []
    def __init__(self,data):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(self.btnbasic)
        self.commandLinkButton_2.clicked.connect(self.btnpro)
        self.commandLinkButton_3.clicked.connect(self.btnimport)
        self.commandLinkButton_4.clicked.connect(self.btnelse)
        self.commandLinkButton_5.clicked.connect(self.btnanother)

        self.pushButton.clicked.connect(self.jumpqueview)
        self.tabWidget.setTabText(0, "问题浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.mydata = data
        self.display()

    # 关闭tab
    def mclose(self, index):
        self.tabWidget.removeTab(index)

    #跳转问题详情
    def jumpqueview(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择问题！")
        else:
            tab_new=Call_quedetail()
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new, "问题详情")
            self.tabWidget.setCurrentIndex(tab_num)

    #显示公文详情
    def display(self):
        str15 = self.label_num.text()  # 发文字号
        self.lineEdit_num.setText(self.mydata[0][2])

        str16 = self.label_num_3.text()  # 公文标题
        self.lineEdit_num_3.setText(self.mydata[0][14])

        str17 = self.label_num_4.text() # 领导审核意见
        self.textEdit_2.setText(self.mydata[0][15])

        str17 = self.label_num_5.text() # 审计办领导审核意见
        self.textEdit_4.setText(self.mydata[0][16])

        str17 = self.label_num_6.text() # 办文情况说明和拟办意见
        self.textEdit_3.setText(self.mydata[0][17])

    def btnbasic(self):
        self.stackedWidget.setCurrentIndex(0)

    def btnpro(self):
        self.stackedWidget.setCurrentIndex(2)

    def btnimport(self):
        self.stackedWidget.setCurrentIndex(3)

    def btnelse(self):
        self.stackedWidget.setCurrentIndex(1)

    def btnanother(self):
        self.stackedWidget.setCurrentIndex(4)