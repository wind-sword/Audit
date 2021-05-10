from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget

from uipy_dir.quedetail import Ui_Form
from logis_fir.tools import tools


class Call_quedetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = -1  # 问题序号

        self.commandLinkButton_4.clicked.connect(self.questionInfo)
        self.commandLinkButton_2.clicked.connect(self.questionZgxq)

        # 初始化问题序号
        self.xh = key

        self.pushButton_1.clicked.connect(self.reviseQuestionDetail)
        self.pushButton_2.clicked.connect(self.updateQuestionDetail)
        self.pushButton_3.clicked.connect(self.cancelQuestionDetail)

        self.stackedWidget.setCurrentIndex(0)
        self.displayQuestionDetail()

    # 问题基本信息
    def questionInfo(self):
        self.stackedWidget.setCurrentIndex(0)
        self.displayQuestionDetail()

    # 整改详情
    def questionZgxq(self):
        self.stackedWidget.setCurrentIndex(1)
        self.displayZgxq()

    # 展示问题整改详情
    def displayZgxq(self):
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改
        sql = "select 整改责任部门,上报次序,应上报整改报告时间,实际上报整改报告时间,整改情况,已整改金额,追责问责人数,推动制度建设数目,推动制度建设文件,部分整改情况具体描述," \
              "未整改原因说明,下一步整改措施及时限,认定整改情况,认定整改金额,整改率 from rectification where 问题序号 = %s" \
              " order by 上报次序 desc" % self.xh
        data = tools.executeSql(sql)
        # 打印结果
        # print(data)

        size = len(data)
        # print("项目数目为:"+str(size))
        self.tableWidget_2.setRowCount(size)

        x = 0
        for i in data:
            y = 0
            for j in i:
                if data[x][y] is None:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem("/"))
                else:
                    self.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1

        self.tableWidget_2.resizeColumnsToContents()  # 根据列调整框大小
        self.tableWidget_2.resizeRowsToContents()  # 根据行调整框大小

    # 展示问题详情
    def displayQuestionDetail(self):
        # 隐藏确认取消按钮,显示修改按钮
        self.pushButton_2.hide()
        self.pushButton_3.hide()
        self.pushButton_1.show()

        sql = "select 被审计领导干部,所在地方或单位,审计报告文号,出具审计报告时间,审计组组长,审计组主审,问题描述,问题一级分类,问题二级分类,问题三级分类,问题四级分类,备注,问题金额," \
              "移送及处理情况 from problem where problem.序号 = %s" % self.xh
        data = tools.executeSql(sql)

        self.lineEdit.setText(data[0][0])  # 被审计领导干部
        self.lineEdit_2.setText(data[0][1])  # 所在地方或单位
        self.lineEdit_3.setText(data[0][2])  # 审计报告（意见）文号
        self.dateEdit.setDate(QDate.fromString(data[0][3], 'yyyy/M/d'))  # 出具审计报告时间
        self.lineEdit_4.setText(data[0][4])  # 审计组组长
        self.lineEdit_5.setText(data[0][5])  # 审计组主审
        self.lineEdit_6.setText(data[0][6])  # 问题描述
        self.lineEdit_7.setText(data[0][7])  # 问题一级分类
        self.lineEdit_8.setText(data[0][8])  # 问题二级分类
        self.lineEdit_9.setText(data[0][9])  # 问题三级分类
        self.lineEdit_10.setText(data[0][10])  # 问题四级分类
        self.lineEdit_11.setText(data[0][11])  # 备注
        self.lineEdit_12.setText(data[0][12])  # 问题金额
        self.lineEdit_13.setText(data[0][13])  # 移送及处理情况

        # 设置不可编辑
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.dateEdit.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_6.setReadOnly(True)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_8.setReadOnly(True)
        self.lineEdit_9.setReadOnly(True)
        self.lineEdit_10.setReadOnly(True)
        self.lineEdit_11.setReadOnly(True)
        self.lineEdit_12.setReadOnly(True)
        self.lineEdit_13.setReadOnly(True)

    # 修改问题详情按钮
    def reviseQuestionDetail(self):
        # 隐藏修改按钮,显示确认和取消按钮
        self.pushButton_1.hide()
        self.pushButton_2.show()
        self.pushButton_3.show()

        # 设置可以编辑
        self.lineEdit.setReadOnly(False)
        self.lineEdit_2.setReadOnly(False)
        self.lineEdit_3.setReadOnly(False)
        self.dateEdit.setReadOnly(False)
        self.lineEdit_4.setReadOnly(False)
        self.lineEdit_5.setReadOnly(False)
        self.lineEdit_6.setReadOnly(False)
        self.lineEdit_7.setReadOnly(False)
        self.lineEdit_8.setReadOnly(False)
        self.lineEdit_9.setReadOnly(False)
        self.lineEdit_10.setReadOnly(False)
        self.lineEdit_11.setReadOnly(False)
        self.lineEdit_12.setReadOnly(False)
        self.lineEdit_13.setReadOnly(False)

    # 确认按钮
    def updateQuestionDetail(self):
        w = QWidget()  # 用作QMessageBox继承,使得弹框大小正常

        input1 = self.lineEdit.text()  # 被审计领导干部
        input2 = self.lineEdit_2.text()  # 所在地方或单位
        input3 = self.lineEdit_3.text()  # 审计报告（意见）文号
        input4 = self.dateEdit.text()  # 出具审计报告时间
        input5 = self.lineEdit_4.text()  # 审计组组长
        input6 = self.lineEdit_5.text()  # 审计组主审
        input7 = self.lineEdit_6.text()  # 问题描述
        input8 = self.lineEdit_7.text()  # 问题一级分类
        input9 = self.lineEdit_8.text()  # 问题二级分类
        input10 = self.lineEdit_9.text()  # 问题三级分类
        input11 = self.lineEdit_10.text()  # 问题四级分类
        input12 = self.lineEdit_11.text()  # 备注
        input13 = self.lineEdit_12.text()  # 问题金额
        input14 = self.lineEdit_13.text()  # 移送及处理情况

        sql = "update problem set 被审计领导干部 = '%s',所在地方或单位 = '%s',审计报告文号 = '%s',出具审计报告时间 = '%s',审计组组长 = '%s'," \
              "审计组主审 = '%s',问题描述 = '%s',问题一级分类 = '%s',问题二级分类 = '%s',问题三级分类 = '%s',问题四级分类 = '%s',备注 = '%s'," \
              "问题金额 = '%s',移送及处理情况 = '%s' where problem.序号 = %s" % (
                  input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11, input12,
                  input13, input14, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(w, "提示", "修改成功！")

        self.displayQuestionDetail()

    # 取消按钮
    def cancelQuestionDetail(self):
        self.displayQuestionDetail()
