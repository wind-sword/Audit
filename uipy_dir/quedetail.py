# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quedetail.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1088, 633)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.line_2 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandLinkButton_4 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_4.setMinimumSize(QtCore.QSize(0, 60))
        self.commandLinkButton_4.setMaximumSize(QtCore.QSize(161, 60))
        self.commandLinkButton_4.setStyleSheet("font: 12pt \"Adobe Devanagari\";")
        self.commandLinkButton_4.setDescription("")
        self.commandLinkButton_4.setObjectName("commandLinkButton_4")
        self.horizontalLayout.addWidget(self.commandLinkButton_4)
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton_2.setMinimumSize(QtCore.QSize(180, 60))
        self.commandLinkButton_2.setMaximumSize(QtCore.QSize(161, 60))
        self.commandLinkButton_2.setStyleSheet("font: 12pt \"Adobe Devanagari\";")
        self.commandLinkButton_2.setDescription("")
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.horizontalLayout.addWidget(self.commandLinkButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.stackedWidget = QtWidgets.QStackedWidget(Form)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_info = QtWidgets.QWidget()
        self.page_info.setObjectName("page_info")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_info)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.page_info)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.page_info)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_2.addWidget(self.line_4, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.page_info)
        self.label_3.setMinimumSize(QtCore.QSize(200, 0))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_5 = QtWidgets.QLabel(self.page_info)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_7.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_7)
        self.gridLayout.addLayout(self.formLayout_5, 0, 1, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.page_info)
        self.label_4.setMinimumSize(QtCore.QSize(200, 0))
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)
        self.formLayout_11 = QtWidgets.QFormLayout()
        self.formLayout_11.setObjectName("formLayout_11")
        self.label_7 = QtWidgets.QLabel(self.page_info)
        self.label_7.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_8.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.formLayout_11.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_8)
        self.gridLayout.addLayout(self.formLayout_11, 1, 1, 1, 1)
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_6 = QtWidgets.QLabel(self.page_info)
        self.label_6.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.gridLayout.addLayout(self.formLayout_6, 2, 0, 1, 1)
        self.formLayout_12 = QtWidgets.QFormLayout()
        self.formLayout_12.setObjectName("formLayout_12")
        self.label_12 = QtWidgets.QLabel(self.page_info)
        self.label_12.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_9.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.formLayout_12.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_9)
        self.gridLayout.addLayout(self.formLayout_12, 2, 1, 1, 1)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_8 = QtWidgets.QLabel(self.page_info)
        self.label_8.setMinimumSize(QtCore.QSize(200, 0))
        self.label_8.setObjectName("label_8")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.dateEdit = QtWidgets.QDateEdit(self.page_info)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
        self.gridLayout.addLayout(self.formLayout_7, 3, 0, 1, 1)
        self.formLayout_13 = QtWidgets.QFormLayout()
        self.formLayout_13.setObjectName("formLayout_13")
        self.label_14 = QtWidgets.QLabel(self.page_info)
        self.label_14.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.formLayout_13.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_10.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.formLayout_13.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_10)
        self.gridLayout.addLayout(self.formLayout_13, 3, 1, 1, 1)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_9 = QtWidgets.QLabel(self.page_info)
        self.label_9.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.gridLayout.addLayout(self.formLayout_8, 4, 0, 1, 1)
        self.formLayout_14 = QtWidgets.QFormLayout()
        self.formLayout_14.setObjectName("formLayout_14")
        self.label_15 = QtWidgets.QLabel(self.page_info)
        self.label_15.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.formLayout_14.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_11.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.formLayout_14.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_11)
        self.gridLayout.addLayout(self.formLayout_14, 4, 1, 1, 1)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_10 = QtWidgets.QLabel(self.page_info)
        self.label_10.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.gridLayout.addLayout(self.formLayout_9, 5, 0, 1, 1)
        self.formLayout_15 = QtWidgets.QFormLayout()
        self.formLayout_15.setObjectName("formLayout_15")
        self.label_16 = QtWidgets.QLabel(self.page_info)
        self.label_16.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.formLayout_15.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_12.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.formLayout_15.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_12)
        self.gridLayout.addLayout(self.formLayout_15, 5, 1, 1, 1)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_11 = QtWidgets.QLabel(self.page_info)
        self.label_11.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.gridLayout.addLayout(self.formLayout_10, 6, 0, 1, 1)
        self.formLayout_16 = QtWidgets.QFormLayout()
        self.formLayout_16.setObjectName("formLayout_16")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.page_info)
        self.lineEdit_13.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.formLayout_16.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_13)
        self.label_17 = QtWidgets.QLabel(self.page_info)
        self.label_17.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.formLayout_16.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.gridLayout.addLayout(self.formLayout_16, 6, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_1 = QtWidgets.QPushButton(self.page_info)
        self.pushButton_1.setMinimumSize(QtCore.QSize(150, 28))
        self.pushButton_1.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_1.setObjectName("pushButton_1")
        self.horizontalLayout_2.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.page_info)
        self.pushButton_2.setMinimumSize(QtCore.QSize(150, 28))
        self.pushButton_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.page_info)
        self.pushButton_3.setMinimumSize(QtCore.QSize(150, 28))
        self.pushButton_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 18)
        self.gridLayout_2.setRowStretch(3, 1)
        self.stackedWidget.addWidget(self.page_info)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_13 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 2)
        self.line_3 = QtWidgets.QFrame(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_3.addWidget(self.line_3, 1, 0, 1, 3)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(15)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(14, item)
        self.gridLayout_3.addWidget(self.tableWidget_2, 2, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">问题详情</span></p></body></html>"))
        self.commandLinkButton_4.setText(_translate("Form", "问题基本信息"))
        self.commandLinkButton_2.setText(_translate("Form", "整改措施及进度"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">问题基本信息</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">被审计领导干部：</span></p></body></html>"))
        self.label_5.setText(_translate("Form", "问题一级分类："))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">所在地方或单位：</span></p></body></html>"))
        self.label_7.setText(_translate("Form", "问题二级分类："))
        self.label_6.setText(_translate("Form", "审计报告（意见）文号："))
        self.label_12.setText(_translate("Form", "问题三级分类："))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">出具审计报告时间：</span></p></body></html>"))
        self.label_14.setText(_translate("Form", "问题四级分类："))
        self.label_9.setText(_translate("Form", "审计组组长："))
        self.label_15.setText(_translate("Form", "备注(不在问题分类中的)："))
        self.label_10.setText(_translate("Form", "审计组主审："))
        self.label_16.setText(_translate("Form", "问题金额："))
        self.label_11.setText(_translate("Form", "问题描述："))
        self.label_17.setText(_translate("Form", "移送及处理情况："))
        self.pushButton_1.setText(_translate("Form", "修改"))
        self.pushButton_2.setText(_translate("Form", "确认"))
        self.pushButton_3.setText(_translate("Form", "取消"))
        self.label_13.setText(_translate("Form", "整改措施及进度："))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "整改责任部门"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "第几次上报"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Form", "应上报整改报告时间"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("Form", "实际上报整改报告时间"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("Form", "整改情况"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("Form", "已整改金额"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("Form", "追责问责人数"))
        item = self.tableWidget_2.horizontalHeaderItem(7)
        item.setText(_translate("Form", "推动制度建设个数"))
        item = self.tableWidget_2.horizontalHeaderItem(8)
        item.setText(_translate("Form", "推动制度建设（文件名称及文号）"))
        item = self.tableWidget_2.horizontalHeaderItem(9)
        item.setText(_translate("Form", "部分整改情况具体描述"))
        item = self.tableWidget_2.horizontalHeaderItem(10)
        item.setText(_translate("Form", "未整改原因说明"))
        item = self.tableWidget_2.horizontalHeaderItem(11)
        item.setText(_translate("Form", "下一步整改措施及时限"))
        item = self.tableWidget_2.horizontalHeaderItem(12)
        item.setText(_translate("Form", "整改情况"))
        item = self.tableWidget_2.horizontalHeaderItem(13)
        item.setText(_translate("Form", "整改金额"))
        item = self.tableWidget_2.horizontalHeaderItem(14)
        item.setText(_translate("Form", "整改率"))
