#此文件为登录窗口UI
# -*- coding: utf-8 -*-
import shutil
import traceback
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QPushButton, QToolButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt, QSize
from PIL import Image
import os
import random
import numpy as np
import ui.buttons


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlags(
            Qt.Window
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
        )

        def get_random_image(folder_path):
            # 定义支持的图像文件扩展名
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']

            # 获取文件夹中的所有文件，并过滤出图像文件
            files = [
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and
                   os.path.splitext(f)[1].lower() in image_extensions
            ]

            if not files:
                raise ValueError(f"No image files found in {folder_path}")

            random_image = random.choice(files)
            return os.path.join(folder_path, random_image).replace("\\", "/")
        try:
            image_path = r"C:\Fuchen\image"
            if not os.path.exists(image_path):
                os.makedirs(image_path)
                with open(os.path.join(image_path, '关于此文件夹.txt'), 'w') as f:
                    f.write('此文件夹为登录随机壁纸文件夹 请将文件放入此文件夹 每次登录将自动随机选择文件作为登录窗口背景\n')
                    f.write('目前支持的图片文件格式为: .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff')
            # 定义支持的图片扩展名集合
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}

            # 检查目录中是否存在图片文件
            if not any(
                    os.path.isfile(os.path.join(image_path, f)) and
                    os.path.splitext(f)[1].lower() in image_extensions  # 提取并检查扩展名
                    for f in os.listdir(image_path)
            ):
                source_folder = './image/Background'

                # 获取源文件夹中的所有文件和子文件夹
                contents = os.listdir(source_folder)

                # 移动每个文件或子文件夹到目标文件夹
                for item in contents:
                    source_path = os.path.join(source_folder, item)
                    destination_path = os.path.join(image_path, item)
                    shutil.move(source_path, destination_path)
        except:
            pass
        #folder_path = "./image/Background"
        folder_path = 'C:\\Fuchen\\image'
        try:
            random_background = get_random_image(folder_path)
            style_sheet = "#MainWindow{border-image: url('" + random_background + "');}"
            MainWindow.setStyleSheet(style_sheet)
        except Exception as e:
            #traceback.print_exc()
            pass
        # 读取随机选择的背景图片
        background_image = Image.open(random_background)  #用来计算右上角大致亮度 来设置控件颜色 防止用户无法正常点击控件
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
        self.Login_Label.setGeometry(QtCore.QRect(400, 100, 80, 50))
        #self.Login_Label.setStyleSheet("color: white;")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(25)
        self.Login_Label.setFont(font)
        self.Login_Label.setObjectName("label")
        self.Login_Label.setStyleSheet("color: white;")
        self.image_user = QtWidgets.QPushButton(self.centralwidget)
        self.image_user.setGeometry(QtCore.QRect(285, 220, 26, 26))
        self.image_user.setObjectName("image_user")
        self.image_user.setStyleSheet("QPushButton#image_user {"
                                               "    border-image: url(./image/Component/用户.png);"
                                               "}")

        self.Account_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Account_lineEdit.setGeometry(QtCore.QRect(330, 220, 270, 31))
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
        
        self.image_password = QToolButton(self.centralwidget)
        self.image_password.setGeometry(QtCore.QRect(285, 270, 28, 28))
        self.image_password.setObjectName("image_password")
        self.image_password.setIconSize(QSize(28, 28))
        self.image_password.setIcon(QIcon("./image/Component/密码2.png"))
        self.image_password.setStyleSheet("background: transparent; border: none; padding-left:0px")

        '''self.image_password.setStyleSheet("QPushButton#image_password {"
                                           "    border-image: url(./image/Component/密码2.png);"
                                           "}")'''

        self.Password_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Password_lineEdit.setGeometry(QtCore.QRect(330, 270, 270, 31))
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

        # 显示密码按钮
        self.show_password_button = QToolButton(self.centralwidget)
        self.show_password_button.setGeometry(QtCore.QRect(570, 270, 31, 31))
        self.show_password_button.setIconSize(QSize(25,25))
        self.show_password_button.setIcon(QIcon("./image/Component/显示密码.png"))  # 可使用图标或文字
        self.show_password_button.setStyleSheet("background: transparent; border: none;")

        # 绑定按钮的按下和松开事件
        self.show_password_button.pressed.connect(self.show_password)
        self.show_password_button.released.connect(self.hide_password)

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(490, 310, 115, 15))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("记住密码")
        self.checkBox.stateChanged.connect(self.sync_checkbox)
        self.checkBox.setToolTip("快捷键：CTRL+1")
        self.checkBox.setStyleSheet('''
            #checkBox {
                font-size: 15px;
                font-family: 等线;
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
        self.checkBox2.setGeometry(QtCore.QRect(490, 330, 115, 15))
        self.checkBox2.setFont(font)
        self.checkBox2.setObjectName("checkBox2")
        self.checkBox2.stateChanged.connect(self.sync_checkbox1)
        self.checkBox2.setToolTip("快捷键：CTRL+2")
        self.checkBox2.setStyleSheet('''
            #checkBox2 {
                font-size: 15px;
                font-family: 等线;
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

        style_font_10 = QtGui.QFont()
        style_font_10.setFamily("等线")
        style_font_10.setPointSize(10)

        self.Login_Button = ui.buttons.LoginAnimatedButton("登录",self.centralwidget)
        self.Login_Button.setGeometry(QtCore.QRect(320, 380, 240, 33))
        self.Login_Button.setObjectName("pushButton_2")
        self.Login_Button.setFont(style_font_10)

        self.Number_Label = QtWidgets.QLabel(self.centralwidget)
        self.Number_Label.setGeometry(QtCore.QRect(10, 475, 120, 16))
        self.Number_Label.setObjectName("label_7")
        self.Number_Label.setStyleSheet("color: white;")
        self.Number_Label.setText("当前在线人数:")

        self.Number_Label.setFont(style_font_10)
        self.Number_Label.setToolTip('游客不计入在内')

        self.Version_Label = QtWidgets.QLabel(self.centralwidget)
        self.Version_Label.setGeometry(QtCore.QRect(10, 455, 110, 12))
        self.Version_Label.setObjectName("label_8")
        self.Version_Label.setStyleSheet("color: white;")
        self.Version_Label.setText("V0.00")
        self.Version_Label.setFont(style_font_10)
        font = QtGui.QFont()
        font.setPointSize(14)

        #self.pushButton_more = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_more = ui.buttons.ComponentButton(self.centralwidget)
        self.pushButton_more.setGeometry(QtCore.QRect(790, 5, 24, 24))
        self.pushButton_more.setObjectName("pushButton_more")
        self.pushButton_more.setToolTip('更多')
        self.pushButton_more.setIcon(QIcon("./image/same/更多.png"))
        self.pushButton_more.setIconSize(QtCore.QSize(21, 21))

        #self.pushButton_short = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_short = ui.buttons.ComponentButton(self.centralwidget)
        self.pushButton_short.setGeometry(QtCore.QRect(820, 5, 24, 24))
        self.pushButton_short.setObjectName("pushButton_short")
        self.pushButton_short.setToolTip('最小化')
        self.pushButton_short.setIcon(QIcon("./image/short.png"))
        self.pushButton_short.setIconSize(QtCore.QSize(21, 21))

        self.pushButton_quit = ui.buttons.CloseButton(self.centralwidget, radius=4)
        self.pushButton_quit.setGeometry(QtCore.QRect(850, 5, 24, 24))
        self.pushButton_quit.setIcon(QIcon("./image/quit.png"))
        self.pushButton_quit.setIconSize(QtCore.QSize(22, 22))
        self.pushButton_quit.setObjectName("pushButton_quit")
        self.pushButton_quit.setToolTip('关闭')






        if brightness < 90:  #黑色背景白色控件
            self.pushButton_quit.setIcon(QIcon("./image/quit_white.png"))
            self.pushButton_short.setIcon(QIcon("./image/short_white.png"))
            self.pushButton_more.setIcon(QIcon("./image/same/更多2_white.png"))

        else:  #白色背景 黑色控件
            self.pushButton_quit.setIcon(QIcon("./image/quit.png"))
            self.pushButton_short.setIcon(QIcon("./image/short.png"))
            self.pushButton_more.setIcon(QIcon("./image/same/更多2.png"))


        self.pushButton_signin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_signin.setGeometry(QtCore.QRect(280, 310, 60, 20))
        self.pushButton_signin.setObjectName("pushButton_signin")
        self.pushButton_signin.setFont(style_font_10)

        self.pushButton_tourist = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tourist.setGeometry(QtCore.QRect(350, 310, 60, 20))
        self.pushButton_tourist.setObjectName("pushButton_tourist")
        self.pushButton_tourist.setFont(style_font_10)

        self.pushButton_reword = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reword.setGeometry(QtCore.QRect(420, 310, 60, 20))
        self.pushButton_reword.setObjectName("pushButton_reword")
        self.pushButton_reword.setFont(style_font_10)


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

    def show_password(self):
        # 显示密码
        self.Password_lineEdit.setEchoMode(QLineEdit.Normal)

    def hide_password(self):
        # 恢复为密码模式
        self.Password_lineEdit.setEchoMode(QLineEdit.Password)

    def sync_checkbox1(self, state):
        if state == 2:  # 当 checkBox1 被选中时，勾选 checkBox2
            self.checkBox.setChecked(True)
    def sync_checkbox(self, state):
        if state == 0:  # 当 checkBox1 被取消时，取消勾选 checkBox2
            if self.checkBox2.isChecked():
                self.checkBox2.setChecked(False)

    '''def showEvent(self, event):
        # 窗口显示后设置焦点
        self.Password_lineEdit.setFocus()
        super().showEvent(event)'''