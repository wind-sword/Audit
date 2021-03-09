import os
import sqlite3

from PyQt5 import QtCore, QtWidgets
from uipy_dir.index import Ui_indexWindow
import sys
import qtawesome
from call_zbdetail import Call_zbdetail
from call_gwdetail import Call_gwdetail
import shutil


class Call_index(QtWidgets.QMainWindow,Ui_indexWindow):
    db_path = "../db/database.db"
    project_word_path = "../project_word"
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
        self.pushButton_file_3.clicked.connect(self.btfun5_1)
        self.pushButton_addac.clicked.connect(self.btfun6)
        self.pushButton_addac_3.clicked.connect(self.btfun6_1)
        self.comboBox_type.currentIndexChanged.connect(self.btfun7)
        self.pushButton_more.clicked.connect(self.btfun8)

    # 执行sql语句
    def executeSql(self,sql):
        print("当前需要执行sql:"+sql)
        con = sqlite3.connect(self.db_path)
        print('Opened database successfully')
        cur = con.cursor()
        cur.execute(sql)
        print('Execute sql successfully'+'\n')
        data = cur.fetchall()
        con.commit()
        con.close()
        return data

    #source对应的文件复制一份到target(project_word)文件夹下,copy方法保留当前文件权限,暂未考虑同名文件
    def copyFile(self,source,target):
        try:
            shutil.copy(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())

    # 显示项目表内容
    def showProjectTable(self):
        #导致表头消失 self.tableWidget.clear()
        sql = 'select project.发文字号,project.收文字号,project.批文字号,project.专报标题,project.公文标题,project.秘密等级,project.是否公开,project.紧急程度,project.报文内容,project.办文日期,project.整改进度 from project'
        data = self.executeSql(sql)
        # 打印结果
        #print(data)

        size = len(data)
        #print("项目数目为:"+str(size))
        self.tableWidget.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

    def mclose(self,index):
        self.tabWidget.removeTab(index)

    #项目浏览按钮
    def btfun1(self):
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.showProjectTable()# 点击项目浏览显示项目表内容

    #新增项目按钮
    def btfun2(self):
        self.stackedWidget.setCurrentIndex(1)

    #统计分析按钮
    def btfun3(self):
        self.stackedWidget.setCurrentIndex(2)

    #项目详情下的项目搜索按钮
    def btfun4(self):
        #需完成真实搜索逻辑
        QtWidgets.QMessageBox.information(self, "提示", "搜索完成！")

    #新增项目下的选择文件夹按钮(专报)
    def btfun5(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file.setText(p[0])

    #新增项目下的选择文件夹按钮(公文)
    def btfun5_1(self):
        p = QtWidgets.QFileDialog.getOpenFileName(None, "选取文件夹", "C:/")
        self.lineEdit_file_3.setText(p[0])

    #新增项目下的确认按钮(专报)
    def btfun6(self):
        str1 = self.label.text() #专报标题
        input1 = self.lineEdit.text()

        str2 = self.label_2.text() #报送范围
        input2 = self.lineEdit_2.text()

        str3 = self.label_3.text() #发文字号
        input3 = self.lineEdit_3.text()

        str4 = self.label_4.text() #紧急程度
        input4 = self.lineEdit_4.text()

        str5 = self.label_5.text() #秘密等级
        input5 = self.lineEdit_5.text()

        str6 = self.label_6.text() #是否公开
        input6 = self.lineEdit_6.text()

        str7 = self.label_7.text() #拟稿人
        input7 = self.lineEdit_7.text()

        str8 = self.label_8.text() #拟稿处室分管厅领导
        input8 = self.lineEdit_12.text()

        str9 = self.label_9.text() #拟稿处室审核
        input9 = self.lineEdit_8.text()

        str10 = self.label_10.text() #综合处编辑
        input10 = self.lineEdit_9.text()

        str11 = self.label_11.text() #综合处审核
        input11 = self.lineEdit_10.text()

        str12 = self.label_12.text() #秘书处审核
        input12 = self.lineEdit_11.text()

        str13 = self.label_13.text() #综合处分管厅领导
        input13 = self.lineEdit_13.text()

        str14 = self.label_14.text() #审计办主任
        input14 = self.lineEdit_14.text()

        str15 = self.label_time.text() #立项日期
        input15 = self.dateEdit_3.text()

        str16 = self.label_file.text() #报文内容
        input_file_path = self.lineEdit_file.text() #文件路径
        input16 = os.path.split(input_file_path)[1] #文件名

        # 执行插入
        sql = "insert into project(专报标题,报送范围,发文字号,紧急程度,秘密等级,是否公开,拟稿人,拟稿处室分管厅领导,拟稿处室审核,综合处编辑,综合处审核,秘书处审核,综合处分管厅领导,审计办主任,办文日期,报文内容,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',1);"%(input1,input2,input3,input4,input5,input6,input7,input8,input9,input10,input11,input12,input13,input14,input15,input16)
        self.executeSql(sql)

        # 导入文件
        self.copyFile(input_file_path,self.project_word_path)

        QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

        #返回显示页面,重新加载项目内容
        self.stackedWidget.setCurrentIndex(0)
        self.showProjectTable()

    #新增项目下的确认按钮(公文)
    def btfun6_1(self):
        str1 = self.label_num.text() #发文字号
        input1 = self.lineEdit_num.text()

        str2 = self.label_num_3.text() #公文标题
        input2 = self.lineEdit_num_3.text()

        str3 = self.label_num_4.text() #领导审核意见
        input3 = self.textEdit.toPlainText()

        str4 = self.label_num_5.text() #审计办领导审核意见
        input4 = self.textEdit_2.toPlainText()

        str5 = self.label_num_6.text() #办文情况说明和拟办意见
        input5 = self.textEdit_3.toPlainText()

        str6 = self.label_time_2.text() #立项日期
        input6 = self.dateEdit_4.text()

        str7 = self.label_file_3.text() #公文内容
        input_file_path = self.lineEdit_file_3.text() #文件路径
        input7 = os.path.split(input_file_path)[1] #文件名

        #执行插入
        sql = "insert into project(发文字号,公文标题,领导审核意见,审计办领导审核意见,办文情况说明和拟办意见,办文日期,报文内容,projectType) VALUES('%s','%s','%s','%s','%s','%s','%s',2);"%(input1,input2,input3,input4,input5,input6,input7)
        self.executeSql(sql)

        # 导入文件
        self.copyFile(input_file_path,self.project_word_path)


        QtWidgets.QMessageBox.information(self, "提示", "新建成功！")

        # 返回显示页面,重新加载项目内容
        self.stackedWidget.setCurrentIndex(0)
        self.showProjectTable()

    #新增项目下的项目类型切换栏
    def btfun7(self,index):
        self.stackedWidget_new.setCurrentIndex(index)

    #项目详情下的查询按钮
    def btfun8(self):
        row = self.tableWidget.currentRow()
        # row为-1表示没有选中某一行,弹出提示信息
        if row == -1:
            QtWidgets.QMessageBox.information(self, "提示", "请选择项目！")
        else:
            # 获取发文字号用于查询
            key = self.tableWidget.item(row,0).text()
            sql = 'select project.专报标题,project.报送范围,project.发文字号,project.紧急程度,project.秘密等级,project.是否公开,project.拟稿人,project.拟稿处室分管厅领导,project.拟稿处室审核,project.综合处编辑,project.综合处审核,project.秘书处审核,project.综合处分管厅领导,project.审计办主任,project.公文标题,project.领导审核意见,project.审计办领导审核意见,project.办文情况说明和拟办意见,project.projectType,project.报文内容 from project where 发文字号 =  \'%s\''%key
            data = self.executeSql(sql)
            #print(data)
            #判断项目类型
            if data[0][18] == 1:
                tab_new=Call_zbdetail(data)
                tab_new.setObjectName('tab_new')
                tab_new.setObjectName('tab_new')
                tab_num=self.tabWidget.addTab(tab_new,"专报项目详情")
                self.tabWidget.setCurrentIndex(tab_num)
            elif data[0][18] == 2:
                tab_new = Call_gwdetail(data)
                tab_new.setObjectName('tab_new')
                tab_num = self.tabWidget.addTab(tab_new,"公文项目详情")
                self.tabWidget.setCurrentIndex(tab_num)



if __name__ == '__main__':
         app = QtWidgets.QApplication(sys.argv)
         callindex = Call_index()
         callindex.show()
         sys.exit(app.exec_())
