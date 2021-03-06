# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_indexWindow(object):
    def setupUi(self, indexWindow):
        indexWindow.setObjectName("indexWindow")
        indexWindow.resize(1366, 767)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(indexWindow.sizePolicy().hasHeightForWidth())
        indexWindow.setSizePolicy(sizePolicy)
        indexWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(indexWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_menu = QtWidgets.QWidget(self.centralwidget)
        self.widget_menu.setStyleSheet("QPushButton{border:none;color:white;}\n"
"QPushButton#btprog,#btanaly{\n"
"        border:none;\n"
"        border-bottom:1px solid white;\n"
"        font-size:24px;\n"
"        font-weight:700;\n"
"        font-family: \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n"
"    }\n"
"QPushButton#btproview,#btproadd,#btanalytemp,#btansear, :hover{border-left:4px solid red;font-weight:700;font-size:18px;}\n"
"QWidget#widget_menu{\n"
"    background:gray;\n"
"    border-top:1px solid white;\n"
"    border-bottom:1px solid white;\n"
"    border-left:1px solid white;\n"
"    border-top-left-radius:10px;\n"
"    border-bottom-left-radius:10px;\n"
"}")
        self.widget_menu.setObjectName("widget_menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_menu)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headwidget = QtWidgets.QWidget(self.widget_menu)
        self.headwidget.setStyleSheet("image: url(../resource_dir/logo.png);")
        self.headwidget.setObjectName("headwidget")
        self.verticalLayout_2.addWidget(self.headwidget)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.btprog = QtWidgets.QPushButton(self.widget_menu)
        self.btprog.setObjectName("btprog")
        self.verticalLayout.addWidget(self.btprog)
        self.btproview = QtWidgets.QPushButton(self.widget_menu)
        self.btproview.setObjectName("btproview")
        self.verticalLayout.addWidget(self.btproview)
        self.btproadd = QtWidgets.QPushButton(self.widget_menu)
        self.btproadd.setObjectName("btproadd")
        self.verticalLayout.addWidget(self.btproadd)
        self.btanaly = QtWidgets.QPushButton(self.widget_menu)
        self.btanaly.setObjectName("btanaly")
        self.verticalLayout.addWidget(self.btanaly)
        self.btansear = QtWidgets.QPushButton(self.widget_menu)
        self.btansear.setObjectName("btansear")
        self.verticalLayout.addWidget(self.btansear)
        self.btanalytemp = QtWidgets.QPushButton(self.widget_menu)
        self.btanalytemp.setObjectName("btanalytemp")
        self.verticalLayout.addWidget(self.btanalytemp)
        self.verticalLayout_space = QtWidgets.QVBoxLayout()
        self.verticalLayout_space.setObjectName("verticalLayout_space")
        self.emptywidget = QtWidgets.QWidget(self.widget_menu)
        self.emptywidget.setObjectName("emptywidget")
        self.verticalLayout_space.addWidget(self.emptywidget)
        self.verticalLayout.addLayout(self.verticalLayout_space)
        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 2)
        self.verticalLayout.setStretch(5, 1)
        self.verticalLayout.setStretch(6, 1)
        self.verticalLayout.setStretch(7, 8)
        self.gridLayout.addWidget(self.widget_menu, 0, 0, 1, 1)
        self.widget_view = QtWidgets.QWidget(self.centralwidget)
        self.widget_view.setStyleSheet("QWidget#widget_view{\n"
"        color:#232C51;\n"
"        background:white;\n"
"        border-top:1px solid darkGray;\n"
"        border-bottom:1px solid darkGray;\n"
"        border-right:1px solid darkGray;\n"
"        border-top-right-radius:10px;\n"
"        border-bottom-right-radius:10px;\n"
"    }\n"
"")
        self.widget_view.setObjectName("widget_view")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_view)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_view)
        self.stackedWidget.setStyleSheet("QStackedWidget#stackedWidget{\n"
"        color:#232C51;\n"
"        background:white;\n"
"    }\n"
"QWidget#page_view,#page_add{\n"
"        color:#232C51;\n"
"        background:white;\n"
"    }\n"
"QPushButton{\n"
"       background:white;\n"
"        border:1px solid gray;\n"
"        width:300px;\n"
"        border-radius:10px;\n"
"        padding:2px 4px;\n"
"}\n"
"QLineEdit{\n"
"        border:1px solid gray;\n"
"        width:300px;\n"
"        border-radius:10px;\n"
"        padding:2px 4px;\n"
"}\n"
"QComboBox{background:white;\n"
"        border:1px solid gray;\n"
"        width:300px;\n"
"        border-radius:10px;\n"
"        padding:2px 4px;\n"
"}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidgetPage1 = QtWidgets.QWidget()
        self.stackedWidgetPage1.setObjectName("stackedWidgetPage1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.stackedWidgetPage1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.stackedWidgetPage1)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_vhead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_vhead.setFont(font)
        self.label_vhead.setObjectName("label_vhead")
        self.verticalLayout_4.addWidget(self.label_vhead)
        self.line = QtWidgets.QFrame(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_key = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_key.setFont(font)
        self.label_key.setObjectName("label_key")
        self.horizontalLayout.addWidget(self.label_key)
        self.lineEdit4search = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit4search.sizePolicy().hasHeightForWidth())
        self.lineEdit4search.setSizePolicy(sizePolicy)
        self.lineEdit4search.setMinimumSize(QtCore.QSize(150, 22))
        self.lineEdit4search.setMaximumSize(QtCore.QSize(150, 22))
        self.lineEdit4search.setStyleSheet("QLineEdit{\n"
"        border:1px solid gray;\n"
"        width:300px;\n"
"        border-radius:10px;\n"
"        padding:2px 4px;\n"
"}")
        self.lineEdit4search.setObjectName("lineEdit4search")
        self.horizontalLayout.addWidget(self.lineEdit4search)
        spacerItem = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_tip1 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tip1.setFont(font)
        self.label_tip1.setObjectName("label_tip1")
        self.horizontalLayout.addWidget(self.label_tip1)
        self.dateEdit = QtWidgets.QDateEdit(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout.addWidget(self.dateEdit)
        self.label_tip2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tip2.setFont(font)
        self.label_tip2.setObjectName("label_tip2")
        self.horizontalLayout.addWidget(self.label_tip2)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit_2.setFont(font)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.horizontalLayout.addWidget(self.dateEdit_2)
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.bt_search = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_search.sizePolicy().hasHeightForWidth())
        self.bt_search.setSizePolicy(sizePolicy)
        self.bt_search.setMinimumSize(QtCore.QSize(200, 22))
        self.bt_search.setMaximumSize(QtCore.QSize(200, 22))
        self.bt_search.setObjectName("bt_search")
        self.horizontalLayout.addWidget(self.bt_search)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 5)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(4, 2)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(6, 2)
        self.horizontalLayout.setStretch(7, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_more = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_more.sizePolicy().hasHeightForWidth())
        self.pushButton_more.setSizePolicy(sizePolicy)
        self.pushButton_more.setMaximumSize(QtCore.QSize(150, 22))
        self.pushButton_more.setObjectName("pushButton_more")
        self.horizontalLayout_2.addWidget(self.pushButton_more)
        self.pushButton_del = QtWidgets.QPushButton(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_del.sizePolicy().hasHeightForWidth())
        self.pushButton_del.setSizePolicy(sizePolicy)
        self.pushButton_del.setMaximumSize(QtCore.QSize(150, 22))
        self.pushButton_del.setObjectName("pushButton_del")
        self.horizontalLayout_2.addWidget(self.pushButton_del)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 8)
        self.verticalLayout_4.setStretch(4, 2)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.stackedWidgetPage2 = QtWidgets.QWidget()
        self.stackedWidgetPage2.setObjectName("stackedWidgetPage2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.stackedWidgetPage2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_nh = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_nh.setFont(font)
        self.label_nh.setObjectName("label_nh")
        self.gridLayout_2.addWidget(self.label_nh, 2, 1, 1, 1)
        self.label_type = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")
        self.gridLayout_2.addWidget(self.label_type, 4, 1, 1, 1)
        self.label_nhead = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_nhead.setFont(font)
        self.label_nhead.setObjectName("label_nhead")
        self.gridLayout_2.addWidget(self.label_nhead, 0, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.stackedWidgetPage2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_2.addWidget(self.line_4, 5, 0, 1, 5)
        self.label_time = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_time.setFont(font)
        self.label_time.setObjectName("label_time")
        self.gridLayout_2.addWidget(self.label_time, 3, 1, 1, 1)
        self.label_nr = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_nr.setFont(font)
        self.label_nr.setObjectName("label_nr")
        self.gridLayout_2.addWidget(self.label_nr, 2, 2, 1, 1)
        self.comboBox_type = QtWidgets.QComboBox(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBox_type.setFont(font)
        self.comboBox_type.setStyleSheet("")
        self.comboBox_type.setObjectName("comboBox_type")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_type, 4, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.stackedWidgetPage2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 5)
        self.label_tmres = QtWidgets.QLabel(self.stackedWidgetPage2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_tmres.setFont(font)
        self.label_tmres.setObjectName("label_tmres")
        self.gridLayout_2.addWidget(self.label_tmres, 3, 2, 1, 1)
        self.stackedWidget_new = QtWidgets.QStackedWidget(self.stackedWidgetPage2)
        self.stackedWidget_new.setObjectName("stackedWidget_new")
        self.page_zb = QtWidgets.QWidget()
        self.page_zb.setObjectName("page_zb")
        self.label = QtWidgets.QLabel(self.page_zb)
        self.label.setGeometry(QtCore.QRect(170, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_file = QtWidgets.QPushButton(self.page_zb)
        self.pushButton_file.setGeometry(QtCore.QRect(509, 40, 121, 22))
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
        self.lineEdit_file = QtWidgets.QLineEdit(self.page_zb)
        self.lineEdit_file.setGeometry(QtCore.QRect(270, 40, 200, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_file.sizePolicy().hasHeightForWidth())
        self.lineEdit_file.setSizePolicy(sizePolicy)
        self.lineEdit_file.setMaximumSize(QtCore.QSize(200, 22))
        self.lineEdit_file.setObjectName("lineEdit_file")
        self.label_file = QtWidgets.QLabel(self.page_zb)
        self.label_file.setGeometry(QtCore.QRect(170, 40, 85, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_file.setFont(font)
        self.label_file.setObjectName("label_file")
        self.pushButton_addac = QtWidgets.QPushButton(self.page_zb)
        self.pushButton_addac.setGeometry(QtCore.QRect(480, 490, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_addac.setFont(font)
        self.pushButton_addac.setObjectName("pushButton_addac")
        self.lineEdit = QtWidgets.QLineEdit(self.page_zb)
        self.lineEdit.setGeometry(QtCore.QRect(280, 79, 661, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.page_zb)
        self.label_2.setGeometry(QtCore.QRect(173, 131, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_zb)
        self.lineEdit_2.setGeometry(QtCore.QRect(280, 130, 661, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.page_zb)
        self.label_3.setGeometry(QtCore.QRect(170, 190, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.page_zb)
        self.label_4.setGeometry(QtCore.QRect(500, 190, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.page_zb)
        self.label_5.setGeometry(QtCore.QRect(170, 230, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.page_zb)
        self.label_6.setGeometry(QtCore.QRect(500, 230, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.page_zb)
        self.label_7.setGeometry(QtCore.QRect(170, 270, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.page_zb)
        self.label_8.setGeometry(QtCore.QRect(500, 280, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.page_zb)
        self.label_9.setGeometry(QtCore.QRect(170, 300, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.page_zb)
        self.label_10.setGeometry(QtCore.QRect(170, 330, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.page_zb)
        self.label_11.setGeometry(QtCore.QRect(170, 360, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.page_zb)
        self.label_12.setGeometry(QtCore.QRect(170, 390, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.page_zb)
        self.label_13.setGeometry(QtCore.QRect(500, 330, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.page_zb)
        self.label_14.setGeometry(QtCore.QRect(500, 390, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.stackedWidget_new.addWidget(self.page_zb)
        self.page_gw = QtWidgets.QWidget()
        self.page_gw.setObjectName("page_gw")
        self.lineEdit_num = QtWidgets.QLineEdit(self.page_gw)
        self.lineEdit_num.setGeometry(QtCore.QRect(280, 80, 200, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_num.sizePolicy().hasHeightForWidth())
        self.lineEdit_num.setSizePolicy(sizePolicy)
        self.lineEdit_num.setMaximumSize(QtCore.QSize(200, 22))
        self.lineEdit_num.setObjectName("lineEdit_num")
        self.label_num = QtWidgets.QLabel(self.page_gw)
        self.label_num.setGeometry(QtCore.QRect(180, 80, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_num.setFont(font)
        self.label_num.setObjectName("label_num")
        self.lineEdit_file_3 = QtWidgets.QLineEdit(self.page_gw)
        self.lineEdit_file_3.setGeometry(QtCore.QRect(280, 40, 200, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_file_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_file_3.setSizePolicy(sizePolicy)
        self.lineEdit_file_3.setMaximumSize(QtCore.QSize(200, 22))
        self.lineEdit_file_3.setObjectName("lineEdit_file_3")
        self.pushButton_file_3 = QtWidgets.QPushButton(self.page_gw)
        self.pushButton_file_3.setGeometry(QtCore.QRect(519, 40, 121, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_file_3.sizePolicy().hasHeightForWidth())
        self.pushButton_file_3.setSizePolicy(sizePolicy)
        self.pushButton_file_3.setMaximumSize(QtCore.QSize(150, 22))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_file_3.setFont(font)
        self.pushButton_file_3.setObjectName("pushButton_file_3")
        self.label_file_3 = QtWidgets.QLabel(self.page_gw)
        self.label_file_3.setGeometry(QtCore.QRect(180, 40, 85, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_file_3.setFont(font)
        self.label_file_3.setObjectName("label_file_3")
        self.label_num_3 = QtWidgets.QLabel(self.page_gw)
        self.label_num_3.setGeometry(QtCore.QRect(180, 120, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_num_3.setFont(font)
        self.label_num_3.setObjectName("label_num_3")
        self.lineEdit_num_3 = QtWidgets.QLineEdit(self.page_gw)
        self.lineEdit_num_3.setGeometry(QtCore.QRect(280, 120, 200, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_num_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_num_3.setSizePolicy(sizePolicy)
        self.lineEdit_num_3.setMaximumSize(QtCore.QSize(200, 22))
        self.lineEdit_num_3.setObjectName("lineEdit_num_3")
        self.label_num_4 = QtWidgets.QLabel(self.page_gw)
        self.label_num_4.setGeometry(QtCore.QRect(180, 155, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_num_4.setFont(font)
        self.label_num_4.setObjectName("label_num_4")
        self.textEdit = QtWidgets.QTextEdit(self.page_gw)
        self.textEdit.setGeometry(QtCore.QRect(280, 180, 541, 51))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.page_gw)
        self.textEdit_2.setGeometry(QtCore.QRect(280, 280, 541, 61))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_num_5 = QtWidgets.QLabel(self.page_gw)
        self.label_num_5.setGeometry(QtCore.QRect(180, 250, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_num_5.setFont(font)
        self.label_num_5.setText("<html><head/><body><p><span style=\" color:#005500;\">审计办领导审核意见：</span></p></body></html>")
        self.label_num_5.setObjectName("label_num_5")
        self.label_num_6 = QtWidgets.QLabel(self.page_gw)
        self.label_num_6.setGeometry(QtCore.QRect(180, 350, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_num_6.setFont(font)
        self.label_num_6.setText("<html><head/><body><p><span style=\" color:#005500;\">办文情况说明和拟办意见：</span></p></body></html>")
        self.label_num_6.setObjectName("label_num_6")
        self.textEdit_3 = QtWidgets.QTextEdit(self.page_gw)
        self.textEdit_3.setGeometry(QtCore.QRect(280, 380, 541, 51))
        self.textEdit_3.setObjectName("textEdit_3")
        self.pushButton_addac_3 = QtWidgets.QPushButton(self.page_gw)
        self.pushButton_addac_3.setGeometry(QtCore.QRect(480, 480, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_addac_3.setFont(font)
        self.pushButton_addac_3.setObjectName("pushButton_addac_3")
        self.stackedWidget_new.addWidget(self.page_gw)
        self.page_jz = QtWidgets.QWidget()
        self.page_jz.setObjectName("page_jz")
        self.label_29 = QtWidgets.QLabel(self.page_jz)
        self.label_29.setGeometry(QtCore.QRect(180, 10, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.stackedWidget_new.addWidget(self.page_jz)
        self.gridLayout_2.addWidget(self.stackedWidget_new, 6, 0, 1, 5)
        self.stackedWidget.addWidget(self.stackedWidgetPage2)
        self.stackedWidgetPage3 = QtWidgets.QWidget()
        self.stackedWidgetPage3.setObjectName("stackedWidgetPage3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.stackedWidgetPage3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_ahead = QtWidgets.QLabel(self.stackedWidgetPage3)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_ahead.setFont(font)
        self.label_ahead.setObjectName("label_ahead")
        self.verticalLayout_5.addWidget(self.label_ahead)
        self.line_3 = QtWidgets.QFrame(self.stackedWidgetPage3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_3.sizePolicy().hasHeightForWidth())
        self.line_3.setSizePolicy(sizePolicy)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_5.addWidget(self.line_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 671, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.stackedWidgetPage3)
        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_view, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)
        indexWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(indexWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget_new.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(indexWindow)

    def retranslateUi(self, indexWindow):
        _translate = QtCore.QCoreApplication.translate
        indexWindow.setWindowTitle(_translate("indexWindow", "审计整改信息管理系统"))
        self.btprog.setText(_translate("indexWindow", "项目管理"))
        self.btproview.setText(_translate("indexWindow", "项目浏览"))
        self.btproadd.setText(_translate("indexWindow", "新增项目"))
        self.btanaly.setText(_translate("indexWindow", "统计分析"))
        self.btansear.setText(_translate("indexWindow", "查询"))
        self.btanalytemp.setText(_translate("indexWindow", "统计"))
        self.label_vhead.setText(_translate("indexWindow", "项目浏览"))
        self.label_key.setText(_translate("indexWindow", "关键字："))
        self.label_tip1.setText(_translate("indexWindow", "立项时间自"))
        self.label_tip2.setText(_translate("indexWindow", "至"))
        self.checkBox.setText(_translate("indexWindow", "倒序"))
        self.bt_search.setText(_translate("indexWindow", "搜索"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("indexWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("indexWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("indexWindow", "3"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("indexWindow", "报文号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("indexWindow", "收文号"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("indexWindow", "批文号"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("indexWindow", "立项时间"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("indexWindow", "项目完成度"))
        self.pushButton_more.setText(_translate("indexWindow", "查看详情"))
        self.pushButton_del.setText(_translate("indexWindow", "删除项目"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("indexWindow", "Tab 1"))
        self.label_nh.setText(_translate("indexWindow", "项目号:"))
        self.label_type.setText(_translate("indexWindow", "项目类型："))
        self.label_nhead.setText(_translate("indexWindow", "新增项目"))
        self.label_time.setText(_translate("indexWindow", "立项时间："))
        self.label_nr.setText(_translate("indexWindow", "（系统生成）"))
        self.comboBox_type.setItemText(0, _translate("indexWindow", "专报项目"))
        self.comboBox_type.setItemText(1, _translate("indexWindow", "公文项目"))
        self.comboBox_type.setItemText(2, _translate("indexWindow", "经责项目"))
        self.label_tmres.setText(_translate("indexWindow", "（系统生成）"))
        self.label.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">专报标题：</span></p></body></html>"))
        self.pushButton_file.setText(_translate("indexWindow", "选择文件"))
        self.label_file.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">报文文件：</span></p></body></html>"))
        self.pushButton_addac.setText(_translate("indexWindow", "确认新增"))
        self.label_2.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">报送范围：</span></p></body></html>"))
        self.label_3.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">发文字号：</span></p></body></html>"))
        self.label_4.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">紧急程度：</span></p></body></html>"))
        self.label_5.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">秘密等级：</span></p></body></html>"))
        self.label_6.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">是否公开：</span></p></body></html>"))
        self.label_7.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿人：</span></p></body></html>"))
        self.label_8.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿处室分管厅领导：</span></p></body></html>"))
        self.label_9.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">拟稿处室：</span></p></body></html>"))
        self.label_10.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处编辑：</span></p></body></html>"))
        self.label_11.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处审核：</span></p></body></html>"))
        self.label_12.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">秘书处审核：</span></p></body></html>"))
        self.label_13.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">综合处分管厅领导：</span></p></body></html>"))
        self.label_14.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">审计办主任（厅长）：</span></p></body></html>"))
        self.label_num.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#005500;\">发文字号：</span></p></body></html>"))
        self.pushButton_file_3.setText(_translate("indexWindow", "选择文件"))
        self.label_file_3.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#005500;\">报文文件：</span></p></body></html>"))
        self.label_num_3.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#005500;\">文件标题：</span></p></body></html>"))
        self.label_num_4.setText(_translate("indexWindow", "<html><head/><body><p><span style=\" color:#005500;\">领导审核意见：</span></p></body></html>"))
        self.pushButton_addac_3.setText(_translate("indexWindow", "确认新增"))
        self.label_29.setText(_translate("indexWindow", "经责文件："))
        self.label_ahead.setText(_translate("indexWindow", "统计分析"))
