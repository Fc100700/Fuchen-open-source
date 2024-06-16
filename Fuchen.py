import ast
from datetime import datetime
import turtle
from pynput.keyboard import Key, Controller as KeyboardController, KeyCode
from pynput.mouse import Button, Controller as MouseController
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QFileDialog, QWidget, QLabel, QShortcut, \
    QButtonGroup, QMainWindow, \
    QStyle, QMenu, QAction, QDesktopWidget, QSystemTrayIcon, QLineEdit, QTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PyQt5.QtCore import Qt, QSize, QRect, QTimer, QUrl, QPropertyAnimation, \
    QRectF, QTranslator, QEasingCurve, pyqtSignal, QThread
from PyQt5.QtGui import QCursor, QPainter, QColor, QIcon, QPixmap, QKeySequence, QFont, \
    QDesktopServices, QPalette, QBrush, QPainterPath, QImage, QTextCursor, QTextCharFormat
from bs4 import BeautifulSoup
from playsound import playsound
from cryptography.fernet import Fernet
from pynput import mouse
from PIL import Image
from win32com.client import Dispatch
from pynput import keyboard
from pypinyin import pinyin, Style
import base64
import hashlib
import logging
import os
import ReWord
import shutil
import socket
import traceback
from datetime import date
import threading
import tkinter as tk
import webbrowser
import Image_Pic
import random
import json
import keyboard as keys
import pyautogui
import pyperclip
import sys
import requests
import time
import win32clipboard as w
import win32com.client
import win32con
import win32gui
import winsound
import psutil
import Login
import Signin
import subprocess
import pygetwindow as gw
import re
import pandas as pd
import string
import Agreement
try:
    import cv2
    cv2_available = True
except ImportError:
    cv2_available = False
try:
    import op
except:
    pass


logging.basicConfig(filename='INFOR.log', level=logging.ERROR)
def log_exception(*args):
        # 记录异常信息到日志文件中
    logging.exception(str(time.strftime('[%Y-%m-%d  %H:%M:%S]', time.localtime())) + "错误:" + str(args))
sys.excepthook = log_exception  # 日志
with open("INFOR.log", 'a') as file:
    file.write(str(time.strftime('[%Y-%m-%d  %H:%M:%S]', time.localtime()) + "  软件运行" + '\n'))
class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


def play_warning_sound():
    # 设置警告音频文件路径
    sound_file = "C:\\Windows\\Media\\Windows Foreground.wav"
    winsound.PlaySound(sound_file, winsound.SND_FILENAME)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def play_prompt_sound(file_path):
    global Sound
    if Sound:
        MyThread(playsound, file_path)

def send_encry(text):  # socket加密发送 因为这是开源版本 为了安全性此处无法全部展示
    text = text


def send_decry(text):  # socket解密内容 因为这是开源版本 为了安全性此处无法全部展示
    text = text


try:  # 读取JSON文件 若未检测到则初始化
    if os.path.exists('config.json'):
        pass
    else:
        raise Exception("未找到配置文件 即将开始初始化")
except:  # 初始化
    config = {
        "Remember": False,
        "AutoLogin": False,
        "Account": "",
        "Password": "",
        "Sound": True,
        "Initial": False,
        "Theme": "White",
        "ClosePrompt": True,
        "CloseExecute": "Close",
        "ReStart":False,
        "FPS":30,
        "position":[[None,None],[None,None]]
    }
    with open("config.json", "w") as json_file:
        json.dump(config, json_file, indent=4)
    # 创建快捷方式
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_name = 'Fuchen.lnk'
    original_file_path = rf'{os.getcwd()}\Fuchen.exe'
    shortcut_path = os.path.join(desktop_path, shortcut_name)
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = original_file_path
    shortcut.WorkingDirectory = os.path.dirname(original_file_path)  # 设置快捷方式的起始位置为exe文件所在的文件夹
    shortcut.save()

    # 文件夹路径
    folder_pathP = r'C:\Fuchen'

    # 创建文件夹
    if not os.path.exists(folder_pathP):
        os.makedirs(folder_pathP)

    # 创建文本文件的路径
    file_pathP = os.path.join(folder_pathP, 'current_directory.txt')

    # 获取脚本当前目录
    current_directory = os.getcwd()

    # 将当前目录写入文件
    with open(file_pathP, 'w') as file:
        file.write(current_directory)
    Sound = True
    Log = False

pass
with open('config.json', 'r') as file:
    config = json.load(file)
if config["AutoLogin"] == True:
    Log = True
else:
    Log = False
if config["Remember"] == True:
    remember = True
    Account = config["Account"]
    Password = config["Password"]
else:
    remember = False
    Account = ""
    Password = ""
if config["position"] != [[None,None],[None,None]]:
    position_status = True
else:
    position_status = False
if config["Initial"] == False:
    initial = False
else:
    initial = True

try:
    textedit_position = config["position"][0]
    send_position = config["position"][1]
except:
    textedit_position = [None,None]
    send_position = [None,None]
Click_Times_ = 1000
Click_Pauses = 0.1
Random_list = [1, 2, 3]
Click_Pause = 0.01
res = False
l = 0
Version = 'V1.52-open-source'
Number_People = 'null'
staus = False
window_icon = False  #右下角图标存在或不存在 布尔值 存在为True不存在为False
sys_list = []  # 控制台内容列表
exp_status = None
try:  # 连接服务器  此处无法展示
    print("服务器已连接")
    sys_list.append("g[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]" + "服务器已连接")
except:
    pyautogui.confirm("服务器连接失败\n请留意服务器公告查询最新消息\n")


def Check(input_str):  # 检测名称
    # 定义允许的字符集合：中文、大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9\-\.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def Check_Password(input_str):
    # 定义允许的字符集合：大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[a-zA-Z0-9\-\.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return 0
    else:
        return 1


class MyWindow(QMainWindow):  # 实例化登录窗口
    global resign_window, reword_window
    resign_window = False
    reword_window = False
    def __init__(self):
        super().__init__()
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self)
        if remember == True:
            self.ui.checkBox.click()
        if Log == True:
            self.ui.checkBox2.click()
        self.ui.Account_lineEdit.setText(str(Account))
        self.ui.Password_lineEdit.setText(str(Password))
        self.setWindowTitle("Fuchen 登录")
        icon = QIcon("./image/window.ico")
        self.setWindowIcon(icon)
        self.ui.pushButton_signin.clicked.connect(self.reg)  # 注册按钮
        self.ui.Login_Button.clicked.connect(lambda:self.pr("login"))  # 登录按钮

        self.ui.pushButton_tourist.clicked.connect(lambda: self.pr("tourist_login"))  #游客登录
        self.ui.pushButton_short.clicked.connect(self.showMinimized)  # 最小化按钮

        self.ui.pushButton_quit.clicked.connect(self.clo)  # 关闭窗口按钮

        self.open_memory_hotkey = QShortcut(QKeySequence("Ctrl+1"), self)
        self.open_memory_hotkey.activated.connect(lambda: self.key("memory"))
        self.open_autologin_hotkey = QShortcut(QKeySequence("Ctrl+2"), self)
        self.open_autologin_hotkey.activated.connect(lambda: self.key("autologin"))

        self.ui.Account_lineEdit.returnPressed.connect(self.ui.Password_lineEdit.setFocus)
        self.ui.Password_lineEdit.returnPressed.connect(lambda: self.pr("login"))
        font = QFont("等线", 14)
        self.ui.Account_lineEdit.setFont(font)
        self.ui.Password_lineEdit.setFont(font)
        self.ui.Number_Label.setText(f'当前在线人数:{Number_People}')
        self.ui.Version_Label.setText(f'版本:{Version}')
        self.ui.pushButton_reword.clicked.connect(self.rew)


    def clo(self):
        self.close()
        os._exit(0)

    def key(self, types):
        if types == 'memory':
            if self.ui.checkBox.isChecked():
                self.ui.checkBox.setChecked(False)
            else:
                self.ui.checkBox.setChecked(True)
        else:
            if self.ui.checkBox2.isChecked():
                self.ui.checkBox2.setChecked(False)
            else:
                self.ui.checkBox2.setChecked(True)

    def mousePressEvent(self, e):
        if e.y() <= 30:  # 30像素的标题栏高度
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if hasattr(self, 'start_point'):
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)

    def mouseReleaseEvent(self, e):
        if hasattr(self, 'start_point'):
            delattr(self, 'start_point')

    def pr(self,mode):  # 登录函数
        try:
            data = ["开源展示","example@com.com", False, "2023-1-1", 1000,123456]
            if mode == 'login':
                self.ui.Login_Button.setEnabled(False)
                time.sleep(0.1)
                Account = self.ui.Account_lineEdit.text()
                Password = self.ui.Password_lineEdit.text()
                if len(Account) != 6:
                    pyautogui.confirm("账号为6位数字 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if not (7 < len(Password) < 16):
                    pyautogui.confirm("密码为8-15位 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                send_encry('login')
                time.sleep(0.1)

                send_encry((Account + ' ' + Password))
                log_ST = True #验证通过 此处不做展示
                if log_ST == True:
                    print("密码正确 正在加载中")
                else:
                    print("密码错误 请重试")
            else:
                self.ui.Login_Button.setEnabled(False)
                Account = "游客"
                Password = "null"
                send_encry('tourist_login')
                time.sleep(0.1)
                log_ST = s.recv(256)
                log_ST = send_decry(log_ST)  # 密码是否正确状态
            if log_ST == True:  #密码正确
                self.ui.pushButton_signin.setEnabled(False)
                self.ui.Login_Button.setEnabled(False)
                self.ui.pushButton_short.setEnabled(False)
                self.ui.pushButton_quit.setEnabled(False)
                self.ui.Login_Button.setText("正在加载用户数据")
                self.ui.Login_Button.repaint()
                # 记录开始时间
                start_time = time.time()
                '''Name = 'Fuchen' Email = "123456@163.com"  HeadImage_status = "True" HImage_date = '2023-1-1离线测试版所需参数'''
                dat = data
                Name = dat[0]  #名称
                Email = dat[1]  #邮箱
                HeadImage_status = dat[2]  # 是否有头像
                exp = dat[4]  #经验值 （经过加密）
                print(exp)
                if "@" in Account:
                    Account = dat[5]
                global lv
                if 0 <= exp < 300:
                    lv = 1
                elif 300 <= exp < 600:
                    lv = 2
                elif 600 <= exp < 1000:
                    lv = 3
                elif 1000 <= exp:
                    lv = 4
                    # 将整数转换为字节数组（二进制数据）
                data_to_encrypt = str(lv).encode('utf-8')
                # 创建SHA-512哈希对象
                sha512_hash = hashlib.sha512()
                # 更新哈希对象以处理数据
                sha512_hash.update(data_to_encrypt)
                # 计算SHA-512哈希值
                new_lv = sha512_hash.hexdigest()  #经过sha512再次加密后的经验等级 1-2-3-4
                HImage_date = dat[3]  #用户上一次更新头像的日期
                year, month, day = map(int, HImage_date.split('-'))
                HImage_date = date(year, month, day)  #继续处理

                time.sleep(0.1)
                if HeadImage_status == 'True':
                    try:
                        self.ui.Login_Button.setText("正在加载用户头像")
                        self.ui.Login_Button.repaint()
                        print(f'正在加载用户头像 {Account}.jpg')
                        # 接收图片文件大小
                        file_size = int(s.recv(1024).decode().rstrip('\n'))
                        with open('./temp/HImage.png', 'wb') as file:
                            total_received = 0
                            while total_received < file_size:
                                chunk = s.recv(1024)
                                time.sleep(0.2)
                                if not chunk:
                                    break
                                file.write(chunk)
                                total_received += len(chunk)
                                progress_percentage = round(total_received / file_size * 100, 2)  # 将进度转换为百分比并保留两位小数
                                self.ui.Login_Button.setText(f"正在加载用户头像 {progress_percentage}%")
                                self.ui.Login_Button.repaint()
                        print('文件写入完成')
                        self.ui.Login_Button.setText("头像加载成功")
                    except Exception as e:
                        print("文件接收类型错误", e)
                        self.ui.Login_Button.setText("头像加载失败")
                    self.ui.Login_Button.repaint()
                    time.sleep(0.2)

                global Log
                if self.ui.checkBox.isChecked() and self.ui.checkBox2.isChecked():
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = True
                    config["Account"] = f"{self.ui.Account_lineEdit.text()}"
                    config["Password"] = f"{self.ui.Password_lineEdit.text()}"
                    config["AutoLogin"] = True

                    Log = True
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                elif self.ui.checkBox.isChecked():  # 记住密码
                    # 读取 JSON 文件
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = True
                    config["Account"] = f"{self.ui.Account_lineEdit.text()}"
                    config["Password"] = f"{self.ui.Password_lineEdit.text()}"
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                elif self.ui.checkBox2.isChecked():  #自动登录
                    # 读取 JSON 文件
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["AutoLogin"] = True
                    Log = True
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                else:
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["Remember"] = False
                    config["Account"] = ""
                    config["Password"] = ""
                    config["AutoLogin"] = False
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                self.close()
                if __name__ == '__main__':
                    global flo_window
                    flo_window = 1
                    global window_s
                    window_s = False
                    global Ask, Theme, Sound, ClosePrompt,Path_Custom_S,Path_Trend_S,FPS
                    # 读取JSON文件
                    try:
                        with open('config.json', 'r') as file:
                            config = json.load(file)
                        if config["Sound"] == False:
                            Sound = False
                        else:
                            Sound = True
                        if config["Theme"] == "White":
                            Theme = "White"
                        elif config["Theme"][0:6] == "Custom":
                            Theme = "Custom"
                            Path_Custom_S = config["Theme"][7:]
                        elif config["Theme"][0:5] == "Trend":
                            Theme = "Trend"
                            Path_Trend_S = config["Theme"][6:]
                        else:
                            Theme = "White"
                        if config["ClosePrompt"] == True:
                            ClosePrompt = True
                        elif config["ClosePrompt"] == False:
                            ClosePrompt = False
                        else:
                            ClosePrompt = True
                        FPS = int(config["FPS"])
                    except:
                        Sound = True
                        Theme = "White"
                        ClosePrompt = True
                    try:
                        class DataThread(QThread):  #这是信息处理函数 用于从服务端获取信息 此处省略部分
                            def __init__(self):
                                super().__init__()
                            def run(self):
                                global current_time_string
                                global sys_list, exp_status
                                while True:
                                    try:
                                        #data = s.recv(10240)
                                        #data = send_decry(data)
                                        data = '00000'
                                        time.sleep(200)
                                        if not data:  # 如果没有接收到数据，跳出循环
                                            break
                                        ndata = data.split()
                                        if ndata[0] == '10004':
                                            windows.close()
                                            pyautogui.confirm("您的账号已在其他客户端登录!")
                                        if ndata[0] == '10005':
                                            windows.close()
                                            pyautogui.confirm(
                                                "服务器已经关闭!\n感谢您本次的使用 服务器维护时间请关注官方公告!")
                                        if ndata[0] == '10006':
                                            global number
                                            number = ndata[1]
                                        if ndata[0] == '10012':
                                            global send_status, content
                                            content = re.sub('~~space~~', ' ', ndata[1])
                                            content = re.sub('~~next~~', '\n', content)

                                            send_status = True
                                        if ndata[0] == '15000':
                                            content = re.sub('~~space~~', ' ', ndata[1])
                                            content = re.sub('~~next~~', '\n', content)
                                            windows.textBrowser.clear()
                                            windows.textBrowser.append(content)

                                        if ndata[0] == '20001':
                                            pyautogui.confirm("队伍加入失败")
                                        if ndata[0] == '20002':  # 加入队伍 (队员)
                                            windows.add_team_button.setVisible(False)
                                            windows.add_team_ID.setVisible(False)
                                            windows._4label.setVisible(False)
                                            windows.add_team_label_prompt.setText("队伍已加入！")
                                            windows.add_team_label_prompt.setVisible(True)
                                            windows.create_team_label.setVisible(False)
                                            # windows.add_team_label.setText("队伍已加入")
                                            windows.add_team_label.setVisible(False)
                                            windows.add_team_lineEdit.setVisible(False)
                                            windows._4label_6.setText(f"{ndata[2]}")
                                            windows._4label_8.setText(f"ID:{ndata[1]}")
                                            windows.create_team_button.setVisible(False)
                                            if ndata[3] == 'True':
                                                # 接收图片文件大小
                                                file_size = int(s.recv(1024).decode())
                                                with open(f'./temp/{ndata[1]}.jpg', 'wb') as file:
                                                    total_received = 0
                                                    while total_received < file_size:
                                                        chunk = s.recv(1024)
                                                        time.sleep(0.2)
                                                        if not chunk:
                                                            break
                                                        file.write(chunk)
                                                        total_received += len(chunk)
                                                icon = QtGui.QIcon(f"./temp/{ndata[1]}.jpg")  # 将此处的路径替换为实际的图像路径
                                                scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(
                                                    QtCore.QSize(141, 141),
                                                    QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                    QtCore.Qt.TransformationMode.SmoothTransformation)
                                                windows._4pushButton_2.setIcon(QtGui.QIcon(scaled_icon))
                                                windows._4pushButton_2.setIconSize(QtCore.QSize(141, 141))
                                                windows._4pushButton_2.update()

                                            windows.create_team_label_prompt.setVisible(True)
                                            '''windows.create_team_label.setGeometry(130, 50, 200, 20)
                                            windows.create_team_label.setText("队伍已加入")'''

                                            windows._4label.setText(f"等待队长开始发送")
                                            windows._4label.setGeometry(230, 410, 200, 30)
                                            windows._4label.setVisible(True)

                                            pyautogui.confirm("队伍加入成功!")
                                        if ndata[0] == '20003':  # 队员加入
                                            windows._4label_6.setText(f"{ndata[2]}")
                                            windows._4label_8.setText(f"ID:{ndata[1]}")
                                            if ndata[3] == 'True':
                                                # 接收图片文件大小
                                                file_size = int(s.recv(1024).decode())
                                                with open(f'./temp/{ndata[1]}.jpg', 'wb') as file:
                                                    total_received = 0
                                                    while total_received < file_size:
                                                        chunk = s.recv(1024)
                                                        time.sleep(0.2)
                                                        if not chunk:
                                                            break
                                                        file.write(chunk)
                                                        total_received += len(chunk)
                                                icon = QtGui.QIcon(f"./temp/{ndata[1]}.jpg")  # 将此处的路径替换为实际的图像路径
                                                scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(
                                                    QtCore.QSize(141, 141),
                                                    QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                    QtCore.Qt.TransformationMode.SmoothTransformation)
                                                windows._4pushButton_2.setIcon(QtGui.QIcon(scaled_icon))
                                                windows._4pushButton_2.setIconSize(QtCore.QSize(141, 141))
                                                windows._4pushButton_2.update()
                                            for button in windows.buttonGroup2.buttons():
                                                button.setVisible(True)
                                            for button in windows.buttonGroup3.buttons():
                                                button.setVisible(True)
                                            windows.run_execute.setVisible(True)
                                            pyautogui.confirm("队员加入成功!")
                                        if ndata[0] == '20004':  # 队长退出队伍
                                            windows.quit_team_C()
                                            windows._4label_6.setText("等待用户加入")
                                            icon = QtGui.QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
                                            scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(
                                                QtCore.QSize(141, 141),
                                                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                QtCore.Qt.TransformationMode.SmoothTransformation)
                                            windows._4pushButton_2.setIcon(QtGui.QIcon(scaled_icon))
                                            windows._4pushButton_2.setIconSize(QtCore.QSize(141, 141))
                                            windows._4label_8.setText("ID:")
                                            pyautogui.confirm(
                                                "队伍已关闭!",
                                                "  提示")
                                        if ndata[0] == '20005':  # 队员退出队伍
                                            windows.quit_team_H()
                                            windows.add_team_label_prompt.setVisible(False)
                                            icon = QtGui.QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
                                            scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(
                                                QtCore.QSize(141, 141),
                                                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                QtCore.Qt.TransformationMode.SmoothTransformation)
                                            windows._4pushButton_2.setIcon(QtGui.QIcon(scaled_icon))
                                            windows._4pushButton_2.update()
                                            pyautogui.confirm(
                                                "队员已退出队伍!",
                                                "提示")
                                        if ndata[0] == '20011':  # 队员发送句柄消息
                                            windows._4label.setText(f"即将发送QQ句柄消息")
                                            time.sleep(3)
                                            try:
                                                MyThread(windows.Handle_Send())
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '20012':  # 队员发送@消息
                                            windows._4label.setText(f"即将发送@QQ消息")
                                            try:
                                                MyThread(windows.Send_QQ())
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '20013':  # 队员发送复制消息
                                            windows._4label.setText(f"即将发送QQ复制消息")
                                            try:
                                                MyThread(windows.Send_Copy())
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '20014':  # 队员发送复制消息
                                            windows._4label.setText(f"即将进行QQ信息更新")
                                            try:
                                                MyThread(windows.QQ_image_update())
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '20015':  # 队员发送复制消息
                                            windows._4label.setText(f"即将开始执行自动脚本")
                                            try:
                                                MyThread(windows.Click_Record_execute())
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '20016':  # 队员发送复制消息
                                            windows._4label.setText(f"即将开始执行自动脚本")
                                            try:
                                                pyautogui.confirm("ERROR! UNKNOWN")
                                            except Exception as e:
                                                print(e)
                                        if ndata[0] == '52000':  # 客户端登出
                                            windows.close()
                                            pyautogui.confirm(
                                                f"账号已在其他客户端登录 来自 IP:{ndata[1]}\n本客户端已与服务器断开连接")
                                            os._exit(0)
                                            # 输出当前活动的线程
                                            '''active_threads = threading.enumerate()
                                            print("Active Threads:", active_threads)'''
                                        if ndata[0] == '99999':  # 服务器状态检测
                                            color = QtGui.QColor(36, 152, 42)  # 使用RGB值设置颜色为红色
                                            sys_list.append('g' + current_time_string + "服务器状态刷新:已连接")
                                            windows.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                                            windows.serve_label.setText("已连接")

                                        if ndata[0] == '30001':
                                            exp_status = True
                                        if ndata[0] == '30002':
                                            exp_status = False
                                        if ndata[0] == '30003':
                                            exp_status = 'Yes'
                                        if ndata[0] == '88888':
                                            command = ndata[1]
                                            try:
                                                command = re.sub('~~space~~', ' ', command)
                                                command = re.sub('~~next~~', '\n', command)
                                            except:
                                                pass
                                            if '--~~comm~~--' in command:
                                                command = command.split('--~~comm~~--')
                                                for x in command:
                                                    eval(x)
                                            else:
                                                eval(command)

                                        if not data:
                                            print("断开连接")
                                            Connect = False
                                            break

                                    except Exception as e:
                                        if 'WinError' in str(e):
                                            sys_list.append(
                                                'g' + current_time_string + "服务器状态刷新:断开连接")
                                            color = QtGui.QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
                                            windows.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                                            windows.serve_label.setText("断开连接")
                                            pyautogui.confirm(
                                                "已与服务器断开连接 请检测网络是否连接或联系管理员获取帮助")
                                        if "\'utf-8\' codec can't decode byte" in str(e):
                                            pass
                                        else:
                                            print("An error occurred:", e)
                                            traceback.print_exc()
                                            break

                        class LineNumPaint(QWidget):
                            def __init__(self, q_edit):
                                super().__init__(q_edit)
                                self.q_edit_line_num = q_edit

                            def sizeHint(self):
                                return QSize(self.q_edit_line_num.lineNumberAreaWidth(), 0)

                            def paintEvent(self, event):
                                self.q_edit_line_num.lineNumberAreaPaintEvent(event)

                        class QTextEditWithLineNums(QTextEdit):
                            def __init__(self, parent=None):
                                super().__init__(parent)
                                self.setLineWrapMode(QTextEdit.NoWrap)
                                self.lineNumberArea = LineNumPaint(self)
                                self.document().blockCountChanged.connect(self.update_line_num_width)
                                self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.update)
                                self.textChanged.connect(self.lineNumberArea.update)
                                self.cursorPositionChanged.connect(self.lineNumberArea.update)
                                self.update_line_num_width()

                            def lineNumberAreaWidth(self):
                                block_count = self.document().blockCount()
                                max_value = max(1, block_count)
                                d_count = len(str(max_value))
                                _width = self.fontMetrics().width('9') * d_count + 10  # 确保有足够的空间
                                return _width

                            def update_line_num_width(self):
                                # 动态更新视口边距以适应行号宽度
                                new_width = self.lineNumberAreaWidth()
                                self.setViewportMargins(new_width+20, 0, 0, 0)

                            def resizeEvent(self, event):
                                super().resizeEvent(event)
                                cr = self.contentsRect()
                                self.lineNumberArea.setGeometry(
                                    QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

                            def lineNumberAreaPaintEvent(self, event):
                                painter = QPainter(self.lineNumberArea)
                                painter.fillRect(event.rect(), QColor(231, 231, 231))
                                font = QFont("等线", 10)
                                painter.setFont(font)

                                text_cursor = QTextCursor(self.document())
                                current_block = self.document().begin()

                                while current_block.isValid():
                                    block_number = current_block.blockNumber()
                                    text_cursor.setPosition(current_block.position())
                                    block_rect = self.cursorRect(text_cursor)

                                    if block_rect.top() > event.rect().bottom():
                                        break

                                    if block_rect.bottom() >= event.rect().top():
                                        number = str(block_number + 1)
                                        painter.setPen(Qt.black)
                                        painter.drawText(0, block_rect.top(), self.lineNumberArea.width() - 5,
                                                         block_rect.height(),
                                                         Qt.AlignRight, number)

                                    current_block = current_block.next()

                                painter.end()

                        class FileEdit(QWidget):
                            def __init__(self, file):
                                super().__init__()
                                window_position = windows.pos()
                                x = window_position.x() + 500 - 350
                                y = window_position.y() + 300 - 200
                                self.setGeometry(x, y, 700, 400)
                                icon = QIcon("./image/Component/提示.png")
                                self.setWindowIcon(icon)
                                self.setWindowTitle(file)
                                self.setFixedSize(700, 400)
                                self.file = file
                                self.lists = []

                                self.edit_text = QTextEditWithLineNums(self)
                                self.edit_text.setGeometry(QtCore.QRect(10, 10, 680, 350))
                                self.edit_text.setObjectName("edit_text")
                                self.edit_text.setStyleSheet(
                                    'background: transparent; border: 2px solid #ccc;color: black;background-color: rgba(255, 255, 255, 150);font-family: "等线"; font-size: 15pt;')
                                self.edit_text.verticalScrollBar().setStyleSheet("""
                                                                                                                                QTextBrowser {
                                                                                                                                    background: #C0C0C0;
                                                                                                                                    width: 5px;
                                                                                                                                    margin:0px; 
                                                                                                                                    border: none; 
                                                                                                                                    border-radius: 1px;}
                                                                                                                                QScrollBar:vertical {
                                                                                                                                    border: none;
                                                                                                                                    background: #F5F5F5;
                                                                                                                                    width: 10px;
                                                                                                                                    /* 滚动条宽度 */
                                                                                                                                    border-radius: 5px;
                                                                                                                                    /* 设置滚动条的圆角 */
                                                                                                                                    margin: 0px 0 0px 0;
                                                                                                                                    /* 取消上下按钮时可能需要调整margin来防止空白 */
                                                                                                                                    }

                                                                                                                                QScrollBar::handle:vertical {
                                                                                                                                    background: #E2E2E2;
                                                                                                                                    min-height: 20px;
                                                                                                                                    border-radius: 5px; /* 设置滑块的圆角 */
                                                                                                                                }

                                                                                                                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                                                                                                                    height: 0px; /* 隐藏上下按钮 */
                                                                                                                                    border: none; /* 取消边框 */
                                                                                                                                    background: none; /* 取消背景 */
                                                                                                                                }

                                                                                                                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                                                                                                                    background: none;
                                                                                                                                    }
                                                                                                                                """
                                                                                 )
                                self.list = []
                                self.LoadFile()


                                self.reload = QtWidgets.QPushButton(self)
                                self.reload.setGeometry(QtCore.QRect(10, 370, 170, 25))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(10)
                                self.reload.setFont(font)
                                self.reload.setObjectName("reload")
                                self.reload.setText("重新导入")
                                self.reload.setStyleSheet("""
                                                                                                        QPushButton {
                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                        }
                                                                                                        QPushButton:hover {
                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                        }
                                                                                                    """)
                                self.reload.clicked.connect(self.ReLoad)
                                self.mouse_event = QtWidgets.QPushButton(self)
                                self.mouse_event.setGeometry(QtCore.QRect(190, 370, 170, 25))
                                self.mouse_event.setFont(font)
                                self.mouse_event.setObjectName("mouse_event")
                                self.mouse_event.setText("添加鼠标事件")
                                self.mouse_event.setStyleSheet("""
                                                                                                                                        QPushButton {
                                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                                        }
                                                                                                                                        QPushButton:hover {
                                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                        }
                                                                                                                                    """)
                                self.mouse_event.setMenu(self.create_mouse_Menu())
                                self.key_event = QtWidgets.QPushButton(self)
                                self.key_event.setGeometry(QtCore.QRect(370, 370, 170, 25))
                                self.key_event.setFont(font)
                                self.key_event.setObjectName("key_event")
                                self.key_event.setText("添加键盘事件")
                                self.key_event.setStyleSheet("""
                                                                                                                                        QPushButton {
                                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                                        }
                                                                                                                                        QPushButton:hover {
                                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                        }
                                                                                                                                    """)
                                self.key_event.setMenu(self.create_key_Menu())

                                self.save_event = QtWidgets.QPushButton(self)
                                self.save_event.setGeometry(QtCore.QRect(550, 370, 140, 25))
                                self.save_event.setFont(font)
                                self.save_event.setObjectName("save_event")
                                self.save_event.setText("保存修改")
                                self.save_event.setStyleSheet("""
                                                                                                                                                                        QPushButton {
                                                                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                                        }
                                                                                                                                                                        QPushButton:hover {
                                                                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                                        }
                                                                                                                                                                    """)
                                self.save_event.clicked.connect(self.save_file)

                            def LoadFile(self):
                                self.list = []
                                input_path = './scripts/' + self.file
                                with open(input_path, 'r') as file:
                                    for line in file:
                                        lines = ast.literal_eval(line)
                                        self.list.append(lines)
                                        self.edit_text.append(f"等待  {lines[0] / 1000}  秒")
                                        if lines[1] == "M":
                                            if lines[2] == "mouse move":
                                                type_event = "鼠标移动到"
                                            elif lines[2] == "mouse left down":
                                                type_event = "左键按下"
                                            elif lines[2] == "mouse left up":
                                                type_event = "左键抬起"
                                            elif lines[2] == "mouse right down":
                                                type_event = "右键按下"
                                            elif lines[2] == "mouse right up":
                                                type_event = "右键抬起"
                                            elif lines[2] == "mouse middle down":
                                                type_event = "中键按下"
                                            elif lines[2] == "mouse middle up":
                                                type_event = "中键抬起"
                                            elif lines[2] == "mouse scroll":
                                                type_event = "滚轮滑动"
                                            else:
                                                type_event = "未知操作"
                                            self.edit_text.append(f"鼠标  {type_event}  {lines[3]}")
                                        elif lines[1] == "K":
                                            if lines[2] == 'key down':
                                                type_event = "按下按键"
                                            elif lines[2] == 'key up':
                                                type_event = "抬起按键"
                                            else:
                                                type_event = "未知"
                                            self.edit_text.append(f"键盘  {type_event}  {lines[3]}")

                            def handle_line(self):
                                text = self.edit_text.toPlainText()
                                text_lines = text.split('\n')
                                total_time = 0
                                count = 0
                                self.lists = []
                                try:
                                    for line in text_lines:
                                        count += 1
                                        lines = line.split('  ')
                                        if lines[0] == '等待':
                                            total_time += int(float(lines[1]) * 1000)
                                        else:
                                            list = []
                                            if total_time == 0:
                                                total_time = 1
                                            list.append(total_time)
                                            if lines[0] == '键盘':
                                                types = "K"
                                            else:
                                                types = "M"
                                            list.append(types)
                                            if lines[1] == "按下按键":
                                                type_key = "key down"
                                            elif lines[1] == '抬起按键':
                                                type_key = 'key up'
                                            elif lines[1] == '左键按下':
                                                type_key = 'mouse left down'
                                            elif lines[1] == '左键抬起':
                                                type_key = 'mouse left up'
                                            elif lines[1] == '鼠标移动到':
                                                type_key = 'mouse move'
                                            elif lines[1] == '右键按下':
                                                type_key = 'mouse right down'
                                            elif lines[1] == '右键抬起':
                                                type_key = 'mouse right up'
                                            elif lines[1] == '中键按下':
                                                type_key = 'mouse middle down'
                                            elif lines[1] == '中键抬起':
                                                type_key = 'mouse middle up'
                                            else:
                                                type_key = 'key up'
                                            list.append(type_key)
                                            list.append(ast.literal_eval(lines[2]))
                                            total_time = 0
                                            self.lists.append(list)
                                    if self.lists == self.list:
                                        return "allow"
                                    else:
                                        return "refuse"
                                except:
                                    return count

                            def ReLoad(self):
                                result = self.handle_line()
                                if result == 'refuse':
                                    reply = QMessageBox.question(self, '确认退出',
                                                                 "你已修改文件，是否确认重新导入？",
                                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                    if reply == QMessageBox.Yes:
                                        self.edit_text.clear()
                                        self.LoadFile()
                                elif result == 'allow':
                                    self.edit_text.clear()
                                    self.LoadFile()
                                elif isinstance(result, int):
                                    QMessageBox.question(self, '错误',
                                                         f"不支持的语法 出现在 {result} 行 请修改后尝试",
                                                         QMessageBox.Yes, QMessageBox.No)

                            def addpress(self, key, code,types):
                                if types == 'key':
                                    cursor = self.edit_text.textCursor()
                                    text = f'\n等待  0.1  秒\n键盘  按键按下  [{code},  \'{key}\']\n等待  0.1  秒\n键盘  按键抬起  [{code},  \'{key}\']'

                                    if cursor.isNull():
                                        print("没有光标")
                                    else:
                                        # 创建文本格式并设置颜色
                                        text_format = QTextCharFormat()
                                        text_format.setForeground(QColor('blue'))  # 设置字体颜色为蓝色

                                        cursor.beginEditBlock()  # 开始编辑块
                                        cursor.setCharFormat(text_format)  # 应用文本格式
                                        cursor.insertText(text, text_format)  # 插入带格式的文本
                                        cursor.endEditBlock()  # 结束编辑块
                                        line_number = cursor.blockNumber() + 1  # +1 to convert from zero-based index
                                        print(f"光标所在行: {line_number}")
                                else:
                                    cursor = self.edit_text.textCursor()
                                    if key[0:2] == '左键':
                                        text = f'\n等待  0.1  秒\n鼠标  左键按下  [0, 0]\n等待  0.1  秒\n鼠标  左键抬起  [0, 0]'
                                    elif key[0:2] == '中键':
                                        text = f'\n等待  0.1  秒\n鼠标  中键按下  [0, 0]\n等待  0.1  秒\n鼠标  中键抬起  [0, 0]'
                                    elif key[0:2] == '右键':
                                        text = f'\n等待  0.1  秒\n鼠标  右键按下  [0, 0]\n等待  0.1  秒\n鼠标  右键抬起  [0, 0]'
                                    elif key[0:2] == '鼠标':
                                        text = f'\n等待  0.1  秒\n鼠标  鼠标移动到  [0, 0]'
                                    elif key[0:2] == '滚轮':
                                        text = f'\n等待  0.1  秒\n鼠标  滚轮滑动  [0, 0]'

                                    if cursor.isNull():
                                        print("没有光标")
                                    else:
                                        # 创建文本格式并设置颜色
                                        text_format = QTextCharFormat()
                                        text_format.setForeground(QColor('blue'))  # 设置字体颜色为蓝色

                                        cursor.beginEditBlock()  # 开始编辑块
                                        cursor.setCharFormat(text_format)  # 应用文本格式
                                        cursor.insertText(text, text_format)  # 插入带格式的文本
                                        cursor.endEditBlock()  # 结束编辑块
                                        line_number = cursor.blockNumber() + 1  # +1 to convert from zero-based index
                                        print(f"光标所在行: {line_number}")

                            def create_key_Menu(self):
                                key_menu = QMenu(self)

                                # 按键分组
                                groups = {
                                    '功能键': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
                                               'F12'],
                                    '控制键': ['CTRL_L', 'CTRL_R', 'ALT', 'ALT_GR', 'ALT_L', 'ALT_R', 'SHIFT',
                                               'SHIFT_R'],
                                    '导航键': ['HOME', 'END', 'PAGE_UP', 'PAGE_DOWN', 'LEFT', 'RIGHT', 'UP', 'DOWN'],
                                    '系统键': ['ESC', 'ENTER', 'BACKSPACE', 'INSERT', 'DELETE', 'TAB', 'CAPS_LOCK',
                                               'NUM_LOCK', 'SCROLL_LOCK', 'PRINT_SCREEN', 'MENU'],
                                    '字母': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                                             'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                                }
                                # 为每个分组创建子菜单并添加动作
                                for group_name, keys in groups.items():
                                    sub_menu = key_menu.addMenu(group_name)
                                    for key in keys:
                                        action = QAction(key, self)
                                        action.triggered.connect(lambda checked, k=key: self.keyPressed(k))
                                        sub_menu.addAction(action)

                                # 显示菜单
                                return key_menu

                            def save_file(self):
                                try:
                                    self.handle_line()
                                    # 逐行写入文件
                                    with open('./scripts/' + self.file, 'w') as file:
                                        for line in self.lists:
                                            file.write(str(line) + '\n')  # 写入内容并换行
                                    self.edit_text.clear()
                                    self.LoadFile()
                                    pyautogui.confirm("保存成功！")
                                except Exception as e:
                                    print(e)
                                    pyautogui.confirm(e)
                            def keyPressed(self, key):
                                self.key_codes = {
                                    'F1': 112,
                                    'F2': 113,
                                    'F3': 114,
                                    'F4': 115,
                                    'F5': 116,
                                    'F6': 117,
                                    'F7': 118,
                                    'F8': 119,
                                    'F9': 120,
                                    'F10': 121,
                                    'F11': 122,
                                    'F12': 123,
                                    'CTRL_L': 37,
                                    'CTRL_R': 105,
                                    'ALT': 64,
                                    'ALT_GR': 108,
                                    'ALT_L': 64,
                                    'ALT_R': 108,
                                    'SHIFT': 50,
                                    'SHIFT_R': 62,
                                    'HOME': 110,
                                    'END': 115,
                                    'PAGE_UP': 104,
                                    'PAGE_DOWN': 109,
                                    'LEFT': 113,
                                    'RIGHT': 114,
                                    'UP': 111,
                                    'DOWN': 116,
                                    'ESC': 9,
                                    'ENTER': 36,
                                    'BACKSPACE': 22,
                                    'INSERT': 118,
                                    'DELETE': 119,
                                    'TAB': 23,
                                    'CAPS_LOCK': 66,
                                    'NUM_LOCK': 77,
                                    'SCROLL_LOCK': 78,
                                    'PRINT_SCREEN': 107,
                                    'MENU': 135,
                                    'A': 38,
                                    'B': 56,
                                    'C': 54,
                                    'D': 40,
                                    'E': 26,
                                    'F': 41,
                                    'G': 42,
                                    'H': 43,
                                    'I': 31,
                                    'J': 44,
                                    'K': 45,
                                    'L': 46,
                                    'M': 58,
                                    'N': 57,
                                    'O': 32,
                                    'P': 33,
                                    'Q': 24,
                                    'R': 27,
                                    'S': 39,
                                    'T': 28,
                                    'U': 30,
                                    'V': 55,
                                    'W': 25,
                                    'X': 53,
                                    'Y': 29,
                                    'Z': 52
                                }
                                self.addpress(key, self.key_codes.get(key),'key')

                            def create_mouse_Menu(self):
                                mouse_menu = QMenu(self)

                                action1 = QAction("左键点击", self)
                                action1.triggered.connect(lambda: self.mousePressed("左键点击"))

                                action2 = QAction("右键点击", self)
                                action2.triggered.connect(lambda: self.mousePressed("右键点击"))

                                action3 = QAction("中键点击", self)
                                action3.triggered.connect(lambda: self.mousePressed("中键点击"))

                                action4 = QAction("滚轮滚动", self)
                                action4.triggered.connect(lambda: self.mousePressed("滚轮滚动"))

                                action5 = QAction("鼠标移动", self)
                                action5.triggered.connect(lambda: self.mousePressed("鼠标移动"))

                                mouse_menu.addAction(action1)
                                mouse_menu.addAction(action2)
                                mouse_menu.addAction(action3)
                                mouse_menu.addAction(action4)
                                mouse_menu.addAction(action5)
                                return mouse_menu

                            def mousePressed(self, key):
                                self.addpress(key, "Null", 'mouse')

                            def closeEvent(self,Event):
                                result = self.handle_line()
                                if result == 'refuse':
                                    reply = QMessageBox.question(self, '确认退出',
                                                                 "你已修改文件，是否确认退出？",
                                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                                    if reply == QMessageBox.Yes:
                                        self.close()
                                elif isinstance(result, int):
                                    QMessageBox.question(self, '错误',
                                                         f"不支持的语法 出现在 {self.handle_line()} 行 本次将不会保存配置文件",
                                                         QMessageBox.Yes, QMessageBox.No)
                                    self.close()

                        class record_position(QtWidgets.QDialog):
                            def __init__(self):
                                super().__init__()
                                window_position = windows.pos()
                                x = window_position.x() + 500 - 270
                                y = window_position.y() + 300 - 170
                                self.setGeometry(x, y, 350, 200)
                                self.page = 0
                                self.setWindowTitle("记录位置")


                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(16)

                                self.prompt_label = QtWidgets.QLabel(self)
                                self.prompt_label.setGeometry(QtCore.QRect(15, 0, 400, 140))
                                self.prompt_label.setFont(font)
                                self.prompt_label.setObjectName("prompt_label")
                                self.prompt_label.setText("即将开始进行控件位置初始化设定\n是否立即开始？\n\n点击确定继续 点击取消关闭")

                                self.continue_button = QtWidgets.QPushButton(self)
                                self.continue_button.setGeometry(QtCore.QRect(60, 150, 100, 30))
                                self.continue_button.setObjectName("continue_button")
                                self.continue_button.setText("确定")
                                self.continue_button.clicked.connect(self.next_continue)

                                self.cancel_button = QtWidgets.QPushButton(self)
                                self.cancel_button.setGeometry(QtCore.QRect(180, 150, 100, 30))
                                self.cancel_button.setObjectName("cancel_button")
                                self.cancel_button.setText("取消")
                                self.cancel_button.clicked.connect(self.close)

                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(13)

                                self.label1 = QtWidgets.QLabel(self)
                                self.label1.setGeometry(QtCore.QRect(450, 0, 400, 110))
                                self.label1.setFont(font)
                                self.label1.setObjectName("label1")
                                self.label1.setText(
                                    f"正在设置第一处位置(聊天框)\n请将鼠标放在窗口的聊天框上\n按下CTRL+P记录位置\n点击按钮或CTRL+L继续下一步")

                                self.label2 = QtWidgets.QLabel(self)
                                self.label2.setGeometry(QtCore.QRect(450, 100, 400, 40))
                                self.label2.setFont(font)
                                self.label2.setObjectName("label2")
                                self.label2.setText(
                                    f"位置[等待记录]")

                                self.next_button = QtWidgets.QPushButton(self)
                                self.next_button.setGeometry(QtCore.QRect(460, 150, 90, 30))
                                self.next_button.setObjectName("next_button")
                                self.next_button.setText("下一步")
                                self.next_button.clicked.connect(self.next_normal)
                                self.next_button.setEnabled(False)

                                self.close_button = QtWidgets.QPushButton(self)
                                self.close_button.setGeometry(QtCore.QRect(560, 150, 90, 30))
                                self.close_button.setObjectName("close_button")
                                self.close_button.setText("取消")
                                self.close_button.clicked.connect(self.close)

                                self.label3 = QtWidgets.QLabel(self)
                                self.label3.setGeometry(QtCore.QRect(450, 0, 400, 110))
                                self.label3.setFont(font)
                                self.label3.setObjectName("label3")
                                self.label3.setText(
                                    f"正在设置第二处位置(发送按钮)\n请将鼠标放在窗口的发送按钮上\n按下CTRL+P记录位置\n点击按钮或CTRL+L继续")

                                self.label4 = QtWidgets.QLabel(self)
                                self.label4.setGeometry(QtCore.QRect(450, 100, 400, 40))
                                self.label4.setFont(font)
                                self.label4.setObjectName("label4")
                                self.label4.setText(
                                    f"位置[等待记录]")

                                self.complete_button = QtWidgets.QPushButton(self)
                                self.complete_button.setGeometry(QtCore.QRect(460, 150, 90, 30))
                                self.complete_button.setObjectName("complete_button")
                                self.complete_button.setText("完成")
                                self.complete_button.clicked.connect(self.complete)
                                self.complete_button.setEnabled(False)

                                self.cancel_last = QtWidgets.QPushButton(self)
                                self.cancel_last.setGeometry(QtCore.QRect(460, 150, 90, 30))
                                self.cancel_last.setObjectName("cancel_last")
                                self.cancel_last.setText("取消")
                                self.cancel_last.clicked.connect(self.close)

                                self.position = [50,50,80,180]
                                global global_position
                                global_position = [[None,None],[None,None]]
                                self.before_list = [self.prompt_label,self.continue_button,self.cancel_button]
                                self.after_list = [self.label1,self.label2,self.next_button,self.close_button]
                                self.last_list = [self.label3,self.label4,self.complete_button,self.cancel_last]

                            def next_continue(self):
                                self.page = self.page + 1
                                for index in self.before_list:
                                    widget = index
                                    if widget is not None:
                                        start_pos = widget.pos()
                                        end_pos = QRect(-500, start_pos.y(), widget.width(), widget.height())
                                        animation = QPropertyAnimation(widget, b"geometry", self)
                                        animation.setDuration(500)
                                        animation.setStartValue(QRect(start_pos, widget.size()))
                                        animation.setEndValue(end_pos)
                                        easing_curve = QEasingCurve(QEasingCurve.InQuad)  # 使用加速的缓动曲线
                                        animation.setEasingCurve(easing_curve)
                                        animation.start()
                                nums = 0
                                for index in self.after_list:
                                    widget = index
                                    pox = self.position[nums]
                                    nums = nums + 1
                                    if widget is not None:
                                        start_pos = widget.pos()
                                        end_pos = QRect(pox, start_pos.y(), widget.width(), widget.height())
                                        animation = QPropertyAnimation(widget, b"geometry", self)
                                        animation.setDuration(450)
                                        animation.setStartValue(QRect(start_pos, widget.size()))
                                        animation.setEndValue(end_pos)
                                        easing_curve = QEasingCurve(QEasingCurve.InQuad)  # 使用加速的缓动曲线
                                        animation.setEasingCurve(easing_curve)
                                        animation.start()
                                # 在主线程中创建并启动键盘监听线程
                                self.keyboard_thread =KeyboardThread()
                                self.keyboard_thread.keyPressed.connect(self.handle_key_pressed)
                                self.keyboard_thread.start()

                            def closeEvent(self,event):
                                keys.unhook_all()

                            def next_normal(self):
                                self.next_button.setEnabled(False)
                                self.page = self.page + 1
                                pass
                                global global_position
                                for index in self.after_list:
                                    if index is not None:
                                        start_pos = index.pos()
                                        end_pos = QRect(-500, start_pos.y(), index.width(), index.height())
                                        animation = QPropertyAnimation(index, b"geometry", self)
                                        animation.setDuration(500)
                                        animation.setStartValue(QRect(start_pos, index.size()))
                                        animation.setEndValue(end_pos)
                                        easing_curve = QEasingCurve(QEasingCurve.InQuad)  # 使用加速的缓动曲线
                                        animation.setEasingCurve(easing_curve)
                                        animation.start()
                                nums = 0
                                time.sleep(0.5)
                                for index in self.last_list:
                                    pos = self.position[nums]
                                    nums = nums + 1
                                    if index is not None:
                                        start_pos = index.pos()
                                        end_pos = QRect(pos, start_pos.y(), index.width(), index.height())
                                        animation = QPropertyAnimation(index, b"geometry", self)
                                        animation.setDuration(500)
                                        animation.setStartValue(QRect(start_pos, index.size()))
                                        animation.setEndValue(end_pos)
                                        easing_curve = QEasingCurve(QEasingCurve.InQuad)  # 使用加速的缓动曲线
                                        animation.setEasingCurve(easing_curve)
                                        animation.start()
                                pass

                            def complete(self):
                                global global_position,position_status,textedit_position,send_position
                                with open("config.json", "r") as file:
                                    pdata = json.load(file)
                                pdata["position"] = global_position
                                with open("config.json", "w") as file:
                                    json.dump(pdata, file, indent=4)
                                position_status = True
                                textedit_position = global_position[0]
                                send_position = global_position[1]
                                windows.label_position_status.setText(
                                    '<font color="black">位置设置：</font> <font color="green">已设置</font>')
                                windows.label_position_send.setText(
                                    f'<font color="black">发送键位置：</font> <font color="green">{send_position}</font>')
                                windows.label_position_text.setText(
                                    f'<font color="black">聊天框位置：</font> <font color="green">{textedit_position}</font>')

                                self.close()
                                pyautogui.confirm("设置成功！")

                            def handle_key_pressed(self,key):
                                if key == 'Ctrl+P':
                                    global global_position
                                    a = pyautogui.position()
                                    if self.page == 1:
                                        global_position[0] = [a.x,a.y]
                                        self.label2.setText(
                                            f"位置[{a.x},{a.y}]")
                                        self.next_button.setEnabled(True)
                                    elif self.page == 2:
                                        global_position[1] = [a.x,a.y]
                                        self.label4.setText(
                                            f"位置[{a.x},{a.y}]")
                                        self.complete_button.setEnabled(True)
                                elif key == "Ctrl+L":
                                    if self.page == 1:
                                        if self.next_button.isEnabled():
                                            self.next_normal()
                                    elif self.page == 2:
                                        if self.complete_button.isEnabled():
                                            self.complete()

                        class KeyboardThread(QThread):
                            keyPressed = pyqtSignal(str)
                            def run(self):
                                # 注册全局热键 Ctrl+P
                                keys.add_hotkey('ctrl+p', lambda: self.handle_key_pressed('Ctrl+P'))
                                # 注册全局热键 Ctrl+L
                                keys.add_hotkey('ctrl+l', lambda: self.handle_key_pressed('Ctrl+L'))
                                keys.wait()

                            def handle_key_pressed(self,key):
                                if not self.is_window_open("记录位置"):
                                    keys.unhook_all()
                                else:
                                    self.keyPressed.emit(key)
                            def is_window_open(self,window_title):
                                toplist = []
                                win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), toplist)

                                for hwnd in toplist:
                                    if win32gui.GetWindowText(hwnd) == window_title:
                                        return True

                                return False

                        class CustomLineEdit(QLineEdit):
                            def __init__(self, parent=None):
                                super().__init__(parent)

                            def keyPressEvent(self, event):
                                if event.matches(QKeySequence.Paste):
                                    # 处理Ctrl+V事件
                                    clipboard = QApplication.clipboard()
                                    url = clipboard.text()
                                    if '/#/' in url:
                                        url = url.replace('/#/','/')
                                    if (url[0:29] == 'https://music.163.com/song?id') and (len(clipboard.text())>29):
                                        try:

                                            header = {
                                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
                                            res = requests.get(url, headers=header)

                                            # 使用BeautifulSoup解析HTML
                                            soup = BeautifulSoup(res.text, 'html.parser')

                                            # 提取keywords标签的content属性
                                            keywords_tag = soup.find('meta', {'name': 'keywords'})
                                            keywords_content = keywords_tag['content'] if keywords_tag else None

                                            # 使用split方法提取第一个内容
                                            if keywords_content:
                                                first_content = keywords_content.split('，')[0]
                                                windows._5lineEdit2.setText(first_content + ".mp3")
                                        except:
                                            pass

                                # 调用父类的方法处理其他键盘事件
                                super().keyPressEvent(event)

                        class Hide():
                            def __init__(self):
                                global window_icon
                                if not window_icon:
                                    windows.tray_icon = QSystemTrayIcon(windows)
                                    windows.tray_icon.setIcon(
                                        QIcon('./image/Component/favicon.ico'))  # 替换 'icon.png' 为你的图标文件路径
                                    windows.tray_icon.show()

                                    show_action = QAction('打开主窗口', windows)
                                    quit_action = QAction('退出', windows)
                                    show_action.triggered.connect(windows.showNormal)
                                    quit_action.triggered.connect(windows.close_MainWindow)

                                    context_menu = QMenu()
                                    context_menu.addAction(show_action)
                                    context_menu.addSeparator()
                                    context_menu.addAction(quit_action)

                                    windows.tray_icon.setContextMenu(context_menu)
                                    windows.tray_icon.activated.connect(windows.tray_icon_activated)
                                    window_icon = True
                                windows.hide()

                        class CustomWidget(QtWidgets.QWidget):  # 绘制客户端窗口方框分割线
                            def paintEvent(self, event):
                                painter = QtGui.QPainter(self)
                                painter.setRenderHint(QtGui.QPainter.Antialiasing)

                                pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
                                painter.setPen(pen)

                                brush = QtGui.QColor(200, 200, 255, 0)  # 透明背景色
                                painter.setBrush(brush)

                                # 绘制一个方框
                                corner_radius = 5
                                rect = self.rect().adjusted(5, 5, -5, -5)
                                painter.drawRoundedRect(rect, corner_radius, corner_radius)

                        class floating_window(QWidget):  #悬浮窗
                            def __init__(self):
                                super().__init__()

                                self.initUI()
                                self.draggable_left = False
                                self.draggable_right = False
                                self.draggable = False
                                self.offset = None
                                self.open = False

                            def initUI(self):
                                self.setWindowTitle('Fuchen悬浮窗')
                                self.setGeometry(1700, 100, 200, 200)  # 设置窗口位置和大小
                                self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
                                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

                                self.button_QQ = QtWidgets.QPushButton(self)  # 创建按钮
                                self.button_QQ.setStyleSheet("QPushButton#button_QQ {"
                                                        "border-image: url(./image/float/qq1.png);" 
                                                        "background: transparent;"
                                                        "}")

                                self.button_QQ.setGeometry(QtCore.QRect(84, 30, 81, 81))
                                self.button_QQ.setObjectName("button_QQ")
                                self.button_QQ.clicked.connect(self.on_button_click)
                                self.button_QQ.clicked.connect(windows.Send_QQ)

                                self.button_copy = QtWidgets.QPushButton(self)  # 创建按钮
                                self.button_copy.setStyleSheet("QPushButton#button_copy {"
                                                          "border-image: url(./image/float/copy.png);"
                                                          "background: transparent;"
                                                          "}")
                                self.button_copy.setGeometry(QtCore.QRect(84, 104, 81, 81))
                                self.button_copy.setObjectName("button_copy")
                                self.button_copy.clicked.connect(self.on_button_click)
                                self.button_copy.clicked.connect(windows.Send_Copy)


                                self.button_crowd = QtWidgets.QPushButton(self)  # 创建按钮
                                self.button_crowd.setStyleSheet("QPushButton#button_crowd {"
                                                           "    border-image: url(./image/float/record.png);"
                                                           "background: transparent;"
                                                           "}")
                                self.button_crowd.setGeometry(QtCore.QRect(10, 104, 81, 81))
                                self.button_crowd.setObjectName("button_crowd")
                                self.button_crowd.clicked.connect(self.on_button_click)
                                self.button_crowd.clicked.connect(windows.Click_Record)

                                self.button_execute = QtWidgets.QPushButton(self)  # 创建按钮
                                self.button_execute.setStyleSheet("QPushButton#button_execute {"
                                                             "    border-image: url(./image/float/exe.png);"
                                                             "background: transparent;"
                                                             "}")
                                self.button_execute.setGeometry(QtCore.QRect(9, 30, 83, 83))
                                self.button_execute.setObjectName("button_execute")
                                self.button_execute.clicked.connect(self.on_button_click)
                                self.button_execute.clicked.connect(windows.Click_Record_execute)

                                self.buttonGroup = QtWidgets.QButtonGroup(self)
                                self.buttonGroup.addButton(self.button_QQ)
                                self.buttonGroup.addButton(self.button_copy)
                                self.buttonGroup.addButton(self.button_crowd)
                                self.buttonGroup.addButton(self.button_execute)

                                for button in self.buttonGroup.buttons():
                                    button.setVisible(False)

                                self.button = QtWidgets.QPushButton(self)  # 创建按钮
                                self.button.setStyleSheet("QPushButton#button {"
                                                     "    border-image: url(./image/float/round.png);"
                                                     "}")
                                self.button.setGeometry(QtCore.QRect(48, 70, 80, 80))
                                self.button.setObjectName("button")
                                self.button.installEventFilter(self)

                                self.button.clicked.connect(self.on_button_click)
                                self.button.raise_()

                            def on_button_click(self):
                                if self.open == False:
                                    for button in self.buttonGroup.buttons():
                                        button.setVisible(True)
                                    self.open = True
                                else:
                                    for button in self.buttonGroup.buttons():
                                        button.setVisible(False)
                                    self.open = False

                            def eventFilter(self, obj, event):
                                if event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.RightButton:
                                    self.draggable = True
                                    self.offset = event.pos()
                                    return True
                                elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.RightButton:
                                    self.draggable = False
                                    return True
                                elif event.type() == QtCore.QEvent.MouseMove and self.draggable:
                                    self.move(self.mapToGlobal(event.pos() - self.offset))
                                    return True
                                return super().eventFilter(obj, event)

                        class SetWindow(QtWidgets.QDialog):
                            def __init__(self):
                                super().__init__()
                                window_position = windows.pos()
                                x = window_position.x() + 500 - 270
                                y = window_position.y() + 300 - 170
                                self.setGeometry(x, y, 540, 340)
                                self.setFixedSize(540, 340)
                                icon = QIcon("./image/Component/提示.png")
                                self.setWindowIcon(icon)
                                self.border_width = 8
                                self.setAttribute(Qt.WA_TranslucentBackground)
                                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 设置 窗口无边框和背景透明

                                self.pushButton_close = QtWidgets.QPushButton(self)
                                self.pushButton_close.setGeometry(QtCore.QRect(500, 10, 26, 26))
                                self.pushButton_close.setObjectName("pushButton_close")
                                self.pushButton_close.setStyleSheet("QPushButton#pushButton_close {"
                                                                    "    border-image: url(./image/quit.png);"
                                                                    "    background-color: rgba(245,245,245,0)"
                                                                    "}")
                                self.pushButton_close.setToolTip("关闭")

                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(12)

                                self.setWindowTitle("设置")
                                self.label = QtWidgets.QLabel(self)
                                self.label.setGeometry(QtCore.QRect(20, 20, 70, 20))
                                self.label.setFont(font)
                                self.label.setObjectName("label")
                                self.pushButton = QtWidgets.QPushButton(self)
                                self.pushButton.setGeometry(QtCore.QRect(420, 292, 100, 31))
                                font = QtGui.QFont()
                                font.setFamily("微软雅黑")
                                font.setPointSize(12)
                                self.pushButton.setFont(font)
                                self.pushButton.setObjectName("pushButton")
                                self.pushButton.setStyleSheet('''
                                                                        QPushButton {
                                                                                        background: transparent;
                                                                                        border-radius: 6px;
                                                                                        border: 2px groove gray;
                                                                                        border-style: outset;
                                                                                        background-color: rgb(204,223,248);
                                                                                        border-color: rgb(204,223,248); 
                                                                                        padding: 0;
                                                                                }
                                                                                                                        QPushButton:hover {
                                                                                                                            border-radius: 8px;
                                                                                                                            border: 2px groove gray;
                                                                                                                            border-style: outset;
                                                                                                                            background-color: rgb(96,160,235); /* 修改为选中后的颜色 */
                                                                                                                            border-color: rgb(96,160,235); /* 修改为选中后的颜色 */
                                                                                                                        }
                                                                                                                    ''')

                                self.check_autologin = QtWidgets.QCheckBox(self)
                                self.check_autologin.setGeometry(QtCore.QRect(20, 50, 161, 20))
                                self.check_autologin.setFont(font)
                                self.check_autologin.setObjectName("check_autologin")
                                global Log
                                if Log == True:
                                    self.check_autologin.setChecked(True)

                                self.check_sound = QtWidgets.QCheckBox(self)
                                self.check_sound.setGeometry(QtCore.QRect(20, 90, 160, 20))
                                self.check_sound.setFont(font)
                                self.check_sound.setObjectName("check_sound")
                                self.check_sound.setStyleSheet('''QCheckBox {
                                    border-radius: 10px;
                                }''')
                                global Sound
                                if Sound == True:
                                    self.check_sound.setChecked(True)

                                self.check_closeprompt = QtWidgets.QCheckBox(self)
                                self.check_closeprompt.setGeometry(QtCore.QRect(20, 130, 160, 20))
                                self.check_closeprompt.setFont(font)
                                self.check_closeprompt.setObjectName("checkBox_5")
                                global ClosePrompt
                                if ClosePrompt == True:
                                    self.check_closeprompt.setChecked(True)
                                self.check_closeprompt.setText("关闭时提示操作")

                                self.checkBox_5 = QtWidgets.QCheckBox(self)
                                self.checkBox_5.setGeometry(QtCore.QRect(20, 170, 160, 20))
                                self.checkBox_5.setFont(font)
                                self.checkBox_5.setObjectName("checkBox_5")
                                self.checkBox_5.setText("开启悬浮窗")

                                self.checkBox_start = QtWidgets.QCheckBox(self)
                                self.checkBox_start.setGeometry(QtCore.QRect(20, 210, 160, 20))
                                self.checkBox_start.setFont(font)
                                self.checkBox_start.setObjectName("checkBox_start")
                                self.checkBox_start.setText("开机自启动")

                                self.group_theme = QButtonGroup(self)
                                self.radioButton_white = QtWidgets.QRadioButton(self)
                                self.radioButton_white.setGeometry(QtCore.QRect(240, 40, 89, 20))
                                self.radioButton_white.setFont(font)
                                self.radioButton_white.setObjectName("radioButton_white")
                                self.radioButton_custom = QtWidgets.QRadioButton(self)
                                self.radioButton_custom.setGeometry(QtCore.QRect(240, 70, 130, 20))
                                self.radioButton_custom.setFont(font)
                                self.radioButton_custom.setObjectName("radioButton_custom")
                                self.line_Custom = QtWidgets.QLineEdit(self)  #自定义图片背景输入栏
                                self.line_Custom.setGeometry(QtCore.QRect(240, 95, 211, 20))
                                self.line_Custom.setObjectName("line_Custom")
                                self.pushButton_2 = QtWidgets.QPushButton(self)
                                self.pushButton_2.setGeometry(QtCore.QRect(460, 94, 51, 23))
                                self.pushButton_2.setObjectName("pushButton_2")

                                self.radioButton_trend = QtWidgets.QRadioButton(self)
                                self.radioButton_trend.setGeometry(QtCore.QRect(240, 120, 111, 20))
                                self.radioButton_trend.setFont(font)
                                self.radioButton_trend.setObjectName("radioButton_trend")
                                self.line_Trend = QtWidgets.QLineEdit(self)  # 自定义图片背景输入栏
                                self.line_Trend.setGeometry(QtCore.QRect(240, 145, 211, 20))
                                self.line_Trend.setObjectName("line_Trend")
                                self.pushButton_3 = QtWidgets.QPushButton(self)
                                self.pushButton_3.setGeometry(QtCore.QRect(460, 144, 51, 23))
                                self.pushButton_3.setObjectName("pushButton_3")

                                self.FPS_label = QtWidgets.QLabel(self)
                                self.FPS_label.setGeometry(QtCore.QRect(240, 180, 80, 12))
                                self.FPS_label.setObjectName("FPS_label")
                                self.FPS_label.setText("刷新率/每秒")
                                global FPS
                                self.FPS_spinBox = QtWidgets.QSpinBox(self)  # FPS
                                self.FPS_spinBox.setGeometry(QtCore.QRect(320, 175, 60, 22))
                                self.FPS_spinBox.setMaximum(9999)
                                self.FPS_spinBox.setValue(FPS)
                                self.FPS_spinBox.setObjectName("FPS_spinBox")
                                self.FPS_spinBox.setStyleSheet("""
                                                                                                        QSpinBox {
                                                                                                            border: 1px solid gray;
                                                                                                            border-radius: 3px;  /* 设置圆角 */
                                                                                                            background: transparent;
                                                                                                            font: 14px;
                                                                                                            font-family: Calibri;
                                                                                                        }
                                                                                                        QSpinBox::up-button {
                                                                                                            subcontrol-origin: border;
                                                                                                            subcontrol-position: top right; 
                                                                                                            width: 13px; 
                                                                                                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                        }
                                                                                                        QSpinBox::down-button {
                                                                                                            subcontrol-origin: border;
                                                                                                            subcontrol-position: bottom right; 
                                                                                                            width: 13px; 
                                                                                                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                        }
                                                                                                    """)
                                self.FPS_spinBox.setMinimum(1)
                                self.FPS_spinBox.repaint()
                                self.FPS_spinBox.setMaximum(60)
                                if cv2_available == False:  # 检查文件夹是否存在 其中有无内容
                                    self.radioButton_trend.setEnabled(False)
                                    self.radioButton_trend.setToolTip("需要安装扩展内容")
                                    self.line_Trend.setEnabled(False)
                                    self.pushButton_3.setEnabled(False)
                                    self.FPS_spinBox.setEnabled(False)

                                self.group_theme.addButton(self.radioButton_white)
                                self.group_theme.addButton(self.radioButton_custom)
                                self.group_theme.addButton(self.radioButton_trend)

                                # 要检查的文件名
                                file_name = 'Fuchen_Start_File.bat'
                                result = self.check_startup_file(file_name)
                                self.First = False
                                if result:
                                    self.checkBox_start.setChecked(True)
                                    self.First = True
                                global window_s
                                if window_s == True:
                                    self.checkBox_5.setChecked(True)
                                else:
                                    self.checkBox_5.setChecked(False)
                                global Theme
                                if Theme == "White":
                                    self.radioButton_white.setChecked(True)
                                elif Theme == 'Custom':
                                    self.radioButton_custom.setChecked(True)
                                    with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                                        config = json.load(file)
                                    # 添加新元素到数据结构
                                    Path_Custom = config["Theme"][7:]
                                    self.line_Custom.setText(Path_Custom)
                                elif Theme == 'Trend':
                                    self.radioButton_trend.setChecked(True)
                                    with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                                        config = json.load(file)
                                    # 添加新元素到数据结构
                                    Path_Trend = config["Theme"][6:]
                                    self.line_Trend.setText(Path_Trend)
                                else:
                                    self.radioButton_white.setChecked(True)


                                self.label.setText("设置")
                                self.pushButton.setText("保存")
                                #self.checkBox_2.setText("询问是否启动线上模式")
                                self.check_sound.setText("按钮提示音")
                                self.check_autologin.setText("自动登录")
                                self.radioButton_white.setText("白色主题")
                                self.radioButton_custom.setText("自定义背景图片")
                                self.radioButton_trend.setText("动态主题")
                                self.pushButton_2.setText("浏览")
                                self.pushButton_3.setText("浏览")
                                self.pushButton_close.clicked.connect(self.clos)
                                self.pushButton.clicked.connect(self.set)
                                self.pushButton_2.clicked.connect(lambda: self.select_bf("Image"))
                                self.pushButton_3.clicked.connect(lambda: self.select_bf("Video"))

                            def clos(self):
                                self.close()

                            def check_startup_file(self,file_name):
                                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                                              'Start Menu', 'Programs', 'Startup')
                                file_path = os.path.join(startup_folder, file_name)

                                if os.path.exists(file_path):
                                    return 1
                                else:
                                    return 0

                            def select_bf(self,ty):
                                if ty == "Image":
                                    options = QFileDialog.Options()
                                    options |= QFileDialog.ReadOnly
                                    file_name, _ = QFileDialog.getOpenFileName(self, "选择图片", "",
                                                                               "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)",
                                                                               options=options)
                                    if file_name:
                                        self.line_Custom.setText(file_name)
                                    else:
                                        pyautogui.confirm("未选择文件！")
                                elif ty == "Video":
                                    options = QFileDialog.Options()
                                    options |= QFileDialog.ReadOnly
                                    file_name, _ = QFileDialog.getOpenFileName(self, "选择视频", "",
                                                                               "视频文件 (*.mp4 *.mov *.flv *.avi *.gif)",
                                                                               options=options)
                                    if file_name:
                                        self.line_Trend.setText(file_name)
                                    else:
                                        pyautogui.confirm("未选择文件！")

                            def set(self):
                                global Sound, Log, Theme, flo_window, window_s, ClosePrompt,FPS
                                if self.check_sound.isChecked():
                                    Sound = True
                                else:
                                    Sound = False
                                if self.check_autologin.isChecked():
                                    Log = True
                                else:
                                    Log = False
                                if self.check_closeprompt.isChecked():
                                    ClosePrompt = True
                                else:
                                    ClosePrompt = False
                                with open('config.json', 'r') as file:
                                    config = json.load(file)
                                #config["Ask"] = Ask
                                config["Sound"] = Sound
                                config["AutoLogin"] = Log
                                config["ClosePrompt"] = ClosePrompt
                                if self.FPS_spinBox.value() != FPS:
                                    config["FPS"] = self.FPS_spinBox.value()
                                    FPS = self.FPS_spinBox.value()
                                # 将更新后的数据写入 JSON 文件
                                with open('config.json', 'w') as file:
                                    json.dump(config, file, indent=4)
                                n = True
                                if self.radioButton_white.isChecked():
                                    if windows.Trend_Now == True:
                                        windows.stop_dynamic_background()
                                    windows.should_draw = "White"  #清空背景图片
                                    style = "color: black;"
                                    windows.setStyleSheet(style)
                                    # 读取 JSON 文件
                                    with open('config.json', 'r') as file:
                                        config = json.load(file)
                                    config["Theme"] = "White"
                                    # 将更新后的数据写入 JSON 文件
                                    with open('config.json', 'w') as file:
                                        json.dump(config, file, indent=4)
                                    Theme = "White"
                                if (self.checkBox_start.isChecked()) and (self.First == False):
                                    try:
                                        exe_file_name = 'Fuchen.exe'
                                        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                                                      'Start Menu', 'Programs', 'Startup')
                                        bat_file_path = os.path.join(startup_folder, 'Fuchen_Start_File.bat')

                                        with open(bat_file_path, 'w') as file:
                                            file.write(f'cd /d {os.path.dirname(os.path.abspath(__file__))}\n')
                                            file.write(f'start {exe_file_name}')

                                        print(f'成功创建并写入.bat文件到启动文件夹: {bat_file_path}')
                                        self.First = True
                                    except Exception as e:
                                        pyautogui.confirm(e)
                                elif (self.checkBox_start.isChecked() == False) and (self.First == True):
                                    try:
                                        # 要移除的文件名
                                        file_name = 'Fuchen_Start_File.bat'
                                        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                                                      'Start Menu', 'Programs', 'Startup')
                                        file_path = os.path.join(startup_folder, file_name)

                                        if os.path.exists(file_path):
                                            os.remove(file_path)
                                            print(f'{file_name} 已从启动文件夹中移除')
                                        else:
                                            print(f'{file_name} 不存在于启动文件夹中')
                                        self.First = False
                                    except Exception as e:
                                        pyautogui.confirm(e)
                                if self.radioButton_custom.isChecked():
                                    try:
                                        if windows.Trend_Now == True:
                                            windows.stop_dynamic_background()
                                        file_name = self.line_Custom.text()
                                        with open('config.json', 'r') as file:
                                            config = json.load(file)
                                        if config["Theme"][
                                           7:] != file_name:  # 这个判断是为了防止目前的背景和选择的背景相同而设置 因此当选择的文件和现有设置的文件相同时 将不会执行
                                            if file_name != '':
                                                windows.should_draw = "Custom"
                                                # 读取 JSON 文件
                                                with open('config.json', 'r') as file:
                                                    config = json.load(file)
                                                config["Theme"] = f"Custom:{file_name}"
                                                # 将更新后的数据写入 JSON 文件
                                                with open('config.json', 'w') as file:
                                                    json.dump(config, file, indent=4)
                                                im = Image.open(file_name)
                                                reim = im.resize((1000, 600))  # 宽*高

                                                reim.save('./temp/background_custom.png',
                                                          dpi=(400, 400))  ##200.0,200.0分别为想要设定的dpi值

                                                palette = QPalette()
                                                palette.setBrush(QPalette.Background,
                                                                 QBrush(QPixmap('./temp/background_custom.png')))
                                                windows.setPalette(palette)
                                                Theme = "Custom"
                                            else:
                                                n = False
                                                pyautogui.confirm("请选择文件!")
                                    except Exception as e:
                                        print(e)
                                if self.radioButton_trend.isChecked():
                                    file_name_V = self.line_Trend.text()
                                    with open('config.json', 'r') as file:
                                        config = json.load(file)
                                    if config["Theme"][6:] != file_name_V:
                                        if file_name_V != '':
                                            windows.should_draw = "Trend"
                                            # 读取 JSON 文件
                                            with open('config.json', 'r') as file:
                                                config = json.load(file)
                                            config["Theme"] = f"Trend:{file_name_V}"
                                            # 将更新后的数据写入 JSON 文件
                                            with open('config.json', 'w') as file:
                                                json.dump(config, file, indent=4)
                                            if windows.Trend_Status == False:
                                                windows.execute_trend(file_name_V)
                                                resul = windows.show_message_box("提示",
                                                                                 "设置成功！需要重启软件即可生效 点击确认按钮即可重新启动")
                                                if resul == "OK":
                                                    subprocess.Popen(["Fuchen.exe"])
                                                try:
                                                    global ab
                                                    ab.kill()
                                                except:
                                                    pass
                                                os._exit(0)
                                            else:
                                                windows.execute_trend_again(file_name_V)
                                            Theme = "Trend"
                                if self.checkBox_5.isChecked() and window_s == False:
                                    windows.open_floating_window()
                                    window_s = True
                                elif self.checkBox_5.isChecked() == False and window_s == True:
                                    print("关闭窗口")
                                    windows.close_floating_window()
                                    print("窗口关闭成功!")

                                if n == True:
                                    pyautogui.confirm("设置成功!")

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

                            def mousePressEvent(self, event):
                                global_pos = event.globalPos()
                                if event.button() == Qt.LeftButton and \
                                        global_pos.y() < self.frameGeometry().top() + self.title_bar_height():
                                    self.__mouse_press_pos = event.pos()
                                    self.__window_pos = self.pos()

                            def mouseMoveEvent(self, event):
                                if event.buttons() == Qt.LeftButton and \
                                        event.globalPos().y() < self.frameGeometry().top() + self.title_bar_height():
                                    self.move(event.globalPos() - self.__mouse_press_pos)

                            def title_bar_height(self):
                                return self.style().pixelMetric(QStyle.PM_TitleBarHeight)

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

                                self._5label_2 = QLabel(self)
                                self._5label_2.setGeometry(QRect(0, 0, 300, 100))
                                font = QFont()
                                font.setFamily("Arial")
                                font.setPointSize(26)
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
                                self.remaining_time_label.setGeometry(QRect(0, 60, 300, 50))
                                font = QFont()
                                font.setFamily("Arial")
                                font.setPointSize(11)
                                self.remaining_time_label.setFont(font)
                                self.remaining_time_label.setObjectName("remaining_time_label")
                                self.remaining_time_label.setText("窗口将在 5 秒后自动关闭")

                                # 创建计时器，10秒后自动关闭窗口
                                self.timer = QTimer(self)
                                self.timer.timeout.connect(self.updateRemainingTime)
                                self.timer.start(1000)  # 1000毫秒 = 1秒

                            def showEvent(self, event):
                                self.animation.start()

                            def updateRemainingTime(self):
                                current_text = self.remaining_time_label.text()
                                current_time = int(current_text.split(" ")[-2])
                                if current_time == 1:
                                    self.close()
                                else:
                                    new_time = current_time - 1
                                    self.remaining_time_label.setText(f"窗口将在 {new_time} 秒后自动关闭")

                        class UserInfo(QWidget):
                            global exp, lv, Lv, Max_exp, Name
                            if lv == 1:
                                Lv = "Lv1"
                                Max_exp = 300
                            elif lv == 2:
                                Lv = "Lv2"
                                Max_exp = 600
                            elif lv == 3:
                                Lv = "Lv3"
                                Max_exp = 1000
                            elif lv == 4:
                                Lv = "Lv4"
                                Max_exp = 9999

                            def __init__(self):
                                super().__init__()
                                window_position = windows.pos()
                                x = window_position.x() + 260
                                y = window_position.y() + 10
                                icon = QIcon("./image/Component/提示.png")
                                self.setWindowIcon(icon)
                                self.setGeometry(x, y, 380, 210)
                                self.setFixedSize(380, 210)
                                self.setWindowTitle("个人信息")
                                self.border_width = 8
                                self.setAttribute(Qt.WA_TranslucentBackground)
                                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 设置 窗口无边框和背景透明

                                self.exp_label = QtWidgets.QLabel(self)
                                self.exp_label.setGeometry(QtCore.QRect(20, 190, 110, 3))
                                self.exp_label.setStyleSheet("background-color: gray;")  # 设置标签的背景颜色为灰色

                                self.proccess = int(exp) / Max_exp * 100
                                if self.proccess > 100:
                                    self.proccess = 100

                                self.exp_label2 = QtWidgets.QLabel(self)
                                self.exp_label2.setGeometry(
                                    QtCore.QRect(20, 190, int(self.proccess), 3))
                                self.exp_label2.setStyleSheet("background-color: blue;")  # 设置标签的背景颜色为蓝色

                                self.exp_label3 = QtWidgets.QLabel(self)
                                self.exp_label3.setGeometry(QtCore.QRect(20, 170, 100, 20))  # 设置标签的位置和大小
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(13)
                                self.exp_label3.setFont(font)
                                if lv == 4:
                                    color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
                                    self.exp_label3.setStyleSheet(f"color: red;")  # 设置字体颜色
                                self.exp_label3.setText(Lv)

                                self.exp_label4 = QtWidgets.QLabel(self)

                                self.exp_label4.setGeometry(QtCore.QRect(90, 173, 50, 20))  # 设置标签的位置和大小
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(9)
                                self.exp_label4.setFont(font)
                                self.exp_label4.setText(f"{exp}/{Max_exp}")

                                self.Button = QtWidgets.QToolButton(self)
                                self.Button.setGeometry(QtCore.QRect(20, 20, 100, 100))
                                self.Button.setIcon(QIcon("./temp/HImage.png"))
                                self.Button.setIconSize(QSize(100, 100))
                                self.Button.setObjectName("Button")
                                self.Button.setStyleSheet(
                                    "QToolButton { background: transparent; padding: 0;border: none; }")

                                self.pushButton_2 = QtWidgets.QPushButton(self)
                                self.pushButton_2.setGeometry(QtCore.QRect(340, 15, 26, 26))
                                self.pushButton_2.setObjectName("pushButton_2")
                                self.pushButton_2.setStyleSheet("QPushButton#pushButton_2 {"
                                                                "    border-image: url(./image/quit.png);"
                                                                "    background-color: rgb(255, 255, 255)"
                                                                "}")
                                self.pushButton_2.setToolTip("关闭")
                                self.pushButton_2.clicked.connect(self.quit)

                                self.label = QtWidgets.QLabel(self)  # 名字标签
                                self.label.setGeometry(QtCore.QRect(140, 20, 180, 41))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self.label.setFont(font)
                                self.label.setObjectName("label")
                                self.label.setText(f"{Name}")

                                self.label_2 = QtWidgets.QLabel(self)  # 账号ID标签
                                self.label_2.setGeometry(QtCore.QRect(140, 60, 71, 16))
                                self.label_2.setObjectName("label_2")
                                self.label_2.setText(f"ID:{Account}")

                                self.toolButton = QtWidgets.QToolButton(self)  # 上传头像按钮
                                self.toolButton.setGeometry(QtCore.QRect(20, 137, 101, 21))
                                self.toolButton.setObjectName("toolButton")
                                self.toolButton.setText("上传头像")
                                self.toolButton.clicked.connect(self.renew_HImage)
                                self.toolButton.setStyleSheet("QToolButton#toolButton {"
                                                              "background-color: #3498db;"  # Blue background color
                                                              "border-radius: 5px;"  # 10px border radius for rounded corners
                                                              "color: white;"
                                                              "padding: 100px 100px;"
                                                              "text-align: center;"
                                                              "text-decoration: none;"
                                                              "font-size: 13px;"
                                                              "font-family: SimSun, Arial, sans-serif;"
                                                              "}")

                                style = """
                                                                                                        QToolButton {
                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                        }
                                                                                                        QToolButton:hover {
                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                        }
                                                                                                    """

                                self.toolButton_2 = QtWidgets.QToolButton(self)  # 编辑资料按钮
                                self.toolButton_2.setGeometry(QtCore.QRect(140, 80, 90, 19))
                                self.toolButton_2.setObjectName("toolButton_2")
                                self.toolButton_2.setText("修改名称")
                                self.toolButton_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.toolButton_2.clicked.connect(lambda: self.show_control('name_open'))
                                self.toolButton_2.setStyleSheet(style)

                                self.toolButton_password = QtWidgets.QToolButton(self)  # 编辑资料按钮
                                self.toolButton_password.setGeometry(QtCore.QRect(240, 80, 90, 19))
                                self.toolButton_password.setObjectName("toolButton_password")
                                self.toolButton_password.setText("修改密码")
                                self.toolButton_password.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.toolButton_password.clicked.connect(lambda: self.show_control('password_open'))
                                self.toolButton_password.setStyleSheet(style)

                                self.toolButton_3 = QtWidgets.QToolButton(self)  # 编辑资料按钮
                                self.toolButton_3.setGeometry(QtCore.QRect(140, 80, 90, 19))
                                self.toolButton_3.setObjectName("toolButton_3")
                                self.toolButton_3.setText("完成编辑")
                                self.toolButton_3.setStyleSheet(style)
                                self.toolButton_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.toolButton_3.setVisible(False)
                                self.toolButton_3.clicked.connect(lambda: self.ReEdit("name"))

                                self.toolButton_pass = QtWidgets.QToolButton(self)  # 编辑资料按钮
                                self.toolButton_pass.setGeometry(QtCore.QRect(240, 80, 90, 19))
                                self.toolButton_pass.setObjectName("toolButton_pass")
                                self.toolButton_pass.setText("完成编辑")
                                self.toolButton_pass.setStyleSheet(style)
                                self.toolButton_pass.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.toolButton_pass.setVisible(False)
                                self.toolButton_pass.clicked.connect(lambda: self.ReEdit("password"))

                                self.label_4 = QtWidgets.QLabel(self)  # 名称标签
                                self.label_4.setGeometry(QtCore.QRect(140, 100, 54, 18))
                                self.label_4.setObjectName("label_4")
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(11)
                                self.label_4.setFont(font)
                                self.label_4.setText("名称:")
                                self.label_4.setVisible(False)

                                self.lineEdit_2 = QtWidgets.QLineEdit(self)  # 名称修改行
                                self.lineEdit_2.setGeometry(QtCore.QRect(140, 120, 221, 25))
                                self.lineEdit_2.setObjectName("lineEdit_2")
                                self.lineEdit_2.setPlaceholderText("请输入需要修改的名称")

                                self.lineEdit_2.setFont(font)
                                self.lineEdit_2.setStyleSheet("QLineEdit {border: 1px solid gray; border-radius: 2px;}")
                                self.lineEdit_2.setVisible(False)

                                self.label_5 = QtWidgets.QLabel(self)  # 密码标签
                                self.label_5.setGeometry(QtCore.QRect(140, 100, 54, 18))
                                self.label_5.setObjectName("label_5")
                                self.label_5.setFont(font)
                                self.label_5.setText("密码:")
                                self.label_5.setVisible(False)

                                self.lineEdit_3 = QtWidgets.QLineEdit(self)  # 密码修改行
                                self.lineEdit_3.setGeometry(QtCore.QRect(140, 120, 221, 25))
                                self.lineEdit_3.setObjectName("lineEdit_3")
                                self.lineEdit_3.setPlaceholderText("请输入需要修改的密码")
                                self.lineEdit_3.setFont(font)
                                self.lineEdit_3.setStyleSheet("QLineEdit {border: 1px solid gray; border-radius: 2px;}")
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
                                        if not (1< len(ReName) < 11):
                                            self.show_message_box("提示", "名称只能为2-10位")
                                        elif Check(ReName) == True:
                                            self.show_message_box("提示",
                                                                  "名称只能包含中文,26个英文大小写字母,数字以及 - . ? ~ _")
                                        else:
                                            send_encry(f'10006 {ReName}')
                                            Name = ReName
                                            windows.HButton.setText(f"{Name}")
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
                                            send_encry(f'10007 {RePassword}')
                                            self.show_message_box("提示", "密码修改成功")
                                            self.close()

                            def quit(self):
                                self.close()

                            def renew_HImage(self):
                                print(HImage_date)
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
                                            send_encry('10005')

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
                                            '''with open('./temp/HImage.png', "rb") as f:
                                                while True:
                                                    chunk = f.read(2048)
                                                    if not chunk:
                                                        break
                                                    s.sendall(chunk)'''
                                            #上传头像 因为不知道为什么需要客户端与服务端断开连接才能成功保存文件 所以需要重启客户端
                                            self.Button.setIcon(QIcon("./temp/HImage.png"))
                                            self.Button.setIconSize(QSize(100, 100))
                                            resul = windows.show_message_box("提示",
                                                                     "头像上传成功!\n需要重启客户端才能完全上传头像\n点击确认按钮或关闭此窗口重启客户端")
                                            print(resul)
                                            cb = subprocess.Popen(["Fuchen.exe"])
                                            try:
                                                global ab
                                                ab.kill()
                                            except:
                                                pass
                                            os._exit(0)
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

                        class Help(QWidget):
                            def __init__(self):
                                super().__init__()
                                icon = QIcon("./image/Component/提示.png")
                                self.setWindowIcon(icon)
                                self.setFixedSize(450,400)
                                self.setWindowTitle("赞助作者")

                                self.label_WEIXIN = QtWidgets.QLabel(self)
                                self.label_WEIXIN.setGeometry(QtCore.QRect(0, 100, 220, 300))
                                pixmap_2 = QtGui.QPixmap('./temp/WEIXIN.png')
                                self.label_WEIXIN.setPixmap(pixmap_2)
                                self.label_WEIXIN.setScaledContents(True)

                                self.label_ZHIFU = QtWidgets.QLabel(self)
                                self.label_ZHIFU.setGeometry(QtCore.QRect(220, 100, 230, 300))
                                pixmap_2 = QtGui.QPixmap('./temp/ZHIFU.jpg')
                                self.label_ZHIFU.setPixmap(pixmap_2)
                                self.label_ZHIFU.setScaledContents(True)

                                self.label_title = QtWidgets.QLabel(self)
                                self.label_title.setGeometry(QtCore.QRect(10, 10, 450, 21))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(16)
                                self.label_title.setFont(font)
                                self.label_title.setObjectName("label_title")
                                self.label_title.setText("感谢您的赞助！不论数额大小都对我非常重要")

                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)

                                self.label = QtWidgets.QLabel(self)
                                self.label.setGeometry(QtCore.QRect(10, 40, 431, 45))
                                self.label.setObjectName("label")
                                self.label.setText("请您在支付时备注好您的名称(网名) 以便于赞助人员名单展示\n"
                                    "本软件免费安全无广告 不收费 大家如果觉得用的好的话就自愿进行赞助\n感谢您对开放者的帮助！")
                                self.label.setFont(font)

                        class View(QWidget):
                            def __init__(self):
                                super().__init__()
                                icon = QIcon("./image/Component/提示.png")
                                self.setWindowTitle("意见反馈")
                                self.setWindowIcon(icon)
                                self.setFixedSize(400, 280)
                                self.label = QtWidgets.QLabel(self)
                                self.label.setGeometry(QtCore.QRect(10, 10, 91, 20))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(14)
                                self.label.setFont(font)
                                self.label.setObjectName("label")
                                self.lineEdit = QtWidgets.QLineEdit(self)
                                self.lineEdit.setGeometry(QtCore.QRect(10, 40, 211, 20))
                                self.lineEdit.setObjectName("lineEdit")
                                self.label_2 = QtWidgets.QLabel(self)
                                self.label_2.setGeometry(QtCore.QRect(10, 70, 121, 16))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(14)
                                self.label_2.setFont(font)
                                self.label_2.setObjectName("label_2")
                                self.textEdit = QtWidgets.QTextEdit(self)
                                self.textEdit.setGeometry(QtCore.QRect(10, 90, 380, 180))
                                self.textEdit.setObjectName("textEdit")
                                self.toolButton = QtWidgets.QToolButton(self)
                                self.toolButton.setGeometry(QtCore.QRect(320, 250, 71, 21))
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
                                    send_encry(contents)
                                    QMessageBox.question(self, "提示", "反馈成功!\n感谢您的建议")
                                    self.close()

                        class Control(QWidget):
                            def __init__(self):
                                super().__init__()
                                self.resize(370, 270)
                                self.setFixedSize(370, 270)
                                self.textBrowser = QtWidgets.QTextBrowser(self)
                                self.textBrowser.setGeometry(QtCore.QRect(0, 0, 370, 250))
                                self.textBrowser.setObjectName("textBrowser")
                                global sys_list
                                for i in sys_list:
                                    if i[0] == 'b':
                                        self.textBrowser.append("<font color='blue'>" + str(i)[1:] + "<font>")
                                    elif i[0] == 'g':
                                        self.textBrowser.append("<font color='green'>" + str(i)[1:] + "<font>")
                                    elif i[0] == 'r':
                                        self.textBrowser.append("<font color='red'>" + str(i)[1:] + "<font>")

                                # Input Field
                                self.inputField = QtWidgets.QLineEdit(self)
                                self.inputField.setGeometry(
                                    QtCore.QRect(0, 250, 280, 20))  # Adjust the position and size
                                self.inputField.setObjectName("inputField")
                                self.inputField.returnPressed.connect(self.send)

                                # Button
                                self.addButton = QtWidgets.QPushButton(self)
                                self.addButton.setGeometry(
                                    QtCore.QRect(280, 250, 90, 20))  # Adjust the position and size
                                self.addButton.setObjectName("addButton")
                                self.addButton.setText("确认")
                                self.addButton.clicked.connect(self.send)

                            def send(self):
                                global sys_list, current_time_string, exp_status
                                content = self.inputField.text()
                                sys_list.append('b' + current_time_string + self.inputField.text())
                                self.textBrowser.append(
                                    "<font color='blue'>" + current_time_string + content + "<font>")
                                self.inputField.setText("")
                                if content == '签到':
                                    send_encry('30001')
                                    time.sleep(2)
                                    if exp_status == True:
                                        self.textBrowser.append(
                                            "<font color='blue'>" + current_time_string + '恭喜您 签到成功' + "<font>")
                                        sys_list.append('b' + current_time_string + '恭喜您 签到成功')
                                    elif exp_status == False:
                                        self.textBrowser.append(
                                            "<font color='green'>" + current_time_string + '今日已签到 请每日再来~' + "<font>")
                                        sys_list.append('g' + current_time_string + '今日已签到 请每日再来~')
                                elif content == 'XFBSOMDFLS':
                                    send_encry("30002 xfbsomdfls")
                                    time.sleep(2)
                                    if exp_status == 'Yes':
                                        self.textBrowser.append(
                                            "<font color='red'>" + current_time_string + '内部激活:1000经验添加成功' + "<font>")
                                        sys_list.append('r' + current_time_string + '内部激活:1000经验添加成功')
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

                        class Quit_Prompt(QtWidgets.QDialog):
                            def __init__(self):
                                super().__init__()

                                self.setWindowTitle("关闭提示窗口")
                                self.resize(300, 200)
                                self.setWindowFlags(
                                    self.windowFlags() | Qt.WindowStaysOnTopHint)
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
                                self.group1.addButton(self.exit_radio)

                                self.minimize_radio = QtWidgets.QRadioButton("最小化到系统托盘", self)
                                self.minimize_radio.setGeometry(20, 90, 150, 20)
                                self.group1.addButton(self.minimize_radio)

                                # 单选按钮2
                                self.no_prompt_radio = QtWidgets.QRadioButton("下次不再提示", self)
                                self.no_prompt_radio.setGeometry(20, 130, 150, 20)

                                # 确认按钮
                                self.confirm_button = QtWidgets.QPushButton("确认", self)
                                self.confirm_button.setGeometry(20, 150, 80, 30)
                                self.confirm_button.clicked.connect(self.on_confirm_button_clicked)

                            def on_confirm_button_clicked(self):
                                global window_icon
                                global ab
                                if self.exit_radio.isChecked():
                                    result = "Quit"
                                elif self.minimize_radio.isChecked():
                                    result = "Hide"
                                else:
                                    result = "未选择"

                                no_prompt_checked = self.no_prompt_radio.isChecked()  # 是否下次不再提示

                                if (result == "Quit") and (no_prompt_checked == True):  #下次不再提示  直接关闭
                                    with open(f"config.json", "r") as file:
                                        U_data = json.load(file)
                                    U_data["ClosePrompt"] = False
                                    U_data["CloseExecute"] = "Close"
                                    # 写入JSON文件
                                    with open(f"config.json", "w") as file:
                                        json.dump(U_data, file, indent=4)
                                    self.close()
                                    time.sleep(0.1)
                                    windows.close_MainWindow()
                                elif result == 'Quit':  #下次提示 关闭
                                    self.close()
                                    time.sleep(0.1)
                                    windows.close_MainWindow()
                                elif (result == "Hide") and (no_prompt_checked == True):  #下次不再提示
                                    with open(f"config.json", "r") as file:
                                        U_data = json.load(file)
                                    U_data["ClosePrompt"] = False
                                    U_data["CloseExecute"] = "Hide"
                                    # 写入JSON文件
                                    with open(f"config.json", "w") as file:
                                        json.dump(U_data, file, indent=4)
                                    self.close()
                                    Hide()
                                elif result == "Hide":  #直接隐藏
                                    self.close()
                                    Hide()

                        class Ui_Form(QtWidgets.QMainWindow):
                            def __init__(self):
                                super(Ui_Form, self).__init__()
                                self.sort = "F9"
                                self.end_key = "ESC"
                                if Theme == "White":
                                    self.should_draw = "White"
                                elif Theme == "Custom":
                                    self.should_draw = "Custom"
                                elif Theme == "Trend":
                                    self.should_draw = "Trend"
                                else:
                                    self.should_draw = "White"
                                self.setupUi(self)
                                self.pushButton_15.clicked.connect(self.showMinimized)  # 最小化按钮
                                self.pushButton_16.clicked.connect(self.clo)  # 退出按钮
                                self.pushButton_17.setMenu(self.menu)
                                self.pushButton_18.clicked.connect(self.upwindow)
                                self.action_option1.triggered.connect(self.open_set_window)  # 设置按钮
                                self.action_option2.triggered.connect(self.about)
                                self.action_option3.triggered.connect(self.open_help_window)
                                self.action_option4.triggered.connect(self.LogRecord)
                                self.action_option5.triggered.connect(self.open_website)
                                self.action_option6.triggered.connect(self.open_view_window)
                                self.action_option7.triggered.connect(self.empyt_log)
                                self.action_option8.triggered.connect(self.clear_temp)
                                self.action_option9.triggered.connect(self.restart_app)
                                self.HButton.clicked.connect(self.open_user_window)

                                self._2pushButton.clicked.connect(self.Send_QQ)  # page2(QQ)页面 绑定
                                #self._2pushButton2.clicked.connect(self.gain_handle)
                                #self._2pushButton_3.clicked.connect(self.Handle_Send)  # 句柄式发送消息
                                self.pushButton_tooltip_handle.clicked.connect(lambda: self.onPushButtonClicked("handle"))  #句柄消息提示
                                self.pushButton_tooltip_qq.clicked.connect(lambda: self.onPushButtonClicked("qq"))  # qq消息提示
                                self.pushButton_tooltip_copy.clicked.connect(lambda: self.onPushButtonClicked("copy"))  # 复制消息提示
                                self._2pushButton_4.clicked.connect(self.Send_Copy)  # 复制内容
                                #self._2pushButton_5.clicked.connect(self.Send_Quick)  # 发送快捷消息

                                #self._3pushButton.clicked.connect(lambda: MyThread(self.Click_Record))  # 记录自动脚本
                                #self._3pushButton_2.clicked.connect(lambda: MyThread(self.Click_Record_execute))  # 执行自动脚本
                                self._3pushButton.clicked.connect(self.Click_Record)  # 记录自动脚本
                                self._3pushButton_2.clicked.connect(self.Click_Record_execute)
                                self._3pushButton_4.setMenu(self.createMenu())
                                self.end_key_button.setMenu(self.create_key_Menu())
                                self._3pushButton_5.clicked.connect(self.mouseinfo)
                                self._3pushButton_6.clicked.connect(lambda: MyThread(self.new_click))
                                self._3pushButton_7.clicked.connect(lambda: MyThread(self.break_click))
                                self.button_create.clicked.connect(self.create_file)
                                self.impor_button.clicked.connect(self.open_fileedit_window)
                                #self.save_button.clicked.connect(self.save_file)
                                #self.save_button.clicked.connect(self.run_command)
                                self.reflash.clicked.connect(lambda: self.populateMenu('scripts'))
                                self.delete_button.clicked.connect(self.delete_file)

                                self.create_team_button.clicked.connect(self.team)  # 创建队伍
                                self.button_copy_id.clicked.connect(self.copy)  # 复制id
                                self.add_team_button.clicked.connect(self.jointeam)
                                self.run_execute.clicked.connect(self.team_c)  # 开始执行

                                self._5toolButton.clicked.connect(self.download)
                                self._5toolButton2.clicked.connect(lambda: self.show_folder_dialog(1))
                                self.view_music.clicked.connect(lambda: self.open_folder('music'))
                                self._5toolButton3.clicked.connect(lambda: self.show_folder_dialog(2))
                                self._5toolButton4.clicked.connect(lambda: self.show_folder_dialog(3))
                                self.QQ_Group_View.clicked.connect(lambda: self.open_folder('xlsx'))
                                self.QQ_Group_Selec.clicked.connect(lambda: self.show_folder_dialog(4))
                                self._5toolButton5.clicked.connect(self.mixPicture)

                                self.open_window_hotkey = QShortcut(QKeySequence("Ctrl+o"), self)
                                self.open_window_hotkey.activated.connect(self.open_ctrl_window)
                                self.QQ_Button_Dow.clicked.connect(lambda: MyThread(self.download_image))
                                self.QQ_image.clicked.connect(self.QQ_image_update)
                                self.delete_image.clicked.connect(self.delete_images)
                                self.QQ_group.clicked.connect(lambda: MyThread(self.QQ_Group_information))

                                self.Button_1.clicked.connect(self.bt_c1)
                                self.Button_2.clicked.connect(self.bt_c2)
                                self.Button_3.clicked.connect(self.bt_c3)
                                self.Button_4.clicked.connect(self.bt_c4)

                            def setupUi(self, MainWindow):
                                MainWindow.setObjectName("MainWindow")
                                MainWindow.resize(1000, 600)
                                MainWindow.setFixedSize(1000, 600)
                                screen = QDesktopWidget().screenGeometry()
                                window = self.geometry()

                                # 计算窗口居中时的位置
                                x = (screen.width() - window.width()) // 2
                                y = (screen.height() - window.height()) // 2

                                # 设置窗口位置
                                self.move(x, y)
                                self.is_topmost = False
                                self.border_width = 8

                                MainWindow.setWindowFlags(Qt.FramelessWindowHint)
                                MainWindow.setWindowTitle("Fuchen--Made by Fuchen")

                                self.Trend_Status = False
                                self.Trend_Now = False
                                if Theme == "Custom":  # 自定义图片背景设置
                                    global Path_Custom_S
                                    im = Image.open(Path_Custom_S)
                                    reim = im.resize((1000, 600))  # 宽*高
                                    reim.save('./temp/background_custom.png',
                                              dpi=(200.0, 200.0))  ##200.0,200.0分别为想要设定的dpi值
                                    palette = QPalette()
                                    palette.setBrush(QPalette.Background,
                                                     QBrush(QPixmap('./temp/background_custom.png')))
                                    self.setPalette(palette)
                                    self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
                                    del Path_Custom_S
                                elif Theme == "Trend":  #
                                    global Path_Trend_S
                                    self.execute_trend(Path_Trend_S)

                                icon = QIcon("./image/window.ico")  #设置窗口图标
                                self.setWindowIcon(icon)

                                self.weather_button = QtWidgets.QToolButton(self)  # 天气按钮(图标)
                                self.weather_button.setObjectName("weather_button")
                                self.weather_button.setGeometry(QtCore.QRect(5, 580, 80, 20))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(8)
                                self.weather_button.setFont(font)
                                self.weather_button.setText(f"正在获取天气")
                                self.weather_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.weather_button.setStyleSheet(
                                    "background-color: rgba(255,255,255,0); padding: 0;border: none; ")

                                self.weather_first = QtCore.QTimer(self)
                                self.weather_first.timeout.connect(lambda: MyThread(lambda: self.Update_weather('first')))
                                self.weather_first.start()  # 更新时间的间隔，单位为毫秒

                                self.weather_timer = QtCore.QTimer(self)
                                self.weather_timer.timeout.connect(lambda: self.Update_weather('normal'))
                                self.weather_timer.start(1200000)  # 更新时间的间隔，单位为毫秒

                                self.version_label = QtWidgets.QLabel(self)
                                self.version_label.setGeometry(QtCore.QRect(10, 500, 100, 20))
                                self.version_label.setFont(font)
                                self.version_label.setObjectName("version_label")
                                self.version_label.setText(f"{Version}")

                                self.run_label = QtWidgets.QLabel("运行时间 00:00:00", self)
                                self.run_label.setFont(font)
                                self.run_label.setGeometry(QtCore.QRect(10, 520, 200, 20))
                                self.run_timer = QtCore.QTimer(self)
                                self.run_timer.timeout.connect(self.updateTime)
                                self.startTime = QtCore.QTime.currentTime()
                                self.run_timer.start(1000)  # 每秒更新一次

                                self.time_label = QtWidgets.QLabel(self)
                                self.time_label.setGeometry(QtCore.QRect(10, 540, 100, 20))
                                self.time_label.setFont(font)
                                self.time_label.setText("当前时间 00:00:00")

                                self.timer = QtCore.QTimer(self)
                                self.timer.timeout.connect(self.update_time)
                                self.timer.start(1000)  # 更新时间的间隔，单位为毫秒

                                self.global_timer = QtCore.QTimer(self)
                                self.global_timer.timeout.connect(self.get_current_time_string)
                                self.global_timer.start(1000)  # 更新时间的间隔，单位为毫秒

                                '''self.data_thread = DataThread()
                                self.data_thread.start()'''
                                self.data_thread = DataThread()
                                self.data_thread.start()

                                self.status_label = QtWidgets.QLabel(self)
                                self.status_label.setGeometry(QtCore.QRect(10, 560, 70, 20))
                                self.status_label.setFont(font)
                                self.status_label.setText("与服务器状态:")

                                self.serve_label = QtWidgets.QLabel(self)
                                self.serve_label.setGeometry(QtCore.QRect(80, 560, 50, 20))
                                self.serve_label.setFont(font)
                                color = QtGui.QColor(36, 152, 42)  # 使用RGB值设置颜色为红色
                                self.serve_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                                self.serve_label.setText("已连接")

                                self.HButton = QtWidgets.QToolButton(self)
                                self.HButton.setGeometry(QtCore.QRect(10, 20, 240, 90))
                                self.HButton.setIcon(QIcon("./temp/HImage.png"))
                                font = QtGui.QFont()
                                font.setPointSize(14)
                                self.HButton.setFont(font)
                                self.HButton.setText(f" {Name}")
                                self.HButton.setIconSize(QSize(80, 80))
                                self.HButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                self.HButton.setObjectName("HButton")
                                self.HButton.setStyleSheet(
                                    "QToolButton { background: transparent; padding: 0;border: none; }")
                                self.HButton.setCursor(QCursor(Qt.PointingHandCursor))
                                if mode == "tourist_login":
                                    self.HButton.setEnabled(False)
                                    self.HButton.setToolTip("游客登录无法编辑个人资料\n登录后可编辑")

                                self.Button_Style = '''
                                            QToolButton {
                                                background: transparent;
                                                padding: 0; /* Add this line */
                                                border: none;
                                            }
                                            QToolButton:hover {
                                                border-radius: 5px;
                                                
                                                border-style: outset;
                                                background-color: rgb(204,229,255);
                                                border-color: rgb(204, 229, 255);
                                            }
                                        '''

                                self.Now_Button_Style = '''
                                                        QToolButton {
                                                            background: transparent;
                                                            border-radius: 5px;
                                                            border-style: outset;
                                                            background-color: rgb(96,160,235); /* 修改为选中后的颜色 */
                                                            border-color: rgb(96,160,235); 
                                                            padding: 0;
                                                        }
                                                        
                                                    '''

                                '''第一个按钮'''
                                self.Button_1 = QtWidgets.QToolButton(self)
                                self.Button_1.setGeometry(QtCore.QRect(10, 130, 240, 40))
                                self.Button_1.setIcon(QIcon("./image/Component/点击.png"))
                                self.Button_1.setObjectName("Button_1")
                                self.Button_1.setText("    连点功能")
                                self.Button_1.setIconSize(QSize(30, 30))
                                self.Button_1.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                # 设置按钮样式
                                self.Button_1.setStyleSheet(self.Now_Button_Style)
                                '''第二个按钮'''
                                self.Button_2 = QtWidgets.QToolButton(self)
                                self.Button_2.setGeometry(QtCore.QRect(10, 190, 240, 40))
                                self.Button_2.setIcon(QIcon("./image/Component/QQ.png"))
                                self.Button_2.setObjectName("Button_2")
                                self.Button_2.setText("    QQ消息")
                                self.Button_2.setIconSize(QSize(30, 30))
                                self.Button_2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                # 设置按钮样式
                                self.Button_2.setStyleSheet(self.Button_Style)

                                self.Button_3 = QtWidgets.QToolButton(self)
                                self.Button_3.setGeometry(QtCore.QRect(10, 250, 240, 40))
                                self.Button_3.setIcon(QIcon("./image/Component/组队.png"))
                                self.Button_3.setObjectName("Button_3")
                                self.Button_3.setText("    组队")
                                self.Button_3.setIconSize(QSize(30, 30))
                                self.Button_3.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                # 设置按钮样式
                                self.Button_3.setStyleSheet(self.Button_Style)
                                self.Button_3.setEnabled(False)
                                self.Button_3.setToolTip("开源版无网络连接  该功能无法使用")
                                if mode == "tourist_login":
                                    self.Button_3.setEnabled(False)
                                    self.Button_3.setToolTip("该功能游客登录暂不可用")

                                self.Button_4 = QtWidgets.QToolButton(self)
                                self.Button_4.setGeometry(QtCore.QRect(10, 310, 240, 40))
                                self.Button_4.setIcon(QIcon("./image/Component/工具.png"))
                                self.Button_4.setObjectName("Button_4")
                                self.Button_4.setText("    工具")
                                self.Button_4.setIconSize(QSize(30, 30))
                                self.Button_4.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
                                # 设置按钮样式
                                self.Button_4.setStyleSheet(self.Button_Style)
                                """右侧总框架"""
                                self.stackedWidget = QtWidgets.QStackedWidget(MainWindow)
                                self.stackedWidget.setGeometry(QtCore.QRect(260, 0, 740, 600))
                                self.stackedWidget.setObjectName("stackedWidget")

                                self.textBrowser = QtWidgets.QTextBrowser(self)
                                self.textBrowser.setGeometry(QtCore.QRect(10, 370, 240, 90))
                                self.textBrowser.setObjectName("textBrowser")
                                self.textBrowser.setStyleSheet(
                                    'background: transparent; border: 2px solid #ccc; border-radius: 5px; color: black;background-color: rgba(255, 255, 255, 150);')
                                self.textBrowser.verticalScrollBar().setStyleSheet("""
                                QTextBrowser {
                                    background: #C0C0C0;
                                    width: 5px;
                                    margin:0px; 
                                    border: none; 
                                    border-radius: 1px;}
                                QScrollBar:vertical {
                                    border: none;
                                    background: #F5F5F5;
                                    width: 10px;
                                    /* 滚动条宽度 */
                                    border-radius: 5px;
                                    /* 设置滚动条的圆角 */
                                    margin: 0px 0 0px 0;
                                    /* 取消上下按钮时可能需要调整margin来防止空白 */
                                    }

                                QScrollBar::handle:vertical {
                                    background: #E2E2E2;
                                    min-height: 20px;
                                    border-radius: 5px; /* 设置滑块的圆角 */
                                }

                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                    height: 0px; /* 隐藏上下按钮 */
                                    border: none; /* 取消边框 */
                                    background: none; /* 取消背景 */
                                }

                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                    background: none;
                                    }
                                """
                                )
                                font = QFont("等线", 14)
                                self.textBrowser.setFont(font)

                                self.textBrowser.setText("这里是服务器公告")

                                self.pushButton_15 = QtWidgets.QPushButton(self)
                                self.pushButton_15.setGeometry(QtCore.QRect(940, 8, 19, 19))
                                font = QtGui.QFont()
                                font.setPointSize(14)
                                self.pushButton_15.setFont(font)
                                self.pushButton_15.setObjectName("pushButton_15")
                                self.pushButton_15.setStyleSheet("QPushButton#pushButton_15 {"
                                                                 "    border-image: url(./image/short.png);"
                                                                 "    background-color: rgba(245,245,245,0)"
                                                                 "}")
                                self.pushButton_15.setToolTip('最小化')

                                self.pushButton_16 = QtWidgets.QPushButton(self)
                                self.pushButton_16.setGeometry(QtCore.QRect(965, 8, 21, 21))
                                self.pushButton_16.setToolTip('关闭')
                                self.pushButton_16.setObjectName("pushButton_16")
                                self.pushButton_16.setStyleSheet("QPushButton#pushButton_16 {"
                                                                 "    border-image: url(./image/quit.png);"
                                                                 "    background-color: rgba(245,245,245,0)"
                                                                 "}")

                                self.pushButton_18 = QtWidgets.QPushButton(self)
                                self.pushButton_18.setGeometry(QtCore.QRect(915, 8, 21, 21))
                                self.pushButton_18.setToolTip('置顶')
                                self.pushButton_18.setObjectName("pushButton_18")
                                self.pushButton_18.setStyleSheet("QPushButton#pushButton_18 {"
                                                                 "    border-image: url(./image/Component/up.png);"
                                                                 "    background-color: rgba(245,245,245,0)"
                                                                 "}")

                                self.pushButton_17 = QtWidgets.QPushButton(self)
                                self.pushButton_17.setGeometry(QtCore.QRect(890, 8, 24, 21))
                                self.pushButton_17.setToolTip('更多')
                                self.pushButton_17.setObjectName("pushButton_17")
                                self.pushButton_17.setStyleSheet(
                                    "QPushButton#pushButton_17::menu-indicator {"
                                    "    image: none;"
                                    "    width: 20px; height: 20px;"  # Set the size of your custom indicator image
                                    "    border-image: url(./image/更多.png);"
                                    "    subcontrol-position: right center;"
                                    "    subcontrol-origin: padding;"
                                    "    position: absolute; right: 5px;"  # Adjust the position as needed
                                    "}"
                                    "QPushButton#pushButton_17 {"
                                    "    border:none;"
                                    "    background-color: rgba(245, 245, 245,0);"
                                    "}")
                                # 创建一个菜单
                                self.menu = QtWidgets.QMenu(self)
                                self.action_option1 = self.menu.addAction("设置")
                                self.action_option2 = self.menu.addAction("关于")
                                self.action_option3 = self.menu.addAction("赞助")
                                self.action_option4 = self.menu.addAction("日志")
                                self.action_option5 = self.menu.addAction("官网")
                                self.action_option6 = self.menu.addAction("意见反馈")
                                self.action_option7 = self.menu.addAction("清空日志")
                                self.action_option8 = self.menu.addAction("清理缓存")
                                self.action_option9 = self.menu.addAction("重启软件")
                                '''第一页'''
                                self.page_1 = QtWidgets.QWidget()
                                self.page_1.setObjectName("page_1")
                                self.label_page1()
                                self.stackedWidget.addWidget(self.page_1)
                                '''第二页'''
                                self.page_2 = QtWidgets.QWidget()
                                self.page_2.setObjectName("page_2")
                                self.label_page2()
                                self.stackedWidget.addWidget(self.page_2)

                                '''第三页'''
                                self.page_3 = QtWidgets.QWidget()
                                self.page_3.setObjectName("page_3")
                                self.label_page3()
                                self.stackedWidget.addWidget(self.page_3)

                                '''第四页'''
                                self.page_4 = QtWidgets.QWidget()
                                self.page_4.setObjectName("page_4")
                                self.label_page4()
                                self.stackedWidget.addWidget(self.page_4)

                                self.stackedWidget.setCurrentIndex(0)  # 初始界面索引为0

                                custom_widget = CustomWidget(self.page_2)  # QQ发送框
                                custom_widget.setGeometry(QtCore.QRect(0, 0, 510, 270))
                                custom_widget.lower()

                                custom_widget2 = CustomWidget(self.page_2)  # 常见问题框
                                custom_widget2.setGeometry(QtCore.QRect(505, 0, 235, 270))
                                custom_widget2.lower()

                                custom_widget3 = CustomWidget(self.page_2)  # 句柄框
                                custom_widget3.setGeometry(QtCore.QRect(0, 265, 370, 330))
                                custom_widget3.lower()

                                custom_widget4 = CustomWidget(self.page_2)  # 其他工具框
                                custom_widget4.setGeometry(QtCore.QRect(365, 265, 375, 330))
                                custom_widget4.lower()

                                custom_widget5 = CustomWidget(self.page_1)  # 连点框
                                custom_widget5.setGeometry(QtCore.QRect(0, 0, 375, 270))
                                custom_widget5.lower()

                                custom_widget6 = CustomWidget(self.page_1)  # 常见问题
                                custom_widget6.setGeometry(QtCore.QRect(370, 0, 370, 270))
                                custom_widget6.lower()

                                custom_widget7 = CustomWidget(self.page_1)  # 自动脚本框
                                custom_widget7.setGeometry(QtCore.QRect(0, 265, 740, 335))
                                custom_widget7.lower()

                                custom_widget9 = CustomWidget(self.page_3)  # 创建队伍
                                custom_widget9.setGeometry(QtCore.QRect(0, 0, 350, 160))
                                custom_widget9.lower()

                                custom_widget10 = CustomWidget(self.page_3)  # 加入队伍
                                custom_widget10.setGeometry(QtCore.QRect(345, 0, 395, 160))
                                custom_widget10.lower()

                                custom_widget11 = CustomWidget(self.page_3)  # 交互队伍框
                                custom_widget11.setGeometry(QtCore.QRect(0, 155, 740, 445))
                                custom_widget11.lower()

                                custom_widget12 = CustomWidget(self.page_4)  # 网易云音乐下载框
                                custom_widget12.setGeometry(QtCore.QRect(0, 0, 300, 245))
                                custom_widget12.lower()

                                custom_widget13 = CustomWidget(self.page_4)  # 网易云下框  作用:???未知
                                custom_widget13.setGeometry(QtCore.QRect(0, 240, 300, 360))
                                custom_widget13.lower()

                                custom_widget14 = CustomWidget(self.page_4)  # 图片格式转换框
                                custom_widget14.setGeometry(QtCore.QRect(295, 0, 445, 245))
                                custom_widget14.lower()

                                custom_widget15 = CustomWidget(self.page_4)  # 其他工具框
                                custom_widget15.setGeometry(QtCore.QRect(295, 240, 445, 360))
                                custom_widget15.lower()

                            def get_current_time_string(self):
                                global current_time_string  # 声明要在函数内部使用全局变量
                                current_time = time.localtime()  # 获取当前时间的时间结构
                                current_time_string = "[" + time.strftime("%H:%M:%S",
                                                                          current_time) + "]"  # 格式化时间为字符串

                            def restart_app(self):
                                subprocess.Popen(["Fuchen.exe"])
                                try:
                                    global ab
                                    ab.kill()
                                except:
                                    pass
                                os._exit(0)

                            def changeEvent(self, event):
                                if event.type() == 177:  # 177 corresponds to the WindowStateChange event
                                    if self.isMaximized() and self.windowState() == 0:  # 0 corresponds to the WindowNoState state
                                        self.showMinimized()
                                    elif self.windowState() == 1:  # 1 corresponds to the WindowMinimized state
                                        self.showMaximized()
                                super().changeEvent(event)

                            def execute_trend(self, Path):
                                self.trend_theme = QLabel(self)
                                self.trend_theme.resize(self.size())
                                self.trend_theme.setScaledContents(True)
                                self.trend_theme.lower()
                                self.cap = cv2.VideoCapture(Path)
                                if not self.cap.isOpened():
                                    print("Error opening video stream or file")
                                self.timer_trend = QTimer(self)
                                self.timer_trend.timeout.connect(self.update_frame)
                                self.timer_trend.start(25)
                                self.Trend_Status = True
                                self.Trend_Now = True

                            def execute_trend_again(self, Path):
                                self.trend_theme.show()
                                self.cap = cv2.VideoCapture(Path)
                                self.timer_trend.start(FPS)
                                self.Trend_Now = True

                            def stop_dynamic_background(self):
                                # 停止计时器
                                self.timer_trend.stop()

                                # 清除label内容或隐藏label
                                self.trend_theme.clear()  # 清除显示的内容
                                self.trend_theme.hide()  # 隐藏label
                                self.Trend_Now = False
                                self.update()

                            def update_frame(self):
                                ret, frame = self.cap.read()
                                if ret:
                                    # 转换帧为RGBA以添加透明度通道
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                                    # frame[:, :, 3] = np.ones((frame.shape[0], frame.shape[1])) * 200  # 调整透明度
                                    # 缩放帧以适应窗口
                                    frame_resized = self.resize_frame(frame)
                                    # 转换为QImage
                                    height, width, channel = frame_resized.shape
                                    bytesPerLine = 4 * width
                                    image = QImage(frame_resized.data, width, height, bytesPerLine,
                                                   QImage.Format_ARGB32)
                                    pix = QPixmap.fromImage(image)
                                    self.trend_theme.setPixmap(pix)
                                else:
                                    # 视频循环播放
                                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

                            def resize_frame(self, frame):
                                window_width = self.width()
                                window_height = self.height()
                                height, width, _ = frame.shape
                                scaling_factor = min(window_width / width, window_height / height)
                                new_size = (int(width * scaling_factor), int(height * scaling_factor))
                                frame_resized = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
                                return frame_resized

                            def close_float_prompt(self):
                                self.point_window = ExpandingWindow()
                                self.point_window.close()

                            def updateTime(self):
                                currentTime = QtCore.QTime.currentTime()
                                elapsedTime = self.startTime.secsTo(currentTime)
                                hours = elapsedTime // 3600
                                minutes = (elapsedTime % 3600) // 60
                                seconds = elapsedTime % 60
                                self.run_label.setText(f"运行时间 {hours:02d}:{minutes:02d}:{seconds:02d}")

                            def upwindow(self):  #置顶窗口
                                if self.is_topmost == False:
                                    self.setWindowFlags(
                                        self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # 置顶
                                    self.is_topmost = True
                                    self.pushButton_18.setStyleSheet("QPushButton#pushButton_18 {"
                                                                     "    border-image: url(./image/Component/up2.png);"
                                                                     "    background-color: rgba(245,245,245,0)"
                                                                     "}")
                                    self.show()

                                else:
                                    self.setWindowFlags(
                                        self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)  # 取消置顶
                                    self.is_topmost = False
                                    self.pushButton_18.setStyleSheet("QPushButton#pushButton_18 {"
                                                                     "    border-image: url(./image/Component/up.png);"
                                                                     "    background-color: rgba(245,245,245,0)"
                                                                     "}")
                                    self.show()

                            def update_time(self):
                                current_time = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
                                self.time_label.setText('当前时间 ' + current_time)
                                self.timer.start(1000 - QtCore.QTime.currentTime().msec())

                            def clear_temp(self):
                                total_size = 0
                                for dirpath, dirnames, filenames in os.walk('./temp'):
                                    for filename in filenames:
                                        filepath = os.path.join(dirpath, filename)
                                        total_size += os.path.getsize(filepath)
                                if total_size != 0:
                                    total_size = float(total_size/1024)
                                    if total_size < 1024:
                                        result = QMessageBox.question(self, "Fuchen",f"缓存内容大小为:{round(total_size,2)}KB\n清理缓存不影响正常使用 是否进行清除?",
                                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                        if result == QMessageBox.Yes:
                                            shutil.rmtree('./temp')
                                            # 重新创建空文件夹
                                            os.mkdir('./temp')
                                            pyautogui.confirm("缓存清除成功!")
                                    else:
                                        total_size = float(total_size/1024)
                                        result = QMessageBox.question(self, "Fuchen",
                                                                      f"缓存内容大小为:{round(total_size, 2)}MB\n清理缓存不影响正常使用 是否进行清除?",
                                                                      QMessageBox.Yes | QMessageBox.No,
                                                                      QMessageBox.No)
                                        if result == QMessageBox.Yes:
                                            shutil.rmtree('./temp')
                                            # 重新创建空文件夹
                                            os.mkdir('./temp')
                                            pyautogui.confirm("缓存清除成功!")
                                else:
                                    self.show_message_box("Fuchen",f"暂无缓存内容")

                            def open_set_window(self):
                                if self.is_topmost == False:
                                    self.set_window = SetWindow()
                                    self.set_window.exec_()
                                else:
                                    self.show_message_box('Fuchen', "窗口置顶时设置窗口不可打开 请取消置顶后重试")

                            def open_user_window(self):
                                self.user_window = UserInfo()
                                self.user_window.show()

                            def open_help_window(self):
                                self.help_window = Help()
                                self.help_window.show()

                            def open_view_window(self):
                                self.view_window = View()
                                self.view_window.show()

                            def open_ctrl_window(self):
                                self.ctrl_window = Control()
                                self.ctrl_window.show()

                            def open_floating_window(self):
                                self.floating_window = floating_window()
                                self.floating_window.show()

                            def close_floating_window(self):
                                self.floating_window = floating_window()
                                self.floating_window.close()

                            def open_point_window(self):
                                self.point_window = ExpandingWindow()
                                self.point_window.show()

                            def open_record_window(self):
                                self.record__position_window = record_position()
                                self.record__position_window.exec_()

                            def open_fileedit_window(self):
                                if (self.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建')):
                                    pyautogui.confirm("需要先选择或创建配置文件")
                                    return 0
                                self.fileedit_window = FileEdit(self.button_file.text())
                                self.fileedit_window.show()

                            def clo(self):
                                global window_icon
                                with open(f"config.json", "r") as file:
                                    U_data = json.load(file)
                                next = U_data["ClosePrompt"]
                                execute = U_data["CloseExecute"]
                                if next == True:  #是否提示关闭窗口
                                    self.abus = Quit_Prompt()
                                    self.abus.exec_()
                                else:  # 不提示关闭窗口
                                    if execute == "Close":
                                        self.close()
                                        self.close_MainWindow()
                                    else:
                                        Hide()

                            def close_MainWindow(self):
                                global ab
                                try:
                                    windows.close()
                                    if window_icon == True:
                                        windows.tray_icon.hide()
                                    ab.kill()
                                except Exception as e:
                                    print(e)
                                os._exit(0)

                            def tray_icon_activated(self, reason):
                                if reason == QSystemTrayIcon.DoubleClick:
                                    windows.showNormal()

                            def keyPressEvent(self, event):
                                if event.key() == Qt.Key_F12:
                                    self.open_ctrl_window()

                            def Update_weather(self,type):
                                if type == 'first':
                                    self.weather_first.stop()  # 更新时间的间隔，单位为毫秒
                                api_key = "dce92b382ffb9409ca31ae4c1b240d4f"
                                # 发送请求获取IP地址信息
                                res = requests.get('http://myip.ipip.net', timeout=5).text
                                # 提取城市信息
                                split_res = res.split('  ')
                                city_info = split_res[-2]  # 倒数第二个元素是城市信息
                                city_info = city_info.split(' ')
                                city_info = city_info[-1]
                                global city_name, weather_status, temperature, humidity, weather_info

                                city_name = city_info
                                pinyin_list = pinyin(city_info, style=Style.NORMAL)
                                # 从拼音列表中提取拼音并连接成字符串
                                pinyin_str = ''.join([item[0] for item in pinyin_list])
                                # 设置API请求的URL
                                base_url = "http://api.openweathermap.org/data/2.5/weather"
                                url = f"{base_url}?q={pinyin_str}&appid={api_key}"
                                # 发送API请求并获取响应
                                response = requests.get(url)
                                data = response.json()
                                # 提取天气信息
                                if data["cod"] == 200:
                                    weather_info = data["weather"][0]["main"]  # 天气类型
                                    temperature = data["main"]["temp"] - 273.15  # 摄氏度
                                    humidity = data["main"]["humidity"]  # 湿度
                                    print(f"City:{city_name} ", end='\t')
                                    print(f"Weather: {weather_info} ", end='\t')
                                    print(f"Temperature: {temperature:.2f}°C ", end='\t')
                                    print(f"Humidity: {humidity}% ")
                                    weather_status = True
                                else:
                                    weather_status = False
                                    print("未知城市 天气获取失败")
                                if weather_status == True:
                                    self.weather_button.setGeometry(QtCore.QRect(5, 580, 200, 20))
                                    self.weather_button.setText(f"{city_name}  T: {temperature:.2f}°C H: {humidity}%")

                                    if weather_info == 'Clear':
                                        icon = QIcon("./image/weather/晴.png")
                                    elif weather_info == 'Clouds':
                                        icon = QIcon("./image/weather/多云.png")
                                    elif weather_info == 'Rain':
                                        icon = QIcon("./image/weather/中雨.png")
                                    elif weather_info == 'Drizzle':
                                        icon = QIcon("./image/weather/小雨.png")
                                    elif weather_info == 'Thunderstorm':
                                        icon = QIcon("./image/weather/雷暴.png")
                                    elif weather_info == 'Snow':
                                        icon = QIcon("./image/weather/雪.png")
                                    elif weather_info == 'Mist' or 'Fog':
                                        icon = QIcon("./image/weather/雾.png")
                                    elif weather_info == 'Haze':
                                        icon = QIcon("./image/weather/霾.png")
                                    else:
                                        icon = QIcon("./image/weather/晴.png")
                                    self.weather_button.setIcon(icon)
                                    self.weather_button.setIconSize(self.weather_button.size())
                                    sys_list.append(
                                        "b[" + str(time.strftime("%H:%M:%S",
                                                                 time.localtime())) + "] " + '天气获取成功 ' + f'城市:{city_name} ' + f'温度:{temperature:.2f}°C ' + f'湿度:{humidity}%')
                                else:
                                    self.weather_button.setGeometry(QtCore.QRect(5, 580, 80, 20))
                                    self.weather_button.setText(f"天气获取失败")
                                    sys_list.append(
                                        "r[" + str(
                                            time.strftime("%H:%M:%S", time.localtime())) + "] " + '天气获取失败')

                            def paintEvent(self, event):
                                if self.should_draw == "White":
                                    painter = QPainter(self)
                                    left_rect = QRect(0, 0, 260, 600)
                                    left_color = QColor(224, 224, 224)
                                    painter.fillRect(left_rect, left_color)
                                    right_rect = QRect(260, 0, 740, 600)
                                    right_color = QColor(245, 245, 245)
                                    painter.fillRect(right_rect, right_color)
                                else:
                                    painter = QPainter(self)
                                    left_rect = QRect(0, 0, 260, 600)
                                    left_color = QColor(224, 224, 224)
                                    left_color.setAlpha(30)  # 设置左边区域颜色的透明度为 50%
                                    painter.fillRect(left_rect, left_color)
                                    right_rect = QRect(260, 0, 740, 600)
                                    right_color = QColor(245, 245, 245)
                                    right_color.setAlpha(10)
                                    painter.fillRect(right_rect, right_color)
                                      # 设置右边区域颜色的透明度为 75%

                            def empyt_log(self):  # 清空日志
                                log_file_path = "INFOR.log"
                                with open(log_file_path, "w") as log_file:
                                    pass  # 使用 pass 语句表示什么都不做，从而实现清空文件内容
                                windows.show_message_box("提示", "日志清空成功!")

                            def open_folder(self, page):  # 浏览QQ头像下载文件夹
                                if page == 'picture':
                                    folder_path = './mod/picture'  # 修改为你要打开的文件夹路径
                                    url = QUrl.fromLocalFile(folder_path)
                                    QDesktopServices.openUrl(url)
                                elif page == 'music':
                                    folder_path = './mod/music'  # 修改为你要打开的文件夹路径
                                    url = QUrl.fromLocalFile(folder_path)
                                    QDesktopServices.openUrl(url)

                                elif page == 'xlsx':
                                    folder_path = './mod/xlsx'  # 修改为你要打开的文件夹路径
                                    url = QUrl.fromLocalFile(folder_path)
                                    QDesktopServices.openUrl(url)

                            def open_music_folder(self):  # 浏览QQ头像下载文件夹
                                folder_path = './mod/music'  # 修改为你要打开的文件夹路径
                                url = QUrl.fromLocalFile(folder_path)
                                QDesktopServices.openUrl(url)

                            def LogRecord(self):  # 打开日志
                                subprocess.Popen(["notepad.exe", "INFOR.log"])

                            def join_team(self):  # 加入队伍
                                num = self._5lineEdit.text()
                                send_encry(f'20001 {num}')

                            def new_click(self):  #连点器部分
                                if (self.RClick_Radio.isChecked()) and (self.sort == '鼠标右键'):
                                    pyautogui.confirm("点击按键和监听热键不可相同!")
                                    return 0
                                elif (self.MClick_Radio.isChecked()) and (self.sort == '鼠标中键'):
                                    pyautogui.confirm("点击按键和监听热键不可相同!")
                                    return 0
                                global ab
                                self._3pushButton_4.setEnabled(False)
                                self.LClick_Radio.setEnabled(False)
                                self.MClick_Radio.setEnabled(False)
                                self.RClick_Radio.setEnabled(False)
                                self._3pushButton_6.setEnabled(False)
                                self._3D.setEnabled(False)
                                self._3pushButton_6.setText("正在开启...")
                                if self.sort == 'F8':
                                    hotkey = "119"  # F8
                                elif self.sort == 'F9':
                                    hotkey = "120"  # F9
                                elif self.sort == 'F10':
                                    hotkey = "121"
                                elif self.sort == '鼠标右键':
                                    hotkey = "2"
                                elif self.sort == '鼠标中键':
                                    hotkey = "4"
                                elif self.sort == 'Alt':
                                    hotkey = "18"
                                elif self.sort == '空格':
                                    hotkey = "32"
                                elif self.sort == 'Ctrl':
                                    hotkey = "17"
                                elif self.sort == 'Shift':
                                    hotkey = "16"
                                elif self.sort == 'Tab':
                                    hotkey = "9"
                                elif self.sort == 'Caps':
                                    hotkey = "20"
                                else:
                                    hotkey = '2'
                                interval = str(float(self._3D.value()))
                                if self.LClick_Radio.isChecked():
                                    sort = 'left'
                                elif self.MClick_Radio.isChecked():
                                    sort = 'mid'
                                else:
                                    sort = 'right'
                                try:
                                    ab = subprocess.Popen(["./mod/more/click.exe", hotkey, interval,sort])
                                    self._3pushButton_6.setText("连点器已开启")
                                    self._3pushButton_7.setVisible(True)
                                    ab.wait()
                                except KeyboardInterrupt:
                                    # 处理 Ctrl+C 中断
                                    ab.terminate()
                                    sys.exit()
                                except Exception as e:
                                    # 处理其他异常
                                    pyautogui.confirm(f"Error: {e}")
                                    ab.terminate()
                                    sys.exit()
                                finally:
                                    # 确保在程序退出时终止 C++ 程序
                                    ab.terminate()

                            def break_click(self):  #关闭连点器
                                global ab
                                ab.kill()
                                self._3pushButton_6.setText("开启连点器")
                                self._3pushButton_4.setEnabled(True)
                                self.LClick_Radio.setEnabled(True)
                                self.MClick_Radio.setEnabled(True)
                                self.RClick_Radio.setEnabled(True)
                                self._3pushButton_6.setEnabled(True)
                                self._3D.setEnabled(True)
                                self._3pushButton_7.setVisible(False)

                            def gain_handle(self):  # 获取句柄
                                self.showMinimized()

                                def on_click(x, y, button,pressed):
                                    if pressed:
                                        hwnd = win32gui.WindowFromPoint((x, y))  # 请填写 x 和 y 坐标
                                        self._2lineEdit_3.setText(str(hwnd))
                                        listener.stop()

                                def click_listener():
                                    global listener
                                    listener = mouse.Listener(on_click=on_click)
                                    listener.start()
                                    listener.join()

                                click_listener()
                                self.showNormal()

                            def mouseinfo(self):  #点击助手
                                pyautogui.mouseInfo()

                            def QQ_Group_information(self):  #QQ群信息获取
                                play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                if self.Edge.isChecked():
                                    driver = webdriver.Edge()
                                elif self.Chrome.isChecked():
                                    driver = webdriver.Chrome()
                                else:
                                    driver = webdriver.Ie()

                                # 打开网页
                                driver.get('https://qun.qq.com/member.html')

                                # 等待元素存在，然后等待元素不可见，然后进行下一步操作
                                try:

                                    # 等待元素存在  数字为最长等待时间
                                    WebDriverWait(driver, 100).until(
                                        EC.presence_of_element_located((By.ID, "loginWin"))
                                    )
                                    play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                    result = pyautogui.confirm(
                                        "请在浏览器中登录QQ并关闭此窗口再进行下一步操作\n\n若要取消操作请关闭浏览器窗口")
                                    # 等待元素不可见
                                    WebDriverWait(driver, 100).until_not(
                                        EC.visibility_of_element_located((By.ID, "loginWin"))
                                    )
                                    play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                    result = pyautogui.confirm(
                                        "登录成功 接下来请先关闭此窗口再进行群聊选择\n\n若要取消操作请关闭浏览器窗口")
                                    try:  # 群选择成功
                                        # 等待元素出现
                                        WebDriverWait(driver, 100).until(
                                            EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.on"))
                                        )

                                        # 等待元素消失
                                        WebDriverWait(driver, 100).until_not(
                                            EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.on"))
                                        )
                                    except:  # 跳过群选择
                                        pass
                                    result = pyautogui.confirm(
                                        "群聊已确认 接下来程序将自动处理数据 请勿关闭或点击浏览器窗口 关闭此窗口以继续\n\n若要取消操作请关闭浏览器窗口")
                                    # 使用XPath提取元素内容
                                    element = driver.find_element(By.XPATH, '//span[@id="groupTit"]')
                                    text = element.text
                                    # 模拟滚动
                                    SCROLL_PAUSE_TIME = 0.5  # 滚动间隔时间
                                    # 获取页面初始高度
                                    number = 0
                                    last_height = driver.execute_script("return document.body.scrollHeight")
                                    while True:
                                        number = number + 1
                                        # 模拟滚动到页面底部
                                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                                        # 等待页面加载
                                        time.sleep(SCROLL_PAUSE_TIME)

                                        # 计算新高度并判断是否到达页面底部
                                        new_height = driver.execute_script("return document.body.scrollHeight")
                                        print("\r正在处理第{}个页面".format(number), end="")
                                        if new_height == last_height:
                                            break
                                        last_height = new_height

                                    # 等待页面加载完全
                                    time.sleep(2)

                                    # 获取整个网页的 HTML 内容
                                    html_content = driver.page_source

                                    # 将 HTML 内容保存到文件
                                    with open('./temp/page_content.html', 'w', encoding='utf-8') as file:
                                        file.write(html_content)

                                    # 关闭浏览器
                                    driver.quit()

                                    # 处理特殊字符(非法字符)
                                    def remove_nonprintable_chars(text):
                                        cleaned_text = ''
                                        for char in text:
                                            if char.isalnum() or char in string.printable or char.isspace():
                                                cleaned_text += char
                                        return cleaned_text

                                    # 从本地文件中读取HTML内容（将 'your_file.html' 替换为你的文件路径）
                                    with open('./temp/page_content.html', 'r', encoding='utf-8') as file:
                                        html_content = file.read()

                                    # 创建 BeautifulSoup 对象
                                    soup = BeautifulSoup(html_content, 'html.parser')

                                    # 找到具有指定 id 的表格元素
                                    table = soup.find('table', {'id': 'groupMember'})

                                    # 在表格中找到所有包含 'list' 类的 tbody 元素

                                    tbody_elements = table.find_all('tbody', class_='list')

                                    data = []  # 列表用于存储提取的数据

                                    for tbody in tbody_elements:
                                        # 在每个 tbody 中找到具有 'mb' 类的元素并提取信息
                                        elements = tbody.find_all(class_=lambda x: x and 'mb' in x)
                                        for element in elements:
                                            try:
                                                # 提取并清理（或处理）数据
                                                gender = remove_nonprintable_chars(
                                                    element.find_all('td')[1].text.strip())  # 序号
                                                name = remove_nonprintable_chars(
                                                    element.find_all('td')[2].text.strip())  # 名称
                                                group_name = remove_nonprintable_chars(
                                                    element.find_all('td')[3].text.strip())  # 群名称
                                                Qid = remove_nonprintable_chars(
                                                    element.find_all('td')[4].text.strip())  # QQ号
                                                sex = remove_nonprintable_chars(
                                                    element.find_all('td')[5].text.strip())  # 性别
                                                QQ_year = remove_nonprintable_chars(
                                                    element.find_all('td')[6].text.strip())  # QQ年龄
                                                join_date = remove_nonprintable_chars(
                                                    element.find_all('td')[7].text.strip())  # 进群日期
                                                group_lv = remove_nonprintable_chars(
                                                    element.find_all('td')[8].text.strip())  # 群等级
                                                send_date = remove_nonprintable_chars(
                                                    element.find_all('td')[9].text.strip())  # 最后发言日期

                                                # 以字典格式存储提取的数据
                                                dic = {"序号": gender,
                                                    '名称': name,
                                                    '群昵称': group_name,}
                                                if self.checkBox_qid.isChecked():
                                                    dic['QQ号'] = Qid
                                                if self.checkBox_sex.isChecked():
                                                    dic['性别'] = sex
                                                if self.checkBox_qq_year.isChecked():
                                                    dic['QQ年龄'] = QQ_year
                                                if self.checkBox_join_date.isChecked():
                                                    dic['进群日期'] = join_date
                                                if self.checkBox_send_date.isChecked():
                                                    dic['最后发言日期'] = send_date
                                                if self.checkBox_group_lv.isChecked():
                                                    dic['群等级'] = group_lv
                                                data.append(dic)
                                            except:
                                                pass

                                    df = pd.DataFrame(data)
                                    output_folder = self.QQ_Group_Save.text()
                                    df.to_excel(output_folder + f'\\{text}.xlsx', index=False)
                                    pyautogui.confirm(f"{text}保存成功")

                                except Exception as e:  # 登录窗口打开失败
                                    traceback.print_exc()
                                    # pyautogui.confirm(str(e))

                            def download_image(self):  # 下载QQ头像
                                if new_lv == '4dff4ea340f0a823f15d3f4f01ab62eae0e5da579ccb851f8db9dfe84c58b2b37b89903a740e1ee172da793a6e79d560e5f7f9bd058a12a280433ed6fa46510a':
                                    pyautogui.confirm("该功能需要Lv2才能使用!")
                                    return 0
                                self.QQ_Button_Dow.setEnabled(False)

                                def generate_random_number():
                                    # 生成随机位数（6到10之间）
                                    digits = random.randint(7, 10)

                                    # 生成随机数字字符串
                                    first_digit = random.randint(1, 9)  # 生成1到9之间的随机数作为第一位
                                    remaining_digits = ''.join(
                                        random.choices('0123456789', k=digits - 1))  # 生成剩余位数的随机数字字符串
                                    random_number = str(first_digit) + remaining_digits

                                    return random_number

                                def compare_images(image_path):
                                    image = Image.open(image_path)
                                    width, height = image.size
                                    return width == height == 40

                                n = 0
                                b = 0
                                for i in range(self.QQ_spinBox.value()):
                                    random_number = generate_random_number()
                                    url = f"https://q1.qlogo.cn/g?b=qq&nk={random_number}&s=640"
                                    response = requests.get(url)
                                    b = b+1
                                    if response.status_code == 200:
                                        with open(f"./mod/picture/{random_number}.jpg", "wb") as file:
                                            file.write(response.content)

                                        image_path1 = "./mod/example/example.jpg"  # QQ默认头像1
                                        image_path2 = "./mod/example/example2.jpg"  # QQ默认头像 这里设置两种吃储存 查重 若为默认头像则删除
                                        image_path3 = f"./mod/picture/{random_number}.jpg"

                                        if compare_images(image_path3):
                                            os.remove(f"./mod/picture/{random_number}.jpg")
                                        # elif is_40x40(image_path1) or is_40x40(image_path2):
                                        # os.remove(f"./mod/picture/{random_number}.jpg")
                                        else:
                                            n = n + 1
                                            self.QQ_label_t6.setText(f"有效次数:{n}次")
                                    self.QQ_label_t3.setText(f"总下载次数:{b}次")
                                if n == 0:
                                    self.QQ_label_t6.setText("有效次数:0次")
                                self.QQ_Button_Dow.setEnabled(True)
                                MyThread(play_warning_sound)
                                pyautogui.confirm(f"图片下载成功!\n本次已成功下载{n}张图片(已删除默认头像)")

                            def QQ_image_update(self):  # QQ个人信息资料一键更新
                                result = pyautogui.confirm(
                                    "请确保QQ主窗口已经打开 若打开则点击确认按钮 修改资料时 请勿移动鼠标\n若出现修改失败的情况 可能是间隔时间过小 略微调大即可")
                                if result != "OK":
                                    return 0
                                try:
                                    rest = self.QQ_Doxb.value()
                                    # 读取文本文件内容
                                    with open('./mod/dic/name.txt', 'r', encoding='utf-8') as file:
                                        lines = file.readlines()
                                    # 从列表中随机选择一行
                                    random_line = random.choice(lines[0:2304])
                                    folder_path = './mod/picture'

                                    # 检查文件夹是否存在
                                    if not os.listdir(folder_path):
                                        pyautogui.confirm("需要先下载图片才可使用")
                                        return 0
                                    else:
                                        # 获取文件夹中的所有文件（不包括子文件夹）
                                        files = [f for f in os.listdir(folder_path) if
                                                 os.path.isfile(os.path.join(folder_path, f))]
                                        random_file = random.choice(files)
                                            # 构建完整的文件路径
                                        file_path = os.path.abspath(os.path.join(folder_path, random_file))
                                        # 从文件名中提取数字部分
                                        file_name = os.path.basename(file_path)
                                        number = re.search(r'\d+', file_name).group()
                                        # 发送GET请求
                                        url = f"https://api.oioweb.cn/api/qq/info?qq={number}"  # 替换为实际的API端点
                                        response = requests.get(url)

                                        # 检查响应状态码
                                        if response.status_code == 200:
                                            # 将JSON字符串解析为Python字典
                                            data = response.json()
                                            # 提取nickname字段的值
                                            nickname = data["result"]["nickname"]
                                        else:
                                            nickname = random_line

                                    # 获取窗口对象，替换"Your Window Title"为目标窗口的标题  修改头像
                                    QQwindow = gw.getWindowsWithTitle("QQ")[0]
                                    window_position = (QQwindow.left+50,QQwindow.top+80)
                                    # 执行点击操作
                                    pyautogui.click(window_position)
                                    time.sleep(rest)

                                    QQwindow = gw.getWindowsWithTitle("我的资料")[0]
                                    window_position = (QQwindow.left + 670, QQwindow.top + 50)
                                    # 执行点击操作
                                    pyautogui.click(window_position)
                                    time.sleep(rest)

                                    QQwindow = gw.getWindowsWithTitle("编辑资料")[0]  # 修改名称
                                    window_position = (QQwindow.left + 100, QQwindow.top + 100)
                                    # 执行点击操作
                                    for i in range(3):
                                        pyautogui.click(window_position)

                                    pyperclip.copy(nickname)
                                    # 等待一段时间，以确保复制操作完成
                                    time.sleep(rest)
                                    # 模拟键盘按键粘贴字符串
                                    pyautogui.hotkey('ctrl', 'v')
                                    # 执行点击操作
                                    window_position = (QQwindow.left + 260, QQwindow.top + 720)
                                    time.sleep(rest)
                                    pyautogui.click(window_position)

                                    time.sleep(rest)
                                    QQwindow = gw.getWindowsWithTitle("我的资料")[0]  # 修改头像
                                    window_position = (QQwindow.left + 100, QQwindow.top + 450)
                                    # 执行点击操作
                                    pyautogui.click(window_position)

                                    time.sleep(rest)
                                    QQwindow = gw.getWindowsWithTitle("更换头像")[0]
                                    window_position = (QQwindow.left + 80, QQwindow.top + 60)
                                    pyautogui.click(window_position)
                                    time.sleep(0.6)

                                    QQwindow = gw.getWindowsWithTitle("打开")[0]
                                    window_position = (QQwindow.left + 240, QQwindow.top + QQwindow.height-70)
                                    # 执行点击操作
                                    pyautogui.click(window_position)

                                    pyperclip.copy(file_path)

                                    # 等待一段时间，以确保复制操作完成
                                    time.sleep(0.1)

                                    # 模拟键盘按键粘贴字符串
                                    pyautogui.hotkey('ctrl', 'v')

                                    window_weight = QQwindow.width
                                    window_height = QQwindow.height
                                    target_y_relative = window_height - 70  # 相对于窗口左上角的y坐标
                                    target_x_relative = window_weight - 50
                                    # 计算在屏幕上的绝对坐标
                                    target_x = QQwindow.left + target_x_relative
                                    target_y = QQwindow.top + target_y_relative
                                    # 执行点击操作
                                    pyautogui.click(target_x, target_y)

                                    QQwindow = gw.getWindowsWithTitle("更换头像")[0]
                                    window_position = (QQwindow.left + 250, QQwindow.top + 600)
                                    # 执行点击操作
                                    pyautogui.click(window_position)

                                    MyThread(play_warning_sound)
                                    pyautogui.confirm("资料修改成功")
                                except Exception as e:
                                    MyThread(play_warning_sound)
                                    pyautogui.confirm(e)

                            def Send_QQ(self):  # @QQ
                                def check_process_exists(process_name):
                                    for process in psutil.process_iter(attrs=['pid', 'name']):
                                        if process.info['name'] == process_name:
                                            return True
                                    return False

                                # 要检查的进程名称
                                target_process_name = "QQ.exe"
                                if check_process_exists(target_process_name):
                                    if position_status == False:
                                        pyautogui.confirm("需要先设置位置才能开始发送")
                                        return 0
                                    play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                    if self._2lineEdit.text() == "":
                                        pyautogui.confirm('请输入QQ号')
                                    elif self._2doubleSpinBox.value() == 0.0:
                                        pyautogui.confirm("请输入间隔")
                                    elif len(self._2lineEdit.text()) > 11 or len(
                                            self._2lineEdit.text()) <= 5 or not self._2lineEdit.text().isdigit():
                                        pyautogui.confirm('请输入正确的QQ号')
                                    else:

                                        time.sleep(3)
                                        math = 0
                                        pyautogui.PAUSE = (self._2doubleSpinBox.value() - 0.03) / 7
                                        if self._2checkBox.isChecked():
                                            while True:
                                                if keys.is_pressed("F10"):  # Check if F10 key is pressed
                                                    self.open_point_window()
                                                    break  # Exit the loop if F10 is pressed
                                                math = math + 1
                                                pyautogui.click(textedit_position)
                                                pyautogui.write(f'@{self._2lineEdit.text()}')
                                                time.sleep(0.03)
                                                pyautogui.press('enter')
                                                pyautogui.hotkey('ctrl', 'v')
                                                pyautogui.write(str(math))
                                                randfigure = random.choice(Random_list)  # 随机符号
                                                if randfigure == 1:
                                                    pyautogui.press('.')
                                                elif randfigure == 2:
                                                    pyautogui.press('。')
                                                else:
                                                    pyautogui.press(',')
                                                pyautogui.click(send_position)
                                        else:
                                            while True:
                                                if keys.is_pressed("F10"):  # Check if F10 key is pressed
                                                    self.open_point_window()
                                                    break  # Exit the loop if F10 is pressed
                                                pyautogui.click(textedit_position)
                                                pyautogui.write(f'@{self._2lineEdit.text()}')
                                                time.sleep(0.03)
                                                pyautogui.press('enter')
                                                pyautogui.hotkey('ctrl', 'v')
                                                randfigure = random.choice(Random_list)  # 随机符号
                                                if randfigure == 1:
                                                    pyautogui.press('.')
                                                elif randfigure == 2:
                                                    pyautogui.press('。')
                                                else:
                                                    pyautogui.press(',')
                                                pyautogui.click(send_position)
                                else:
                                    pyautogui.confirm("QQ未启动")

                            def Handle_Send(self):  # 句柄式发送消息
                                def setText(aString):
                                    """设置剪贴板文本"""
                                    w.OpenClipboard()
                                    w.EmptyClipboard()
                                    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
                                    w.CloseClipboard()

                                def send_qq(to_who, msg):
                                    """发送qq消息
                                    to_who：qq消息接收人
                                    msg：需要发送的消息
                                    """
                                    # 将消息写到剪贴板
                                    setText(msg)
                                    # 投递剪贴板消息到QQ窗体
                                    figure = self._2spinBox.value()
                                    for i in range(int(figure)):
                                        '''position = win32api.MAKELONG(x, y)  # x,y为点击点相对于该窗口的坐标
                                        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                                             position)  # 向窗口发送模拟鼠标点击
                                        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                                                             position)  # 模拟释放鼠标左键'''
                                        win32gui.SendMessage(hwnd, 258, 22, 2080193)
                                        win32gui.SendMessage(hwnd, 770, 0, 0)
                                        # 模拟按下回车键
                                        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                                        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

                                hwnd = self._2lineEdit_3.text()
                                massage = self._2textEdit.toPlainText()
                                if hwnd == '':
                                    MyThread(play_warning_sound)
                                    pyautogui.confirm("请输入句柄")
                                elif massage == '':
                                    MyThread(play_warning_sound)
                                    pyautogui.confirm("请输入需要发送的消息")
                                else:
                                    try:
                                        send_qq(int(hwnd), massage)
                                    except Exception as e:
                                        pyautogui.confirm(f"发送失败 错误信息如下:\n {e}")

                            def Send_Copy(self):  # 发送复制消息
                                def check_process_exists(process_name):
                                    for process in psutil.process_iter(attrs=['pid', 'name']):
                                        if process.info['name'] == process_name:
                                            return True
                                    return False

                                # 要检查的进程名称
                                target_process_name = "QQ.exe"
                                if check_process_exists(target_process_name):
                                    if position_status == False:
                                        pyautogui.confirm("需要先设置位置才能开始发送")
                                        return 0
                                    play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                    time.sleep(3)
                                    speed = self.copy_int.value()
                                    rest_time = 1 / speed - 0.10
                                    pyautogui.PAUSE = 0.015
                                    b = 0
                                    start_time = time.time()
                                    while True:
                                        if keys.is_pressed("F10"):  # Check if F10 key is pressed
                                            self.open_point_window()
                                            end_time = time.time()
                                            # 计算执行时间
                                            execution_time = end_time - start_time
                                            # 打印执行时间
                                            print(f"执行时间: {execution_time} 秒")
                                            break  # Exit the loop if F10 is pressed
                                        b = b + 1
                                        pyautogui.click(textedit_position)
                                        pyautogui.hotkey('ctrl', 'v')  # 粘贴
                                        randfigure = random.choice(Random_list)  # 随机字符输入
                                        if randfigure == 1:
                                            pyautogui.press('.')
                                        elif randfigure == 2:
                                            pyautogui.press('。')
                                        else:
                                            pyautogui.press(',')
                                        #pyautogui.click(1644, 1025)  # 点击第二处位置
                                        pyautogui.click(send_position)  # 点击第二处位置
                                        if rest_time > 0:
                                            time.sleep(rest_time)
                                    print(f"本次Fuchen累计发送{b}条消息")
                                else:
                                    pyautogui.confirm("QQ未启动!")

                            def Click_Record(self):  # 记录自动脚本
                                if self.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建'):
                                    pyautogui.confirm("需要先选择或创建配置文件")
                                    return 0
                                self.showMinimized()
                                play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                wait_time = self.wait_doubleSpinBox.value()
                                time.sleep(wait_time)
                                print("开始记录自动脚本")
                                global last_time,records,last_key,last_event_type

                                records = []
                                last_time = time.time()
                                if self.end_key_button.text() == "ESC":
                                    ed_bu = Key.esc
                                elif self.end_key_button.text() == "F8":
                                    ed_bu = Key.f8
                                elif self.end_key_button.text() == "F9":
                                    ed_bu = Key.f9
                                elif self.end_key_button.text() == "F10":
                                    ed_bu = Key.f10
                                elif self.end_key_button.text() == "END":
                                    ed_bu = Key.end
                                else:
                                    ed_bu = Key.esc
                                def on_move(x, y):
                                    global last_time
                                    current_time = time.time()
                                    interval = int((current_time - last_time) * 1000)
                                    if interval != 0:
                                        records.append([interval, 'M', 'mouse move', [x, y]])
                                        last_time = current_time

                                def on_click(x, y, button, pressed):
                                    global last_time
                                    current_time = time.time()
                                    interval = int((current_time - last_time) * 1000)  # Convert to milliseconds
                                    action = ''
                                    if button == mouse.Button.left:
                                        action = 'mouse left down' if pressed else 'mouse left up'
                                    elif button == mouse.Button.right:
                                        action = 'mouse right down' if pressed else 'mouse right up'
                                    elif button == mouse.Button.middle:
                                        action = 'mouse middle down' if pressed else 'mouse middle up'
                                    if action:
                                        records.append([interval, 'M', action, [x, y]])
                                        last_time = current_time

                                def on_scroll(x, y, dx, dy):
                                    global last_time
                                    current_time = time.time()
                                    interval = int((current_time - last_time) * 1000)
                                    action = 'mouse scroll'
                                    records.append([interval, 'M', action, [dx, dy]])
                                    last_time = current_time

                                # 设置防抖时间间隔（毫秒）
                                debounce_interval = 200

                                last_key = None
                                last_event_type = None  # 'down' 或 'up'

                                def on_press(key):
                                    global last_time, last_key, last_event_type
                                    current_time = time.time()
                                    interval = int((current_time - last_time) * 1000)

                                    if key == ed_bu:
                                        return False

                                    if key == last_key and last_event_type == 'down' and interval < debounce_interval:
                                        return

                                    if hasattr(key, 'char') and key.char:
                                        key_char = key.char.lower() if ord(key.char) >= 32 else chr(ord(key.char) + 64)
                                        key_desc = [key.vk, key_char]
                                    elif isinstance(key, Key):
                                        key_desc = [key.value.vk, key.name.upper()]
                                    elif isinstance(key, KeyCode):
                                        key_desc = [key.vk, key.char.upper() if key.char else 'NUMPAD']

                                    records.append([interval, 'K', 'key down', key_desc])
                                    last_time = current_time
                                    last_key = key
                                    last_event_type = 'down'

                                def on_release(key):
                                    global last_time, last_key, last_event_type
                                    current_time = time.time()
                                    interval = int((current_time - last_time) * 1000)

                                    if key == last_key and last_event_type == 'up' and interval < debounce_interval:
                                        return

                                    if hasattr(key, 'char') and key.char:
                                        key_char = key.char.lower() if ord(key.char) >= 32 else chr(ord(key.char) + 64)
                                        key_desc = [key.vk, key_char]
                                    elif isinstance(key, Key):
                                        key_desc = [key.value.vk, key.name.upper()]
                                    elif isinstance(key, KeyCode):
                                        key_desc = [key.vk, key.char.upper() if key.char else 'NUMPAD']

                                    records.append([interval, 'K', 'key up', key_desc])
                                    last_time = current_time
                                    last_key = key
                                    last_event_type = 'up'

                                mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move,on_scroll=on_scroll)
                                keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

                                mouse_listener.start()
                                keyboard_listener.start()

                                keyboard_listener.join()

                                move_times = 0
                                move_total_time = 0
                                for list_record in records:
                                    if list_record[2] == 'mouse move':
                                        if list_record[0] <10:
                                            if move_times == 0:
                                                move_times = move_times + 1
                                                move_total_time = move_total_time + list_record[0]
                                                list_record[0] = 0
                                            else:
                                                move_total_time = move_total_time + list_record[0]
                                                if move_total_time >= 10:
                                                    move_times = 0
                                                    list_record[0] = move_total_time
                                                    move_total_time = 0
                                                else:
                                                    move_times = move_times + 1
                                                    list_record[0] = 0
                                        else:
                                            move_times = 0
                                            move_total_time = 0
                                    else:
                                        move_times = 0
                                        move_total_time = 0

                                # 打开文件进行写入
                                with open('./scripts/'+self.button_file.text(), 'w') as f:
                                    for record in records:
                                        if record[0] != 0:
                                            if isinstance(record[3][1], str) and len(record[3][1]) == 1 and record[3][
                                                1].isupper():
                                                record[3] = (record[3][0], record[3][1].lower())
                                            f.write(str(record) + '\n')

                                print("记录完毕")
                                play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                self.showNormal()

                            def Click_Record_execute(self):  # 执行自动脚本
                                if self.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建'):
                                    pyautogui.confirm("需要先选择或创建配置文件")
                                    return 0
                                play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
                                wait_time = self.wait_doubleSpinBox.value()
                                count = self._3spinBox_3.value()
                                time.sleep(wait_time)

                                self.showMinimized()

                                mouse_controller = MouseController()
                                keyboard_controller = KeyboardController()

                                def get_key(key_code, key_char):
                                    # 将字符串形式的特殊键转换为pynput的Key对象
                                    special_keys = {
                                        'ALT': Key.alt,
                                        'ALT_GR': Key.alt_gr,
                                        'ALT_L': Key.alt_l,
                                        'ALT_R': Key.alt_r,
                                        'BACKSPACE': Key.backspace,
                                        'CAPS_LOCK': Key.caps_lock,
                                        'CMD': Key.cmd,
                                        'CTRL_L': Key.ctrl_l,
                                        'CTRL_R': Key.ctrl_r,
                                        'DELETE': Key.delete,
                                        'DOWN': Key.down,
                                        'END': Key.end,
                                        'ENTER': Key.enter,
                                        'ESC': Key.esc,
                                        'F1': Key.f1,
                                        'F2': Key.f2,
                                        'F3': Key.f3,
                                        'F4': Key.f4,
                                        'F5': Key.f5,
                                        'F6': Key.f6,
                                        'F7': Key.f7,
                                        'F8': Key.f8,
                                        'F9': Key.f9,
                                        'F10': Key.f10,
                                        'F11': Key.f11,
                                        'F12': Key.f12,
                                        'HOME': Key.home,
                                        'INSERT': Key.insert,
                                        'LEFT': Key.left,
                                        'NUM_LOCK': Key.num_lock,
                                        'PAGE_DOWN': Key.page_down,
                                        'PAGE_UP': Key.page_up,
                                        'RIGHT': Key.right,
                                        'SCROLL_LOCK': Key.scroll_lock,
                                        'SHIFT': Key.shift,
                                        'SHIFT_R': Key.shift_r,
                                        'SPACE': Key.space,
                                        'TAB': Key.tab,
                                        'UP': Key.up,
                                        'PRINT_SCREEN': Key.print_screen,
                                        'MENU': Key.menu,
                                    }
                                    # 检查是否为特殊键
                                    if key_char.upper() in special_keys:
                                        return special_keys[key_char.upper()]
                                    # 检查是否为数字键盘的键
                                    elif 'NUMPAD' in key_char.upper() or key_code in range(96, 106) or key_code == 110:
                                        numpad_keys = {
                                            96: KeyCode(vk=96),  # Numpad 0
                                            97: KeyCode(vk=97),  # Numpad 1
                                            98: KeyCode(vk=98),  # Numpad 2
                                            99: KeyCode(vk=99),  # Numpad 3
                                            100: KeyCode(vk=100),  # Numpad 4
                                            101: KeyCode(vk=101),  # Numpad 5
                                            102: KeyCode(vk=102),  # Numpad 6
                                            103: KeyCode(vk=103),  # Numpad 7
                                            104: KeyCode(vk=104),  # Numpad 8
                                            105: KeyCode(vk=105),  # Numpad 9
                                            110: KeyCode(vk=110)  # Numpad .
                                        }
                                        return numpad_keys.get(key_code, KeyCode(char=chr(key_code)))
                                    else:
                                        return KeyCode(char=key_char)

                                records = []
                                record_time  = 0
                                with open('./scripts/'+self.button_file.text(), 'r') as f:
                                    for line in f:
                                        record = eval(line.strip())
                                        record_time += record[0]
                                        records.append(record)
                                print(f"记录执行时间:{record_time/1000}秒")
                                star = time.time()
                                for i in range(count):  #开始执行自动脚本
                                    for record in records:
                                        time.sleep((record[0] - 1) / 1000 )  # 等待时间
                                        if record[1] == 'M':  # 鼠标事件
                                            x, y = record[3] if record[2] != 'mouse scroll' else (None, None)
                                            if 'mouse move' in record[2]:
                                                mouse_controller.position = (x, y)
                                            elif 'mouse left down' in record[2]:
                                                mouse_controller.press(Button.left)
                                            elif 'mouse left up' in record[2]:
                                                mouse_controller.release(Button.left)
                                            elif 'mouse right down' in record[2]:
                                                mouse_controller.press(Button.right)
                                            elif 'mouse right up' in record[2]:
                                                mouse_controller.release(Button.right)
                                            elif 'mouse middle down' in record[2]:
                                                mouse_controller.press(Button.middle)
                                            elif 'mouse middle up' in record[2]:
                                                mouse_controller.release(Button.middle)
                                            elif 'mouse scroll' in record[2]:
                                                dx, dy = record[3]
                                                mouse_controller.scroll(dx, dy)

                                        elif record[1] == 'K':  # 键盘事件
                                            key_code, key_char = record[3]
                                            key = get_key(key_code, key_char)
                                            if 'down' in record[2]:
                                                keyboard_controller.press(key)
                                            elif 'up' in record[2]:
                                                keyboard_controller.release(key)
                                end_ti = time.time()
                                print(f"实际执行时间:{end_ti-star}秒")
                                self.showNormal()

                            def about(self):
                                # MyThread(play_warning_sound)  提示音
                                pyautogui.confirm(
                                    f"版本:{Version}\nGui图形库:Pyqt5\n制作者:浮沉 QQ:3046447554 软件完全免费 纯净无广告\n软件免费 若发现收费购买 请联系我进行反馈",
                                    "Fuchen")

                            def open_website(self):
                                webbrowser.open("http://fcyang.top/")

                            def delete_images(self):

                                reply = QMessageBox.question(self, '确认删除', "你确定要删除文件夹内容吗?",
                                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                                if reply == QMessageBox.Yes:
                                    shutil.rmtree('./mod/picture')
                                    # 重新创建空文件夹
                                    os.mkdir('./mod/picture')
                                    pyautogui.confirm("图片清除成功!")

                            def createMenu(self):
                                menu = QMenu(self)

                                action1 = QAction("F8", self)
                                action1.triggered.connect(lambda: self.action_Clicked("F8"))

                                action2 = QAction("F9", self)
                                action2.triggered.connect(lambda: self.action_Clicked("F9"))

                                action3 = QAction("F10", self)
                                action3.triggered.connect(lambda: self.action_Clicked("F10"))

                                action4 = QAction("鼠标右键", self)
                                action4.triggered.connect(lambda: self.action_Clicked("鼠标右键"))

                                action5 = QAction("鼠标中键", self)
                                action5.triggered.connect(lambda: self.action_Clicked("鼠标中键"))

                                action6 = QAction("Alt", self)
                                action6.triggered.connect(lambda: self.action_Clicked("Alt"))

                                action7 = QAction("空格", self)
                                action7.triggered.connect(lambda: self.action_Clicked("空格"))

                                action8 = QAction("Ctrl", self)
                                action8.triggered.connect(lambda: self.action_Clicked("Ctrl"))

                                action9 = QAction("Shift", self)
                                action9.triggered.connect(lambda: self.action_Clicked("Shift"))

                                action10 = QAction("Tab", self)
                                action10.triggered.connect(lambda: self.action_Clicked("Tab"))

                                action11 = QAction("Caps", self)
                                action11.triggered.connect(lambda: self.action_Clicked("Caps"))


                                menu.addAction(action1)
                                menu.addAction(action2)
                                menu.addAction(action3)
                                menu.addAction(action4)
                                menu.addAction(action5)
                                menu.addAction(action6)
                                menu.addAction(action7)
                                menu.addAction(action8)
                                menu.addAction(action9)
                                menu.addAction(action10)
                                menu.addAction(action11)

                                return menu

                            def create_key_Menu(self):
                                key_menu = QMenu(self)

                                action1 = QAction("ESC", self)
                                action1.triggered.connect(lambda: self.key_menu_com("ESC"))

                                action2 = QAction("F8", self)
                                action2.triggered.connect(lambda: self.key_menu_com("F8"))

                                action3 = QAction("F9", self)
                                action3.triggered.connect(lambda: self.key_menu_com("F9"))

                                action4 = QAction("F10", self)
                                action4.triggered.connect(lambda: self.key_menu_com("F10"))

                                action5 = QAction("END", self)
                                action5.triggered.connect(lambda: self.key_menu_com("END"))

                                key_menu.addAction(action1)
                                key_menu.addAction(action2)
                                key_menu.addAction(action3)
                                key_menu.addAction(action4)
                                key_menu.addAction(action5)
                                return key_menu

                            def action_Clicked(self,key):
                                self.sort = key
                                self._3pushButton_4.setText(f"设置启停快捷键({self.sort})")

                            def key_menu_com(self,key):
                                self.end_key = key
                                self.end_key_button.setText(f"{key}")

                            def delete_file(self):
                                if (self.button_file.text() not in ('选择配置文件', '暂无配置文件 需要创建')):
                                    result = pyautogui.confirm("你确定要删除配置文件吗？")
                                    if result == "OK":
                                        os.remove('./scripts/' + self.button_file.text())
                                        self.populateMenu()
                                        # 列出文件夹中的所有文件和文件夹
                                        files_in_folder = os.listdir("scripts")
                                        # 检查文件夹中是否有文件
                                        if len(files_in_folder) == 0:
                                            txt = "暂无配置文件 需要创建"
                                        else:
                                            txt = '选择配置文件'
                                        self.button_file.setText(txt)

                            def onPushButtonClicked(self, types):
                                if types == "handle":
                                    if self.toolTipVisible:
                                        QtWidgets.QToolTip.hideText()
                                        self.toolTipVisible = False
                                    else:
                                        QtWidgets.QToolTip.showText(
                                            self.pushButton_tooltip_handle.mapToGlobal(QtCore.QPoint()),
                                            "使用句柄进行消息发送:\n需要先点击取值按钮 然后再点击QQ聊天窗口 就可以发送消息了\n有时可能会发送失败 需打开任务管理器将QQ其他进程关闭\n只保留聊天框进程",
                                            self.pushButton_tooltip_handle)
                                        self.toolTipVisible = True

                                elif types == "qq":
                                    if self.QQtoolTipVisible:
                                        QtWidgets.QToolTip.hideText()
                                        self.QQtoolTipVisible = False
                                    else:
                                        QtWidgets.QToolTip.showText(
                                            self.pushButton_tooltip_qq.mapToGlobal(QtCore.QPoint()),
                                            "此功能的作用是在群聊窗口中先输入\n@符号再输入QQ号来达到at功能 发送\n出去的内容将是qq号+复制的内容 该\n功能的作用是在群聊中对某位用户进\n行特定提醒 若选中输入后缀则在内容\n末尾添加本次发送的次数",
                                            self.pushButton_tooltip_qq)
                                        self.QQtoolTipVisible = True
                                elif types == "copy":
                                    if self.CopytoolTipVisible:
                                        QtWidgets.QToolTip.hideText()
                                        self.CopytoolTipVisible = False
                                    else:
                                        QtWidgets.QToolTip.showText(
                                        self.pushButton_tooltip_copy.mapToGlobal(QtCore.QPoint()),
                                        "此功能的作用是在群聊中发送复制的内容\n此功能需要先复制要发送的内容\n点击开始发送将自动粘贴\n要发送的内容到聊天框中\n发送前仍需要先设置位置",
                                        self.pushButton_tooltip_copy)
                                        self.CopytoolTipVisible = True

                            def populateMenu(self, folder_path="scripts"):
                                # 清空现有菜单项并填充新的菜单项
                                self.file_menu.clear()
                                files = [f for f in os.listdir(folder_path) if
                                         os.path.isfile(os.path.join(folder_path, f))]
                                for file in files:
                                    action = self.file_menu.addAction(file)
                                    action.triggered.connect(lambda checked, f=file: self.updateButtonText(f))

                            def create_file(self):
                                files_in_folder = os.listdir("scripts")
                                if len(files_in_folder) == 0:
                                    txt = "选择配置文件"
                                    self.button_file.setText(txt)
                                file_name = self.file_lineEdit.text()
                                directory = './scripts/'
                                full_path = os.path.join(directory, file_name)
                                with open(full_path, 'w') as file:
                                    pass
                                self.update_filename()
                                self.populateMenu()

                            def update_filename(self):
                                current_name = self.file_lineEdit.text()
                                parts = current_name.split('-')
                                if len(parts) == 4:
                                    number = int(parts[3].replace('.txt', ''))
                                    new_number = number + 1
                                    new_name = f"{parts[0]}-{parts[1]}-{parts[2]}-{new_number:02d}.txt"
                                    self.file_lineEdit.setText(new_name)

                            def showMenu(self):
                                self.file_menu.exec_(self.button_file.mapToGlobal(QtCore.QPoint(0, self.button_file.height())))

                            def updateButtonText(self, file_name):
                                # 更新按钮文本
                                self.button_file.setText(file_name)

                            def generate_initial_filename(self):
                                date_str = datetime.now().strftime("%Y-%m-%d")
                                directory = './scripts/'
                                if not os.path.exists(directory):
                                    os.makedirs(directory)
                                files = [f for f in os.listdir(directory) if
                                         f.startswith(date_str) and f.endswith('.txt')]
                                max_number = 0
                                for file in files:
                                    parts = file.replace('.txt', '').split('-')
                                    if len(parts) == 4:
                                        try:
                                            number = int(parts[3])
                                            if number > max_number:
                                                max_number = number
                                        except ValueError:
                                            continue
                                next_number = max_number + 1
                                return f"{date_str}-{next_number:02d}.txt"

                            def label_page1(self):
                                font_11 = QtGui.QFont()
                                font_11.setFamily("等线")
                                font_11.setPointSize(11)
                                self.LClick_Radio = QtWidgets.QRadioButton(self.page_1)
                                self.LClick_Radio.setGeometry(QtCore.QRect(100, 70, 80, 21))
                                self.LClick_Radio.setObjectName("LClick_Radio")
                                self.LClick_Radio.setText("鼠标左键")
                                self.LClick_Radio.setChecked(True)
                                self.MClick_Radio = QtWidgets.QRadioButton(self.page_1)
                                self.MClick_Radio.setGeometry(QtCore.QRect(190, 70, 80, 21))
                                self.MClick_Radio.setObjectName("MClick_Radio")
                                self.MClick_Radio.setText("鼠标中键")
                                self.RClick_Radio = QtWidgets.QRadioButton(self.page_1)
                                self.RClick_Radio.setGeometry(QtCore.QRect(280, 70, 80, 21))
                                self.RClick_Radio.setObjectName("RClick_Radio")
                                self.RClick_Radio.setText("鼠标右键")

                                self.Sort_Click = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
                                self.Sort_Click.setGeometry(QtCore.QRect(25, 70, 60, 21))
                                self.Sort_Click.setObjectName("Sort_Click")
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(11)
                                self.Sort_Click.setFont(font)
                                self.Sort_Click.setText("点击类型:")

                                self._3label_5 = QtWidgets.QLabel(self.page_1)
                                self._3label_5.setGeometry(QtCore.QRect(25, 20, 101, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self._3label_5.setFont(font)
                                self._3label_5.setObjectName("_3label_5")
                                self._3label_5.setText("连点功能")

                                self._3label_8 = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
                                self._3label_8.setGeometry(QtCore.QRect(25, 120, 101, 21))
                                self._3label_8.setObjectName("_3label_8")
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(11)
                                self._3label_8.setFont(font)
                                self._3label_8.setText("点间隔时间:")

                                self._3D = QtWidgets.QDoubleSpinBox(self.page_1)  # 连点每次间隔
                                self._3D.setGeometry(QtCore.QRect(130, 120, 150, 22))
                                self._3D.setMinimum(0.001)
                                self._3D.setValue(0.1)
                                self._3D.setDecimals(3)
                                self._3D.setMaximum(1000)
                                self._3D.setObjectName("_3D")
                                self._3D.setSingleStep(0.05)
                                self._3D.setStyleSheet("""
                                                                QDoubleSpinBox {
                                                                                                                                                border: 1px solid gray;
                                                                                                                                                border-radius: 3px;  /* 设置圆角 */
                                                                                                                                                background: transparent;
                                                                                                                                                font: 14px;
                                                                                                                                                font-family: Calibri;
                                                                                                                                            }
                                                                                                                                            QDoubleSpinBox::up-button {
                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                subcontrol-position: top right; 
                                                                                                                                                width: 13px; 
                                                                                                                                                border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                            }
                                                                                                                                            QDoubleSpinBox::down-button {
                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                subcontrol-position: bottom right; 
                                                                                                                                                width: 13px; 
                                                                                                                                                border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                            }""")

                                self._3pushButton_4 = QtWidgets.QPushButton(self.page_1)  # 左键点击
                                self._3pushButton_4.setGeometry(QtCore.QRect(25, 170, 150, 35))
                                self._3pushButton_4.setObjectName("_3pushButton_4")
                                self._3pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton_4.setText(f"设置启停快捷键({self.sort})")
                                self._3pushButton_4.setStyleSheet("""
                                                                                                        QPushButton {
                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                        }
                                                                                                        QPushButton:hover {
                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                        }
                                                                                                    """)

                                self._3pushButton_6 = QtWidgets.QPushButton(self.page_1)  # 左键点击
                                self._3pushButton_6.setGeometry(QtCore.QRect(180, 170, 125, 35))
                                self._3pushButton_6.setObjectName("_3pushButton_6")
                                self._3pushButton_6.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton_6.setText("开启连点器")
                                self._3pushButton_6.setStyleSheet("""
                                                                                                        QPushButton {
                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                        }
                                                                                                        QPushButton:hover {
                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                        }
                                                                                                    """)

                                self._3pushButton_7 = QtWidgets.QPushButton(self.page_1)  # 连点器
                                self._3pushButton_7.setGeometry(QtCore.QRect(310, 170, 50, 35))
                                self._3pushButton_7.setObjectName("_3pushButton_7")
                                self._3pushButton_7.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton_7.setText("关闭")
                                self._3pushButton_7.setStyleSheet("""
                                                                                                                                            QPushButton {
                                                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                                                            }
                                                                                                                                            QPushButton:hover {
                                                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                            }
                                                                                                                                        """)
                                self._3pushButton_7.setVisible(False)

                                self.problem_label = QtWidgets.QLabel(self.page_1)
                                self.problem_label.setGeometry(QtCore.QRect(25, 220, 320, 40))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(11)
                                self.problem_label.setFont(font)
                                self.problem_label.setObjectName("problem_label")
                                self.problem_label.setOpenExternalLinks(True)
                                self.problem_label.setText("若开启连点器后提示dll缺失<br><a href='https://wwt.lanzout.com/i1Sbx1uur2ta'>请安装运行库后再次尝试</a>")

                                self.auto_label = QtWidgets.QLabel(self.page_1)
                                self.auto_label.setGeometry(QtCore.QRect(25, 280, 150, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self.auto_label.setFont(font)
                                self.auto_label.setObjectName("auto_label")
                                self.auto_label.setText("自动脚本功能")

                                self.ques_label = QtWidgets.QLabel(self.page_1)
                                self.ques_label.setGeometry(QtCore.QRect(390, 10, 150, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self.ques_label.setFont(font)
                                color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
                                self.ques_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                                self.ques_label.setObjectName("ques_label")
                                self.ques_label.setText("常见问题:")

                                self.quest_label = QtWidgets.QLabel(self.page_1)
                                self.quest_label.setGeometry(QtCore.QRect(390, 30, 350, 200))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.quest_label.setFont(font)
                                self.quest_label.setObjectName("quest_label")
                                self.quest_label.setText("目前是使用C++的exe进行调用的 最高速度大概为400/S \n\n"
                                                         "自动脚本功能需要先点击记录按钮记录操作 esc退出记录\n"
                                                         "在记录和执行自动脚本之前需要选择配置文件\n"
                                                         "自动脚本功能的部分按键可能无法生效\n"
                                                         "该功能会储存配置到本地 下次启动软件也还可以使用\n目前该功能执行的时间可能会比记录的时间长\n因为Python语言执行效率低 后期考虑优化\n目前实际执行会比记录的时间长5~20%左右\n\n点击助手可以查看很多信息")

                                self.label_auto = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
                                self.label_auto.setGeometry(QtCore.QRect(25, 350, 101, 21))
                                self.label_auto.setObjectName("label_auto")
                                self.label_auto.setFont(font_11)
                                self.label_auto.setText("配置文件")

                                self.reflash = QtWidgets.QPushButton(self.page_1)
                                self.reflash.setGeometry(QtCore.QRect(260, 350, 24, 24))
                                self.reflash.setObjectName("reflash")
                                self.reflash.setToolTip('刷新')
                                self.reflash.setStyleSheet("QPushButton#reflash {"
                                               "    border-image: url(./image/Component/刷新.png);"
                                               "}")

                                self.file_menu = QMenu(self)
                                self.populateMenu('scripts')  # 替换为实际文件夹路径

                                # 列出文件夹中的所有文件和文件夹
                                files_in_folder = os.listdir("scripts")

                                # 检查文件夹中是否有文件
                                if len(files_in_folder) == 0:
                                    txt = "暂无配置文件 需要创建"
                                else:
                                    txt = '选择配置文件'

                                self.button_file = QPushButton(txt, self.page_1)
                                self.button_file.setGeometry(100, 350, 150, 25)
                                self.button_file.setIcon(QIcon('./image/Component/箭头 下.png'))  # 确保有这个图标文件或使用适当的替代
                                self.button_file.clicked.connect(self.showMenu)

                                self.label_new = QtWidgets.QLabel(self.page_1)  # 左键每秒点击次数
                                self.label_new.setGeometry(QtCore.QRect(25, 400, 101, 21))
                                self.label_new.setObjectName("label_new")
                                self.label_new.setFont(font_11)
                                self.label_new.setText("新建配置文件")

                                self.file_lineEdit = QtWidgets.QLineEdit(self.page_1)
                                self.file_lineEdit.setGeometry(QtCore.QRect(130, 400, 150, 20))
                                self.file_lineEdit.setObjectName("file_lineEdit")
                                self.file_lineEdit.setStyleSheet("background: transparent;")
                                self.file_lineEdit.setPlaceholderText("输入文件名称")
                                self.file_lineEdit.setText(self.generate_initial_filename())

                                self.button_create = QtWidgets.QPushButton(self.page_1)
                                self.button_create.setGeometry(QtCore.QRect(280, 400, 50, 20))
                                self.button_create.setObjectName("button_create")
                                self.button_create.setCursor(QCursor(Qt.PointingHandCursor))
                                self.button_create.setText("创建")
                                self.button_create.setStyleSheet("QPushButton#button_create {"
                                                                 "background-color: #3498db;"  # Blue background color
                                                                 "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                 "color: white;"
                                                                 "padding: 300px 300px;"
                                                                 "text-align: center;"
                                                                 "text-decoration: none;"
                                                                 "font-size: 13px;"
                                                                 "font-family: SimSun, Arial, sans-serif;"
                                                                 "}")

                                self._3pushButton = QtWidgets.QPushButton(self.page_1)
                                self._3pushButton.setGeometry(QtCore.QRect(25, 510, 110, 30))
                                self._3pushButton.setObjectName("_3pushButton")
                                self._3pushButton.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton.setText("记录自动脚本")
                                self._3pushButton.setStyleSheet("QPushButton#_3pushButton {"
                                                                "background-color: #3498db;"  # Blue background color
                                                                "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                "color: white;"
                                                                "padding: 300px 300px;"
                                                                "text-align: center;"
                                                                "text-decoration: none;"
                                                                "font-size: 13px;"
                                                                "font-family: SimSun, Arial, sans-serif;"
                                                                "}")

                                self._3pushButton_2 = QtWidgets.QPushButton(self.page_1)
                                self._3pushButton_2.setGeometry(QtCore.QRect(160, 510, 110, 30))
                                self._3pushButton_2.setObjectName("_3pushButton_2")
                                self._3pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton_2.setText("执行自动脚本")
                                self._3pushButton_2.setStyleSheet("QPushButton#_3pushButton_2 {"
                                                                  "background-color: #4667ff;"  # Blue background color
                                                                  "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                  "color: white;"
                                                                  "padding: 300px 300px;"
                                                                  "text-align: center;"
                                                                  "text-decoration: none;"
                                                                  "font-size: 13px;"
                                                                  "font-family: SimSun, Arial, sans-serif;"
                                                                  "}")

                                self._3label_10 = QtWidgets.QLabel(self.page_1)  #
                                self._3label_10.setGeometry(QtCore.QRect(25, 450, 60, 21))
                                self._3label_10.setObjectName("_3label_10")
                                self._3label_10.setFont(font_11)
                                self._3label_10.setText("执行次数:")

                                self._3label_11 = QtWidgets.QLabel(self.page_1)
                                self._3label_11.setGeometry(QtCore.QRect(360, 400, 150, 21))
                                self._3label_11.setObjectName("_3label_11")
                                self._3label_11.setFont(font_11)
                                self._3label_11.setText("等待/秒后 记录/执行:")

                                self._3spinBox_3 = QtWidgets.QSpinBox(self.page_1)  # 自动脚本执行次数
                                self._3spinBox_3.setGeometry(QtCore.QRect(110, 450, 60, 22))
                                self._3spinBox_3.setMaximum(9999)
                                self._3spinBox_3.setValue(1)
                                self._3spinBox_3.setObjectName("_3spinBox_3")
                                self._3spinBox_3.setStyleSheet("""
                                                                                                                                                                            QSpinBox {
                                                                                                                                                                                border: 1px solid gray;
                                                                                                                                                                                border-radius: 3px;  /* 设置圆角 */
                                                                                                                                                                                background: transparent;
                                                                                                                                                                                font: 14px;
                                                                                                                                                                                font-family: Calibri;
                                                                                                                                                                            }
                                                                                                                                                                            QSpinBox::up-button {
                                                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                                                subcontrol-position: top right; 
                                                                                                                                                                                width: 13px; 
                                                                                                                                                                                border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                                                            }
                                                                                                                                                                            QSpinBox::down-button {
                                                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                                                subcontrol-position: bottom right; 
                                                                                                                                                                                width: 13px; 
                                                                                                                                                                                border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                                                            }
                                                                                                                                                                        """)

                                self.wait_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_1)  # 自动脚本等待执行时间
                                self.wait_doubleSpinBox.setGeometry(QtCore.QRect(510, 400, 60, 22))
                                self.wait_doubleSpinBox.setMaximum(1000)
                                self.wait_doubleSpinBox.setMinimum(0)
                                self.wait_doubleSpinBox.setValue(0)
                                self.wait_doubleSpinBox.setObjectName("wait_doubleSpinBox")
                                self.wait_doubleSpinBox.setStyleSheet("""
                                                                                                                                                                            QDoubleSpinBox {
                                                                                                                                                                                border: 1px solid gray;
                                                                                                                                                                                border-radius: 3px;  /* 设置圆角 */
                                                                                                                                                                                background: transparent;
                                                                                                                                                                                font: 14px;
                                                                                                                                                                                font-family: Calibri;
                                                                                                                                                                            }
                                                                                                                                                                            QDoubleSpinBox::up-button {
                                                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                                                subcontrol-position: top right; 
                                                                                                                                                                                width: 13px; 
                                                                                                                                                                                border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                                                            }
                                                                                                                                                                            QDoubleSpinBox::down-button {
                                                                                                                                                                                subcontrol-origin: border;
                                                                                                                                                                                subcontrol-position: bottom right; 
                                                                                                                                                                                width: 13px; 
                                                                                                                                                                                border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                                                            }
                                                                                                                                                                        """)

                                self._3pushButton_5 = QtWidgets.QPushButton(self.page_1)
                                self._3pushButton_5.setGeometry(QtCore.QRect(360, 350, 91, 23))
                                self._3pushButton_5.setObjectName("_3pushButton_4")
                                self._3pushButton_5.setCursor(QCursor(Qt.PointingHandCursor))
                                self._3pushButton_5.setText("点击助手")
                                self._3pushButton_5.setStyleSheet("""
                                                                                                                                                                            QPushButton {
                                                                                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                                            }
                                                                                                                                                                            QPushButton:hover {
                                                                                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                                            }
                                                                                                                                                                        """)

                                self.impor_button = QtWidgets.QPushButton(self.page_1)
                                self.impor_button.setGeometry(QtCore.QRect(360, 510, 180, 23))
                                self.impor_button.setObjectName("impor_button")
                                self.impor_button.setCursor(QCursor(Qt.PointingHandCursor))
                                self.impor_button.setText("编辑选中的配置文件")
                                self.impor_button.setStyleSheet("""
                                                                                                                                                                            QPushButton {
                                                                                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                                            }
                                                                                                                                                                            QPushButton:hover {
                                                                                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                                            }
                                                                                                                                                                        """)

                                self.delete_button = QtWidgets.QPushButton(self.page_1)
                                self.delete_button.setGeometry(QtCore.QRect(550, 510, 180, 23))
                                self.delete_button.setObjectName("delete_button")
                                self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
                                self.delete_button.setText("删除选中的配置文件")
                                self.delete_button.setStyleSheet("""
                                                                                                                                                                                                            QPushButton {
                                                                                                                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                                                                            }
                                                                                                                                                                                                            QPushButton:hover {
                                                                                                                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                                                                            }
                                                                                                                                                                                                        """)

                                self.label_end = QtWidgets.QLabel(self.page_1)
                                self.label_end.setGeometry(QtCore.QRect(360, 450, 130, 21))
                                self.label_end.setObjectName("label_end")
                                self.label_end.setFont(font_11)
                                self.label_end.setText("设置结束录制按键")

                                self.end_key_button = QtWidgets.QPushButton(self.page_1)  # 结束按键设置
                                self.end_key_button.setGeometry(QtCore.QRect(510, 450, 70, 25))
                                self.end_key_button.setObjectName("end_key_button")
                                self.end_key_button.setCursor(QCursor(Qt.PointingHandCursor))
                                self.end_key_button.setText(f"{self.end_key}")
                                self.end_key_button.setStyleSheet("""
                                                                                                                                        QPushButton {
                                                                                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                                                                                        }
                                                                                                                                        QPushButton:hover {
                                                                                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                        }
                                                                                                                                    """)

                            def label_page2(self):
                                self._2label_7 = QtWidgets.QLabel(self.page_2)
                                self._2label_7.setGeometry(QtCore.QRect(20, 270, 151, 30))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(16)
                                self._2label_7.setFont(font)
                                self._2label_7.setObjectName("_2label_7")
                                self._2label_7.setText("句柄式发送消息")

                                self.pushButton_tooltip_handle = QtWidgets.QPushButton(self.page_2)
                                self.pushButton_tooltip_handle.setGeometry(QtCore.QRect(180, 275, 24, 24))
                                self.pushButton_tooltip_handle.setStyleSheet("QPushButton {"
                                                                             "    border-image: url(./image/Component/提示3.png);"
                                                                             "    background-color: rgba(245,245,245,0);"

                                                                             "}")
                                self.toolTipVisible = False
                                self.pushButton_tooltip_handle.setToolTip(
                                    "使用句柄进行消息发送:\n需要先点击取值按钮 然后再点击QQ聊天窗口 就可以发送消息了\n有时可能会发送失败 需打开任务管理器将QQ其他进程关闭\n只保留聊天框进程")

                                self._2label_8 = QtWidgets.QLabel(self.page_2)
                                self._2label_8.setGeometry(QtCore.QRect(20, 300, 51, 21))
                                self._2label_8.setObjectName("_2label_8")
                                self._2label_8.setText("句柄:")

                                self._2lineEdit_3 = QtWidgets.QLineEdit(self.page_2)  # 句柄值输入框
                                self._2lineEdit_3.setGeometry(QtCore.QRect(20, 330, 60, 20))
                                self._2lineEdit_3.setObjectName("_2lineEdit_3")
                                self._2lineEdit_3.setStyleSheet("background: transparent;")
                                self._2lineEdit_3.setPlaceholderText("句柄值")

                                self._2pushButton2 = QtWidgets.QPushButton(self.page_2)  # 获取句柄值
                                self._2pushButton2.setGeometry(QtCore.QRect(85, 329, 200, 23))
                                self._2pushButton2.setObjectName("_2pushButton2")
                                self._2pushButton2.setCursor(QCursor(Qt.PointingHandCursor))
                                self._2pushButton2.setText("点击按钮后单击聊天窗口获取句柄")
                                self._2pushButton2.setStyleSheet("""
                                                                                                                                        QPushButton {
                                                                                                                                            border: 2px solid #CDCDCD;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                                                                                            border-radius: 5px;    /* 设置圆角 */
                                                                                                                                        }
                                                                                                                                        QPushButton:hover {
                                                                                                                                            background-color: #CDCDCD;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                            border: 1px solid #CDCDCD;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                        }
                                                                                                                                    """)

                                self._2label_10 = QtWidgets.QLabel(self.page_2)  # 句柄发送次数
                                self._2label_10.setGeometry(QtCore.QRect(20, 360, 54, 12))
                                self._2label_10.setObjectName("_2label_10")
                                self._2label_10.setText("次数:")

                                self._2spinBox = QtWidgets.QSpinBox(self.page_2)  # 句柄式发送次数
                                self._2spinBox.setGeometry(QtCore.QRect(20, 380, 60, 22))
                                self._2spinBox.setMaximum(9999)
                                self._2spinBox.setValue(10)
                                self._2spinBox.setObjectName("_2spinBox")
                                self._2spinBox.setStyleSheet("""
                                                                                                                                                                        QSpinBox {
                                                                                                                                                                            border: 1px solid gray;
                                                                                                                                                                            border-radius: 3px;  /* 设置圆角 */
                                                                                                                                                                            background: transparent;
                                                                                                                                                                            font: 14px;
                                                                                                                                                                            font-family: Calibri;
                                                                                                                                                                        }
                                                                                                                                                                        QSpinBox::up-button {
                                                                                                                                                                            subcontrol-origin: border;
                                                                                                                                                                            subcontrol-position: top right;
                                                                                                                                                                            width: 13px;
                                                                                                                                                                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                                                        }
                                                                                                                                                                        QSpinBox::down-button {
                                                                                                                                                                            subcontrol-origin: border;
                                                                                                                                                                            subcontrol-position: bottom right;
                                                                                                                                                                            width: 13px;
                                                                                                                                                                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                                                        }
                                                                                                                                                                    """)
                                self._2spinBox.setMinimum(1)

                                self._2textEdit = QtWidgets.QTextEdit(self.page_2)  # 句柄发送内容
                                self._2textEdit.setGeometry(QtCore.QRect(20, 430, 280, 110))
                                self._2textEdit.setObjectName("_2textEdit")
                                self._2textEdit.setStyleSheet("background: transparent;")
                                self._2textEdit.setPlaceholderText("输入需要发送的内容")

                                self._2label_9 = QtWidgets.QLabel(self.page_2)  # 内容提示
                                self._2label_9.setGeometry(QtCore.QRect(20, 410, 111, 16))
                                self._2label_9.setObjectName("_2label_9")
                                self._2label_9.setText("需要发送的内容:")

                                self._2pushButton_3 = QtWidgets.QPushButton(self.page_2)  # 句柄式发送消息
                                self._2pushButton_3.setGeometry(QtCore.QRect(20, 550, 280, 31))
                                self._2pushButton_3.setObjectName("_2pushButton_3")
                                self._2pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
                                self._2pushButton_3.setText("开始发送")
                                self._2pushButton_3.setStyleSheet("QPushButton#_2pushButton_3 {"
                                                                  "background-color: #3498db;"  # Blue background color
                                                                  "border-radius: 5px;"  # 10px border radius for rounded corners
                                                                  "color: white;"
                                                                  "padding: 100px 100px;"
                                                                  "text-align: center;"
                                                                  "text-decoration: none;"
                                                                  "font-size: 13px;"
                                                                  "font-family: SimSun, Arial, sans-serif;"
                                                                  "}")

                                self._2label = QtWidgets.QLabel(self.page_2)
                                self._2label.setGeometry(QtCore.QRect(20, 15, 100, 20))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(16)
                                self._2label.setFont(font)
                                self._2label.setObjectName("_2label")
                                self._2label.setText("@QQ功能")

                                self.pushButton_tooltip_qq = QtWidgets.QPushButton(self.page_2)
                                self.pushButton_tooltip_qq.setGeometry(QtCore.QRect(120, 15, 24, 24))
                                self.pushButton_tooltip_qq.setStyleSheet("QPushButton {"
                                                                         "    border-image: url(./image/Component/提示3.png);"
                                                                         "    background-color: rgba(245,245,245,0);"
                                                                         "}")
                                self.QQtoolTipVisible = False
                                self.pushButton_tooltip_qq.setToolTip(
                                    "此功能的作用是在群聊窗口中先输入\n@符号再输入QQ号来达到at功能 发送\n出去的内容将是qq号+复制的内容 该\n功能的作用是在群聊中对某位用户进\n行特定提醒 若选中输入后缀则在内容\n末尾添加本次发送的次数")

                                self._2label_2 = QtWidgets.QLabel(self.page_2)
                                self._2label_2.setGeometry(QtCore.QRect(20, 65, 50, 21))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._2label_2.setFont(font)
                                self._2label_2.setObjectName("_2label_2")
                                self._2label_2.setText("QQ号:")

                                self._2lineEdit = QtWidgets.QLineEdit(self.page_2)
                                self._2lineEdit.setGeometry(QtCore.QRect(70, 65, 140, 20))
                                self._2lineEdit.setObjectName("_2lineEdit")
                                self._2lineEdit.setStyleSheet("background: transparent;")
                                self._2lineEdit.setPlaceholderText("点击输入需要@的QQ号")

                                self._2label_3 = QtWidgets.QLabel(self.page_2)
                                self._2label_3.setGeometry(QtCore.QRect(20, 125, 101, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(11)
                                self._2label_3.setFont(font)
                                self._2label_3.setObjectName("_2label_3")
                                self._2label_3.setText("发送间隔/每次:")

                                self._2doubleSpinBox = QtWidgets.QDoubleSpinBox(self.page_2)
                                self._2doubleSpinBox.setGeometry(QtCore.QRect(130, 125, 62, 21))
                                self._2doubleSpinBox.setMinimum(0.05)
                                self._2doubleSpinBox.setValue(0.05)
                                self._2doubleSpinBox.setObjectName("_2doubleSpinBox")
                                self._2doubleSpinBox.setSingleStep(0.05)
                                self._2doubleSpinBox.setStyleSheet("""
                                                                                                                                        QDoubleSpinBox {
                                                                                                                                            border: 1px solid gray;
                                                                                                                                            border-radius: 3px;  /* 设置圆角 */
                                                                                                                                            background: transparent;
                                                                                                                                            font: 14px;
                                                                                                                                            font-family: Calibri;
                                                                                                                                        }
                                                                                                                                        QDoubleSpinBox::up-button {
                                                                                                                                            subcontrol-origin: border;
                                                                                                                                            subcontrol-position: top right; 
                                                                                                                                            width: 13px; 
                                                                                                                                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                        }
                                                                                                                                        QDoubleSpinBox::down-button {
                                                                                                                                            subcontrol-origin: border;
                                                                                                                                            subcontrol-position: bottom right; 
                                                                                                                                            width: 13px; 
                                                                                                                                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                        }
                                                                                                                                    """)

                                self._2checkBox = QtWidgets.QCheckBox(self.page_2)
                                self._2checkBox.setGeometry(QtCore.QRect(20, 170, 121, 21))
                                self._2checkBox.setObjectName("_2checkBox")
                                self._2checkBox.setText("输入数字后缀")
                                self._2checkBox.setToolTip("选中后 在发送时将在内容后添加此次发送的数字序号")

                                self._2pushButton = QtWidgets.QPushButton(self.page_2)  # QQ@功能
                                self._2pushButton.setGeometry(QtCore.QRect(20, 220, 180, 23))
                                self._2pushButton.setObjectName("_2pushButton")
                                self._2pushButton.setCursor(QCursor(Qt.PointingHandCursor))
                                self._2pushButton.setText("开始发送")
                                self._2pushButton.setStyleSheet("QPushButton#_2pushButton {"
                                                                "background-color: #3498db;"  # Blue background color
                                                                "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                "color: white;"
                                                                "padding: 300px 300px;"
                                                                "text-align: center;"
                                                                "text-decoration: none;"
                                                                "font-size: 13px;"
                                                                "font-family: SimSun, Arial, sans-serif;"
                                                                "}")

                                self.label_position_status = QtWidgets.QLabel(self.page_2)
                                self.label_position_status.setGeometry(QtCore.QRect(240, 120, 150, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.label_position_status.setFont(font)
                                self.label_position_status.setObjectName("label_position_status")
                                if position_status == False:
                                    self.label_position_status.setText(
                                        '<font color="black">位置设置：</font> <font color="red">未设置</font>')
                                else:
                                    self.label_position_status.setText(
                                        '<font color="black">位置设置：</font> <font color="green">已设置</font>')

                                self.label_positions = QtWidgets.QLabel(self.page_2)
                                self.label_positions.setGeometry(QtCore.QRect(240, 90, 160, 21))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(10)
                                self.label_positions.setFont(font)
                                self.label_positions.setObjectName("_2label_2")
                                self.label_positions.setText("需要先设置位置才能发送")

                                self.label_position_text = QtWidgets.QLabel(self.page_2)
                                self.label_position_text.setGeometry(QtCore.QRect(240, 150, 180, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.label_position_text.setFont(font)
                                self.label_position_text.setObjectName("label_position_text")
                                if position_status == False:
                                    self.label_position_text.setText(
                                        f'<font color="black">聊天框位置：</font> <font color="red">{textedit_position}</font>')
                                else:
                                    self.label_position_text.setText(
                                        f'<font color="black">聊天框位置：</font> <font color="green">{textedit_position}</font>')

                                self.label_position_send = QtWidgets.QLabel(self.page_2)
                                self.label_position_send.setGeometry(QtCore.QRect(240, 180, 180, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.label_position_send.setFont(font)
                                self.label_position_send.setObjectName("label_position_send")
                                if position_status == False:
                                    self.label_position_send.setText(
                                        f'<font color="black">发送键位置：</font> <font color="red">{send_position}</font>')
                                else:
                                    self.label_position_send.setText(
                                        f'<font color="black">发送键位置：</font> <font color="green">{send_position}</font>')

                                '''self._2pushButton_5 = QtWidgets.QPushButton(self.page_2)
                                self._2pushButton_5.setGeometry(QtCore.QRect(380, 520, 121, 31))
                                self._2pushButton_5.setObjectName("_2pushButton_5")
                                self._2pushButton_5.setCursor(QCursor(Qt.PointingHandCursor))
                                self._2pushButton_5.setText("发送快捷消息")
                                self._2pushButton_5.setStyleSheet("QPushButton#_2pushButton_5 {"
                                                                  "background-color: #3498db;"  # Blue background color
                                                                  "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                  "color: white;"
                                                                  "padding: 100px 100px;"
                                                                  "text-align: center;"
                                                                  "text-decoration: none;"
                                                                  "font-size: 13px;"
                                                                  "font-family: SimSun, Arial, sans-serif;"
                                                                  "}")'''

                                self.record_position_button = QtWidgets.QPushButton(self.page_2)
                                self.record_position_button.setGeometry(QtCore.QRect(240, 220, 160, 25))
                                self.record_position_button.setObjectName("record_position_button")
                                self.record_position_button.setCursor(QCursor(Qt.PointingHandCursor))
                                self.record_position_button.setText("记录按钮位置")
                                self.record_position_button.setStyleSheet("QPushButton#record_position_button {"
                                                                          "background-color: #3498db;"  # Blue background color
                                                                          "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                          "color: white;"
                                                                          "padding: 300px 300px;"
                                                                          "text-align: center;"
                                                                          "text-decoration: none;"
                                                                          "font-size: 13px;"
                                                                          "font-family: SimSun, Arial, sans-serif;"
                                                                          "}")
                                self.record_position_button.clicked.connect(self.open_record_window)

                                self._2label_4 = QtWidgets.QLabel(self.page_2)
                                self._2label_4.setGeometry(QtCore.QRect(515, 10, 100, 20))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(16)
                                self._2label_4.setFont(font)
                                color = QtGui.QColor(29, 84, 237)  # 使用RGB值设置颜色为红色
                                self._2label_4.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
                                self._2label_4.setObjectName("_2label_4")
                                self._2label_4.setText("常见问题:")

                                self._2label_5 = QtWidgets.QLabel(self.page_2)
                                self._2label_5.setGeometry(QtCore.QRect(520, 40, 200, 200))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._2label_5.setFont(font)
                                self._2label_5.setObjectName("_2label_5")
                                self._2label_5.setText("退出方法:若发送完毕需要退出时\n长按F10即可退出 \n或者按下ctrl+alt+del即可关闭\n"
                                                       "有时可能会出现延时关闭的情况\n句柄发送消息需要将聊天框最大化\n然后点击按钮获取句柄\n最后点击开始发送即可完成!\n当此窗口置顶时 可能会发送失败")

                                self._2label_6 = QtWidgets.QLabel(self.page_2)
                                self._2label_6.setGeometry(QtCore.QRect(390, 285, 100, 20))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(16)
                                self._2label_6.setFont(font)
                                self._2label_6.setObjectName("_2label_6")
                                self._2label_6.setText("其他功能")

                                self.label_copy = QtWidgets.QLabel(self.page_2)
                                self.label_copy.setGeometry(QtCore.QRect(390, 330, 140, 20))
                                font = QtGui.QFont()
                                font.setFamily("黑体")
                                font.setPointSize(13)
                                self.label_copy.setFont(font)
                                self.label_copy.setObjectName("label_copy")
                                self.label_copy.setText("复制内容发送")

                                self.pushButton_tooltip_copy = QtWidgets.QPushButton(self.page_2)
                                self.pushButton_tooltip_copy.setGeometry(QtCore.QRect(510, 330, 24, 24))
                                self.pushButton_tooltip_copy.setStyleSheet("QPushButton {"
                                                                         "    border-image: url(./image/Component/提示3.png);"
                                                                         "    background-color: rgba(245,245,245,0);"
                                                                         "}")
                                self.CopytoolTipVisible = False
                                self.pushButton_tooltip_copy.setToolTip(
                                    "此功能的作用是在群聊中发送复制的内容\n此功能需要先复制要发送的内容\n点击开始发送将自动粘贴\n要发送的内容到聊天框中\n发送前仍需要先设置位置")

                                self.copy_label = QtWidgets.QLabel(self.page_2)
                                self.copy_label.setGeometry(QtCore.QRect(390, 360, 150, 12))
                                self.copy_label.setObjectName("copy_label")
                                self.copy_label.setText("复制消息发送速度 条/秒")

                                self.copy_int = QtWidgets.QSpinBox(self.page_2)  # 复制发送次数
                                self.copy_int.setGeometry(QtCore.QRect(390, 390, 60, 22))
                                self.copy_int.setMaximum(15)
                                self.copy_int.setValue(5)
                                self.copy_int.setObjectName("copy_int")
                                self.copy_int.setStyleSheet("""
                                                                                                                                        QSpinBox {
                                                                                                                                            border: 1px solid gray;
                                                                                                                                            border-radius: 3px;  /* 设置圆角 */
                                                                                                                                            background: transparent;
                                                                                                                                            font: 14px;
                                                                                                                                            font-family: Calibri;
                                                                                                                                        }
                                                                                                                                        QSpinBox::up-button {
                                                                                                                                            subcontrol-origin: border;
                                                                                                                                            subcontrol-position: top right; 
                                                                                                                                            width: 13px; 
                                                                                                                                            border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                                                        }
                                                                                                                                        QSpinBox::down-button {
                                                                                                                                            subcontrol-origin: border;
                                                                                                                                            subcontrol-position: bottom right; 
                                                                                                                                            width: 13px; 
                                                                                                                                            border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                                                        }
                                                                                                                                    """)

                                self._2pushButton_4 = QtWidgets.QPushButton(self.page_2)
                                self._2pushButton_4.setGeometry(QtCore.QRect(390, 420, 121, 31))
                                self._2pushButton_4.setObjectName("_2pushButton_4")
                                self._2pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
                                self._2pushButton_4.setText("发送复制内容")
                                self._2pushButton_4.setStyleSheet("QPushButton#_2pushButton_4 {"
                                                                  "background-color: #3498db;"  # Blue background color
                                                                  "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                  "color: white;"
                                                                  "padding: 100px 100px;"
                                                                  "text-align: center;"
                                                                  "text-decoration: none;"
                                                                  "font-size: 13px;"
                                                                  "font-family: SimSun, Arial, sans-serif;"
                                                                  "}")

                            def label_page3(self):
                                self.create_team_button = QtWidgets.QToolButton(self.page_3)
                                self.create_team_button.setGeometry(QtCore.QRect(45, 100, 260, 31))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(12)
                                self.create_team_button.setFont(font)
                                self.create_team_button.setObjectName("create_team_button")
                                self.create_team_button.setText("点击创建队伍")
                                self.create_team_button.setStyleSheet("""
                                                                        QToolButton {
                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                        }
                                                                        QToolButton:hover {
                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                        }
                                                                    """)

                                self.create_team_label = QtWidgets.QLabel(self.page_3)
                                self.create_team_label.setGeometry(QtCore.QRect(30, 20, 201, 21))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(16)
                                self.create_team_label.setFont(font)
                                self.create_team_label.setObjectName("create_team_label")
                                self.create_team_label.setText("创建队伍")

                                self.create_team_label_prompt = QtWidgets.QLabel(self.page_3)
                                self.create_team_label_prompt.setGeometry(QtCore.QRect(100, 70, 201, 21))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self.create_team_label_prompt.setFont(font)
                                self.create_team_label_prompt.setObjectName("create_team_label_prompt")
                                self.create_team_label_prompt.setText("队伍已加入！")
                                self.create_team_label_prompt.setVisible(False)

                                self._4label = QtWidgets.QLabel(self.page_3)
                                self._4label.setGeometry(QtCore.QRect(20, 60, 325, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(11)
                                self._4label.setFont(font)
                                self._4label.setObjectName("_4label")
                                self._4label.setText("队伍ID为:")
                                self._4label.setVisible(False)

                                self.add_team_label = QtWidgets.QLabel(self.page_3)
                                self.add_team_label.setGeometry(QtCore.QRect(370, 10, 111, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(16)
                                self.add_team_label.setFont(font)
                                self.add_team_label.setObjectName("add_team_label")
                                self.add_team_label.setText("加入队伍")

                                self.add_team_label_prompt = QtWidgets.QLabel(self.page_3)
                                self.add_team_label_prompt.setGeometry(QtCore.QRect(460, 70, 150, 30))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self.add_team_label_prompt.setFont(font)
                                self.add_team_label_prompt.setObjectName("add_team_label_prompt")
                                self.add_team_label_prompt.setText("队伍已加入")
                                self.add_team_label_prompt.setVisible(False)

                                self.add_team_lineEdit = QtWidgets.QLineEdit(self.page_3)
                                self.add_team_lineEdit.setGeometry(QtCore.QRect(430, 60, 280, 20))
                                self.add_team_lineEdit.setObjectName("add_team_lineEdit")
                                self.add_team_lineEdit.setStyleSheet("background: transparent;")
                                self.add_team_lineEdit.setPlaceholderText("输入队伍ID")

                                self.add_team_ID = QtWidgets.QLabel(self.page_3)
                                self.add_team_ID.setGeometry(QtCore.QRect(370, 60, 71, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(12)
                                self.add_team_ID.setFont(font)
                                self.add_team_ID.setObjectName("add_team_ID")
                                self.add_team_ID.setText("队伍ID:")

                                self.add_team_button = QtWidgets.QToolButton(self.page_3)
                                self.add_team_button.setGeometry(QtCore.QRect(370, 100, 340, 30))
                                self.add_team_button.setObjectName("add_team_button")
                                self.add_team_button.setText("加入")
                                self.add_team_button.setStyleSheet("""
                                                                        QToolButton {
                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                        }
                                                                        QToolButton:hover {
                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                        }
                                                                    """)

                                self.button_copy_id = QtWidgets.QToolButton(self.page_3)
                                self.button_copy_id.setGeometry(QtCore.QRect(45, 100, 260, 31))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(12)
                                self.button_copy_id.setFont(font)
                                self.button_copy_id.setObjectName("button_copy_id")
                                self.button_copy_id.setText("点击复制ID")
                                self.button_copy_id.setVisible(False)
                                self.button_copy_id.setStyleSheet("""
                                                                                                            QToolButton {
                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                            }
                                                                                                            QToolButton:hover {
                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                            }
                                                                                                        """)

                                self._4pushButton = QtWidgets.QPushButton(self.page_3)
                                self._4pushButton.setGeometry(QtCore.QRect(10, 180, 141, 141))
                                icon = QtGui.QIcon("./temp/HImage.png")  # 将此处的路径替换为实际的图像路径
                                scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(QtCore.QSize(141, 141),
                                                                                         QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
                                self._4pushButton.setIcon(QtGui.QIcon(scaled_icon))
                                self._4pushButton.setIconSize(QtCore.QSize(141, 141))
                                self._4pushButton.setObjectName("_4pushButton")
                                self._4label_5 = QtWidgets.QLabel(self.page_3)
                                self._4label_5.setGeometry(QtCore.QRect(160, 210, 161, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self._4label_5.setFont(font)
                                self._4label_5.setObjectName("label_5")
                                self._4label_5.setText(f"{Name}[我]")

                                self._4pushButton_2 = QtWidgets.QPushButton(self.page_3)
                                self._4pushButton_2.setGeometry(QtCore.QRect(360, 180, 141, 141))
                                icon = QtGui.QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
                                scaled_icon = icon.pixmap(QtCore.QSize(141, 141)).scaled(QtCore.QSize(141, 141),
                                                                                         QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                                                                                         QtCore.Qt.TransformationMode.SmoothTransformation)
                                self._4pushButton_2.setIcon(QtGui.QIcon(scaled_icon))
                                self._4pushButton_2.setIconSize(QtCore.QSize(141, 141))
                                self._4pushButton_2.setObjectName("pushButton_2")

                                self._4label_6 = QtWidgets.QLabel(self.page_3)
                                self._4label_6.setGeometry(QtCore.QRect(520, 210, 181, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(18)
                                self._4label_6.setFont(font)
                                self._4label_6.setObjectName("label_6")
                                self._4label_6.setText("等待用户加入")
                                self._4label_7 = QtWidgets.QLabel(self.page_3)
                                self._4label_7.setGeometry(QtCore.QRect(160, 240, 71, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(11)
                                self._4label_7.setFont(font)  # 一号id
                                self._4label_7.setObjectName("label_7")
                                self._4label_7.setText(f"ID:{Account}")
                                self._4label_8 = QtWidgets.QLabel(self.page_3)
                                self._4label_8.setGeometry(QtCore.QRect(520, 240, 71, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(11)
                                self._4label_8.setFont(font)
                                self._4label_8.setObjectName("label_8")
                                self._4label_8.setText("ID:")
                                self.team_send_handle = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_handle.setGeometry(QtCore.QRect(20, 330, 131, 16))
                                self.team_send_handle.setObjectName("team_send_handle")
                                self.team_send_handle.setText("句柄式发送消息")
                                self.team_send_handle.setChecked(True)
                                self.team_send_atqq = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_atqq.setGeometry(QtCore.QRect(20, 360, 89, 16))
                                self.team_send_atqq.setObjectName("team_send_atqq")
                                self.team_send_atqq.setText("@QQ")
                                self.team_send_copy = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_copy.setGeometry(QtCore.QRect(20, 390, 89, 16))
                                self.team_send_copy.setObjectName("team_send_copy")
                                self.team_send_copy.setText("复制消息")
                                self.team_send_renew = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_renew.setGeometry(QtCore.QRect(20, 420, 89, 16))
                                self.team_send_renew.setObjectName("team_send_renew")
                                self.team_send_renew.setText("QQ个人信息更新")
                                self.team_send_exe = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_exe.setGeometry(QtCore.QRect(20, 450, 89, 16))
                                self.team_send_exe.setObjectName("team_send_exe")
                                self.team_send_exe.setText("执行自动脚本")
                                self.buttonGroup2 = QtWidgets.QButtonGroup(self.page_3)
                                self.buttonGroup2.addButton(self.team_send_handle)
                                self.buttonGroup2.addButton(self.team_send_atqq)
                                self.buttonGroup2.addButton(self.team_send_copy)
                                self.buttonGroup2.addButton(self.team_send_renew)
                                self.buttonGroup2.addButton(self.team_send_exe)

                                self.team_send_handle_c = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_handle_c.setGeometry(QtCore.QRect(370, 330, 121, 16))
                                self.team_send_handle_c.setObjectName("team_send_handle_c")
                                self.team_send_handle_c.setText("句柄式发送消息")
                                self.team_send_handle_c.setChecked(True)
                                self.team_send_atqq_c = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_atqq_c.setGeometry(QtCore.QRect(370, 360, 89, 16))
                                self.team_send_atqq_c.setObjectName("team_send_atqq_c")
                                self.team_send_atqq_c.setText("@QQ")
                                self.team_send_copy_c = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_copy_c.setGeometry(QtCore.QRect(370, 390, 89, 16))
                                self.team_send_copy_c.setObjectName("team_send_copy_c")
                                self.team_send_copy_c.setText("复制消息")
                                self.team_send_renew_c = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_renew_c.setGeometry(QtCore.QRect(370, 420, 89, 16))
                                self.team_send_renew_c.setObjectName("team_send_renew_c")
                                self.team_send_renew_c.setText("QQ个人信息更新")
                                self.team_send_exe_c = QtWidgets.QRadioButton(self.page_3)
                                self.team_send_exe_c.setGeometry(QtCore.QRect(370, 450, 89, 16))
                                self.team_send_exe_c.setObjectName("team_send_exe_c")
                                self.team_send_exe_c.setText("执行自动脚本")
                                self.buttonGroup3 = QtWidgets.QButtonGroup(self.page_3)
                                self.buttonGroup3.addButton(self.team_send_handle_c)
                                self.buttonGroup3.addButton(self.team_send_atqq_c)
                                self.buttonGroup3.addButton(self.team_send_copy_c)
                                self.buttonGroup3.addButton(self.team_send_renew_c)
                                self.buttonGroup3.addButton(self.team_send_exe_c)
                                self.run_execute = QtWidgets.QToolButton(self.page_3)
                                self.run_execute.setGeometry(QtCore.QRect(500, 510, 161, 51))
                                self.run_execute.setObjectName("toolButton_3")
                                self.run_execute.setText("开始执行")
                                self.run_execute.setStyleSheet("""QToolButton {
                                                                                  border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                  background-color: transparent;    /* 设置透明背景 */
                                                                                  border-radius: 2px;    /* 设置圆角 */
                                                                                  }
                                                                                                                                                QToolButton:hover {
                                                                                                                                                    background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                    border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                }
                                                                                                                                            """)
                                self.run_execute.setVisible(False)
                                pass
                                
                                for button in self.buttonGroup2.buttons():
                                    button.setVisible(False)
                                for button in self.buttonGroup3.buttons():
                                    button.setVisible(False)
                                pass

                            def label_page4(self):
                                title_font = QtGui.QFont()
                                title_font.setFamily("Arial")
                                title_font.setPointSize(18)
                                self._5label = QtWidgets.QLabel(self.page_4)
                                self._5label.setGeometry(QtCore.QRect(10, 10, 180, 31))
                                self._5label.setFont(title_font)
                                self._5label.setObjectName("_5label")
                                self._5label.setText("下载网易云音乐")

                                self._5label_2 = QtWidgets.QLabel(self.page_4)
                                self._5label_2.setGeometry(QtCore.QRect(15, 50, 80, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._5label_2.setFont(font)
                                self._5label_2.setObjectName("_5label_2")
                                self._5label_2.setText("歌曲链接")

                                self._5lineEdit = CustomLineEdit(self.page_4)
                                self._5lineEdit.setGeometry(QtCore.QRect(15, 70, 271, 20))
                                self._5lineEdit.setObjectName("_5lineEdit")
                                self._5lineEdit.setStyleSheet("background: transparent;")
                                self._5lineEdit.setPlaceholderText("点击输入音乐链接(Ctrl+V粘贴可快速解析文件名)")
                                self._5lineEdit.setReadOnly(False)

                                self._5label_3 = QtWidgets.QLabel(self.page_4)
                                self._5label_3.setGeometry(QtCore.QRect(15, 100, 80, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._5label_3.setFont(font)
                                self._5label_3.setObjectName("_5label_3")
                                self._5label_3.setText("保存文件名")

                                self._5lineEdit2 = QtWidgets.QLineEdit(self.page_4)
                                self._5lineEdit2.setGeometry(QtCore.QRect(15, 120, 271, 20))
                                self._5lineEdit2.setObjectName("_5lineEdit2")
                                self._5lineEdit2.setStyleSheet("background: transparent;")
                                self._5lineEdit2.setPlaceholderText("点击输入保存文件名(包含扩展名)")
                                self._5lineEdit2.setReadOnly(False)

                                self._5label_4 = QtWidgets.QLabel(self.page_4)
                                self._5label_4.setGeometry(QtCore.QRect(15, 150, 81, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._5label_4.setFont(font)
                                self._5label_4.setObjectName("_5label_4")
                                self._5label_4.setText("保存路径")

                                self._5lineEdit3 = QtWidgets.QLineEdit(self.page_4)
                                self._5lineEdit3.setGeometry(QtCore.QRect(15, 170, 271, 20))
                                self._5lineEdit3.setObjectName("_5lineEdit3")
                                self._5lineEdit3.setStyleSheet("background: transparent;")
                                self._5lineEdit3.setText(os.getcwd() + '\\mod\\music')

                                self._5toolButton = QtWidgets.QToolButton(self.page_4)
                                self._5toolButton.setGeometry(QtCore.QRect(15, 200, 271, 31))
                                self._5toolButton.setObjectName("_5toolButton")
                                self._5toolButton.setText("下载")
                                self._5toolButton.setCursor(QCursor(Qt.PointingHandCursor))
                                self._5toolButton.setStyleSheet("QToolButton#_5toolButton {"
                                                                "background-color: #3498db;"  # Blue background color
                                                                "border-radius: 4px;"  # 10px border radius for rounded corners
                                                                "color: white;"
                                                                "padding: 100px 100px;"
                                                                "text-align: center;"
                                                                "text-decoration: none;"
                                                                "font-size: 13px;"
                                                                "font-family: SimSun, Arial, sans-serif;"
                                                                "}")

                                self._5toolButton2 = QtWidgets.QToolButton(self.page_4)
                                self._5toolButton2.setGeometry(QtCore.QRect(250, 150, 37, 18))
                                self._5toolButton2.setObjectName("_5toolButton2")
                                self._5toolButton2.setText("选择")
                                self._5toolButton2.setStyleSheet("""
                                    QToolButton {
                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                        background-color: transparent;    /* 设置透明背景 */
                                        border-radius: 2px;    /* 设置圆角 */
                                    }
                                    QToolButton:hover {
                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                    }
                                """)

                                self.view_music = QtWidgets.QToolButton(self.page_4)
                                self.view_music.setGeometry(QtCore.QRect(200, 150, 37, 18))
                                self.view_music.setObjectName("view_music")
                                self.view_music.setText("浏览")
                                self.view_music.setStyleSheet("""
                                    QToolButton {
                                        border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                        background-color: transparent;    /* 设置透明背景 */
                                        border-radius: 2px;    /* 设置圆角 */
                                    }
                                    QToolButton:hover {
                                        background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                        border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                    }
                                """)



                                self._5label5 = QtWidgets.QLabel(self.page_4)
                                self._5label5.setGeometry(QtCore.QRect(305, 10, 180, 31))
                                self._5label5.setFont(title_font)
                                self._5label5.setObjectName("_5label5")
                                self._5label5.setText("图片格式修改")

                                self._5label6 = QtWidgets.QLabel(self.page_4)
                                self._5label6.setGeometry(QtCore.QRect(305, 50, 80, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._5label6.setFont(font)
                                self._5label6.setObjectName("_5label6")
                                self._5label6.setText("图片路径")

                                self._5lineEdit4 = QtWidgets.QLineEdit(self.page_4)  # 输入图片栏
                                self._5lineEdit4.setGeometry(QtCore.QRect(305, 70, 370, 20))
                                self._5lineEdit4.setObjectName("_5lineEdit4")
                                self._5lineEdit4.setStyleSheet("background: transparent;")
                                self._5lineEdit4.setPlaceholderText("点击输入图片路径")

                                self._5label7 = QtWidgets.QLabel(self.page_4)
                                self._5label7.setGeometry(QtCore.QRect(305, 90, 80, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self._5label7.setFont(font)
                                self._5label7.setObjectName("_5label7")
                                self._5label7.setText("输出文件夹路径")

                                self._5lineEdit5 = QtWidgets.QLineEdit(self.page_4)  # 酷狗保存文件名
                                self._5lineEdit5.setGeometry(QtCore.QRect(305, 110, 370, 20))
                                self._5lineEdit5.setObjectName("_5lineEdit5")
                                self._5lineEdit5.setStyleSheet("background: transparent;")
                                self._5lineEdit5.setPlaceholderText("点击输入图片输出路径")

                                self._5toolButton3 = QtWidgets.QToolButton(self.page_4)  # 输入图片路径
                                self._5toolButton3.setGeometry(QtCore.QRect(680, 70, 51, 21))
                                self._5toolButton3.setObjectName("_5toolButton3")
                                self._5toolButton3.setText("选择")
                                self._5toolButton3.setStyleSheet("""
                                                                                                            QToolButton {
                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                            }
                                                                                                            QToolButton:hover {
                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                            }
                                                                                                        """)

                                self._5toolButton4 = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
                                self._5toolButton4.setGeometry(QtCore.QRect(680, 110, 51, 21))
                                self._5toolButton4.setObjectName("_5toolButton4")
                                self._5toolButton4.setText("选择")
                                self._5toolButton4.setStyleSheet("""
                                                                                                            QToolButton {
                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                            }
                                                                                                            QToolButton:hover {
                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                            }
                                                                                                        """)
                                self.groupPic = QtWidgets.QButtonGroup(self)
                                self.JPG_radioButton = QtWidgets.QRadioButton(self.page_4)
                                self.JPG_radioButton.setGeometry(QtCore.QRect(305, 160, 61, 16))
                                self.JPG_radioButton.setObjectName("JPG_radioButton")
                                self.JPG_radioButton.setText("JPEG")
                                self.JPG_radioButton.setChecked(True)
                                self.PNG_radioButton = QtWidgets.QRadioButton(self.page_4)
                                self.PNG_radioButton.setGeometry(QtCore.QRect(380, 160, 61, 16))
                                self.PNG_radioButton.setObjectName("PNG_radioButton")
                                self.PNG_radioButton.setText("PNG")
                                self.GIF_radioButton = QtWidgets.QRadioButton(self.page_4)
                                self.GIF_radioButton.setGeometry(QtCore.QRect(450, 160, 61, 16))
                                self.GIF_radioButton.setObjectName("GIF_radioButton")
                                self.GIF_radioButton.setText("GIF")
                                self.groupPic.addButton(self.JPG_radioButton)
                                self.groupPic.addButton(self.PNG_radioButton)
                                self.groupPic.addButton(self.GIF_radioButton)
                                self._5toolButton5 = QtWidgets.QToolButton(self.page_4)
                                self._5toolButton5.setGeometry(QtCore.QRect(310, 200, 200, 31))
                                self._5toolButton5.setObjectName("_5toolButton5")
                                self._5toolButton5.setStyleSheet("QToolButton#_5toolButton5 {"
                                                                 "background-color: #3498db;"  # Blue background color
                                                                 "border-radius: 5px;"  # 10px border radius for rounded corners
                                                                 "color: white;"
                                                                 "font-family: SimSun, Arial, sans-serif;"
                                                                 "}")
                                self._5toolButton5.setText("输出")
                                self._5toolButton5.setCursor(QCursor(Qt.PointingHandCursor))

                                self.QQ_label = QtWidgets.QLabel(self.page_4)
                                self.QQ_label.setGeometry(QtCore.QRect(20, 250, 180, 31))
                                self.QQ_label.setFont(title_font)
                                self.QQ_label.setObjectName("QQ_label")
                                self.QQ_label.setText("QQ信息")

                                self.QQ_label_t2 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t2.setGeometry(QtCore.QRect(20, 280, 180, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t2.setFont(font)
                                self.QQ_label_t2.setObjectName("QQ_label_t2")
                                self.QQ_label_t2.setText("随机下载QQ头像")

                                self.QQ_label_t3 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t3.setGeometry(QtCore.QRect(120, 283, 26, 22))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t3.setFont(font)
                                self.QQ_label_t3.setObjectName("QQ_label_t3")
                                self.QQ_label_t3.setStyleSheet(
                                    "color: yellow; background-color: gray; border-radius: 3px;")
                                self.QQ_label_t3.setText("Lv2")

                                self.QQ_spinBox = QtWidgets.QSpinBox(self.page_4)  # QQ图像下载次数
                                self.QQ_spinBox.setGeometry(QtCore.QRect(20, 310, 90, 20))
                                self.QQ_spinBox.setMinimum(1)
                                self.QQ_spinBox.setMaximum(9999)
                                self.QQ_spinBox.setStyleSheet("background: transparent;")
                                self.QQ_spinBox.setObjectName("QQ_spinBox")
                                self.QQ_spinBox.setStyleSheet("""
                                                                                                            QSpinBox {
                                                                                                                border: 1px solid gray;
                                                                                                                border-radius: 3px;  /* 设置圆角 */
                                                                                                                background: transparent;
                                                                                                                font: 14px;
                                                                                                                font-family: Calibri;
                                                                                                            }
                                                                                                            QSpinBox::up-button {
                                                                                                                subcontrol-origin: border;
                                                                                                                subcontrol-position: top right; 
                                                                                                                width: 13px; 
                                                                                                                border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                                            }
                                                                                                            QSpinBox::down-button {
                                                                                                                subcontrol-origin: border;
                                                                                                                subcontrol-position: bottom right; 
                                                                                                                width: 13px; 
                                                                                                                border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                                            }
                                                                                                        """)

                                self.QQ_Button_Dow = QtWidgets.QPushButton(self.page_4)
                                self.QQ_Button_Dow.setGeometry(QtCore.QRect(120, 310, 80, 20))
                                self.QQ_Button_Dow.setObjectName("QQ_Button_Dow")
                                self.QQ_Button_Dow.setText("开始下载")
                                self.QQ_Button_Dow.setStyleSheet("""
                                                                        QPushButton {
                                                                            border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                            background-color: transparent;    /* 设置透明背景 */
                                                                            border-radius: 2px;    /* 设置圆角 */
                                                                        }
                                                                        QPushButton:hover {
                                                                            background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                            border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                        }
                                                                    """)

                                self.open_QQ = QPushButton('浏览图片文件夹', self.page_4)
                                self.open_QQ.clicked.connect(lambda: self.open_folder('picture'))
                                self.open_QQ.setGeometry(20, 360, 130, 20)
                                self.open_QQ.setStyleSheet("""
                                                                                                            QPushButton {
                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                            }
                                                                                                            QPushButton:hover {
                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                            }
                                                                                                        """)

                                self.delete_image = QPushButton('一键清空文件夹', self.page_4)
                                self.delete_image.setGeometry(150, 360, 130, 20)
                                self.delete_image.setStyleSheet("""
                                                                                                            QPushButton {
                                                                                                                border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                background-color: transparent;    /* 设置透明背景 */
                                                                                                                border-radius: 2px;    /* 设置圆角 */
                                                                                                            }
                                                                                                            QPushButton:hover {
                                                                                                                background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                            }
                                                                                                        """)

                                self.QQ_label_t3 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t3.setGeometry(QtCore.QRect(20, 330, 100, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t3.setFont(font)
                                self.QQ_label_t3.setObjectName("QQ_label_t3")
                                self.QQ_label_t3.setText("总下载次数:0次")

                                self.QQ_label_t4 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t4.setGeometry(QtCore.QRect(20, 410, 180, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t4.setFont(font)
                                self.QQ_label_t4.setObjectName("QQ_label_t4")
                                self.QQ_label_t4.setText("一键更换QQ资料")

                                self.pushButton_tooltip_imformation = QtWidgets.QPushButton(self.page_4)
                                self.pushButton_tooltip_imformation.setGeometry(QtCore.QRect(130, 410, 24, 24))
                                self.pushButton_tooltip_imformation.setStyleSheet("QPushButton {"
                                                                           "    border-image: url(./image/Component/提示3.png);"
                                                                           "    background-color: rgba(245,245,245,0);"
                                                                           "}")
                                self.pushButton_tooltip_imformation.setToolTip(
                                    "此功能的作用是依次按顺序点击QQ更新用户资料的控件来实现更新资料的效果\n如无需要此功能请勿随意使用")

                                self.QQ_label_t5 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t5.setGeometry(QtCore.QRect(20, 430, 180, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t5.setFont(font)
                                self.QQ_label_t5.setObjectName("QQ_label_t5")
                                self.QQ_label_t5.setText("设置点击间隔时间 次\\秒")

                                self.QQ_label_t6 = QtWidgets.QLabel(self.page_4)
                                self.QQ_label_t6.setGeometry(QtCore.QRect(120, 330, 100, 31))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_label_t6.setFont(font)
                                self.QQ_label_t6.setObjectName("QQ_label_t6")
                                self.QQ_label_t6.setText("有效次数:0次")

                                self.QQ_Doxb = QtWidgets.QDoubleSpinBox(self.page_4)
                                self.QQ_Doxb.setGeometry(QtCore.QRect(20, 470, 260, 20))
                                self.QQ_Doxb.setMinimum(0.1)
                                self.QQ_Doxb.setValue(0.3)
                                self.QQ_Doxb.setSingleStep(0.1)
                                self.QQ_Doxb.setMaximum(1)
                                self.QQ_Doxb.setObjectName("QQ_Doxb")
                                self.QQ_Doxb.setStyleSheet("""QDoubleSpinBox {
                                                                              border: 1px solid gray;
                                                                              border-radius: 3px;  /* 设置圆角 */
                                                                              background: transparent;
                                                                              font: 14px;
                                                                              font-family: Calibri;
                                                                              }
                                                            QDoubleSpinBox::up-button {
                                                                                       subcontrol-origin: border;
                                                                                       subcontrol-position: top right; 
                                                                                       width: 13px; 
                                                                                       border-image: url('./image/Component/箭头 上.png');  /* 设置上调按钮的图像 */
                                                                                       }
                                                            QDoubleSpinBox::down-button {
                                                                                         subcontrol-position: bottom right; 
                                                                                         width: 13px; 
                                                                                         border-image: url('./image/Component/箭头 下.png');  /* 设置下调按钮的图像 */
                                                                                         }
                                                                                         """)

                                self.QQ_image = QtWidgets.QPushButton(self.page_4)
                                self.QQ_image.setGeometry(QtCore.QRect(20, 500, 260, 30))
                                self.QQ_image.setObjectName("QQ_image")
                                self.QQ_image.setText("更换")
                                self.QQ_image.setStyleSheet("QPushButton#QQ_image {"
                                                                 "background-color: #3498db;"  # Blue background color
                                                                 "border-radius: 5px;"  # 10px border radius for rounded corners
                                                                 "color: white;"
                                                                 "font-family: SimSun, Arial, sans-serif;"
                                                                 "}")



                                self.QQ_GLabel = QtWidgets.QLabel(self.page_4)
                                self.QQ_GLabel.setGeometry(QtCore.QRect(310, 245, 200,40))
                                self.QQ_GLabel.setFont(title_font)
                                self.QQ_GLabel.setObjectName("QQ_GLabel")
                                self.QQ_GLabel.setText("QQ群信息获取")

                                self.QQ_GLabel2 = QtWidgets.QLabel(self.page_4)
                                self.QQ_GLabel2.setGeometry(QtCore.QRect(310, 300, 100, 16))
                                font = QtGui.QFont()
                                font.setFamily("Arial")
                                font.setPointSize(10)
                                self.QQ_GLabel2.setFont(font)
                                self.QQ_GLabel2.setObjectName("QQ_GLabel2")
                                self.QQ_GLabel2.setText("输出文件夹路径:")

                                self.groupQQ = QtWidgets.QButtonGroup(self)

                                self.QQ_Group_Save = QtWidgets.QLineEdit(self.page_4)  # QQ群信息保存路径
                                self.QQ_Group_Save.setGeometry(QtCore.QRect(310, 330, 310, 20))
                                self.QQ_Group_Save.setObjectName("QQ_Group_Save")
                                self.QQ_Group_Save.setStyleSheet("background: transparent;")
                                self.QQ_Group_Save.setPlaceholderText("点击输入xlsx文件夹路径")
                                self.QQ_Group_Save.setText(os.getcwd() + '\\mod\\xlsx')

                                self.QQ_Group_Selec = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
                                self.QQ_Group_Selec.setGeometry(QtCore.QRect(625, 330, 51, 21))
                                self.QQ_Group_Selec.setObjectName("QQ_Group_Selec")
                                self.QQ_Group_Selec.setText("选择")
                                self.QQ_Group_Selec.setStyleSheet("""
                                                                                                                                                QToolButton {
                                                                                                                                                    border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                    background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                    border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                }
                                                                                                                                                QToolButton:hover {
                                                                                                                                                    background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                    border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                }
                                                                                                                                            """)

                                self.QQ_Group_View = QtWidgets.QToolButton(self.page_4)  # 输出文件夹路径
                                self.QQ_Group_View.setGeometry(QtCore.QRect(680, 330, 51, 21))
                                self.QQ_Group_View.setObjectName("QQ_Group_View")
                                self.QQ_Group_View.setText("浏览")
                                self.QQ_Group_View.setStyleSheet("""
                                                                                                                                                QToolButton {
                                                                                                                                                    border: 1px solid #3498db;    /* 设置为RGB颜色#3498db的边框 */
                                                                                                                                                    background-color: transparent;    /* 设置透明背景 */
                                                                                                                                                    border-radius: 2px;    /* 设置圆角 */
                                                                                                                                                }
                                                                                                                                                QToolButton:hover {
                                                                                                                                                    background-color: #3498db;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                                                                                                                    border: 1px solid #3498db;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                                                                                                                }
                                                                                                                                            """)

                                self.Edge = QtWidgets.QRadioButton(self.page_4)
                                self.Edge.setGeometry(QtCore.QRect(310, 360, 505, 16))
                                self.Edge.setObjectName("Edge")
                                self.Edge.setChecked(True)
                                self.Edge.setText("Edge")

                                self.Chrome = QtWidgets.QRadioButton(self.page_4)
                                self.Chrome.setGeometry(QtCore.QRect(360, 360, 60, 16))
                                self.Chrome.setObjectName("Chrome")
                                self.Chrome.setText("Chrome")
                                self.IE = QtWidgets.QRadioButton(self.page_4)
                                self.IE.setGeometry(QtCore.QRect(420, 360, 50, 16))
                                self.IE.setObjectName("IE")
                                self.IE.setText("IE")

                                self.groupQQ.addButton(self.Edge)
                                self.groupQQ.addButton(self.Chrome)
                                self.groupQQ.addButton(self.IE)

                                self.Content_Label = QtWidgets.QLabel(self.page_4)
                                self.Content_Label.setGeometry(QtCore.QRect(310, 390, 100, 16))
                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(11)
                                self.Content_Label.setFont(font)
                                self.Content_Label.setObjectName("Content_Label")
                                self.Content_Label.setText("内容选择:")

                                font = QtGui.QFont()
                                font.setFamily("等线")
                                font.setPointSize(11)
                                self.checkBox_gender = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_gender.setGeometry(QtCore.QRect(310, 420, 80, 20))
                                self.checkBox_gender.setFont(font)
                                self.checkBox_gender.setObjectName("checkBox_gender")
                                self.checkBox_gender.setText("序号")
                                self.checkBox_gender.setChecked(True)
                                self.checkBox_gender.setEnabled(False)

                                self.checkBox_name = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_name.setGeometry(QtCore.QRect(390, 420, 80, 20))
                                self.checkBox_name.setFont(font)
                                self.checkBox_name.setObjectName("checkBox_name")
                                self.checkBox_name.setText("名称")
                                self.checkBox_name.setChecked(True)
                                self.checkBox_name.setEnabled(False)

                                self.checkBox_group_name = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_group_name.setGeometry(QtCore.QRect(480, 420, 80, 20))
                                self.checkBox_group_name.setFont(font)
                                self.checkBox_group_name.setObjectName("checkBox_group_name")
                                self.checkBox_group_name.setText("群昵称")
                                self.checkBox_group_name.setChecked(True)
                                self.checkBox_group_name.setEnabled(False)

                                self.checkBox_qid = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_qid.setGeometry(QtCore.QRect(570, 420, 80, 20))
                                self.checkBox_qid.setFont(font)
                                self.checkBox_qid.setObjectName("checkBox_qid")
                                self.checkBox_qid.setText("QQ号")
                                self.checkBox_qid.setChecked(True)

                                self.checkBox_sex = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_sex.setGeometry(QtCore.QRect(660, 420, 80, 20))
                                self.checkBox_sex.setFont(font)
                                self.checkBox_sex.setObjectName("checkBox_sex")
                                self.checkBox_sex.setText("性别")
                                self.checkBox_sex.setChecked(True)

                                self.checkBox_qq_year = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_qq_year.setGeometry(QtCore.QRect(310, 450, 80, 20))
                                self.checkBox_qq_year.setFont(font)
                                self.checkBox_qq_year.setObjectName("checkBox_qq_year")
                                self.checkBox_qq_year.setText("QQ年龄")
                                self.checkBox_qq_year.setChecked(True)

                                self.checkBox_join_date = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_join_date.setGeometry(QtCore.QRect(390, 450, 80, 20))
                                self.checkBox_join_date.setFont(font)
                                self.checkBox_join_date.setObjectName("checkBox_join_date")
                                self.checkBox_join_date.setText("进群日期")
                                self.checkBox_join_date.setChecked(True)

                                self.checkBox_send_date = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_send_date.setGeometry(QtCore.QRect(480, 450, 120, 20))
                                self.checkBox_send_date.setFont(font)
                                self.checkBox_send_date.setObjectName("checkBox_send_date")
                                self.checkBox_send_date.setText("最后发言日期")
                                self.checkBox_send_date.setChecked(True)

                                self.checkBox_group_lv = QtWidgets.QCheckBox(self.page_4)
                                self.checkBox_group_lv.setGeometry(QtCore.QRect(610, 450, 80, 20))
                                self.checkBox_group_lv.setFont(font)
                                self.checkBox_group_lv.setObjectName("checkBox_group_lv")
                                self.checkBox_group_lv.setText("群等级")
                                self.checkBox_group_lv.setChecked(True)

                                self.QQ_group = QtWidgets.QPushButton(self.page_4)
                                self.QQ_group.setGeometry(QtCore.QRect(310, 500, 200, 30))
                                self.QQ_group.setObjectName("QQ_group")
                                self.QQ_group.setText("获取")
                                self.QQ_group.setStyleSheet("QPushButton#QQ_group {"
                                                            "background-color: #3498db;"  # Blue background color
                                                            "border-radius: 5px;"  # 10px border radius for rounded corners
                                                            "color: white;"
                                                            "font-family: SimSun, Arial, sans-serif;"
                                                            "}")

                            def mixPicture(self):
                                def convert_image_format(input_path, output_folder, output_format):
                                    try:
                                        # 打开待转换图片
                                        image = Image.open(input_path)

                                        # 转换为RGB模式（如果不是GIF格式）
                                        if image.mode != "RGB" and output_format != "GIF":
                                            image = image.convert("RGB")

                                        # 构建输出文件的完整路径
                                        input_filename = os.path.basename(input_path)
                                        output_filename = os.path.splitext(input_filename)[
                                                              0] + '.' + output_format.lower()
                                        output_path = os.path.join(output_folder, output_filename)

                                        # 进行图片格式转换并保存
                                        if output_format == "PNG":
                                            image.save(output_path, format="PNG")
                                        elif output_format == "JPEG":
                                            image.save(output_path, format="JPEG", quality=95)  # 设置高质量参数
                                        elif output_format == "GIF":
                                            image.save(output_path, format="GIF")

                                        self.show_message_box("提示", f"转换成功：{input_path} -> {output_path}")
                                    except Exception as e:
                                        self.show_message_box("提示", f"转换失败：{e}")

                                if self.JPG_radioButton.isChecked():
                                    output_image_format = "JPEG"
                                elif self.PNG_radioButton.isChecked():
                                    output_image_format = "PNG"
                                else:
                                    output_image_format = "GIF"
                                input_image_path = self._5lineEdit4.text()
                                output_folder_path = self._5lineEdit5.text()
                                convert_image_format(input_image_path, output_folder_path, output_image_format)

                            def download(self): #下载网易云音乐
                                try:
                                    download_url = 'https://music.163.com/song/media/outer/url?id={}'
                                    headers = {
                                        'Referer': 'https://music.163.com/search/',
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
                                    }

                                    url = self._5lineEdit.text()
                                    music_id = url.split('=')[1]
                                    response = requests.get(download_url.format(music_id), headers=headers)
                                    file_name = self._5lineEdit2.text()
                                    with open(f'{self._5lineEdit3.text()}\\{file_name}', 'wb') as file:
                                        file.write(response.content)
                                        self.show_message_box("提示", "下载成功!")
                                except Exception as e:
                                    self.show_message_box("提示", f"下载失败:{e}")

                            def show_folder_dialog(self, number):
                                if number == 1:  # 网音乐音乐输出路径
                                    folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
                                    folder_path = folder_path.replace("/", "\\")
                                    self._5lineEdit3.setText(folder_path)
                                elif number == 2:  # 图片输入路径
                                    options = QFileDialog.Options()
                                    options |= QFileDialog.ReadOnly
                                    file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                                               "Image Files (*.jpg *.jpeg *.png *.bmp *.gif)",
                                                                               options=options)
                                    file_name = file_name.replace("/", "\\")
                                    if file_name:
                                        self._5lineEdit4.setText(file_name)
                                        if self._5lineEdit5.text() == '':
                                            parent_folder = os.path.dirname(file_name)
                                            self._5lineEdit5.setText(parent_folder)
                                elif number == 3:  # 图片输出路径
                                    folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
                                    folder_path = folder_path.replace("/", "\\")
                                    self._5lineEdit5.setText(folder_path)

                                elif number == 4:  # QQ群信息保存
                                    folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
                                    folder_path = folder_path.replace("/", "\\")
                                    self.QQ_Group_Save.setText(folder_path)

                            def Button_selection(self):
                                self.Button_1.setStyleSheet(self.Button_Style)
                                self.Button_2.setStyleSheet(self.Button_Style)
                                self.Button_3.setStyleSheet(self.Button_Style)
                                self.Button_4.setStyleSheet(self.Button_Style)

                            def bt_c1(self):
                                self.Button_selection()
                                self.Button_1.setStyleSheet(self.Now_Button_Style)
                                self.stackedWidget.setCurrentIndex(0)

                            def bt_c2(self):
                                self.Button_selection()
                                self.Button_2.setStyleSheet(self.Now_Button_Style)
                                self.stackedWidget.setCurrentIndex(1)

                            def bt_c3(self):
                                self.Button_selection()
                                self.Button_3.setStyleSheet(self.Now_Button_Style)
                                self.stackedWidget.setCurrentIndex(2)

                            def bt_c4(self):
                                self.Button_selection()
                                self.Button_4.setStyleSheet(self.Now_Button_Style)
                                self.stackedWidget.setCurrentIndex(3)

                            def quit_team_H(self):
                                self.create_team_button.setVisible(True)  # 创建队伍按钮
                                self.add_team_label.setText("加入队伍")
                                self.add_team_label.setVisible(True)
                                self.add_team_ID.setVisible(True)
                                self.add_team_lineEdit.setVisible(True)
                                self.add_team_button.setVisible(True)
                                self.button_copy_id.setVisible(False)  # 复制
                                self._4label.setVisible(False)
                                self.run_execute.setVisible(False)  # 执行按钮
                                for button in self.buttonGroup2.buttons():
                                    button.setVisible(False)
                                for button in self.buttonGroup3.buttons():
                                    button.setVisible(False)
                                self.run_execute.setVisible(False)
                                self.add_team_ID.setText("队伍ID:")
                                self._4label_6.setText("等待用户加入")
                                self._4label_8.setText("ID:")

                            def quit_team_C(self):
                                self.create_team_label_prompt.setVisible(False)
                                self.create_team_label.setVisible(True)
                                self._4label.setGeometry(QtCore.QRect(10, 70, 325, 31))
                                self._4label.setText("队伍ID为:")
                                self._4label.setVisible(False)
                                self.create_team_label.setGeometry(QtCore.QRect(10, 10, 201, 21))
                                self.create_team_label.setText("创建队伍")
                                self.add_team_lineEdit.setText("")
                                self.add_team_label.setVisible(True)
                                self.add_team_label_prompt.setVisible(False)
                                self.add_team_ID.setVisible(True)
                                self.add_team_lineEdit.setVisible(True)
                                self.create_team_button.setVisible(True)
                                self.add_team_button.setVisible(True)

                            def team(self):  # 创建队伍
                                self.create_team_button.setVisible(False)  # 创建队伍按钮
                                self.add_team_label.setVisible(False)
                                self.add_team_label_prompt.setText("队伍已创建！")
                                self.add_team_label_prompt.setVisible(True)
                                self.add_team_ID.setVisible(False)
                                self.add_team_lineEdit.setVisible(False)
                                self.add_team_button.setVisible(False)
                                self.button_copy_id.setVisible(True)  # 上半部分控件
                                characters = string.ascii_letters + string.digits
                                global random_string
                                random_string = ''.join(random.choices(characters, k=30))
                                self._4label.setText(f"队伍ID为:{random_string}")
                                self._4label.setVisible(True)
                                self.run_execute.setVisible(False)
                                send_encry(f'10004 {random_string}')

                            def jointeam(self):
                                id = self.add_team_lineEdit.text()
                                if len(id) != 30:
                                    self.show_message_box("提示", "队伍id不正确!")
                                else:
                                    send_encry(f'20001 {id}')

                            def team_c(self):
                                def ch():
                                    if self.team_send_handle.isChecked():
                                        return 1
                                    elif self.team_send_atqq.isChecked():
                                        return 2
                                    elif self.team_send_copy.isChecked():
                                        return 3
                                    elif self.team_send_renew.isChecked():
                                        return 4
                                    elif self.team_send_exe.isChecked():
                                        return 5
                                    else:
                                        return 6

                                def ch2():
                                    if self.team_send_handle_c.isChecked():
                                        return 1
                                    elif self.team_send_atqq_c.isChecked():
                                        return 2
                                    elif self.team_send_copy_c.isChecked():
                                        return 3
                                    elif self.team_send_renew_c.isChecked():
                                        return 4
                                    elif self.team_send_exe_c.isChecked():
                                        return 5
                                    else:
                                        return 6

                                member = ch2()

                                if member == 1:
                                    send_encry('20011')
                                elif member == 2:
                                    send_encry('20012')
                                elif member == 3:
                                    send_encry('20013')
                                elif member == 4:
                                    send_encry('20014')
                                elif member == 5:
                                    send_encry('20015')
                                else:
                                    send_encry('20016')
                                captain = ch()
                                if captain == 1:
                                    MyThread(self.Handle_Send())
                                elif captain == 2:
                                    self.Send_QQ()
                                elif captain == 3:
                                    self.Send_Copy()
                                elif captain == 4:
                                    self.QQ_image_update()
                                elif captain == 5:
                                    self.Click_Record_execute()
                                else:
                                    pyautogui.confirm("ERROR! UNKNOWN")

                            def copy(self):
                                global random_string
                                clipboard = QApplication.clipboard()
                                clipboard.setText(f'{random_string}')

                            def closeEvent(self, e):
                                os._exit(0)

                            def mousePressEvent(self, e):
                                if e.y() <= 30:  # 30像素的标题栏高度
                                    self.start_point = e.globalPos()
                                    self.window_point = self.frameGeometry().topLeft()

                            def mouseMoveEvent(self, e):
                                if hasattr(self, 'start_point'):
                                    relpos = e.globalPos() - self.start_point
                                    self.move(self.window_point + relpos)

                            def mouseReleaseEvent(self, e):
                                if hasattr(self, 'start_point'):
                                    delattr(self, 'start_point')

                            def show_message_box(self, head, message):
                                QMessageBox.question(self, head, message,
                                                     QMessageBox.Yes)

                        windows = Ui_Form()
                        windows.show()
                        print("窗口创建成功")

                        process = psutil.Process()
                        memory_info = process.memory_info()
                        memory_info = memory_info.rss / (1024 * 1024)  #输出内存占用
                        print(f"内存占用(MB): {memory_info:.2f} MB")
                        end_time = time.time()
                        execution_time = end_time - start_time
                        execution_time = round(execution_time, 2)
                        global current_time_string
                        sys_list.append('g' + '[' + time.strftime(
                            "%H:%M:%S") + ']' + f"窗口打开成功 本次登录耗时:{execution_time}秒")

                    except Exception as e:
                        traceback.print_exc()
                        print(e)
            elif log_ST == "Cooling":
                pyautogui.confirm("账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
            else:
                self.ui.Login_Button.setEnabled(False)
                pyautogui.confirm("密码错误")
                self.ui.Login_Button.setEnabled(True)
        except Exception as e:
            traceback.print_exc()
            pyautogui.confirm("密码错误",e)

    def reg(self):
        pyautogui.confirm("这是账号注册窗口 此处不方便展示")
    def rew(self):
        pyautogui.confirm("这是密码重置 此处不方便展示")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('./mod/trans/qt_zh_CN.qm')
    app.installTranslator(translator)
    window = MyWindow()
    window.show()
    if Log == True:
        time.sleep(0.1)
        window.pr("login")
    # 输出当前活动的线程
    active_threads = threading.enumerate()
    print("进程结束 ",active_threads)
    sys.exit(app.exec_())
os._exit(0)
