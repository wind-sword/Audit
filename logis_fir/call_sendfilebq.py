from PyQt5 import QtWidgets

from uipy_dir.sendfilebq import Ui_Dialog
from logis_fir.tools import tools


class Call_sendfilebq(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, key):
        super().__init__()
        self.setupUi(self)

        self.xh = key  # 发文表主键

        # 初始化页面数据
        self.displaySendfilebqDetail()

        self.pushButton_revise.clicked.connect(self.reviseSendfilebqDetail)
        self.pushButton_quit.clicked.connect(self.closeWindow)

    def displaySendfilebqDetail(self):
        sql = "select 标识,签发人,份数,公文运转情况,批示办理情况,起草处室 from sendfile where 序号 = %s" % self.xh
        data = tools.executeSql(sql)

        self.lineEdit_1.setText(data[0][0])  # 标识
        self.lineEdit_2.setText(data[0][1])  # 签发人
        if data[0][2] is None:
            self.spinBox.setValue(0)
        else:
            self.spinBox.setValue(data[0][2])  # 份数
        self.lineEdit_3.setText(data[0][3])  # 公文运转情况
        self.lineEdit_4.setText(data[0][4])  # 批示办理情况
        self.lineEdit_5.setText(data[0][5])  # 起草处室

    def reviseSendfilebqDetail(self):
        input1 = self.lineEdit_1.text()  # 标识
        input2 = self.lineEdit_2.text()  # 签发人
        input3 = self.spinBox.value()  # 份数
        input4 = self.lineEdit_3.text()  # 公文运转情况
        input5 = self.lineEdit_4.text()  # 批示办理情况
        input6 = self.lineEdit_5.text()  # 起草处室

        sql = "update sendfile set 标识 = '%s',签发人 = '%s',份数 = %s,公文运转情况 = '%s',批示办理情况 = '%s',起草处室 = '%s' where 序号 = %s" % (
            input1, input2, input3, input4, input5, input6, self.xh)
        tools.executeSql(sql)

        QtWidgets.QMessageBox.information(self, "提示", "修改成功！")

        self.close()

    def closeWindow(self):
        self.close()
