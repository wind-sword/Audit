import os
import sys
from logis_fir import call_index
from PyQt5 import QtWidgets

if __name__ == '__main__':
    # 切换目录到当前目录
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    app = QtWidgets.QApplication(sys.argv)
    call_index = call_index.Call_index()
    call_index.show()
    sys.exit(app.exec_())