from PyQt5 import QtCore, QtWidgets
from uipy_dir.index import Ui_indexWindow
import sys
import qtawesome
from call_zbdetail import Call_zbdetail
from call_gwdetail import Call_gwdetail


class Call_index(QtWidgets.QMainWindow,Ui_indexWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.logi()

    def init_ui(self):
        self.bt_search.setFont(qtawesome.font('fa', 16))
        self.bt_search.setText(chr(0xf002) + ' '+'搜索')
        #qtawesome用法
        #icon_close=qtawesome.icon("fa.close",color='white')
        #self.btclose.setIcon(icon_close)

       # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.tabWidget.setTabText(0,"项目浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.RightSide,None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

    def logi(self):
        self.btproview.clicked.connect(self.btfun1)
        self.btproadd.clicked.connect(self.btfun2)
        self.btanalytemp.clicked.connect(self.btfun3)
        self.btansear.clicked.connect(self.btfun3)
        self.bt_search.clicked.connect(self.btfun4)
        self.pushButton_file.clicked.connect(self.btfun5)
        self.pushButton_addac.clicked.connect(self.btfun6)
        self.comboBox_type.currentIndexChanged.connect(self.btfun7)
        self.pushButton_more.clicked.connect(self.btfun8)

    def mclose(self,index):
        self.tabWidget.removeTab(index)

    def btfun1(self):
        self.stackedWidget.setCurrentIndex(0)

    def btfun2(self):
        self.stackedWidget.setCurrentIndex(1)

    def btfun3(self):
        self.stackedWidget.setCurrentIndex(2)

    def btfun4(self):
        #需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    def btfun5(self):
        p = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")
        self.lineEdit_file.setText(p)

    def btfun6(self):
        QtWidgets.QMessageBox.information(self, "提示", "新建成功！")
        # 测试数据,真实的新建需验证输入信息的完整，之后将数据存入库中之后展示
        newItem = QtWidgets.QTableWidgetItem('测试报文号1')
        self.tableWidget.setItem(0, 0, newItem)
        newItem = QtWidgets.QTableWidgetItem('测试收文号1')
        self.tableWidget.setItem(0, 1, newItem)
        newItem = QtWidgets.QTableWidgetItem('测试批文号1')
        self.tableWidget.setItem(0, 2, newItem)
        newItem = QtWidgets.QTableWidgetItem('2021/3/2')
        self.tableWidget.setItem(0, 3, newItem)
        newItem = QtWidgets.QTableWidgetItem('已完成')
        self.tableWidget.setItem(0, 4, newItem)
        #
        self.stackedWidget.setCurrentIndex(0)

    def btfun7(self,index):
            self.stackedWidget_new.setCurrentIndex(index)

    def btfun8(self):
        type=self.tableWidget.currentRow()
        print(type)
        if type%2==0:
            tab_new=Call_zbdetail()
            tab_new.setObjectName('tab_new')
            tabnum=self.tabWidget.addTab(tab_new,"专报项目详情")
            self.tabWidget.setCurrentIndex(tabnum)
        else:
            tab_new = Call_gwdetail()
            tab_new.setObjectName('tab_new')
            tabnum = self.tabWidget.addTab(tab_new, "公文项目详情")
            self.tabWidget.setCurrentIndex(tabnum)



if __name__ == '__main__':
         app = QtWidgets.QApplication(sys.argv)
         callindex = Call_index()
         callindex.show()
         sys.exit(app.exec_())
