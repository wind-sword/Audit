import sqlite3

from PyQt5 import QtCore, QtWidgets
from uipy_dir.index import Ui_indexWindow
import sys
import qtawesome
from call_zbdetail import Call_zbdetail
from call_gwdetail import Call_gwdetail


class Call_index(QtWidgets.QMainWindow,Ui_indexWindow):
    db_path = "../db/database.db"
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

        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.tabWidget.setTabText(0,"项目浏览")
        self.tabWidget.setTabsClosable(1)
        self.tabWidget.tabBar().setTabButton(0,QtWidgets.QTabBar.RightSide,None)
        self.tabWidget.tabCloseRequested.connect(self.mclose)

        self.showProjectTable() #初始化显示

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

    #执行sql语句
    def executeSql(self,sql):
        con = sqlite3.connect(self.db_path)
        print('Opened database successfully')
        cur = con.cursor()
        cur.execute(sql)
        print('Execute sql successfully')
        data = cur.fetchall()
        con.commit()
        con.close()
        return data

    # 显示项目表内容
    def showProjectTable(self):
        self.tableWidget.clear()
        sql = 'select project.发文字号,project.收文字号,project.批文字号,project.专报标题,project.公文标题,project.秘密等级,project.是否公开,project.紧急程度,project.报文内容,project.办文日期,project.整改进度 from project'
        data = self.executeSql(sql)
        # 打印结果
        print(data)
        x = 0
        for i in data:
            y = 0
            for j in i:
                self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

    def mclose(self,index):
        self.tabWidget.removeTab(index)

    def btfun1(self):
        self.stackedWidget.setCurrentIndex(0)
        self.showProjectTable()# 点击项目浏览显示项目表内容

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
        str1 = self.label.text()#专报标题
        input1 = self.lineEdit.text()

        str2 = self.label_2.text()#报送范围
        input2 = self.lineEdit_2.text()

        str3 = self.label_3.text()#发文字号
        input3 = self.lineEdit_3.text()

        str4 = self.label_4.text()#紧急程度
        input4 = self.lineEdit_4.text()

        str5 = self.label_5.text()#秘密等级
        input5 = self.lineEdit_5.text()

        str6 = self.label_6.text()#是否公开
        input6 = self.lineEdit_6.text()

        str7 = self.label_7.text()#拟稿人
        input7 = self.lineEdit_7.text()

        str8 = self.label_8.text()#拟稿处室分管厅领导
        input8 = self.lineEdit_12.text()

        str9 = self.label_9.text()#拟稿处室
        input9 = self.lineEdit_8.text()

        str10 = self.label_10.text()#综合处编辑
        input10 = self.lineEdit_9.text()

        str11 = self.label_11.text()#综合处审核
        input11 = self.lineEdit_10.text()

        str12 = self.label_12.text()#秘书处审核
        input12 = self.lineEdit_11.text()

        str13 = self.label_13.text()#综合处分管厅领导
        input13 = self.lineEdit_13.text()

        str14 = self.label_14.text()#审计办主任
        input14 = self.lineEdit_14.text()

        sql = "insert into project(专报标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"%(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10,input11,input12,input13,input14)
        self.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

        #返回显示页面,重新加载项目内容
        self.stackedWidget.setCurrentIndex(0)
        self.showProjectTable()


    def btfun7(self,index):
        self.stackedWidget_new.setCurrentIndex(index)

    def btfun8(self):
        row = self.tableWidget.currentRow()
        #获取发文字号用于查询
        key = self.tableWidget.item(row,0).text()
        sql = 'select project.专报标题,project.报送范围,project.发文字号,project.紧急程度,project.秘密等级,project.是否公开,project.拟稿人,project.拟稿处室分管厅领导,project.拟稿处室,project.综合处编辑,project.综合处审核,project.秘书处审核,project.综合处分管厅领导,project.审计办主任 from project where 发文字号 =  \'%s\''%key
        data = self.executeSql(sql)
        print(data)

        if row % 2 == 0:
            tab_new=Call_zbdetail(data)
            tab_new.setObjectName('tab_new')
            tab_num=self.tabWidget.addTab(tab_new,"专报项目详情")
            self.tabWidget.setCurrentIndex(tab_num)
        else:
            tab_new = Call_gwdetail()
            tab_new.setObjectName('tab_new')
            tab_num = self.tabWidget.addTab(tab_new,"公文项目详情")
            self.tabWidget.setCurrentIndex(tab_num)



if __name__ == '__main__':
         app = QtWidgets.QApplication(sys.argv)
         callindex = Call_index()
         callindex.show()
         sys.exit(app.exec_())
