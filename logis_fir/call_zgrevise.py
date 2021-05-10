from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.zgrevise import Ui_Dialog
from logis_fir.tools import tools


class Call_zgrevise(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = key  # 整改表主键

        # 初始化页面数据
        self.displayRectificationDetail()

        self.pushButton_revise.clicked.connect(self.reviseRectification)
        self.pushButton_quit.clicked.connect(self.closeWindow)

    def displayRectificationDetail(self):
        sql = "select 整改责任部门,应上报整改报告时间,实际上报整改报告时间,整改情况,已整改金额,追责问责人数,推动制度建设数目,推动制度建设文件,部分整改情况具体描述,未整改原因说明,下一步整改措施及时限," \
              "认定整改情况,认定整改金额,整改率 from rectification where 序号 = %s" % self.xh
        data = tools.executeSql(sql)

        self.lineEdit_1.setText(data[0][0])  # 整改责任部门
        self.dateEdit.setDate(QDate.fromString(data[0][1], 'yyyy/M/d'))  # 应上报整改报告时间
        self.dateEdit_2.setDate(QDate.fromString(data[0][2], 'yyyy/M/d'))  # 实际上报整改报告时间
        self.lineEdit_2.setText(data[0][3])  # 整改情况
        self.lineEdit_3.setText(data[0][4])  # 已整改金额
        self.spinBox.setValue(data[0][5])  # 追责问责人数
        self.spinBox_2.setValue(data[0][6])  # 推动制度建设数目
        self.lineEdit_6.setText(data[0][7])  # 推动制度建设文件
        self.lineEdit_7.setText(data[0][8])  # 部分整改情况具体描述
        self.lineEdit_8.setText(data[0][9])  # 未整改原因说明
        self.lineEdit_9.setText(data[0][10])  # 下一步整改措施及时限
        self.lineEdit_10.setText(data[0][11])  # 认定整改情况
        self.lineEdit_11.setText(data[0][12])  # 认定整改金额
        self.lineEdit_12.setText(data[0][13])  # 整改率

    def reviseRectification(self):
        input1 = self.lineEdit_1.text()  # 整改责任部门
        input2 = self.dateEdit.text()  # 应上报整改报告时间
        input3 = self.dateEdit_2.text()  # 实际上报整改报告时间
        input4 = self.lineEdit_2.text()  # 整改情况
        input5 = self.lineEdit_3.text()  # 已整改金额
        input6 = self.spinBox.value()  # 追责问责人数
        input7 = self.spinBox_2.value()  # 推动制度建设数目
        input8 = self.lineEdit_6.text()  # 推动制度建设文件
        input9 = self.lineEdit_7.text()  # 部分整改情况具体描述
        input10 = self.lineEdit_8.text()  # 未整改原因说明
        input11 = self.lineEdit_9.text()  # 下一步整改措施及时限
        input12 = self.lineEdit_10.text()  # 认定整改情况
        input13 = self.lineEdit_11.text()  # 认定整改金额
        input14 = self.lineEdit_12.text()  # 整改率

        sql = "update rectification set 整改责任部门 = '%s',应上报整改报告时间 = '%s',实际上报整改报告时间 = '%s',整改情况 = '%s',已整改金额 = '%s'," \
              "追责问责人数 = %s,推动制度建设数目 = %s,推动制度建设文件 = '%s',部分整改情况具体描述 = '%s',未整改原因说明 = '%s',下一步整改措施及时限 = '%s'," \
              "认定整改情况 = '%s',认定整改金额 = '%s',整改率 = '%s' where 序号 = %s" % (
                  input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12,
                  input13, input14, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "修改成功！")

        self.close()

    def closeWindow(self):
        self.close()
