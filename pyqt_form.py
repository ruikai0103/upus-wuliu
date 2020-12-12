import xlrd
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem
import sys
from Upus import LOPClass
from pyQt_upus import Ui_Form


class Upus(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "选择文件", "", 'Excel files(*.xlsx , *.xls)')
        global file_path_name
        file_path_name = file_name[0]

    def show_form(self):
        if len(file_path_name) > 0:
            show_file_path = file_path_name.split("/")[-1]
            self.ui.textBrowser.setText(show_file_path)

    def start_run(self):
        self.lop = LOPClass(file_path_name)
        self.lop.get_data()
        self.ui.show_text.append(",".join(self.lop.result_list) + "\n")

    def cleal_form(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    upus = Upus()
    upus.show()
    sys.exit(app.exec_())
