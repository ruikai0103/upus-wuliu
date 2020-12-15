from base64 import b64decode

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import sys, os
from memory_pic import *
from Upus import LOPClass
from PyQt5.QtGui import QIcon
from pyQt_upus import Ui_Form


def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(b64decode(pic_code))
    image.close()


class Upus(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Upus物流查询")
        self.setWindowIcon(QIcon("upus.ico"))

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "选择文件", "", 'Excel files(*.xlsx , *.xls)')
        global file_path_name
        file_path_name = file_name[0]

    def show_form(self):
        if len(file_path_name) > 0:
            show_file_path = file_path_name.split("/")[-1]
            self.ui.textBrowser.setText(show_file_path)
            # 查询按钮可以点击
            self.ui.pushButton.setEnabled(True)

    def show_result_form(self):
        # 获取页面参数
        sleep_time = self.ui.sleep_time.text()
        thread_num = self.ui.thread_num.text()

        # 程序开始执行  按钮不可点击
        self.ui.pushButton.setEnabled(False)
        radio_ip_isChecked = self.ui.radioButton.isChecked()
        print(radio_ip_isChecked)
        self.myThread = LOPClass(file_path_name, sleep_time, thread_num, radio_ip_isChecked)
        # 接受信号产生回调参数
        self.myThread.update_data.connect(self.Display)
        # 启动线程
        self.myThread.start()
        # 结束可以点击按钮
        self.ui.pushButton.setEnabled(True)

    def radio_change(self):
        pass

    def Display(self, data):
        self.ui.show_text.append(data + "\n")
        self.ui.show_text.moveCursor(self.ui.show_text.textCursor().End)
        QApplication.processEvents()

        # self.ui.show_text.append("开始查询:请勿多次点击！！开始可能会有卡顿。")
        # self.ui.show_text.moveCursor(self.ui.show_text.textCursor().End)
        # QApplication.processEvents()
        # self.lop = LOPClass(file_path_name,sleep_time,thread_num)
        # result_list = self.lop.get_data(sleep_time)
        # for result in result_list:
        #     self.ui.show_text.append(",".join(result) + "\n")
        #     self.ui.show_text.moveCursor(self.ui.show_text.textCursor().End)
        #     QApplication.processEvents()
        #     print(result)
        #     # import time
        #     # time.sleep(1)
        # else:
        #     self.ui.show_text.append("----------------查询完了----------------")
        #     # 结束后可以点击
        #     self.ui.pushButton.setEnabled(True)


if __name__ == '__main__':
    get_pic(upus_ico, "upus.ico")
    # os.remove('upus.ico')
    app = QApplication(sys.argv)
    upus = Upus()
    upus.show()
    sys.exit(app.exec_())
