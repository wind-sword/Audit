# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zbdetail.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 658)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_head = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_head.setFont(font)
        self.label_head.setObjectName("label_head")
        self.verticalLayout.addWidget(self.label_head)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton.sizePolicy().hasHeightForWidth())
        self.commandLinkButton.setSizePolicy(sizePolicy)
        self.commandLinkButton.setMinimumSize(QtCore.QSize(170, 66))
        self.commandLinkButton.setMaximumSize(QtCore.QSize(170, 66))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.commandLinkButton.setFont(font)
        self.commandLinkButton.setStyleSheet("font: 14pt \"Adobe Devanagari\";\n"
"")
        self.commandLinkButton.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.horizontalLayout.addWidget(self.commandLinkButton)
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_2.setMinimumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_2.setMaximumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_2.setStyleSheet("font: 14pt \"Adobe Devanagari\";")
        self.commandLinkButton_2.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.horizontalLayout.addWidget(self.commandLinkButton_2)
        self.commandLinkButton_3 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_3.setMinimumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_3.setMaximumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_3.setStyleSheet("font: 14pt \"Adobe Devanagari\";")
        self.commandLinkButton_3.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton_3.setObjectName("commandLinkButton_3")
        self.horizontalLayout.addWidget(self.commandLinkButton_3)
        self.commandLinkButton_4 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_4.setMinimumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_4.setMaximumSize(QtCore.QSize(170, 66))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.commandLinkButton_4.setFont(font)
        self.commandLinkButton_4.setStyleSheet("font: 14pt \"Adobe Devanagari\";")
        self.commandLinkButton_4.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton_4.setObjectName("commandLinkButton_4")
        self.horizontalLayout.addWidget(self.commandLinkButton_4)
        self.commandLinkButton_5 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_5.setMinimumSize(QtCore.QSize(170, 66))
        self.commandLinkButton_5.setMaximumSize(QtCore.QSize(170, 66))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.commandLinkButton_5.setFont(font)
        self.commandLinkButton_5.setStyleSheet("font: 14pt \"Adobe Devanagari\";")
        self.commandLinkButton_5.setIconSize(QtCore.QSize(40, 40))
        self.commandLinkButton_5.setObjectName("commandLinkButton_5")
        self.horizontalLayout.addWidget(self.commandLinkButton_5)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(4, 8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_basicinfo = QtWidgets.QWidget()
        self.page_basicinfo.setObjectName("page_basicinfo")
        self.pushButton_file = QtWidgets.QPushButton(self.page_basicinfo)
        self.pushButton_file.setGeometry(QtCore.QRect(489, 30, 121, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_file.sizePolicy().hasHeightForWidth())
        self.pushButton_file.setSizePolicy(sizePolicy)
        self.pushButton_file.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_file.setFont(font)
        self.pushButton_file.setObjectName("pushButton_file")
        self.lineEdit_file = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_file.setGeometry(QtCore.QRect(250, 30, 200, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_file.sizePolicy().hasHeightForWidth())
        self.lineEdit_file.setSizePolicy(sizePolicy)
        self.lineEdit_file.setMaximumSize(QtCore.QSize(200, 22))
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.label_4 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_4.setGeometry(QtCore.QRect(150, 180, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit.setGeometry(QtCore.QRect(260, 69, 661, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_10 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_10.setGeometry(QtCore.QRect(150, 320, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_12 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_12.setGeometry(QtCore.QRect(150, 350, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_8 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_8.setGeometry(QtCore.QRect(480, 270, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_9.setGeometry(QtCore.QRect(150, 290, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_file = QtWidgets.QLabel(self.page_basicinfo)
        self.label_file.setGeometry(QtCore.QRect(150, 30, 85, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_file.setFont(font)
        self.label_file.setObjectName("label_file")
        self.label_5 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_5.setGeometry(QtCore.QRect(480, 180, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 120, 661, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_6 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_6.setGeometry(QtCore.QRect(480, 220, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_7.setGeometry(QtCore.QRect(150, 260, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_14 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_14.setGeometry(QtCore.QRect(150, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label = QtWidgets.QLabel(self.page_basicinfo)
        self.label.setGeometry(QtCore.QRect(150, 70, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_15 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_15.setGeometry(QtCore.QRect(480, 380, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_16.setGeometry(QtCore.QRect(153, 121, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_17.setGeometry(QtCore.QRect(480, 320, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.page_basicinfo)
        self.label_18.setGeometry(QtCore.QRect(150, 380, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_4.setGeometry(QtCore.QRect(260, 180, 161, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_5.setGeometry(QtCore.QRect(260, 220, 161, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_8.setGeometry(QtCore.QRect(260, 260, 161, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_9.setGeometry(QtCore.QRect(260, 290, 161, 21))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_10.setGeometry(QtCore.QRect(260, 320, 161, 21))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_11.setGeometry(QtCore.QRect(260, 350, 161, 21))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_12.setGeometry(QtCore.QRect(260, 380, 161, 21))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_13.setGeometry(QtCore.QRect(580, 180, 161, 21))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_14.setGeometry(QtCore.QRect(580, 220, 161, 21))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_15.setGeometry(QtCore.QRect(670, 270, 161, 21))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_16.setGeometry(QtCore.QRect(650, 320, 161, 21))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.page_basicinfo)
        self.lineEdit_17.setGeometry(QtCore.QRect(670, 380, 161, 21))
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.stackedWidget.addWidget(self.page_basicinfo)
        self.page_relfile = QtWidgets.QWidget()
        self.page_relfile.setObjectName("page_relfile")
        self.label_11 = QtWidgets.QLabel(self.page_relfile)
        self.label_11.setGeometry(QtCore.QRect(30, 110, 52, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.page_relfile)
        self.lineEdit_6.setEnabled(True)
        self.lineEdit_6.setGeometry(QtCore.QRect(130, 110, 113, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_3 = QtWidgets.QLabel(self.page_relfile)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_fix2 = QtWidgets.QPushButton(self.page_relfile)
        self.pushButton_fix2.setGeometry(QtCore.QRect(260, 260, 71, 31))
        self.pushButton_fix2.setObjectName("pushButton_fix2")
        self.pushButton_save2 = QtWidgets.QPushButton(self.page_relfile)
        self.pushButton_save2.setGeometry(QtCore.QRect(250, 260, 91, 31))
        self.pushButton_save2.setObjectName("pushButton_save2")
        self.comboBox = QtWidgets.QComboBox(self.page_relfile)
        self.comboBox.setGeometry(QtCore.QRect(130, 70, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_19 = QtWidgets.QLabel(self.page_relfile)
        self.label_19.setGeometry(QtCore.QRect(30, 70, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.pushButton_save2_2 = QtWidgets.QPushButton(self.page_relfile)
        self.pushButton_save2_2.setGeometry(QtCore.QRect(370, 260, 91, 31))
        self.pushButton_save2_2.setObjectName("pushButton_save2_2")
        self.pushButton_fix2.raise_()
        self.label_11.raise_()
        self.lineEdit_6.raise_()
        self.label_3.raise_()
        self.pushButton_save2.raise_()
        self.comboBox.raise_()
        self.label_19.raise_()
        self.pushButton_save2_2.raise_()
        self.stackedWidget.addWidget(self.page_relfile)
        self.page_que = QtWidgets.QWidget()
        self.page_que.setObjectName("page_que")
        self.pushButton_queimport = QtWidgets.QPushButton(self.page_que)
        self.pushButton_queimport.setGeometry(QtCore.QRect(310, 320, 75, 23))
        self.pushButton_queimport.setObjectName("pushButton_queimport")
        self.label_2 = QtWidgets.QLabel(self.page_que)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.page_que)
        self.tableWidget.setGeometry(QtCore.QRect(50, 80, 561, 181))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.stackedWidget.addWidget(self.page_que)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label_13 = QtWidgets.QLabel(self.page)
        self.label_13.setGeometry(QtCore.QRect(30, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.stackedWidget.addWidget(self.page)
        self.page_piwen = QtWidgets.QWidget()
        self.page_piwen.setObjectName("page_piwen")
        self.label_20 = QtWidgets.QLabel(self.page_piwen)
        self.label_20.setGeometry(QtCore.QRect(20, 20, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.pushButton_save2_3 = QtWidgets.QPushButton(self.page_piwen)
        self.pushButton_save2_3.setGeometry(QtCore.QRect(260, 270, 91, 31))
        self.pushButton_save2_3.setObjectName("pushButton_save2_3")
        self.pushButton_save2_4 = QtWidgets.QPushButton(self.page_piwen)
        self.pushButton_save2_4.setGeometry(QtCore.QRect(370, 270, 91, 31))
        self.pushButton_save2_4.setObjectName("pushButton_save2_4")
        self.label_22 = QtWidgets.QLabel(self.page_piwen)
        self.label_22.setGeometry(QtCore.QRect(30, 120, 52, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.page_piwen)
        self.lineEdit_7.setEnabled(True)
        self.lineEdit_7.setGeometry(QtCore.QRect(130, 120, 113, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_21 = QtWidgets.QLabel(self.page_piwen)
        self.label_21.setGeometry(QtCore.QRect(30, 180, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.textEdit = QtWidgets.QTextEdit(self.page_piwen)
        self.textEdit.setGeometry(QtCore.QRect(130, 170, 431, 91))
        self.textEdit.setObjectName("textEdit")
        self.label_23 = QtWidgets.QLabel(self.page_piwen)
        self.label_23.setGeometry(QtCore.QRect(300, 120, 54, 12))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_piwen)
        self.lineEdit_3.setGeometry(QtCore.QRect(370, 120, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_save2_5 = QtWidgets.QPushButton(self.page_piwen)
        self.pushButton_save2_5.setGeometry(QtCore.QRect(260, 270, 91, 31))
        self.pushButton_save2_5.setObjectName("pushButton_save2_5")
        self.stackedWidget.addWidget(self.page_piwen)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 18)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_head.setText(_translate("Form", "专报项目详情"))
        self.commandLinkButton.setText(_translate("Form", "项目报文导入"))
        self.commandLinkButton.setDescription(_translate("Form", "已完成"))
        self.commandLinkButton_2.setText(_translate("Form", "项目问题表导入"))
        self.commandLinkButton_2.setDescription(_translate("Form", "未完成"))
        self.commandLinkButton_3.setText(_translate("Form", "信息采集补全"))
        self.commandLinkButton_3.setDescription(_translate("Form", "未完成"))
        self.commandLinkButton_4.setText(_translate("Form", "收文录入"))
        self.commandLinkButton_4.setDescription(_translate("Form", "未完成"))
        self.commandLinkButton_5.setText(_translate("Form", "批文录入"))
        self.commandLinkButton_5.setDescription(_translate("Form", "未完成"))
        self.pushButton_file.setText(_translate("Form", "选择文件"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">发文字号：</span></p></body></html>"))
        self.label_10.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处编辑：</span></p></body></html>"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处审核：</span></p></body></html>"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿处室分管厅领导：</span></p></body></html>"))
        self.label_9.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿处室：</span></p></body></html>"))
        self.label_file.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">报文文件：</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">紧急程度：</span></p></body></html>"))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">是否公开：</span></p></body></html>"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿人：</span></p></body></html>"))
        self.label_14.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">秘密等级：</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">专报标题：</span></p></body></html>"))
        self.label_15.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">审计办主任（厅长）：</span></p></body></html>"))
        self.label_16.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">报送范围：</span></p></body></html>"))
        self.label_17.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处分管厅领导：</span></p></body></html>"))
        self.label_18.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#ff0000;\">秘书处审核：</span></p></body></html>"))
        self.label_11.setText(_translate("Form", "收文号："))
        self.lineEdit_6.setText(_translate("Form", "情字收文1"))
        self.label_3.setText(_translate("Form", "收文信息"))
        self.pushButton_fix2.setText(_translate("Form", "修改"))
        self.pushButton_save2.setText(_translate("Form", "保存"))
        self.comboBox.setItemText(0, _translate("Form", "情字"))
        self.comboBox.setItemText(1, _translate("Form", "请字"))
        self.label_19.setText(_translate("Form", "收文类型："))
        self.pushButton_save2_2.setText(_translate("Form", "撤销"))
        self.pushButton_queimport.setText(_translate("Form", "导入问题表"))
        self.label_2.setText(_translate("Form", "问题列表"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "问题id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "整改意见"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "整改措施"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "责任部门"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "整改进度"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "完成情况"))
        self.label_13.setText(_translate("Form", "信息补全"))
        self.label_20.setText(_translate("Form", "批文信息"))
        self.pushButton_save2_3.setText(_translate("Form", "修改"))
        self.pushButton_save2_4.setText(_translate("Form", "撤销"))
        self.label_22.setText(_translate("Form", "批文号："))
        self.lineEdit_7.setText(_translate("Form", "测试批文号1"))
        self.label_21.setText(_translate("Form", "批文内容："))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">责令部门整改</p></body></html>"))
        self.label_23.setText(_translate("Form", "批示人："))
        self.lineEdit_3.setText(_translate("Form", "某某某"))
        self.pushButton_save2_5.setText(_translate("Form", "保存"))