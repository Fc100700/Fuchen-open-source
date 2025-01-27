#此文件为重置密码窗口UI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("重置密码")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 220)
        MainWindow.setFixedSize(440,220)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 35, 71, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 71, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        font_line = QtGui.QFont()
        font_line.setFamily("等线")
        font_line.setPointSize(13)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 40, 271, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(font_line)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 100, 161, 28))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFont(font_line)

        regex = QRegExp(r'\d{6}')
        validator = QRegExpValidator(regex)
        self.lineEdit_2.setValidator(validator)

        self.pushButton_getcheck = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_getcheck.setGeometry(QtCore.QRect(285, 100, 105, 30))
        font_11 = QtGui.QFont()
        font_11.setFamily("等线")
        font_11.setPointSize(11)
        self.pushButton_getcheck.setFont(font_11)
        self.pushButton_getcheck.setObjectName("pushButton_getcheck")
        self.pushButton_getcheck.setStyleSheet("""
                    QPushButton#pushButton_getcheck {
                        background-color: #55c3ff;
                        border: 2px solid #55c3ff;
                        color: white;
                        border-radius: 10px;
                    }
                    QPushButton#pushButton_getcheck:hover {
                        background-color: #3e8eaa;
                        border: 2px solid #3e8eaa;
                    }
                    QPushButton#pushButton_getcheck:pressed {
                        background-color: #27819f;
                        border: 2px solid #27819f;
                    }
                """)

        self.pushButton_check = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_check.setGeometry(QtCore.QRect(120, 160, 201, 31))
        self.pushButton_check.setObjectName("pushButton_check")
        self.pushButton_check.setFont(font_11)

        self.label_a = QtWidgets.QLabel(self.centralwidget)
        self.label_a.setGeometry(QtCore.QRect(530, 35, 71, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(16)
        self.label_a.setFont(font)
        self.label_a.setObjectName("label_a")
        self.label_a2 = QtWidgets.QLabel(self.centralwidget)
        self.label_a2.setGeometry(QtCore.QRect(530, 90, 91, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_a2.setFont(font)
        self.label_a2.setObjectName("label_a2")
        self.lineEdit_a = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_a.setGeometry(QtCore.QRect(650, 40, 271, 28))
        self.lineEdit_a.setObjectName("lineEdit_a")
        self.lineEdit_a.setFont(font_line)
        self.lineEdit_a2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_a2.setGeometry(QtCore.QRect(650, 100, 271, 28))
        self.lineEdit_a2.setObjectName("lineEdit_a2")
        self.lineEdit_a2.setEchoMode(QLineEdit.Password)
        self.lineEdit_a2.setFont(font_line)
        self.pushButton_a = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_a.setGeometry(QtCore.QRect(650, 160, 201, 31))
        self.pushButton_a.setObjectName("pushButton_a")
        self.pushButton_a.setFont(font_11)

        #MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "邮箱："))
        self.label_2.setText(_translate("MainWindow", "验证码："))
        self.pushButton_getcheck.setText(_translate("MainWindow", "获取验证码"))
        self.pushButton_check.setText(_translate("MainWindow", "验证"))

        self.label_a.setText(_translate("MainWindow", "密码："))
        self.label_a2.setText(_translate("MainWindow", "确认密码："))
        self.pushButton_a.setText(_translate("MainWindow", "确认修改"))
