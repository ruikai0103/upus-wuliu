# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\hello\zhuye.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(478, 465)

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 60, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(60, 170, 351, 251))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.yunxing)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))


from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import re
from threading import Thread
import PyQt5.sip

import time
from PyQt5.QtWidgets import QApplication, QWidget



# 1.首先 继承QtCore.QThrea这个类 （这个类中是在按钮点击之后的槽函数进行实例化与运行的）
class Runthread(QtCore.QThread):
    # 4定义信号参数为str类型
    updata_date = QtCore.pyqtSignal(str)

    # 2进行父类的初始化
    def __init__(self, kw):
        super(Runthread, self).__init__()
        self.kw = kw

    # 3将要实现的逻辑代码存放到这个里面
    def run(self):

        print("开始")
        self.get_url_page(self.kw)
        print("结束")

    def get_url_page(self, leimu, ):

        main_url = r'http://jwc.qfnu.edu.cn/' + leimu + '.htm'
        rs = requests.get(main_url)
        rs.encoding = "UTF-8"
        p_index = re.compile(r"共.*?&nbsp;&nbsp;1/(.*?)&nbsp;</td>")
        y_index = p_index.search(rs.text)
        paginate = y_index.group(1)
        for x in range(0, int(paginate)):
            if x == 0:
                fenye_url = main_url

            else:
                fenye_url = "http://jwc.qfnu.edu.cn/" + leimu + "/" + str(x) + ".htm"
            self.paqu(fenye_url, leimu)

    def paqu(self, url, leimu):
        url_content = requests.get(url)
        url_content.encoding = "UTF-8"
        self.updata_date.emit(str(time.time()))
        p = re.compile(r'<a href="(.*?)" target="_blank" title=".*?">(.*?)</a>\r\n   <span class="time">(.*?)</span>', )
        for m in p.finditer(url_content.text):
            time.sleep(1)

            a = m.group(1) + "\n" + m.group(2) + "\n" + m.group(3)
            # 5发送信号，触发打印函数（Display）
            self.updata_date.emit(str(a))

            print(m.group(1))
            print(m.group(2))
            print(m.group(3))
            print(leimu)

            print("\n")


class MyCalc(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def yunxing(self):
        #

        self.myThread = Runthread("tz_j_")
        # 6.接收信号并产生回调函数
        self.myThread.updata_date.connect(self.Display)

        self.myThread.start()

    # 7我是回调函数
    def Display(self, data):
        self.ui.textEdit.append(data)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    win = MyCalc()
    win.show()
    sys.exit(app.exec_())