# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'revfilebq.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1017, 699)
        Dialog.setStyleSheet("QComboBox{\n"
"    background:white;\n"
"    border:1px solid gray;\n"
"    width:300px;\n"
"    border-radius:10px;\n"
"    padding:2px 4px;\n"
"}\n"
"QLineEdit{\n"
"    border:1px solid gray;\n"
"    width:300px;\n"
"    border-radius:10px;\n"
"    padding:2px 4px;\n"
"}\n"
"QPushButton{  \n"
"    border: 1px solid #C0C0C0;  \n"
"    background-color:#FFFFFF;  \n"
"    border-style: solid;  \n"
"    border-radius:0px;  \n"
"    width: 100px;  \n"
"    height:20px;  \n"
"    padding:0 0px;  \n"
"} \n"
"QPushButton:hover{     \n"
"    border: 1px solid #E3C46F;  \n"
"    background-color:#FEF4BF;  \n"
"    border-style: solid;  \n"
"    border-radius:2px;  \n"
"    width: 40px;  \n"
"    height:20px;  \n"
"    padding:0 0px;  \n"
"}\n"
"QPushButton:pressed{  \n"
"    background-color:#EAF0FF;  \n"
"    border: 1px solid #AAB4C4;  \n"
"    width: 40px;  \n"
"    height:20px;  \n"
"    padding:0 0px;  \n"
"    border-radius:1px;  \n"
"} ")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_1 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.verticalLayout.addWidget(self.label_1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(200, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dateEdit_1 = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_1.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dateEdit_1.setFont(font)
        self.dateEdit_1.setCalendarPopup(True)
        self.dateEdit_1.setObjectName("dateEdit_1")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dateEdit_1)
        self.verticalLayout.addLayout(self.formLayout_3)
        self.formLayout_1 = QtWidgets.QFormLayout()
        self.formLayout_1.setObjectName("formLayout_1")
        self.label_3 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout_1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_1 = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_1.setFont(font)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.formLayout_1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_1)
        self.verticalLayout.addLayout(self.formLayout_1)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.pushButton_revise = QtWidgets.QPushButton(Dialog)
        self.pushButton_revise.setMinimumSize(QtCore.QSize(150, 28))
        self.pushButton_revise.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_revise.setFont(font)
        self.pushButton_revise.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_revise.setObjectName("pushButton_revise")
        self.horizontalLayout_1.addWidget(self.pushButton_revise)
        self.pushButton_quit = QtWidgets.QPushButton(Dialog)
        self.pushButton_quit.setMinimumSize(QtCore.QSize(150, 28))
        self.pushButton_quit.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_quit.setFont(font)
        self.pushButton_quit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.horizontalLayout_1.addWidget(self.pushButton_quit)
        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_1.setText(_translate("Dialog", "收文补全："))
        self.label_2.setText(_translate("Dialog", "要求时间："))
        self.dateEdit_1.setDisplayFormat(_translate("Dialog", "yyyy/MM/dd"))
        self.label_3.setText(_translate("Dialog", "文件去向："))
        self.pushButton_revise.setText(_translate("Dialog", "确认"))
        self.pushButton_quit.setText(_translate("Dialog", "退出"))

