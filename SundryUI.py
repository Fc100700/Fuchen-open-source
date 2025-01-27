import random
import re
import subprocess
import sys
import turtle
from PyQt5.QtCore import Qt, QRectF, QRect, QPropertyAnimation, QTimer, QSize, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QBrush, QPainterPath, QFont, QCursor, QLinearGradient, QPen
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QLabel, QLineEdit, QTextEdit, QToolButton, \
    QMessageBox, QPushButton, QSystemTrayIcon, QAction, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt5 import QtGui, QtWidgets, QtCore
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import ui.style
import ui.buttons
from datetime import date
import pyautogui
from PIL import Image
import time
import json
import tkinter as tk
from SocketThread import socket_information
'''from ctypes import cdll
from ctypes.wintypes import HWND'''
from ui.style import style_lineEdit
import os

style_Radio = ui.style.style_Radio
style_font_9 = ui.style.style_font_9
style_font_10 = ui.style.style_font_10
style_font_11 = ui.style.style_font_11


def Check(input_str):  # 检测名称
    # 定义允许的字符集合：中文、大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def Check_Password(input_str):
    # 定义允许的字符集合：大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def encrypt(message,text, txt):  #网络数据传输加密 因开源所以无法展示
    message = message

def decrypt(ciphertext,text,txt): #网络数据传输加密 因开源所以无法展示
    ciphertext = ciphertext

def send_encry(text):  #网络数据传输加密 因开源所以无法展示
    text = text

def send_decry(text):  #网络数据传输加密 因开源所以无法展示
    text = text

class UpdateDialog(QtWidgets.QDialog):
    def __init__(self, lis):
        super().__init__()
        global Version, Versions
        Version = lis[0]
        Versions = lis[1]
        self.setWindowTitle("更新提示")
        self.result = None
        self.setFixedSize(300, 120)
        self.init_ui()

    def init_ui(self):
        # 设置布局
        layout = QtWidgets.QVBoxLayout(self)
        icon = QIcon("./image/same/更新.png")
        self.setWindowIcon(icon)
        font = QFont()
        font.setFamily("等线")
        font.setPointSize(12)

        # 提示信息
        label = QtWidgets.QLabel(f"当前版本为:{Version} 现已发布新版{Versions}\n此版本为强制更新 是否更新? \n\n推荐使用网盘更新 自动更新速度较慢")
        label.setFont(font)
        layout.addWidget(label)

        font = QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        # 创建按钮
        button_layout = QtWidgets.QHBoxLayout()
        btn_auto = QtWidgets.QPushButton("自动更新")
        btn_auto.clicked.connect(lambda: self.set_result("auto_update"))
        btn_auto.setFont(font)
        button_layout.addWidget(btn_auto)

        btn_cloud = QtWidgets.QPushButton("网盘更新")
        btn_cloud.clicked.connect(lambda: self.set_result("cloud_update"))
        btn_cloud.setFont(font)
        button_layout.addWidget(btn_cloud)

        btn_cancel = QtWidgets.QPushButton("取消更新")
        btn_cancel.clicked.connect(lambda: self.set_result("cancel_update"))
        btn_cancel.setFont(font)
        button_layout.addWidget(btn_cancel)

        layout.addLayout(button_layout)


    def set_result(self, result):
        self.result = result
        self.accept()  # 关闭对话框并返回结果

    def closeEvent(self, event):
        # 当用户点击右上角的关闭按钮时，将返回值设置为“取消更新”
        self.result = "cancel_update"
        super().closeEvent(event)


# 创建一个函数来显示消息提示框并返回结果
def show_update_dialog(lis):
    app = QtWidgets.QApplication(sys.argv)
    dialog = UpdateDialog(lis)
    dialog.exec_()  # 显示对话框并等待用户操作
    return dialog.result


class DownloadDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.selected_method = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("下载方式选择")
        self.setFixedSize(300, 100)

        # 创建布局和部件
        layout = QVBoxLayout()
        label = QLabel("请选择你的下载方式\n自动下载处于测试阶段 如果下载失败请手动下载")

        # 按钮布局
        btn_layout = QHBoxLayout()
        self.btn_manual = QPushButton("手动下载")
        self.btn_auto = QPushButton("自动下载")

        # 连接信号
        self.btn_manual.clicked.connect(self.select_manual)
        self.btn_auto.clicked.connect(self.select_auto)

        # 将部件添加到布局
        btn_layout.addWidget(self.btn_manual)
        btn_layout.addWidget(self.btn_auto)

        layout.addWidget(label)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def select_manual(self):
        self.selected_method = "manual"
        self.accept()  # 关闭对话框并返回Accepted

    def select_auto(self):
        self.selected_method = "auto"
        self.accept()

class UserInfo(QWidget):
    def __init__(self, lis):
        super().__init__()
        global windows, Account, Name, HImage_date, exp, skt, keys, ivs, Lv,HImage_load_status,  Max_exp
        windows = lis[0]
        Account = lis[1]
        Name = lis[2]
        HImage_date = lis[3]
        exp = lis[4]
        skt = lis[5]
        keys = lis[6]
        ivs = lis[7]
        HImage_load_status = lis[8]
        if 0 <= exp < 20:
            Lv = "Lv1"
            Max_exp = 20
        elif 20 <= exp <300:
            Lv = "Lv2"
            Max_exp = 300
        elif 300 <= exp < 600:
            Lv = "Lv3"
            Max_exp = 600
        elif 600 <= exp <1000:
            Lv = "Lv4"
            Max_exp = 1000
        elif 1000 <= exp:
            Lv = "Lv5"
            Max_exp = 9999

        window_position = windows.pos()
        x = window_position.x() + 260
        y = window_position.y() + 10
        icon = QIcon("./image/Component/提示.png")
        self.setWindowIcon(icon)
        self.setGeometry(x, y, 380, 210)
        self.setFixedSize(380, 210)
        self.setWindowTitle("Fuchen个人信息")
        self.border_width = 8
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 设置 窗口无边框和背景透明

        self.exp_label = QLabel(self)
        self.exp_label.setGeometry(QRect(20, 190, 110, 3))
        self.exp_label.setStyleSheet("background-color: rgb(238, 238, 238);")  # 设置为灰色

        self.proccess = int(exp) / Max_exp * 100
        if self.proccess > 100:
            self.proccess = 100

        self.exp_label2 = QLabel(self)
        self.exp_label2.setGeometry(
            QRect(20, 190, int(self.proccess), 3))
        if exp < 300:
            self.exp_label2.setStyleSheet("background-color: rgb(0, 138, 225);")  # 设置标签的背景颜色为蓝色
        elif 300 < exp < 1000:
            self.exp_label2.setStyleSheet("background-color: rgb(255, 119, 0);")  # 设置标签的背景颜色为橙色
        elif 1000 < exp:
            self.exp_label2.setStyleSheet("background-color: rgb(255, 61, 54);")  # 设置标签的背景颜色为红色
        self.exp_label3 = QLabel(self)
        self.exp_label3.setGeometry(QRect(20, 170, 100, 20))  # 设置标签的位置和大小
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(13)
        self.exp_label3.setFont(font)

        self.exp_label3.setText(Lv)

        self.exp_label4 = QLabel(self)

        self.exp_label4.setGeometry(QRect(90, 173, 50, 20))  # 设置标签的位置和大小
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(9)
        self.exp_label4.setFont(font)
        self.exp_label4.setText(f"{exp}/{Max_exp}")
        if Lv == "Lv5":
            color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
            self.exp_label3.setStyleSheet(f"color: red;")  # 设置字体颜色
            self.exp_label4.setGeometry(QRect(75, 173, 60, 20))  # 设置标签的位置和大小

        self.Button = QToolButton(self)
        self.Button.setGeometry(QRect(20, 20, 100, 100))
        if HImage_load_status == True:  # 判断头像是否成功加载
            self.Button.setIcon(QIcon("./temp/HImage.png"))
        else:
            self.Button.setIcon(QIcon("./image/float/fc.png"))
        self.Button.setIconSize(QSize(100, 100))
        self.Button.setObjectName("Button")
        self.Button.setStyleSheet(
            "QToolButton { background: transparent; padding: 0;border: none; }")

        '''self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QRect(340, 15, 26, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2 {"
                                        "    border-image: url(./image/quit.png);"
                                        "    background-color: rgb(255, 255, 255)"
                                        "}")
        self.pushButton_2.setToolTip("关闭")
        self.pushButton_2.clicked.connect(self.close)'''

        self.Button_Close = ui.buttons.CloseButton(self,radius=4)
        self.Button_Close.setGeometry(340, 15, 24, 24)
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QtCore.QSize(22, 22))
        self.Button_Close.setObjectName("Button_Close")
        self.Button_Close.clicked.connect(self.close)

        self.label = QLabel(self)  # 名字标签
        self.label.setGeometry(QRect(140, 20, 180, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText(f"{Name}")

        self.label_2 = QLabel(self)  # 账号ID标签
        self.label_2.setGeometry(QRect(140, 60, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setText(f"ID:{Account}")
        self.label_2.setFont(ui.style.style_font_9)

        self.toolButton = ui.buttons.AnimatedButton(self)
        self.toolButton.setGeometry(QRect(20, 137, 101, 21))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.setText("上传头像")
        self.toolButton.setFont(ui.style.style_font_10)
        self.toolButton.clicked.connect(self.renew_HImage)

        style = """
                    QToolButton {
                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                        background-color: transparent;    /* 设置透明背景 */
                        border-radius: 2px;    /* 设置圆角 */
                    }
                    QToolButton:hover {
                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                    }"""

        self.toolButton_2 = QToolButton(self)  # 编辑资料按钮
        self.toolButton_2.setGeometry(QRect(140, 80, 90, 19))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_2.setText("修改名称")
        self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_2.clicked.connect(lambda: self.show_control('name_open'))
        self.toolButton_2.setStyleSheet(style)
        self.toolButton_2.setFont(ui.style.style_font_10)

        self.toolButton_password = QToolButton(self)  # 编辑资料按钮
        self.toolButton_password.setGeometry(QRect(240, 80, 90, 19))
        self.toolButton_password.setObjectName("toolButton_password")
        self.toolButton_password.setText("修改密码")
        self.toolButton_password.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_password.clicked.connect(lambda: self.show_control('password_open'))
        self.toolButton_password.setStyleSheet(style)
        self.toolButton_password.setFont(ui.style.style_font_10)

        self.toolButton_3 = QToolButton(self)  # 编辑资料按钮
        self.toolButton_3.setGeometry(QRect(140, 80, 90, 19))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_3.setText("完成编辑")
        self.toolButton_3.setStyleSheet(style)
        self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_3.setVisible(False)
        self.toolButton_3.clicked.connect(lambda: self.ReEdit("name"))
        self.toolButton_3.setFont(ui.style.style_font_10)

        self.toolButton_pass = QToolButton(self)  # 编辑资料按钮
        self.toolButton_pass.setGeometry(QRect(240, 80, 90, 19))
        self.toolButton_pass.setObjectName("toolButton_pass")
        self.toolButton_pass.setText("完成编辑")
        self.toolButton_pass.setStyleSheet(style)
        self.toolButton_pass.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_pass.setVisible(False)
        self.toolButton_pass.clicked.connect(lambda: self.ReEdit("password"))
        self.toolButton_pass.setFont(ui.style.style_font_10)

        self.label_4 = QLabel(self)  # 名称标签
        self.label_4.setGeometry(QRect(140, 100, 54, 18))
        self.label_4.setObjectName("label_4")
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setText("名称:")
        self.label_4.setVisible(False)

        self.lineEdit_2 = QLineEdit(self)  # 名称修改行
        self.lineEdit_2.setGeometry(QRect(140, 120, 221, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("请输入需要修改的名称")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet(style_lineEdit)
        self.lineEdit_2.setVisible(False)

        self.label_5 = QLabel(self)  # 密码标签
        self.label_5.setGeometry(QRect(140, 100, 54, 18))
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(font)
        self.label_5.setText("密码:")
        self.label_5.setVisible(False)

        self.lineEdit_3 = QLineEdit(self)  # 密码修改行
        self.lineEdit_3.setGeometry(QRect(140, 120, 221, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setPlaceholderText("请输入需要修改的密码")
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet(style_lineEdit)
        self.lineEdit_3.setVisible(False)

    def show_control(self, mode):
        if mode == 'name_open':
            if self.lineEdit_3.isVisible():
                self.lineEdit_3.setVisible(False)
                self.label_5.setVisible(False)
                self.toolButton_password.setVisible(True)
                self.toolButton_pass.setVisible(False)
            self.lineEdit_2.setVisible(True)
            self.label_4.setVisible(True)
            self.toolButton_2.setVisible(False)
            self.toolButton_3.setVisible(True)

        elif mode == 'password_open':
            if self.lineEdit_2.isVisible():
                self.lineEdit_2.setVisible(False)
                self.label_4.setVisible(False)
                self.toolButton_2.setVisible(True)
                self.toolButton_3.setVisible(False)
            self.lineEdit_3.setVisible(True)
            self.label_5.setVisible(True)
            self.toolButton_password.setVisible(False)
            self.toolButton_pass.setVisible(True)
        elif mode == 'name_close':
            self.lineEdit_2.setVisible(False)
            self.label_4.setVisible(False)
            self.toolButton_3.setVisible(False)
            self.toolButton_2.setVisible(True)
        elif mode == 'password_close':
            self.lineEdit_3.setVisible(False)
            self.label_5.setVisible(False)
            self.toolButton_pass.setVisible(False)
            self.toolButton_password.setVisible(True)

    def show_message_box(self, head, message):
        QMessageBox.question(self, head, message)

    def ReEdit(self, mode):
        if mode == 'name':
            ReName = self.lineEdit_2.text()
            if ReName == '':
                self.show_control('name_close')
            else:
                if not (1 < len(ReName) < 11):
                    self.show_message_box("提示", "名称只能为2-10位")
                elif Check(ReName) == True:
                    self.show_message_box("提示",
                                          "名称只能包含中文,26个英文大小写字母,数字以及 - . ? ~ _")
                else:
                    send_encry(f'10006 {ReName}', skt, keys, ivs )
                    Name = ReName
                    windows.update_information(Name)
                    windows.uim.HButton.setText(f"{Name}")
                    self.Button.setText(f"{Name}")
                    self.show_message_box("提示",
                                          "信息修改成功\n名称已经修改成功 个人信息窗口可能会未刷新\n实际已修改成功 重启客户端即可刷新!")
                    self.close()
        else:
            RePassword = self.lineEdit_3.text()
            if RePassword == '':
                self.show_control('password_close')
            else:
                if not (7 < len(RePassword) < 16):
                    self.show_message_box("提示", "密码只能为8-15位")
                elif Check_Password(RePassword) == True:
                    self.show_message_box("提示",
                                          "密码只能包含26个英文大小写字母,数字以及 - . ? ~ _")
                else:
                    send_encry(f'10007 {RePassword}', skt, keys, ivs )
                    self.show_message_box("提示", "密码修改成功")
                    self.close()

    def renew_HImage(self):
        current_date = date.today()
        # 计算日期差异
        delta = current_date - HImage_date
        days_diff = delta.days
        if days_diff < 3:
            pyautogui.confirm("距上次修改头像未满三天")
        else:
            file_dialog = QFileDialog(self)
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            f_path, _ = file_dialog.getOpenFileName(self, "Select File", "",
                                                    "Image Files (*.jpg *.png)",
                                                    options=options)
            if f_path != '':
                if (f_path[-4:] == '.jpg' or f_path[-4:] == '.png'):
                    send_encry('10005', skt, keys, ivs )

                    def crop_and_compress(image_path, save_path):
                        # 打开原始图片
                        image = Image.open(image_path)
                        # 将图像转换为RGB模式
                        image = image.convert("RGB")
                        # 裁剪为正方形
                        width, height = image.size
                        size = min(width, height)
                        left = (width - size) // 2
                        top = (height - size) // 2
                        right = left + size
                        bottom = top + size
                        cropped_image = image.crop((left, top, right, bottom))
                        # 压缩分辨率为128x128
                        resized_image = cropped_image.resize((256, 256),
                                                             Image.Resampling.LANCZOS)
                        # 保存裁剪后的图片为JPEG格式
                        resized_image.save(save_path, "JPEG")

                    # 调用函数进行裁剪和压缩
                    crop_and_compress(f_path, './temp/HImage.png')
                    with open('./temp/HImage.png', "rb") as f:
                        while True:
                            chunk = f.read(2048)
                            if not chunk:
                                break
                            skt.sendall(chunk)
                    self.Button.setIcon(QIcon("./temp/HImage.png"))
                    self.Button.setIconSize(QSize(100, 100))
                    resul = windows.show_message_box("提示",
                                                     "头像上传成功!\n需要重启客户端才能完全上传头像\n点击确认按钮或关闭此窗口重启客户端")
                    if resul == 'OK':
                        subprocess.Popen(["Fuchen.exe"])
                        windows.close()
                else:
                    pyautogui.confirm("未选择图片或图片上传失败\n图片只能为jpg, png",
                                      "头像上传失败")

    def paintEvent(self, event):
        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        color = QColor(171, 171, 171, 70)

        for i in range(10):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2,
                         self.height() - (10 - i) * 2)
            # i_path.addRect(ref)
            i_path.addRoundedRect(ref, self.border_width, self.border_width)
            color.setAlpha(int(150 - i ** 0.5 * 50))
            pat.setPen(color)
            pat.drawPath(i_path)

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat2.drawRoundedRect(rect, 4, 4)

    def mousePressEvent(self, e):
        if e.y() <= 25:  # 30像素的标题栏高度
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'start_point'):
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        if hasattr(self, 'start_point'):
            delattr(self, 'start_point')

class PromptWindow(QtWidgets.QDialog):
    def __init__(self, lis):
        super().__init__()
        global windows, texts
        windows = lis[0]
        texts = lis[1]
        self.setWindowTitle("提示")
        x = windows.x() + 500 - 100
        y = windows.y() + 300 - 50
        self.setGeometry(x, y, 200, 100)
        self.setFixedSize(200, 100)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("./image/Component/提示.png"))

        self.label = QtWidgets.QLabel(texts, self)
        self.label.setGeometry(20, 20, 200, 40)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label.setFont(font)

class ExpandingWindow(QWidget):  # 提示窗口
    def __init__(self):
        super().__init__(None)
        desktop = QApplication.desktop()
        rect = desktop.screenGeometry(desktop.primaryScreen())
        taskbar_height = rect.height() - desktop.availableGeometry().height()

        # 设置初始位置
        screen_geometry = QApplication.desktop().screenGeometry()
        initial_geometry = QRect(screen_geometry.width() - 300,
                                 screen_geometry.height() - taskbar_height, 300,
                                 0)  # 初始位置在屏幕底部
        self.setGeometry(initial_geometry)
        # 设置窗口标题
        self.setWindowTitle("Fuchen")
        icon = QIcon("./image/window.ico")
        self.setWindowIcon(icon)

        # 创建动画
        self.animation = QPropertyAnimation(self, b'geometry')

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)  # 置顶/隐藏最大化
        self.animation.setDuration(450)
        self.animation.setStartValue(initial_geometry)
        final_geometry = QRect(screen_geometry.width() - 300,
                               screen_geometry.height() - 150 - taskbar_height, 300,
                               150)  # 最终位置在屏幕顶部
        self.animation.setEndValue(final_geometry)

        self.opacity_animation = QPropertyAnimation(self, b'windowOpacity')
        self.opacity_animation.setDuration(450)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)

        self._5label_2 = QLabel(self)
        self._5label_2.setGeometry(QRect(10, 0, 300, 100))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self._5label_2.setFont(font)
        self._5label_2.setObjectName("_5label_2")
        self._5label_2.setText("Fuchen已执行完毕")

        self._5label_3 = QLabel(self)
        self._5label_3.setGeometry(QRect(30, 0, 100, 26))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self._5label_3.setFont(font)
        self._5label_3.setObjectName("_5label_3")
        self._5label_3.setText("Fuchen")
        color = QtGui.QColor(255, 255, 255)  # 使用RGB值设置颜色为红色
        self._5label_3.setStyleSheet(f"color: {color.name()};")

        # 创建标签来显示剩余秒数
        self.remaining_time_label = QLabel(self)
        self.remaining_time_label.setGeometry(QRect(10, 60, 300, 50))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.remaining_time_label.setFont(font)
        self.remaining_time_label.setObjectName("remaining_time_label")
        self.remaining_time_label.setText("窗口将在 5 秒后自动关闭")

        # 创建计时器 自动关闭窗口
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRemainingTime)
        self.timer.start(1000)  # 1000毫秒 = 1秒

    def showEvent(self, event):
        self.animation.start()
        self.opacity_animation.start()

    def updateRemainingTime(self):
        current_text = self.remaining_time_label.text()
        current_time = int(current_text.split(" ")[-2])
        if current_time == 1:
            self.close()
        else:
            new_time = current_time - 1
            self.remaining_time_label.setText(f"窗口将在 {new_time} 秒后自动关闭")

class ExpandingWindow2(QWidget):  # 提示窗口
    def __init__(self):
        super().__init__(None)
        desktop = QApplication.desktop()
        rect = desktop.screenGeometry(desktop.primaryScreen())
        taskbar_height = rect.height() - desktop.availableGeometry().height()

        # 设置初始位置
        screen_geometry = desktop.screenGeometry()
        initial_geometry = QRect(screen_geometry.width() - 300,
                                 screen_geometry.height() - taskbar_height, 300,
                                 0)  # 初始位置在屏幕底部
        self.setGeometry(initial_geometry)

        # 设置窗口标题和图标
        self.setWindowTitle("Fuchen")
        icon = QIcon("./image/window.ico")
        self.setWindowIcon(icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        try:
            # 调用api
            hWnd = HWND(int(self.winId()))  # 直接HWND(self.winId())会报错
            cdll.LoadLibrary('./mod/dll/aeroDll.dll').setBlur(hWnd)  # dll和脚本放在同一个目录下会报错找不到dll
        except:
            print("导入失败")

        self.animation = QPropertyAnimation(self, b'geometry')  # 创建位置动画
        self.animation.setDuration(450)
        self.animation.setStartValue(initial_geometry)
        final_geometry = QRect(screen_geometry.width() - 300,
                               screen_geometry.height() - 150 - taskbar_height, 300, 150)
        self.animation.setEndValue(final_geometry)

        # 创建透明度动画
        self.opacity_animation = QPropertyAnimation(self, b'windowOpacity')
        self.opacity_animation.setDuration(450)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)

        # 动画组，确保两个动画同时进行
        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.opacity_animation)


        font = QFont("等线", 11)
        self._5label_3 = QLabel(self)
        self._5label_3.setGeometry(10, 0, 100, 26)
        self._5label_3.setFont(font)
        self._5label_3.setText("提示:")

        self.Button_Close = ui.buttons.CloseButton(self)
        self.Button_Close.setGeometry(270, 5, 26, 26)
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QtCore.QSize(24, 24))
        self.Button_Close.setObjectName("Button_Close")

        font = QFont("等线", 24)
        self._5label_2 = QLabel(self)
        self._5label_2.setGeometry(10, 40, 300, 40)

        self._5label_2.setFont(font)
        self._5label_2.setText("Fuchen已执行完毕")

        # 剩余时间标签
        self.remaining_time_label = QLabel(self)
        self.remaining_time_label.setGeometry(10, 80, 300, 50)
        font = QFont("等线", 12)
        self.remaining_time_label.setFont(font)
        self.remaining_time_label.setText("窗口将在 5 秒后自动关闭")

        # 计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRemainingTime)
        self.timer.start(1000)
    def showEvent(self, event):
        # 在窗口显示时启动动画
        self.animation_group.start()
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # 创建从上到下的线性渐变
        gradient = QLinearGradient(0, 0, 0, 30)
        gradient.setColorAt(0, QColor(205, 205, 205, 150))  # 顶部为白色
        gradient.setColorAt(1, QColor(255, 255, 255, 100))  # 底部为灰色

        # 使用渐变作为画刷绘制上部区域
        painter.setBrush(gradient)
        painter.drawRect(0, 0, self.width(), 30)

        pen = QPen(Qt.gray, 2)  # 黑色线条，宽度为2
        painter.setPen(pen)

        # 在y=30绘制水平线，从x=10到x=290
        painter.drawLine(0, 30, 300, 30)

        # 使用白色作为画刷绘制下部区域
        painter.setBrush(QColor(255, 255, 255, 180))
        painter.drawRect(0, 30, self.width(), self.height() - 30)

        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 0, 0)
    '''def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置透明度
        painter.setOpacity(0.5)  # 0.0完全透明，1.0完全不透明

        # 设置颜色
        color = QColor(0, 0, 0)  # 黑色
        painter.fillRect(QRect(0, 0, 300, 30), color)
        # 设置画笔
        pen = QPen(Qt.gray, 1)  # 黑色线条，宽度为2
        painter.setPen(pen)

        # 在y=30绘制水平线，从x=10到x=290
        painter.drawLine(0, 30, 300, 30)

        painter.end()'if self.should_draw == "White":  # 白色主题
            painter = QPainter(self)
            # 左侧灰色矩形
            left_rect = QRect(0, 0, 260, 600)
            left_color = QColor(224, 224, 224)
            painter.fillRect(left_rect, left_color)

            # 右侧渐变矩形（从灰色到白色）
            right_rect = QRect(260, 0, 740, 600)
            gradient = QLinearGradient(right_rect.topLeft(), right_rect.bottomLeft())  # 从上到下的渐变
            gradient.setColorAt(0.0, QColor(230, 230, 230))  # 顶部为灰色
            gradient.setColorAt(1.0, QColor(241, 241, 241))  # 底部为白色
            painter.fillRect(right_rect, gradient)'''


    def updateRemainingTime(self):
        # 更新倒计时
        current_text = self.remaining_time_label.text()
        current_time = int(current_text.split(" ")[-2])
        if current_time == 1:
            self.timer.stop()  # 停止计时器
            self.close()
        else:
            new_time = current_time - 1
            self.remaining_time_label.setText(f"窗口将在 {new_time} 秒后自动关闭")

class View(QWidget):
    def __init__(self, lis):
        super().__init__()
        global windows, s, key, iv
        windows = lis[0]
        s = lis[1]
        key = lis[2]
        iv = lis[3]
        icon = QIcon("./image/Component/提示.png")
        self.setWindowTitle("意见反馈")
        self.setWindowIcon(icon)
        self.setFixedSize(400, 280)
        self.label = QLabel(self)
        self.label.setGeometry(QRect(10, 10, 91, 20))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(10, 40, 211, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(10, 70, 121, 16))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(QRect(10, 90, 380, 180))
        self.textEdit.setObjectName("textEdit")
        self.toolButton = QToolButton(self)
        self.toolButton.setGeometry(QRect(320, 250, 71, 21))
        self.toolButton.setObjectName("toolButton")
        icon = QIcon("./image/Component/完成.png")  # 替换为你的图标路径
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(self.toolButton.size())
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.label.setText("联系方式:")
        self.lineEdit.setPlaceholderText("电话\\QQ\\邮箱\\微信等均可")
        self.label_2.setText("反馈内容:")
        self.toolButton.setText("完成")
        self.toolButton.clicked.connect(self.save)

    def save(self):
        if self.lineEdit.text() == '':
            QMessageBox.question(self, "提示", "联系方式不能为空")
        elif self.textEdit.toPlainText() == '':
            QMessageBox.question(self, "提示", "反馈内容不能为空")
        elif len(self.textEdit.toPlainText()) > 400:
            QMessageBox.question(self, "提示", "反馈内容过多!")
        else:
            view = self.textEdit.toPlainText()
            view = re.sub(' ', '~~space~~', view)
            view = re.sub('\n', '~~next~~', view)
            contents = f'10011 {self.lineEdit.text()} {view}'
            send_encry(contents, s ,key, iv)
            QMessageBox.question(self, "提示", "反馈成功!\n感谢您的建议")
            print("反馈成功")
            self.close()

class Hide():
    def __init__(self, lis):
        global window_icon, windows
        windows = lis[0]
        window_icon = lis[1]
        if not window_icon:
            windows.tray_icon = QSystemTrayIcon(windows)
            windows.tray_icon.setIcon(
                QIcon('./image/Component/favicon.ico'))
            windows.tray_icon.show()

            show_action = QAction('打开主窗口', windows)
            quit_action = QAction('退出', windows)
            show_action.triggered.connect(windows.showNormal)
            quit_action.triggered.connect(windows.close)

            context_menu = QMenu()
            context_menu.addAction(show_action)
            context_menu.addSeparator()
            context_menu.addAction(quit_action)

            windows.tray_icon.setContextMenu(context_menu)
            windows.tray_icon.activated.connect(windows.tray_icon_activated)
            windows.window_icon = True
        windows.hide()


class Quit_Prompt(QtWidgets.QDialog):
    def __init__(self, lis):
        super().__init__()
        global windows, window_icon
        windows = lis[0]
        window_icon = lis[1]
        self.setWindowTitle("关闭提示窗口")
        x = windows.x() + 500 - 150
        y = windows.y() + 300 - 100
        self.setGeometry(x, y, 300, 200)
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("./image/Component/提示.png"))

        self.label = QtWidgets.QLabel("请选择要进行的操作:", self)
        self.label.setGeometry(20, 20, 200, 40)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)
        self.label.setFont(font)

        # 单选按钮组1
        self.group1 = QtWidgets.QButtonGroup(self)

        self.exit_radio = QtWidgets.QRadioButton("退出软件", self)
        self.exit_radio.setGeometry(20, 60, 100, 20)
        self.exit_radio.setChecked(True)
        self.exit_radio.setStyleSheet(style_Radio)
        self.exit_radio.setFont(style_font_10)
        self.group1.addButton(self.exit_radio)

        self.minimize_radio = QtWidgets.QRadioButton("最小化到系统托盘", self)
        self.minimize_radio.setGeometry(20, 90, 150, 20)
        self.minimize_radio.setStyleSheet(style_Radio)
        self.minimize_radio.setFont(style_font_10)
        self.group1.addButton(self.minimize_radio)

        # 单选按钮2
        self.no_prompt_radio = QtWidgets.QRadioButton("下次不再提示(可在设置中再次开启)", self)
        self.no_prompt_radio.setGeometry(20, 130, 230, 20)
        self.no_prompt_radio.setStyleSheet(style_Radio)
        self.no_prompt_radio.setFont(style_font_10)

        # 确认按钮
        self.confirm_button = QtWidgets.QPushButton("确认", self)
        self.confirm_button.setGeometry(20, 160, 120, 28)
        self.confirm_button.clicked.connect(self.on_confirm_button_clicked)
        self.confirm_button.setFont(style_font_11)

    def on_confirm_button_clicked(self):
        #global window_icon, thread_for_exe
        if self.exit_radio.isChecked():
            result = "Quit"
        elif self.minimize_radio.isChecked():
            result = "Hide"
        else:
            result = "未选择"

        no_prompt_checked = self.no_prompt_radio.isChecked()  # 是否下次不再提示

        if (result == "Quit") and (no_prompt_checked == True):  # 下次不再提示  直接关闭
            with open(f"config.json", "r") as file:
                U_data = json.load(file)
            U_data["ClosePrompt"] = False
            U_data["CloseExecute"] = "Close"
            # 写入JSON文件
            with open(f"config.json", "w") as file:
                json.dump(U_data, file, indent=4)
            self.close()
            time.sleep(0.1)
            windows.close()
            os._exit(0)
            #windows.close_MainWindow()
        elif result == 'Quit':  # 下次提示 关闭
            self.close()
            time.sleep(0.1)
            windows.close()
            os._exit(0)
            #windows.close_MainWindow()
        elif (result == "Hide") and (no_prompt_checked == True):  # 下次不再提示
            with open(f"config.json", "r") as file:
                U_data = json.load(file)
            U_data["ClosePrompt"] = False
            U_data["CloseExecute"] = "Hide"
            # 写入JSON文件
            with open(f"config.json", "w") as file:
                json.dump(U_data, file, indent=4)
            self.close()
            Hide([windows, windows.window_icon])
        elif result == "Hide":  # 直接隐藏
            self.close()
            Hide([windows, windows.window_icon])


class Help(QWidget):
    def __init__(self):
        super().__init__()
        icon = QIcon("./image/Component/提示.png")
        self.setWindowIcon(icon)
        self.setFixedSize(450, 400)
        self.setWindowTitle("赞助作者")

        self.label_WEIXIN = QtWidgets.QLabel(self)
        self.label_WEIXIN.setGeometry(QRect(0, 100, 220, 300))
        pixmap_2 = QPixmap('./image/Component/WEIXIN.png')
        self.label_WEIXIN.setPixmap(pixmap_2)
        self.label_WEIXIN.setScaledContents(True)

        self.label_ZHIFU = QtWidgets.QLabel(self)
        self.label_ZHIFU.setGeometry(QRect(220, 100, 230, 300))
        pixmap_2 = QPixmap('./image/Component/ZHIFU.jpg')
        self.label_ZHIFU.setPixmap(pixmap_2)
        self.label_ZHIFU.setScaledContents(True)

        self.label_title = QtWidgets.QLabel(self)
        self.label_title.setGeometry(QRect(10, 10, 450, 21))
        self.label_title.setFont(ui.style.style_font_black_16)
        self.label_title.setObjectName("label_title")
        self.label_title.setText("感谢您的赞助！不论数额大小都对我非常重要")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QRect(10, 40, 431, 45))
        self.label.setObjectName("label")
        self.label.setText("请您在支付时备注好您的名称(网名) 以便于赞助人员名单展示\n"
                           "本软件免费安全无广告 不收费 大家如果觉得用的好的话就自愿进行赞助\n感谢您对开发者的帮助！")
        self.label.setFont(ui.style.style_font_10)


class floating_window(QWidget):  # 悬浮窗
    def __init__(self, main):
        global windows
        windows = main
        super().__init__()
        self.initUI()
        self.draggable = False
        self.offset = None

    def initUI(self):
        self.setWindowTitle('Fuchen悬浮窗')
        self.setGeometry(1700, 100, 130, 35)

        self.button = QtWidgets.QPushButton(self)
        self.button.setStyleSheet("QPushButton#button {"
                                  "border-image: url(./image/float/fc.png);"
                                  "background: transparent;"
                                  "border-radius: 8px;"
                                  "}")
        self.button.setGeometry(QtCore.QRect(0, 0, 35, 35))
        self.button.setObjectName("button")
        self.button.installEventFilter(self)

        self.button_menu = ui.buttons.FloatAnimatedButton("       右键展开菜单", self)
        self.button_menu.setGeometry(QtCore.QRect(0, 0, 130, 35))  # 设置标签位置和大小
        self.button.raise_()
        self.button.setCursor(QCursor(Qt.SizeAllCursor))
        # 创建菜单
        self.menu = QMenu(self)

        # 创建QAction，并为其设置图标
        action1 = QAction(QIcon('./image/float/QQ.png'), "@QQ功能", self)
        action2 = QAction(QIcon('./image/float/复制.png'), "复制消息发送", self)
        action3 = QAction(QIcon('./image/float/句柄.png'), "句柄式消息发送", self)
        action4 = QAction(QIcon('./image/float/记录.png'), "记录脚本", self)
        action5 = QAction(QIcon('./image/float/执行.png'), "执行脚本", self)
        action6 = QAction(QIcon('./image/float/关闭.png'), "关闭程序", self)

        font = QtGui.QFont("等线", 10)  # 使用等线字体，字号为10

        # 设置每个 QAction 的字体
        action1.setFont(font)
        action2.setFont(font)
        action3.setFont(font)
        action4.setFont(font)
        action5.setFont(font)
        action6.setFont(font)
        # 连接每个QAction到相应的槽函数
        action1.triggered.connect(windows.Send_QQ)
        action2.triggered.connect(windows.Send_Copy)
        action3.triggered.connect(windows.Handle_Send)
        action4.triggered.connect(windows.Click_Record)
        action5.triggered.connect(windows.Click_Record_execute)
        action6.triggered.connect(windows.clo)

        # 添加QAction到菜单
        self.menu.addAction(action1)
        self.menu.addAction(action2)
        self.menu.addAction(action3)
        self.menu.addAction(action4)
        self.menu.addAction(action5)
        self.menu.addAction(action6)

        # 连接右键点击事件
        self.button_menu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.button_menu.customContextMenuRequested.connect(self.showMenu)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def showMenu(self, pos):
        global_pos = self.button_menu.mapToGlobal(self.button_menu.rect().bottomLeft())
        self.menu.exec_(global_pos)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            self.draggable = False
            return True
        elif event.type() == QtCore.QEvent.MouseMove and self.draggable:
            # 计算目标位置
            new_pos = self.mapToGlobal(event.pos() - self.offset)

            # 获取屏幕几何信息
            screen = QtWidgets.QApplication.primaryScreen().availableGeometry()

            # 获取窗口尺寸
            window_width = self.frameGeometry().width()
            window_height = self.frameGeometry().height()

            # 限制窗口不会超出屏幕边界
            new_pos.setX(max(screen.left(), min(new_pos.x(), screen.right() - window_width)))
            new_pos.setY(max(screen.top(), min(new_pos.y(), screen.bottom() - window_height)))

            # 移动窗口到限制后的新位置
            self.move(new_pos)
            return True
        return super().eventFilter(obj, event)


class Control(QWidget):
    def __init__(self, lis):
        super().__init__()
        global windows, s, key, iv, sys_list
        windows = lis[0]
        s = lis[1]
        key = lis[2]
        iv = lis[3]
        sys_list = lis[4]
        x = windows.x() + 500 - 185
        y = windows.y() + 300- 135
        self.setGeometry(x, y, 370, 270)
        self.setFixedSize(370, 270)
        self.setWindowTitle("控制台Control")
        self.setWindowIcon(QIcon('./image/window.ico'))

        # TextBrowser
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 370, 250))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFont(style_font_9)

        # Input Field
        self.inputField = QtWidgets.QLineEdit(self)
        self.inputField.setGeometry(QtCore.QRect(0, 250, 280, 20))
        self.inputField.setObjectName("inputField")
        self.inputField.returnPressed.connect(self.send)

        # Confirm Button
        #self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton = ui.buttons.CustomButton(self, radius=0, start_color=QColor(207, 207, 207, 0),
                                                       hover_color=QColor(33, 150, 243, 255),
                                                       border_color=QColor(33, 120, 255), border_width=1,
                                                       font_color=QColor(0, 0, 0))
        self.confirmButton.setGeometry(QtCore.QRect(280, 250, 90, 20))
        self.confirmButton.setObjectName("confirmButton")
        self.confirmButton.setText("确认")
        self.confirmButton.setFont(style_font_10)
        self.confirmButton.clicked.connect(self.send)

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateConsole)
        self.timer.start(500)  # 每秒检查一次 sys_list

        # 已显示的 sys_list 元素数量
        self.displayed_count = 0

        # 初次显示 sys_list 内容，避免延迟
        self.updateConsole()

    def updateConsole(self):
        global sys_list
        # 只添加新的元素
        while self.displayed_count < len(sys_list):
            item = sys_list[self.displayed_count]
            if item[0] == 'b':
                self.textBrowser.append("<font color='blue'>" + str(item)[1:] + "</font>")
            elif item[0] == 'g':
                self.textBrowser.append("<font color='green'>" + str(item)[1:] + "</font>")
            elif item[0] == 'r':
                self.textBrowser.append("<font color='red'>" + str(item)[1:] + "</font>")
            self.displayed_count += 1

    def send(self):
        global sys_list, current_time_string, exp_status, temp_content, COLOR
        content = self.inputField.text()
        current_time_string = '[' + time.strftime("%H:%M:%S") + ']'
        custom_command = self.inputField.text()
        sys_list.append('b' + current_time_string + self.inputField.text())
        #self.textBrowser.append("<font color='blue'>" + current_time_string + content + "<font>")
        self.inputField.setText("")
        if content == '签到':
            send_encry('30001', s, key, iv)
            try:
                exp = socket_information.get(timeout=3)
                sys_list.append("g" + current_time_string + exp[1] + ' 客户端经验值可能未更新 请重启客户端后重试')
                windows.update_exp(int(exp[2]))
            except:
                sys_list.append("r" + current_time_string + "签到失败:信息获取超时")
        elif content == 'XFBSOMDFLS114514':
            send_encry("30002 xfbsomdfls", s, key, iv)
            try:
                exp = socket_information.get(timeout=3)
                sys_list.append("r" + current_time_string + exp)
            except:
                sys_list.append("r" + current_time_string + "经验值添加失败")
        elif content == '帮助' or content == 'help':
            sys_list.append("g" + current_time_string + '1.handle x y 手动设置句柄发送输入栏位置')
            sys_list.append("g" + current_time_string + '2.签到 每日可签到一次')
            sys_list.append("g" + current_time_string + '3.random 选项1 选项2.... 可以随机做出一个选择')
        elif 'handle' in content.lower():
            x = int(content.split(' ')[1])
            y = int(content.split(' ')[2])
            windows.update_handle_value(x, y)
            sys_list.append("g" + current_time_string + f"发送位置修改成功{x} {y}")

        elif 'i love you' in content.lower():
            turtle.screensize(300, 300)
            turtle.title("I Love You")
            turtle.pensize(4)  # 设置画笔像素为4像素
            turtle.pencolor("red")  # 设置画笔颜色为红色
            turtle.fillcolor("pink")  # 设置填充颜色为粉红色
            turtle.begin_fill()  # 开始填充
            # 开始绘制爱心
            turtle.left(135)
            turtle.forward(100)
            turtle.circle(-50, 180)  # 第一个半圆
            turtle.left(90)
            turtle.circle(-50, 180)  # 第二个半圆
            turtle.forward(100)
            turtle.end_fill()  # 结束填充
            turtle.done()

        elif 'myself' in content.lower():
            # 创建一个Tkinter窗口
            root = tk.Tk()
            root.title("做自己")

            # 设置窗口为全屏
            root.attributes('-fullscreen', True)

            # 设置窗口背景颜色为白色
            root.configure(background='white')

            # 创建一个Label用于显示文本
            label = tk.Label(root, text="须知少年凌云志\n曾许人间第一流",
                             font=("SansSerif", 40), bg="white", fg="black")
            label.pack(expand=True)  # 将标签居中

            # 运行主循环
            root.mainloop()

        elif content == "管理员权限":
            send_encry("90000", s, key, iv)
            try:
                result = socket_information.get(timeout=3)
                sys_list.append("r" + current_time_string + result)
                print(result, type(result))
                if result == '管理员权限存在':
                    sys_list.append("r" + current_time_string + '请输入 查询 ID')

            except:
                sys_list.append("r" + current_time_string + "管理员权限获取失败")

        elif content[0:2] == '查询':
            send_encry(f"90001 查询 {content[3:]}", s, key, iv)
            try:
                result = socket_information.get(timeout=3)
                sys_list.append("r" + current_time_string + result)
            except:
                sys_list.append("r" + current_time_string + "管查询失败")
        elif content[0:6] == 'random':
            contents = content.split()
            result = random.choice(contents[1:])
            sys_list.append("g" + current_time_string + result)
        '''else:
            sys_list.append('b' + current_time_string + custom_command)'''

    def showEvent(self, event):
        """窗口显示时触发的事件"""
        super().showEvent(event)  # 调用父类处理
        self.inputField.setFocus()  # 设置焦点到lineEdit