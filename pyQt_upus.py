# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyQt_upus.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(738, 495)
        Form.setMinimumSize(QtCore.QSize(738, 495))
        Form.setMaximumSize(QtCore.QSize(738, 495))
        self.openFile = QtWidgets.QPushButton(Form)
        self.openFile.setGeometry(QtCore.QRect(20, 30, 75, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.openFile.setFont(font)
        self.openFile.setObjectName("openFile")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(590, 30, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(110, 30, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.show_text = QtWidgets.QTextBrowser(Form)
        self.show_text.setGeometry(QtCore.QRect(10, 150, 711, 331))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.show_text.setFont(font)
        self.show_text.setObjectName("show_text")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(380, 30, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.thread_num = QtWidgets.QSpinBox(Form)
        self.thread_num.setGeometry(QtCore.QRect(450, 30, 61, 31))
        self.thread_num.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.thread_num.setFont(font)
        self.thread_num.setMinimum(1)
        self.thread_num.setMaximum(50)
        self.thread_num.setObjectName("thread_num")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(380, 70, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.sleep_time = QtWidgets.QSpinBox(Form)
        self.sleep_time.setGeometry(QtCore.QRect(450, 70, 61, 31))
        self.sleep_time.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.sleep_time.setFont(font)
        self.sleep_time.setMaximum(5)
        self.sleep_time.setObjectName("sleep_time")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(33, 83, 221, 41))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radioButton = QtWidgets.QRadioButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        spacerItem1 = QtWidgets.QSpacerItem(18, 28, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)

        self.retranslateUi(Form)
        self.openFile.clicked.connect(Form.open_file)
        self.pushButton.clicked.connect(Form.show_result_form)
        self.openFile.clicked.connect(Form.show_form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.openFile.setText(_translate("Form", "打开"))
        self.pushButton.setText(_translate("Form", "查询"))
        self.label.setText(_translate("Form", "线程数："))
        self.label_2.setText(_translate("Form", "等    待："))
        self.label_3.setText(_translate("Form", "代理IP："))
        self.radioButton.setText(_translate("Form", "是"))
        self.radioButton_2.setText(_translate("Form", "否"))
