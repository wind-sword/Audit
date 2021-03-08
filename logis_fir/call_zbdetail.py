from PyQt5 import QtCore, QtWidgets
from uipy_dir.zbdetail import Ui_Form

class Call_zbdetail(QtWidgets.QWidget,Ui_Form):
    mydata = []
    def __init__(self,data):
        super().__init__()
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(self.btnbasic)
        self.commandLinkButton_2.clicked.connect(self.btnpro)
        self.commandLinkButton_3.clicked.connect(self.btnimport)
        self.commandLinkButton_4.clicked.connect(self.btnelse)
        self.commandLinkButton_5.clicked.connect(self.btnanother)
        self.mydata = data
        self.display()

    #展示项目报文详情
    def display(self):
        str1 = self.label.text()  # 专报标题
        self.lineEdit.setText(self.mydata[0][0])

        str2 = self.label_16.text()  # 专报标题
        self.lineEdit_2.setText(self.mydata[0][1])

        str3 = self.label_4.text()#发文字号
        self.lineEdit_4.setText(self.mydata[0][2])

        str4 = self.label_5.text()#紧急程度
        self.lineEdit_13.setText(self.mydata[0][3])

        str5 = self.label_14.text()#秘密等级
        self.lineEdit_5.setText(self.mydata[0][4])

        str6 = self.label_6.text()#是否公开
        self.lineEdit_14.setText(self.mydata[0][5])

        str7 = self.label_7.text()#拟稿人
        self.lineEdit_8.setText(self.mydata[0][6])

        str8 = self.label_8.text()#拟稿处室分管厅领导
        self.lineEdit_15.setText(self.mydata[0][7])

        str9 = self.label_9.text()#拟稿处室
        self.lineEdit_9.setText(self.mydata[0][8])

        str10 = self.label_10.text()#综合处编辑
        self.lineEdit_10.setText(self.mydata[0][9])

        str11 = self.label_12.text()#综合处审核
        self.lineEdit_11.setText(self.mydata[0][10])

        str12 = self.label_18.text()#秘书处审核
        self.lineEdit_12.setText(self.mydata[0][11])

        str13 = self.label_17.text()#综合处分管厅领导
        self.lineEdit_16.setText(self.mydata[0][12])

        str14 = self.label_15.text()#审计办主任
        self.lineEdit_17.setText(self.mydata[0][13])

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