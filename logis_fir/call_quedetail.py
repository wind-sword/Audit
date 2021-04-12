from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate

from uipy_dir.quedetail import Ui_Form
from tools import tools


class Call_quedetail(QtWidgets.QWidget, Ui_Form):
    def __init__(self, key1, key2):
        super().__init__()
        self.setupUi(self)

        self.xh_pro = -1  # 问题顺序号
        self.xh_send = -1  # 发文序号

        self.commandLinkButton_4.clicked.connect(self.questionInfo)
        self.commandLinkButton_2.clicked.connect(self.questionZgxq)

        self.xh_pro = key1
        self.xh_send = key2
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
        sql = "select 整改责任部门,序号,应上报整改报告时间,实际上报整改报告时间,整改情况,已整改金额,追责问责人数,推动制度建设数目,推动制度建设文件,部分整改情况具体描述," \
              "未整改原因说明,下一步整改措施及时限,认定整改情况,认定整改金额,整改率 from rectification where 问题顺序号 = %s and 发文序号 = %s" % (
                  self.xh_pro, self.xh_send)
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
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 表格不可修改

    # 展示问题详情
    def displayQuestionDetail(self):
        sql = "select problem.被审计领导干部,problem.所在地方和单位,problem.出具审计报告时间,problem.审计组主审,problem.审计组组长,sendfile.发文字号," \
              "problem.审计报告文号,problem.问题描述 from problem,sendfile where 问题顺序号 = %s and 发文序号 = %s and problem.发文序号 = " \
              "sendfile.序号" % (self.xh_pro, self.xh_send)
        data = tools.executeSql(sql)
        # 被审计领导干部
        self.lineEdit.setText(data[0][0])
        # 所在地方或单位
        self.lineEdit_2.setText(data[0][1])
        # 出具审计报告时间
        self.dateEdit_2.setDate(QDate.fromString(data[0][2], 'yyyy/M/d'))
        # 审计组主审
        self.lineEdit_8.setText(data[0][3])
        # 审计组组长
        self.lineEdit_7.setText(data[0][4])
        # 发文字号
        self.lineEdit_3.setText(data[0][5])
        # 审计报告文号
        self.lineEdit_4.setText(data[0][6])
        # 问题描述
        self.lineEdit_9.setText(data[0][7])
