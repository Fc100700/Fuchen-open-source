# -*- coding: utf-8 -*-
import traceback
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PIL import Image
import os
import random
import numpy as np
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTextBrowser, QPushButton, QDesktopWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlags(Qt.FramelessWindowHint) # 隐藏边框

        def get_random_file(folder_path):
            # 获取文件夹中的所有文件
            files = os.listdir(folder_path)
            # 从文件列表中随机选择一个文件
            random_file = random.choice(files)
            # 返回选定的文件的完整路径，并将反斜杠替换为正斜杠
            return os.path.join(folder_path, random_file).replace("\\", "/")

        folder_path = "./image/Background"
        random_background = get_random_file(folder_path)
        style_sheet = "#MainWindow{border-image: url('" + random_background + "');}"
        try:
            MainWindow.setStyleSheet(style_sheet)
        except Exception as e:
            traceback.print_exc()
        # 读取随机选择的背景图片
        background_image = Image.open(random_background)

        # 定义要计算亮度的区域范围，右上角
        top_left_x = background_image.size[0]-50
        top_left_y = 0
        width = 50
        height = 50
        # 转换为 numpy 数组
        image_data = np.array(background_image)
        # 获取指定区域的像素数据
        region_data = image_data[top_left_y:top_left_y + height, top_left_x:top_left_x + width]

        # 计算区域内所有像素的平均亮度
        brightness_values = np.dot(region_data[..., :3], [0.299, 0.587, 0.114])
        brightness = np.mean(brightness_values)
        # 根据亮度值判断使用哪种背景图片
        MainWindow.resize(880, 500)
        font = QtGui.QFont()
        font.setFamily("黑体")
        MainWindow.setFont(font)
        MainWindow.setFixedSize(880, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Login_Label = QtWidgets.QLabel(self.centralwidget)
        self.Login_Label.setGeometry(QtCore.QRect(400, 90, 80, 50))
        self.Login_Label.setStyleSheet("color: white;")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(25)
        self.Login_Label.setFont(font)
        self.Login_Label.setObjectName("label")

        self.image_user = QtWidgets.QPushButton(self.centralwidget)
        self.image_user.setGeometry(QtCore.QRect(285, 220, 26, 26))
        self.image_user.setObjectName("image_user")
        self.image_user.setStyleSheet("QPushButton#image_user {"
                                               "    border-image: url(./image/Component/用户.png);"
                                               "}")

        self.Account_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Account_lineEdit.setGeometry(QtCore.QRect(330, 220, 280, 31))
        self.Account_lineEdit.setObjectName("lineEdit")
        self.Account_lineEdit.setStyleSheet(
            "QLineEdit {"
            "border: none;"
            "border-bottom: 1px solid #FFFFFF;"  # 下划线样式
            "background: transparent;"  # 设置背景为透明
            "color: #FFFFFF;"  # 文本颜色
            "font-size: 17px;"
            "}"
        )
        self.Account_lineEdit.setPlaceholderText("输入账号或邮箱")
        
        self.image_password = QtWidgets.QPushButton(self.centralwidget)
        self.image_password.setGeometry(QtCore.QRect(285, 270, 26, 26))
        self.image_password.setObjectName("image_password")
        self.image_password.setStyleSheet("QPushButton#image_password {"
                                           "    border-image: url(./image/Component/密码2.png);"
                                           "}")

        self.Password_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Password_lineEdit.setGeometry(QtCore.QRect(330, 270, 280, 31))
        self.Password_lineEdit.setStyleSheet(
            "QLineEdit {"
            "border: none;"
            "border-bottom: 1px solid #FFFFFF;"  # 下划线样式
            "background: transparent;"  # 设置背景为透明
            "color: #FFFFFF;"  # 文本颜色
            "font-size: 17px;"
            "}"
        )
        self.Password_lineEdit.setPlaceholderText("输入密码")
        self.Password_lineEdit.setEchoMode(QLineEdit.Password)
        self.Password_lineEdit.setObjectName("lineEdit_2")

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(500, 310, 115, 15))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("记住密码")
        self.checkBox.stateChanged.connect(self.sync_checkbox)
        self.checkBox.setStyleSheet('''
            #checkBox {
                font-size: 18px;
                color: #FFFFFF;
            }

            #checkBox::indicator {
                padding-top: 1px;
                width: 35px;
                height: 31px;
                border: none;
            }

            #checkBox::indicator:unchecked {
                image: url(./image/Component/开关1.svg);
            }

            #checkBox::indicator:checked {
                image: url(./image/Component/开关2.svg);
            }
        ''')

        self.checkBox2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox2.setGeometry(QtCore.QRect(500, 330, 115, 15))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.checkBox2.setFont(font)
        self.checkBox2.setObjectName("checkBox2")
        self.checkBox2.stateChanged.connect(self.sync_checkbox1)
        self.checkBox2.setStyleSheet('''
            #checkBox2 {
                font-size: 18px;
                color: #FFFFFF; /* 设置字体颜色为白色 */
            }

            #checkBox2::indicator {
                padding-top: 1px;
                width: 35px;
                height: 31px;
                border: none;
            }

            #checkBox2::indicator:unchecked {
                image: url(./image/Component/开关1.svg);
            }

            #checkBox2::indicator:checked {
                image: url(./image/Component/开关2.svg);
            }
        ''')

        self.Login_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Login_Button.setGeometry(QtCore.QRect(340, 380, 200, 31))
        self.Login_Button.setObjectName("pushButton_2")
        self.Login_Button.setStyleSheet(
            "QPushButton {"
            "background-color: rgb(120, 187, 235);"  # 默认颜色
            "border-radius: 13px;"
            "color: #FFFFFF;"
            "}"
            "QPushButton:hover {"
            "background-color: rgb(100, 187, 235);"  # 悬停时的颜色
            "}"
            "QPushButton:pressed {"
            "background-color: rgb(35, 138, 175);"  # 点击时的颜色
            "}"
        )

        self.Number_Label = QtWidgets.QLabel(self.centralwidget)
        self.Number_Label.setGeometry(QtCore.QRect(10, 475, 120, 16))
        self.Number_Label.setObjectName("label_7")
        self.Number_Label.setStyleSheet("color: white;")
        self.Version_Label = QtWidgets.QLabel(self.centralwidget)
        self.Version_Label.setGeometry(QtCore.QRect(10, 455, 65, 12))
        self.Version_Label.setObjectName("label_8")
        self.Version_Label.setStyleSheet("color: white;")
        self.Number_Label.setText("当前在线人数:")
        self.Version_Label.setText("V0.00")


        self.pushButton_short = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_short.setGeometry(QtCore.QRect(820, 0, 21, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_short.setFont(font)
        self.pushButton_short.setObjectName("pushButton_short")
        self.pushButton_short.setToolTip('最小化')

        self.pushButton_quit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_quit.setGeometry(QtCore.QRect(850, 0, 21, 21))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.pushButton_quit.setToolTip('关闭')

        if brightness < 90:  #黑色主题 白色控件
            self.pushButton_quit.setStyleSheet("QPushButton#pushButton_quit {"
                                               "    border-image: url(./image/quit_white.png);"
                                               "}")
            self.pushButton_short.setStyleSheet("QPushButton#pushButton_short {"
                                               "    border-image: url(./image/short_white.png);"
                                               "}")
        else:  #白色主题 黑色控件
            self.pushButton_quit.setStyleSheet("QPushButton#pushButton_quit {"
                                               "    border-image: url(./image/quit.png);"
                                               "}")
            self.pushButton_short.setStyleSheet("QPushButton#pushButton_short {"
                                               "    border-image: url(./image/short.png);"
                                               "}")


        self.pushButton_signin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_signin.setGeometry(QtCore.QRect(280, 310, 60, 20))
        self.pushButton_signin.setObjectName("pushButton_signin")

        self.pushButton_tourist = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tourist.setGeometry(QtCore.QRect(350, 310, 60, 20))
        self.pushButton_tourist.setObjectName("pushButton_tourist")

        self.pushButton_reword = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reword.setGeometry(QtCore.QRect(420, 310, 60, 20))
        self.pushButton_reword.setObjectName("pushButton_reword")


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login_Window"))
        self.Login_Label.setText(_translate("MainWindow", "登 录"))
        self.pushButton_signin.setText(_translate("MainWindow", "注册账号"))
        self.pushButton_signin.setStyleSheet("color: white;background-color: transparent;")  # 将按钮背景设置为透明
        self.pushButton_signin.setCursor(QCursor(Qt.PointingHandCursor))
        self.checkBox2.setText(_translate("MainWindow", "自动登录"))
        self.Login_Button.setText(_translate("MainWindow", "登录"))
        self.pushButton_tourist.setText(_translate("MainWindow","游客登录"))
        self.pushButton_tourist.setStyleSheet("color: white;background-color: transparent;")
        self.pushButton_tourist.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_reword.setText(_translate("MainWindow", "忘记密码"))
        self.pushButton_reword.setStyleSheet("color: white;background-color: transparent;")
        self.pushButton_reword.setCursor(QCursor(Qt.PointingHandCursor))

    def sync_checkbox1(self, state):
        if state == 2:  # 当 checkBox1 被选中时，勾选 checkBox2
            self.checkBox.setChecked(True)
    def sync_checkbox(self, state):
        if state == 0:  # 当 checkBox1 被选中时，勾选 checkBox2
            if self.checkBox2.isChecked():
                self.checkBox2.setChecked(False)
