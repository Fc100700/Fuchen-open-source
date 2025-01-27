import platform
import concurrent.futures
import logging
import os
import ReWord
import shutil
import socket
import traceback
from datetime import date
import threading
import webbrowser
import random
import json
import keyboard as keys
import pyautogui
import pyperclip
import sys
import requests
import time
import win32com.client
import win32con
import win32gui
import win32clipboard as w
import win32api
import winsound
import psutil
import Login
import RecordPosition
import Signin
import subprocess
import pygetwindow as gw
import re
import string
import function
import SetWindowUI
import ui.Agreement
import ui.style
import page
import SundryUI
import SocketThread
import update_install

try:
    import cv2
    cv2_available = True
except ImportError:
    cv2_available = False
try:
    import op  #计数文件
except:
    pass
from playsound import playsound
from pynput import mouse
from PIL import Image
from pynput import keyboard
from pypinyin import pinyin, Style
from collections import deque
from datetime import datetime
from pynput.keyboard import Key, Controller as KeyboardController, KeyCode
from pynput.mouse import Button, Controller as MouseController
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from PyQt5.QtCore import Qt, QSize, QRect, QTimer, QUrl, QPropertyAnimation, \
    QRectF, QTranslator, QEasingCurve, pyqtSignal, QThread
from PyQt5.QtGui import QCursor, QPainter, QColor, QIcon, QPixmap, QKeySequence, QFont, \
    QDesktopServices, QPalette, QBrush, QPainterPath, QImage, QLinearGradient
from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QFileDialog, QWidget, QLabel, QShortcut, \
    QButtonGroup, QMainWindow, QMenu, QAction, QSystemTrayIcon, QToolButton
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.fileEdit

logging.basicConfig(filename='INFOR.log', level=logging.ERROR)


def log_exception(*args):
    # 记录异常信息到日志文件中
    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(args))
# 文件名
# 检查文件是否存在
if os.path.isfile('Fuchen.tmp'):  #检测文件是否存在 如果存在则删除旧版本内容
    try:
    # 打开文件并读取第一行
        with open('Fuchen.tmp', 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()  # 读取第一行并去除首尾空白字符
        shutil.rmtree(first_line)
        shutil.rmtree("Fuchen.tmp")
    except:
        pass


sys.excepthook = log_exception  # 日志
with open("INFOR.log", 'a') as file:
    file.write(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime()) + "  软件运行" + '\n'))



class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)

def play_prompt_sound(file_path):
    global Sound
    try:
        if Sound:
            MyThread(playsound, file_path)
    except:
        pass

def play_warning_sound():
    # 设置警告音频文件路径
    try:
        sound_file = "C:\\Windows\\Media\\Windows Foreground.wav"
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except:
        pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def encrypt(message,text, txt):  #网络数据传输加密 因开源所以无法展示
    message = message

def decrypt(ciphertext,text,txt): #网络数据传输加密 因开源所以无法展示
    ciphertext = ciphertext

def send_encry(text):  #网络数据传输加密 因开源所以无法展示
    text = text

def send_decry(text):  #网络数据传输加密 因开源所以无法展示
    text = text

function.initialization()

with open('config.json', 'r') as file:
    config = json.load(file)
Log = config.get("AutoLogin", False)
remember = config.get("Remember", False)
Account = config.get("Account", "") if remember else ""
Password = config.get("Password", "") if remember else ""
position_status = config["position"] != [[None, None], [None, None]]
initial = config.get("Initial", True)
positions = config.get("position", [[None, None], [None, None]])
textedit_position = positions[0]
send_position = positions[1]
del positions

Click_Times_ = 1000
Click_Pauses = 0.1
Random_list = [1, 2, 3]
handle_position = [30, -60]
Click_Pause = 0.01
res = False
Version = 'V1.66'
Number_People = '加载中...'

IP = '47.116.75.93'  # IP地址192.168.2.203 47.116.75.93
Port = 30003  # 端口号
information = '正在加载公告...'
sys_list = []  # 控制台内容列表
exp_status = None
HImage_load_status = False  #头像加载
resign_window = False  # 注册窗口是否开启
reword_window = False  # 重置密码窗口是否开启
connect_status = None
Fuchen_name, Fuchen_type, Fuchen_fullname = function.get_exefile_name()
Name = None
mode = None
HImage_date = None
exp = None

try:  # 连接服务器
    '''s.settimeout(10)
    s.connect((IP, Port))
    # 客户端代码
    Connect_Password = f"Zi7hEfQm6mvMB47sWC"  # 连接密码 (明文)
    s.send(Connect_Password.encode('utf-8'))  # 将密码发送到服务器端进行验证'''
    print("服务器已连接", IP, Port)
    sys_list.append("g[" + str(time.strftime("%H:%M:%S", time.localtime())) + "]" + "服务器已连接")
    connect_status = True
except Exception as e:
    pyautogui.confirm("服务器连接失败\n请留意服务器公告查询最新消息\n")
    print(e)

'''try:  # 处理信息\公告
    # 接收服务端发送的密钥和IV
    if connect_status == None:
        raise Exception()
    time.sleep(0.1)
    key_iv_data = s.recv(128)  # 32 key + 16 IV + 其余password
    key = key_iv_data[:32]
    iv = key_iv_data[32:48]
    key_password = key_iv_data[48:].decode('utf-8')
    send_encry(key_password)
    content = s.recv(4096)
    data = send_decry(content)
    data = data.split()
    data = []
    Versions = data[0]
    Number_People = data[1]
    link = data[2]
    information = data[3]
    try:
        information = re.sub('~~space~~', ' ', information)
        information = re.sub('~~next~~', '\n', information)
        print(f"更新日志:{information}")
    except:
        pass
except Exception as e:
    if connect_status != None:  #服务器连接成功 但数据接收失败
        print(traceback.print_exc())
        pyautogui.confirm("数据接收失败 请重新启动软件\n如多次重试失败 请尝试更新到最新版客户端")
        os._exit(0)
        raise Exception()
    else:  #服务器连接失败 以离线模式启动
        result = pyautogui.confirm("服务器连接失败 是否以离线模式启动?")
        if result == "OK":
            Versions = Version[0:5]
            key = b'\x96#e\xad\xc2GQ\xcct\x97\xd9\xb0\xba\x04I\x9d\x83v\xd5\xe0\xa0\xa9\xde\x9fRzN)L7\xce\x88'
            iv = b':\x0cz\x83Z\xdb U@\x07\x8f\xfbZ_Y<'
            information = "当前是离线模式 \n部分状态可能未正常显示\n部分功能可能无法正常使用"
        else:
            sys.exit()

if Versions != Version[0:5]:
    try:
        update_window = update_install.show_update_dialog(['', Version, Versions])
        if update_window == 'update_successful':
            # 创建快捷方式
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            Fuchen_name = 'Fuchen'
            shortcut_name = f'{Fuchen_name}.lnk'
            back_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
            old_path = os.path.join(back_path, f'Fuchen_{Versions}')
            original_file_path = rf'{old_path}\{Fuchen_name}.exe'
            shortcut_path = os.path.join(desktop_path, shortcut_name)
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = original_file_path
            shortcut.WorkingDirectory = os.path.dirname(original_file_path)  # 设置快捷方式的起始位置为exe文件所在的文件夹
            shortcut.save()
            current_directory = os.getcwd()
            with open(f"{old_path}\\Fuchen.tmp", "w") as f:
                f.write(f'{current_directory}')
            pyautogui.confirm("您已成功更新 请关闭此窗口 使用桌面的快捷方式启动")

            sys.exit()
        elif update_window == 'cancel_update':
            sys.exit()
        else:
            sys.exit()
        os._exit(0)
    except Exception as e:
        print(f"GUI Error: {str(e)}")
        sys.exit()'''



def ConfigReEdit(name,value):
    pass


def Check(input_str):  # 检测名称
    # 定义允许的字符集合：中文、大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def Check_Password(input_str):
    # 定义允许的字符集合：大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return 0
    else:
        return 1


def check_process_exists(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False
try:
    res = requests.get('http://myip.ipip.net', timeout=5).text
    # 提取城市信息
    split_res = res.split('  ')
    city_info = split_res[-2]  # 倒数第二个元素是城市信息
    city_info = city_info.split(' ')
    city_info = city_info[-2]+city_info[-1]+(split_res[-1].replace('\n',''))
    city_name = city_info
    del city_info
except:
    city_name = 'Unknown'

system = platform.system()  # 系统类型
computer_name = platform.node()  # 计算机网络名称


class Ui_Form(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Form, self).__init__()
        page.Name = Name
        page.Account = Account
        page.Version = Version
        page.information = information
        page.HImage_load_status = HImage_load_status
        page.position_status = position_status
        page.textedit_position = textedit_position
        page.send_position = send_position
        page.mode = mode

        self.open_status = False
        self.c_thread_object = None

        if Theme == "White":
            self.should_draw = "White"
        elif Theme == "Custom":
            self.should_draw = "Custom"
        elif Theme == "Trend":
            self.should_draw = "Trend"
        else:
            self.should_draw = "White"
        self.window_icon = False  # 右下角图标存在或不存在 布尔值 存在为True不存在为False
        self.setupUi(self)
        self.uim.Button_Minisize.clicked.connect(self.showMinimized)  # 最小化按钮
        self.uim.Button_Close.clicked.connect(self.clo)  # 退出按钮

        self.uim.Button_SetTop.clicked.connect(self.upwindow)
        self.uim.action_option1.triggered.connect(self.open_set_window)  # 设置按钮
        self.uim.action_option2.triggered.connect(self.about)
        self.uim.action_option3.triggered.connect(self.open_help_window)
        self.uim.action_option4.triggered.connect(self.LogRecord)
        self.uim.action_option5.triggered.connect(self.open_website)
        self.uim.action_option6.triggered.connect(self.open_view_window)
        self.uim.action_option7.triggered.connect(self.empyt_log)
        self.uim.action_option8.triggered.connect(self.clear_temp)
        self.uim.action_option9.triggered.connect(self.restart_app)
        self.uim.action_option10.triggered.connect(self.open_website_help)
        self.uim.action_option11.triggered.connect(self.get_update)
        #self.uim.action_option11.triggered.connect(lambda: self.open_prompt_window("提示信息"))
        self.uim.HButton.clicked.connect(self.open_user_window)

        self.uim._3pushButton.clicked.connect(self.Click_Record)  # 记录自动脚本
        self.uim._3pushButton_2.clicked.connect(self.Click_Record_execute)
        self.uim._3pushButton_4.setMenu(self.createMenu())
        self.uim.end_key_button.setMenu(self.create_key_Menu('record'))
        self.uim.end_execute_button.setMenu(self.create_key_Menu('execute'))
        self.uim._3pushButton_5.clicked.connect(self.mouseinfo)
        self.uim._3pushButton_6.clicked.connect(lambda: MyThread(self.open_click))
        self.uim._3pushButton_7.clicked.connect(lambda: MyThread(self.break_click))
        self.uim.button_create.clicked.connect(self.create_file)
        self.uim.impor_button.clicked.connect(self.open_fileedit_window)
        self.uim.reflash.clicked.connect(lambda: self.uim.populateMenu('scripts'))
        self.uim.delete_button.clicked.connect(self.delete_file)

        self.uim._2pushButton.clicked.connect(self.Send_QQ)  # page2(QQ)页面 绑定
        self.uim._2pushButton_4.clicked.connect(self.Send_Copy)  # 复制内容
        self.uim.record_position_button.clicked.connect(self.open_record_window)
        self.uim._2pushButton2.clicked.connect(self.gain_handle)
        self.uim._2pushButton_3.clicked.connect(self.Handle_Send)
        self.uim.order_pushButton.clicked.connect(self.order_send)
        self.uim.order_toolButton.clicked.connect(lambda: self.show_folder_dialog(5))
        self.uim.order_radio_list.toggled.connect(self.update_checks)
        self.uim.order_radio_random.toggled.connect(self.update_checks)
        self.uim.old_QQ.toggled.connect(lambda checked: self.QQ_change("old"))
        self.uim.new_QQ.toggled.connect(lambda checked: self.QQ_change("new"))

        self.uim.create_team_button.clicked.connect(self.team)  # 创建队伍
        self.uim.button_copy_id.clicked.connect(self.copy)  # 复制id
        self.uim.add_team_button.clicked.connect(self.jointeam)
        self.uim.run_execute.clicked.connect(self.team_c)  # 开始执行
        self.uim.talk_lineEdit.returnPressed.connect(self.send_talk)

        self.uim._5toolButton.clicked.connect(self.download)
        self.uim._5toolButton2.clicked.connect(lambda: self.show_folder_dialog(1))
        self.uim.view_music.clicked.connect(lambda: self.open_folder('music'))
        self.uim._5toolButton3.clicked.connect(lambda: self.show_folder_dialog(2))
        self.uim._5toolButton4.clicked.connect(lambda: self.show_folder_dialog(3))
        self.uim.QQ_Group_View.clicked.connect(lambda: self.open_folder('xlsx'))
        self.uim.QQ_Group_Selec.clicked.connect(lambda: self.show_folder_dialog(4))
        self.uim._5toolButton5.clicked.connect(self.mixPicture)

        self.uim.open_QQ.clicked.connect(lambda: self.open_folder('picture'))
        self.open_window_hotkey = QShortcut(QKeySequence("Ctrl+o"), self)
        self.open_window_hotkey.activated.connect(self.open_ctrl_window)
        self.uim.QQ_Button_Dow.clicked.connect(lambda: MyThread(self.download_image))
        self.uim.QQ_image.clicked.connect(self.QQ_image_update)
        self.uim.delete_image.clicked.connect(self.delete_images)
        self.uim.QQ_group.clicked.connect(lambda: MyThread(self.QQ_Group_information))

        self.image_cache = deque(maxlen=30)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.is_topmost = False
        self.border_width = 8

        MainWindow.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏任务栏
        MainWindow.setWindowTitle("Fuchen 浮沉制作")
        self.uim = page.Ui_FormS()
        self.uim.setupUi(self)

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
        if Theme == 'Trend':
            self.execute_trend()

        icon = QIcon("./image/window.ico")  # 设置窗口图标
        self.setWindowIcon(icon)

        MyThread(self.Update_weather)

        self.weather_timer = QtCore.QTimer(self)
        self.weather_timer.timeout.connect(self.Update_weather)
        self.weather_timer.start(1200000)  # 更新时间的间隔，单位为毫秒

        self.run_timer = QtCore.QTimer(self)
        self.run_timer.timeout.connect(self.updateTime)
        self.startTime = QtCore.QTime.currentTime()
        self.run_timer.start(1000)  # 每秒更新一次

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 更新时间的间隔，单位为毫秒

        self.global_timer = QtCore.QTimer(self)
        self.global_timer.timeout.connect(self.get_current_time_string)
        self.global_timer.start(1000)  # 更新时间的间隔，单位为毫秒

        # self.data_thread = DataThread()
        self.data_thread = SocketThread.DataThread([self, s, 'key', 'iv', sys_list])
        self.data_thread.start()

    def get_current_time_string(self):
        global current_time_string
        current_time = time.localtime()  # 获取当前时间的时间结构
        current_time_string = "[" + time.strftime("%H:%M:%S",
                                                  current_time) + "]"  # 格式化时间为字符串

    def restart_app(self):
        #global thread_for_exe, C_thread
        subprocess.Popen([Fuchen_fullname])
        self.close()
        '''if thread_for_exe != True:
            C_thread.kill()'''
        os._exit(0)

    def get_update(self):
        result = function.get_update_data(Version)
        if type(result) == str:
            pyautogui.confirm(result)
            return 0
        else:
            if result[0] == None or result[1] == None:
                pyautogui.confirm("版本信息获取失败 请重试")
                return 0
            else:
                if result[1] == False:
                    pyautogui.confirm(result[0])
                else:
                    usru = pyautogui.confirm(result[0])
                    if usru == "OK":
                        webbrowser.open(result[2])

    def load_images(self, folder_path):  # 动态主题导入文件
        images = []
        directory = './trend'  # 图片文件夹路径
        file_count = len(
            [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        for i in range(1, file_count):  # 假设图片名称格式为 'frame_1.jpg', 'frame_2.jpg', ...
            img_path = os.path.join(folder_path, f'frame_{i}.jpg')
            img = cv2.imread(img_path)
            img = cv2.resize(img, (1000, 600))
            if img is not None:
                images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 转换颜色空间
        return images

    def update_frame(self):
        if self.images:
            # 显示当前索引的图片
            frame = self.images[self.image_index]
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap.fromImage(image)
            self.trend_theme.setPixmap(pix)
            # 更新索引，循环播放
            self.image_index = (self.image_index + 1) % len(self.images)

    def execute_trend(self):
        self.image_index = 0  # 当前显示的图片索引
        # 加载文件夹里的图片
        self.images = self.load_images('./trend')  # 设置图片文件夹路径
        if not self.images:
            pyautogui.alert("未找到图片或图片导入失败")
            return 0
        self.trend_theme = QLabel(self)
        self.trend_theme.resize(self.size())
        self.trend_theme.setScaledContents(True)
        self.trend_theme.show()
        self.trend_theme.lower()

        # 设置定时器以每秒更新30帧
        self.timer_trend = QTimer(self)
        self.timer_trend.timeout.connect(self.update_frame)
        self.timer_trend.start(int(1000 / FPS))  # 每帧 = (1000 ms / fps)

    def execute_trend_again(self):
        self.stop_dynamic_background()
        self.execute_trend()

    def stop_dynamic_background(self):
        self.timer_trend.stop()
        self.timer_trend.deleteLater()
        self.trend_theme.clear()
        self.trend_theme.deleteLater()
        del self.image_index, self.images

    def resize_frame(self, frame):
        window_width = self.width()
        window_height = self.height()
        height, width, _ = frame.shape
        scaling_factor = min(window_width / width, window_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        frame_resized = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
        return frame_resized

    def close_float_prompt(self):
        self.point_window = SundryUI.ExpandingWindow()
        self.point_window.close()

    def updateTime(self):
        currentTime = QtCore.QTime.currentTime()
        elapsedTime = self.startTime.secsTo(currentTime)
        hours = elapsedTime // 3600
        minutes = (elapsedTime % 3600) // 60
        seconds = elapsedTime % 60
        self.uim.run_label.setText(f"运行时间 {hours:02d}:{minutes:02d}:{seconds:02d}")

    def upwindow(self):  # 置顶窗口
        if self.is_topmost == False:  # 置顶
            self.windowHandle().setFlags(
                self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            self.is_topmost = True
            self.uim.Button_SetTop.setIcon(QIcon("./image/Component/Top2.png"))
        else:  #取消置顶
            self.windowHandle().setFlags(
                self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.is_topmost = False
            self.uim.Button_SetTop.setIcon(QIcon("./image/Component/Top.png"))

    def update_time(self):
        current_time = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        self.uim.time_label.setText('当前时间 ' + current_time)
        self.timer.start(1000 - QtCore.QTime.currentTime().msec())

    def QQ_change(self, checked):  # 句柄发送位置切换
        global handle_position
        if checked == 'old':
            handle_position = [30, -60]
        else:
            handle_position = [-30, -60]

    def clear_temp(self):
        #global Theme
        total_size = 0
        for dirpath, dirnames, filenames in os.walk('./temp'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        if Theme != "Trend":
            for dirpath, dirnames, filenames in os.walk('./trend'):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
        if total_size != 0:
            total_size = float(total_size / 1024)
            if total_size < 1024:
                result = QMessageBox.question(self, "Fuchen",
                                              f"缓存内容大小为:{round(total_size, 2)}KB\n清理缓存不影响正常使用 是否进行清除?",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    shutil.rmtree('./temp')
                    # 重新创建空文件夹
                    os.mkdir('./temp')
                    pyautogui.confirm("缓存清除成功!")
            else:
                total_size = float(total_size / 1024)
                result = QMessageBox.question(self, "Fuchen",
                                              f"缓存内容大小为:{round(total_size, 2)}MB\n清理缓存不影响正常使用 是否进行清除?",
                                              QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.No)
                if result == QMessageBox.Yes:
                    shutil.rmtree('./temp')
                    # 重新创建空文件夹
                    os.mkdir('./temp')
                    if Theme != "Trend":
                        shutil.rmtree('./trend')
                        # 重新创建空文件夹
                        os.mkdir('./trend')
                    pyautogui.confirm("缓存清除成功!")
        else:
            self.show_message_box("Fuchen", f"暂无缓存内容")

    def open_set_window(self):
        if self.is_topmost == False:
            SetList = [self, cv2_available, Log, Sound, ClosePrompt, CloseExecute, window_s, Theme, transparent,
                       FPS]
            self.set_window = SetWindowUI.SetWindow(SetList)
            self.set_window.exec_()
        else:
            self.show_message_box('Fuchen', "窗口置顶时设置窗口不可打开 请取消置顶后重试")

    def setValue(self, Set):
        global Log, Sound, ClosePrompt, CloseExecute,window_s, Theme, transparent, FPS
        Log = Set[0]
        Sound = Set[1]
        ClosePrompt = Set[2]
        CloseExecute = Set[3]
        window_s = Set[4]
        Theme = Set[5]
        transparent = Set[6]
        FPS = Set[7]
    def update_exp(self, value):
        global exp
        exp = value
    def update_position(self, value):
        global position_status, textedit_position, send_position
        position_status = True
        textedit_position = value[0]
        send_position = value[1]

    def update_handle_value(self, x, y):
        global handle_position
        handle_position[0] = x
        handle_position[1] = y
    def update_information(self, value):
        global Name
        Name = value

    def run_team_command(self, command):
        if command == "handle":
            MyThread(self.Handle_Send)
        elif command == 'qq':
            MyThread(self.Send_QQ)
        elif command == 'copy':
            MyThread(self.Send_Copy)
        elif command == 'update':
            MyThread(self.QQ_image_update)
        elif command == 'execute':
            MyThread(self.Click_Record_execute)

    def open_user_window(self):
        # 查找窗口
        usr_win = gw.getWindowsWithTitle('Fuchen个人信息')
        # 判断窗口是否存在
        if usr_win:
            usr_win[0].close()  # 关闭第一个匹配的窗口
        lis = [self, Account, Name, HImage_date, exp, s,'key', 'iv', HImage_load_status]
        self.user_window = SundryUI.UserInfo(lis)
        self.user_window.show()

    def open_help_window(self):
        self.help_window = SundryUI.Help()
        self.help_window.show()

    def open_view_window(self):
        if mode == "tourist_login":
            pyautogui.confirm(
                "游客模式下此功能正处于测试阶段 每次登录只能反馈一次\n如有更多信息请发送至Fcyang_top@126.com")
            lis = [self, s, 'key', 'iv']
            self.view_window = SundryUI.View(lis)
            self.view_window.show()
        else:
            lis = [self, s, 'key', 'iv']
            self.view_window = SundryUI.View(lis)
            self.view_window.show()

    def open_ctrl_window(self):
        lis = [self, s, 'key', 'iv', sys_list]
        self.ctrl_window = SundryUI.Control(lis)
        self.ctrl_window.show()

    def open_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.show()

    def close_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.close()

    def open_point_window(self):
        self.point_window = SundryUI.ExpandingWindow2()
        self.point_window.show()

    def open_record_window(self):
        self.record__position_window = RecordPosition.record_position(self)
        self.record__position_window.exec_()

    def open_fileedit_window(self):
        if (self.uim.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建')):
            pyautogui.confirm("需要先选择或创建配置文件")
            return 0
        pyautogui.confirm("此功能还处于开发中 功能不全面可能有BUG")
        self.fileedit_window = ui.fileEdit.FileEdit(self.uim.button_file.text(), self.x(), self.y())
        self.fileedit_window.show()

    def clo(self):
        with open(f"config.json", "r") as file:
            U_data = json.load(file)
        next = U_data["ClosePrompt"]
        execute = U_data["CloseExecute"]
        if next == True:  # 是否提示关闭窗口
            self.abus = SundryUI.Quit_Prompt([self, self.window_icon])
            self.abus.exec_()
        else:  # 不提示关闭窗口
            if execute == "Close":
                self.close()
                #self.close_MainWindow()
                os._exit(0)
            else:
                SundryUI.Hide([self, self.window_icon])
    def play_sound(self):
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")


    def send_talk(self):
        text = self.uim.talk_lineEdit.text()
        text = re.sub(' ', '~~space~~', text)
        send_encry("20030 "+text)
        self.uim.talk_lineEdit.clear()


    def closeEvent(self, e):
        try:
            if self.open_status == True:
                self.c_thread_object.kill()
            if self.window_icon == True:
                self.tray_icon.hide()
            os._exit(0)
        except Exception as e:
            print(e)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
    def cv2_download_link(self):
        result = function.get_dwonload_link()
        print(result)
        return result
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F12:
            self.open_ctrl_window()

    def Update_weather(self):  # 获取天气
        api_key = "dce92b382ffb9409ca31ae4c1b240d4f"
        # 发送请求获取IP地址信息
        res = requests.get('http://myip.ipip.net', timeout=5).text
        # 提取城市信息
        split_res = res.split('  ')
        city_info = split_res[-2]  # 倒数第二个元素是位置信息
        city_info = city_info.split(' ')
        country = city_info[-3]
        city_info = city_info[-1]
        global city_name, weather_status, temperature, humidity, weather_info
        if country[-2:] == '中国':
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
                self.uim.weather_button.setGeometry(QtCore.QRect(5, 580, 200, 20))
                self.uim.weather_button.setText(
                    f"{city_name}  T: {temperature:.2f}°C H: {humidity}%")
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
                self.uim.weather_button.setIcon(icon)
                self.uim.weather_button.setIconSize(self.uim.weather_button.size())
                sys_list.append(
                    "b[" + str(time.strftime("%H:%M:%S",
                                             time.localtime())) + "] " + '天气获取成功 ' + f'城市:{city_name} ' + f'温度:{temperature:.2f}°C ' + f'湿度:{humidity}%')
            else:
                self.uim.weather_button.setGeometry(QtCore.QRect(5, 580, 80, 20))
                self.uim.weather_button.setText(f"天气获取失败")
                sys_list.append(
                    "r[" + str(
                        time.strftime("%H:%M:%S", time.localtime())) + "] " + '天气获取失败')
        else:
            self.uim.weather_button.setGeometry(QtCore.QRect(10, 580, 120, 20))
            self.uim.weather_button.setText(f"暂不支持非中国天气解析")
            sys_list.append(
                "r[" + str(
                    time.strftime("%H:%M:%S",
                                  time.localtime())) + "] " + '暂不支持非中国天气解析')

    def paintEvent(self, event):
        if self.should_draw == "White":  # 白色主题
            painter = QPainter(self)
            # 左侧灰色矩形
            left_rect = QRect(0, 0, 260, 600)
            left_color = QColor(224, 224, 224)
            #left_color.setAlpha(250)
            painter.fillRect(left_rect, left_color)

            # 右侧渐变矩形（从灰色到白色）
            right_rect = QRect(260, 0, 740, 600)
            '''right_color = QColor(245, 245, 245)
            right_color.setAlpha(230)
            painter.fillRect(right_rect, right_color)'''
            gradient = QLinearGradient(right_rect.topLeft(), right_rect.bottomLeft())  # 从上到下的渐变
            gradient.setColorAt(0.0, QColor(230, 230, 230))  # 顶部为灰色
            gradient.setColorAt(1.0, QColor(241, 241, 241))  # 底部为白色
            painter.fillRect(right_rect, gradient)
        else:  # 自定义主题 动态主题不知道为什么不生效
            painter = QPainter(self)
            left_rect = QRect(0, 0, 260, 600)
            left_color = QColor(224, 224, 224)
            left_color.setAlpha(transparent)  # 设置左边区域颜色的透明度为 50%
            painter.fillRect(left_rect, left_color)
            right_rect = QRect(260, 0, 740, 600)
            right_color = QColor(245, 245, 245)
            right_color.setAlpha(transparent - 20)
            painter.fillRect(right_rect, right_color)
            # 设置右边区域颜色的透明度为 75%

    def empyt_log(self):  # 清空日志
        log_file_path = "INFOR.log"
        with open(log_file_path, "w") as log_file:
            pass  # 使用 pass 语句表示什么都不做，从而实现清空文件内容
        self.show_message_box("提示", "日志清空成功!")

    def open_folder(self, page):  # 浏览QQ头像下载文件夹
        if page == 'picture':
            folder_path = './mod/picture'  # 修改为你要打开的文件夹路径
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == 'music':
            folder_path = self.uim._5lineEdit3.text()
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == 'xlsx':
            folder_path = './mod/xlsx'  # 修改为你要打开的文件夹路径
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

    def open_music_folder(self):  # 浏览QQ头像下载文件夹
        folder_path = './mod/music'
        url = QUrl.fromLocalFile(folder_path)
        QDesktopServices.openUrl(url)

    def LogRecord(self):  # 打开日志
        subprocess.Popen(["notepad.exe", "INFOR.log"])

    def join_team(self):  # 加入队伍
        num = self.uim._5lineEdit.text()
        send_encry(f'20001 {num}')

    def open_click(self):  # 开启连点器部分
        if (self.uim.RClick_Radio.isChecked()) and (self.uim.sort == '鼠标右键'):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        elif (self.uim.MClick_Radio.isChecked()) and (self.uim.sort == '鼠标中键'):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        try:
            print("开启中")
            self.uim._3pushButton_4.setEnabled(False)
            self.uim.LClick_Radio.setEnabled(False)
            self.uim.MClick_Radio.setEnabled(False)
            self.uim.RClick_Radio.setEnabled(False)
            self.uim._3pushButton_6.setText("正在开启...")
            self.uim._3pushButton_6.setEnabled(False)
            self.uim._3D.setEnabled(False)

            if self.uim.sort == 'F8':
                hotkey = "119"  # F8
            elif self.uim.sort == 'F9':
                hotkey = "120"  # F9
            elif self.uim.sort == 'F10':
                hotkey = "121"
            elif self.uim.sort == '鼠标右键':
                hotkey = "2"
            elif self.uim.sort == '鼠标中键':
                hotkey = "4"
            elif self.uim.sort == 'Alt':
                hotkey = "18"
            elif self.uim.sort == '空格':
                hotkey = "32"
            elif self.uim.sort == 'Ctrl':
                hotkey = "17"
            elif self.uim.sort == 'Shift':
                hotkey = "16"
            elif self.uim.sort == 'Tab':
                hotkey = "9"
            elif self.uim.sort == 'Caps':
                hotkey = "20"
            elif self.uim.sort[0] == '自':
                hotkey = (self.uim.sort.split(' '))[1]
            else:
                hotkey = '2'
            interval = str(float(self.uim._3D.value()))
            if self.uim.LClick_Radio.isChecked():
                sort = 'left'
            elif self.uim.MClick_Radio.isChecked():
                sort = 'mid'
            else:
                sort = 'right'
            try:
                self.c_thread_object = subprocess.Popen(["./mod/more/click.exe", hotkey, interval, sort])
                self.open_status = True
                self.uim._3pushButton_6.setText("连点器已开启")
                self.uim._3pushButton_7.setVisible(True)
                self.c_thread_object.wait()
            except KeyboardInterrupt:
                # 处理 Ctrl+C 中断
                self.c_thread_object.terminate()
                sys.exit()
            except Exception as e:
                print(e)
                self.uim._3pushButton_6.setText("开启失败")
                self.uim._3pushButton_7.setVisible(True)
                # 处理其他异常
                pyautogui.confirm(f"Error: {e}")

                self.c_thread_object.kill()
                sys.exit()
            '''finally:
                # 确保在程序退出时终止 程序
                C_thread.terminate()'''
        except Exception as e:
            print(e)
            pyautogui.confirm(e)

    def break_click(self):  # 关闭连点器
        try:
            if self.open_status == True:
                print(type(self.c_thread_object))
                self.c_thread_object.terminate()
                del self.c_thread_object
                self.c_thread_object = None
                self.open_status = False
                self.uim._3pushButton_6.setText("开启连点器")
                self.uim._3pushButton_4.setEnabled(True)
                self.uim.LClick_Radio.setEnabled(True)
                self.uim.MClick_Radio.setEnabled(True)
                self.uim.RClick_Radio.setEnabled(True)
                self.uim._3pushButton_6.setEnabled(True)
                self.uim._3D.setEnabled(True)
                self.uim._3pushButton_7.setVisible(False)
        except Exception as e:
            print(e)
            pyautogui.confirm(e)

    def gain_handle(self):  # 获取句柄
        self.showMinimized()

        def on_click(x, y, button, pressed):
            if pressed:
                if button == mouse.Button.left:  # 如果是左键点击
                    hwnd = win32gui.WindowFromPoint((x, y))  # 获取句柄
                    self.uim._2lineEdit_3.setText(str(hwnd))  # 设置句柄到lineEdit
                    listener.stop()  # 停止监听
                elif button == mouse.Button.right:  # 如果是右键点击
                    listener.stop()

        def click_listener():
            global listener
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()

        click_listener()
        self.showNormal()

    def mouseinfo(self):  # 鼠标信息
        pyautogui.mouseInfo()

    def QQ_Group_information(self):  # QQ群信息获取
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        if self.uim.Edge.isChecked():
            mode = 'Edge'
        elif self.uim.Chrome.isChecked():
            mode = 'Chrome'
        elif self.uim.IE.isChecked():
            mode = 'Ie'
        else:
            pyautogui.confirm("文件选择类型错误 请重试!")
            return 0
        Qid = self.uim.checkBox_qid.isChecked()
        sex = self.uim.checkBox_sex.isChecked()
        QQ_year = self.uim.checkBox_qq_year.isChecked()
        join_date = self.uim.checkBox_join_date.isChecked()
        send_date = self.uim.checkBox_send_date.isChecked()
        group_lv = self.uim.checkBox_group_lv.isChecked()
        folder = self.uim.QQ_Group_Save.text()
        result = function.QQ_Group_Obtain(mode, folder, Qid, sex, QQ_year, join_date, send_date, group_lv)
        if str(type(result)) == '<class \'selenium.common.exceptions.NoSuchWindowException\'>':
            pyautogui.confirm("操作取消")
        elif result == 'Cancel':
            pyautogui.confirm("操作取消")
        elif str(result[0:6]) == '文件保存成功':
            pyautogui.confirm(result)
        else:
            pyautogui.confirm(result, "错误:")

    def download_image(self):  # 下载QQ头像
        if exp < 20:
            pyautogui.confirm("该功能需要Lv2才能使用!\n按ctrl+o 或按f12 打开控制台 输入签到 签到一天即可使用!")
            return 0
        self.uim.QQ_Button_Dow.setEnabled(False)

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

        success = 0
        total = 0
        for i in range(self.uim.QQ_spinBox.value()):
            random_number = generate_random_number()
            url = f"https://q1.qlogo.cn/g?b=qq&nk={random_number}&s=640"
            response = requests.get(url)
            total = total + 1
            if response.status_code == 200:
                with open(f"./mod/picture/{random_number}.jpg", "wb") as file:
                    file.write(response.content)

                image_path = f"./mod/picture/{random_number}.jpg"

                if compare_images(image_path):
                    os.remove(f"./mod/picture/{random_number}.jpg")
                else:
                    success = success + 1
                    self.uim.QQ_label_t6.setText(f"有效次数:{success}次")
            self.uim.QQ_label_t3.setText(f"总下载次数:{total}次")
        if success == 0:
            self.uim.QQ_label_t6.setText("有效次数:0次")
        self.uim.QQ_Button_Dow.setEnabled(True)
        MyThread(play_warning_sound)
        pyautogui.confirm(f"图片下载成功!\n本次已成功下载{success}张图片(已删除默认头像)")

    def QQ_image_update(self):  # QQ个人信息资料一键更新
        result = pyautogui.confirm(
            "此功能只适用于旧版QQ! 请确认QQ版本后再使用\n请确保QQ主窗口已经打开 若打开则点击确认按钮 修改资料时 请勿移动鼠标\n若出现修改失败的情况 可能是间隔时间过小 略微调大即可")
        if result != "OK":
            return 0
        try:
            rest = self.uim.QQ_Doxb.value()
            result = function.QQ_Information_Update(rest)
            if result == 0:
                MyThread(play_warning_sound)
                pyautogui.confirm("资料修改成功")
            elif result == "Not Found":
                pyautogui.confirm("需要先下载图片才可使用")
                return 0
            else:
                raise Exception(result)
        except Exception as e:
            MyThread(play_warning_sound)
            pyautogui.confirm(e)
            traceback.print_exc()

    def Send_QQ(self):  # @QQ
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            if self.uim._2lineEdit.text() == "":
                pyautogui.confirm('请输入QQ号')
            elif self.uim._2doubleSpinBox.value() == 0.0:
                pyautogui.confirm("请输入间隔")
            elif len(self.uim._2lineEdit.text()) > 11 or len(
                    self.uim._2lineEdit.text()) <= 5 or not self.uim._2lineEdit.text().isdigit():
                pyautogui.confirm('请输入正确的QQ号')
            else:
                time.sleep(3)
                math = 0
                pause_time = self.uim._2doubleSpinBox.value()
                pyautogui.PAUSE = pause_time
                if self.uim._2checkBox.isChecked():
                    while True:
                        if keys.is_pressed("F10"):  # 按下F10退出
                            self.open_point_window()
                            break
                        math = math + 1
                        pyautogui.click(textedit_position)
                        pyautogui.write(f'@{self.uim._2lineEdit.text()}')
                        time.sleep(0.02)
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
                        if keys.is_pressed("F10"):  # 按下F10退出
                            self.open_point_window()
                            break
                        pyautogui.click(textedit_position)
                        pyautogui.write(f'@{self.uim._2lineEdit.text()}')
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
        def setText(aString):  # 设置剪贴板文本
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
            w.CloseClipboard()

        def getWindowSize(hwnd):  # 获取窗口的宽度和高度
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            return width, height

        def doClick(cx, cy, hwnd):
            width, height = getWindowSize(hwnd)  # 获取窗口的尺寸
            click_x = width + cx
            click_y = height + cy  # 计算相对底部的y坐标HELLO
            long_position = win32api.MAKELONG(click_x, click_y)  # 模拟鼠标指针 传送到指定坐标
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                 long_position)  # 模拟鼠标按下
            win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                                 long_position)  # 模拟鼠标弹起
            # 发送 Ctrl+V 来像聊天框粘贴信息

            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            # 按下 Ctrl 键
            win32api.keybd_event(ord('V'), 0, 0, 0)
            # 按下 V 键
            win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
            # 放开 V 键
            win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            # 放开 Ctrl 键

            # 向指定窗口发送 Enter 键
            win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)  # 按下 Enter 键
            win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开 Enter 键

        def send_qq(hwnd, msg):
            if msg != '###UNCOPY###':  # 当字符不等于这个时 复制内容
                setText(msg)
            # 投递剪贴板消息到QQ窗体
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            figure = self.uim._2spinBox.value()
            wait_time = self.uim._2doubleSpinBox_speed.value()
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)  # 等待窗口聚焦

            for i in range(int(figure)):
                doClick(handle_position[0], handle_position[1], hwnd)  # 点击 (30, height-60)
                time.sleep(wait_time)  # 等待操作完成

        hwnd = self.uim._2lineEdit_3.text()
        massage = self.uim._2textEdit.toPlainText()
        if hwnd == '':
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            pyautogui.confirm("请输入句柄")
        elif massage == '':
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            pyautogui.confirm("请输入需要发送的消息")
        else:
            try:
                send_qq(int(hwnd), massage)
                self.open_point_window()
            except Exception as e:
                pyautogui.confirm(f"发送失败 错误信息如下:\n {e}")

    def Send_Copy(self):  # 发送复制消息
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            time.sleep(3)
            pause_time = self.uim.copy_int.value()
            pyautogui.PAUSE = pause_time
            b = 0
            start_time = time.time()
            while True:
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.open_point_window()
                    end_time = time.time()
                    # 计算执行时间
                    execution_time = end_time - start_time
                    # 打印执行时间
                    print(f"执行时间: {execution_time} 秒")
                    break
                b = b + 1
                pyautogui.click(textedit_position)
                pyautogui.hotkey('ctrl', 'v')  # 粘贴
                time.sleep(0.02)
                randfigure = random.choice(Random_list)  # 随机字符输入
                if randfigure == 1:
                    pyautogui.press('.')
                elif randfigure == 2:
                    pyautogui.press('。')
                else:
                    pyautogui.press(',')
                pyautogui.click(send_position)  # 点击第二处位置
            print(f"本次Fuchen累计发送{b}条消息")
        else:
            pyautogui.confirm("QQ未启动!")

    def order_send(self):
        if self.uim.order_lineEdit.text() == '':
            pyautogui.confirm("请先选择文件")
            return 0
        target_process_name = "QQ.exe"
        if not check_process_exists(target_process_name):
            pyautogui.confirm("请先启动QQ！")
            return 0
        if position_status == False:
            pyautogui.confirm("需要先设置位置才能开始发送")
            return 0
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        time.sleep(3)

        if self.uim.order_radio_list.isChecked():
            wait_time = self.uim._2doubleSpinBox_order_list.value()
            pyautogui.PAUSE = wait_time
            for i in range(self.uim.order_list_int.value()):
                with open(self.uim.order_lineEdit.text(), 'r', encoding='utf-8') as file:
                    # 逐行读取文件内容
                    for line in file:
                        # 去除行尾的换行符
                        line = line.strip()
                        # 打印该行内容（可以查看复制内容是否正确）
                        if keys.is_pressed("F10"):  # 按下F10退出
                            self.open_point_window()
                            break
                        # 复制该行内容到剪切板
                        pyperclip.copy(line)
                        pyautogui.click(textedit_position)
                        #time.sleep(wait_time)
                        pyautogui.hotkey('ctrl', 'v')
                        time.sleep(0.02)
                        pyautogui.click(send_position)
                        # 暂停等待用户操作或观察复制内容
        else:
            wait_time = self.uim._2doubleSpinBox_order_random.value()
            pyautogui.PAUSE = wait_time
            # 读取文件内容到列表中
            with open(self.uim.order_lineEdit.text(), 'r', encoding='utf-8') as file:
                lines = file.readlines()
            # 随机选择一行
            for i in range(self.uim.order_random_int.value()):
                random_line = random.choice(lines).strip()
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.open_point_window()
                    break
                # 复制该行内容到剪切板
                pyperclip.copy(random_line)
                pyautogui.click(textedit_position)
                #time.sleep(wait_time)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.02)
                pyautogui.click(send_position)

    def Click_Record(self):  # 记录自动脚本
        if self.uim.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建'):
            pyautogui.confirm("需要先选择或创建配置文件")
            return 0
        self.showMinimized()
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        wait_time = self.uim.wait_doubleSpinBox.value()
        time.sleep(wait_time)
        current_position = pyautogui.position()
        print("开始记录自动脚本")
        global last_time, records, last_key, last_event_type

        records = []
        last_time = time.time()
        if self.uim.end_key_button.text() == "ESC":
            ed_bu = Key.esc
        elif self.uim.end_key_button.text() == "F8":
            ed_bu = Key.f8
        elif self.uim.end_key_button.text() == "F9":
            ed_bu = Key.f9
        elif self.uim.end_key_button.text() == "F10":
            ed_bu = Key.f10
        elif self.uim.end_key_button.text() == "END":
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
            interval = int((current_time - last_time) * 1000)  # 转换为毫秒
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

        def on_scroll(dx, dy):
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

        mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
        keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

        mouse_listener.start()
        keyboard_listener.start()

        keyboard_listener.join()

        move_times = 0
        move_total_time = 0
        for list_record in records:
            if list_record[2] == 'mouse move':
                if list_record[0] < 10:
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
        with open('./scripts/' + self.uim.button_file.text(), 'w') as f:
            for record in records:
                if record[0] != 0:
                    if isinstance(record[3][1], str) and len(record[3][1]) == 1 and record[3][
                        1].isupper():
                        record[3] = (record[3][0], record[3][1].lower())
                    f.write(str(record) + '\n')

        print("记录完毕")
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        self.showNormal()
        pyautogui.moveTo(current_position.x, current_position.y)

    def Click_Record_execute(self):  # 执行自动脚本
        if self.uim.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建'):
            pyautogui.confirm("需要先选择或创建配置文件")
            return 0
        stop_script = False  # 局部变量，用于控制脚本停止
        listener = None  # 全局引用监听器

        def key_listener():
            """监听键盘按键，检测终止按键"""
            nonlocal stop_script  # 使用非局部变量

            def on_press(key):
                try:
                    # 检测到按键时停止脚本
                    if self.uim.end_key_button.text() == "ESC":
                        ed_bu = Key.esc
                    elif self.uim.end_key_button.text() == "F8":
                        ed_bu = Key.f8
                    elif self.uim.end_key_button.text() == "F9":
                        ed_bu = Key.f9
                    elif self.uim.end_key_button.text() == "F10":
                        ed_bu = Key.f10
                    elif self.uim.end_key_button.text() == "END":
                        ed_bu = Key.end
                    else:
                        ed_bu = Key.esc
                    if key == ed_bu:
                        nonlocal stop_script
                        stop_script = True
                        print(f"检测到 {self.uim.end_key_button.text()}，脚本终止中...")
                except Exception as e:
                    print(f"按键监听异常: {e}")

            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            listener.join()

        # 启动键盘监听器线程
        listener_thread = threading.Thread(target=key_listener, daemon=True)
        listener_thread.start()


        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        wait_time = self.uim.wait_doubleSpinBox.value()
        current_position = pyautogui.position()
        count = self.uim._3spinBox_3.value()
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
            if key_char.upper() in special_keys:
                return special_keys[key_char.upper()]
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

        def precise_sleep(milliseconds):
            start = time.perf_counter()
            end = start + milliseconds / 1000.0
            while time.perf_counter() < end:
                pass

        records = []
        record_time = 0
        speed = self.uim.spinbox_play_speed.value()/100
        print('speed:', speed)
        with open('./scripts/' + self.uim.button_file.text(), 'r') as f:
            for line in f:
                if line[0] != '#':
                    record = eval(line.strip())
                    record_time += record[0]
                    records.append(record)
        print(f"记录执行时间:{record_time / 1000}秒")
        deal_time = 0
        for x in records:
            x[0] = int(x[0]/speed)
            deal_time += x[0]
        print(f"处理执行时间:{deal_time / 1000}秒")
        star = time.time()
        for i in range(count):  # 开始执行自动脚本
            for record in records:
                if stop_script:  # 检测是否需要终止
                    print("脚本执行已终止。")
                    listener.stop()  # 停止按键监听器
                    break
                #time.sleep((record[0] - 1) / 1000)  # 等待时间````
                precise_sleep(record[0]-1)
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
        print(f"实际执行时间:{(end_ti - star):.2f}秒")
        self.showNormal()
        pyautogui.moveTo(current_position.x, current_position.y)

        # 停止监听器
        if listener is not None:
            listener.stop()

    def about(self):
        pyautogui.confirm(
            f"版本:{Version}\nGui图形库:Pyqt5\n制作者:浮沉 QQ:3046447554 软件完全免费 纯净无广告\n软件免费 若发现收费购买 请联系我进行反馈\nUI设计本人没有灵感 略微草率还请谅解 如有建议请反馈",
            "Fuchen")

    def open_website(self):
        webbrowser.open("https://fcyang.cn/")

    def open_website_help(self):
        webbrowser.open("https://fcyang.cn/others/help.html")

    def delete_images(self):
        reply = QMessageBox.question(self, '确认删除', "你确定要删除文件夹内容吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            shutil.rmtree('./mod/picture')
            # 重新创建空文件夹
            os.mkdir('./mod/picture')
            pyautogui.confirm("图片清除成功!")

    def createMenu(self):  #连点器开启按键
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

        action12 = QAction("自定义", self)
        action12.triggered.connect(lambda: self.action_Clicked("自定义"))

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
        menu.addAction(action12)

        return menu

    def create_key_Menu(self, types):  # 自动脚本录制结束按钮菜单
        if types == 'record':
            key_menu = QMenu(self)

            action1 = QAction("ESC", self)
            action1.triggered.connect(lambda: self.key_menu_com('record','ESC'))

            action2 = QAction("F8", self)
            action2.triggered.connect(lambda: self.key_menu_com('record',"F8"))

            action3 = QAction("F9", self)
            action3.triggered.connect(lambda: self.key_menu_com('record',"F9"))

            action4 = QAction("F10", self)
            action4.triggered.connect(lambda: self.key_menu_com("record", 'F10'))

            action5 = QAction("END", self)
            action5.triggered.connect(lambda: self.key_menu_com("record", 'END'))

            key_menu.addAction(action1)
            key_menu.addAction(action2)
            key_menu.addAction(action3)
            key_menu.addAction(action4)
            key_menu.addAction(action5)
            return key_menu
        elif types == 'execute':
            key_menu = QMenu(self)

            action1 = QAction("ESC", self)
            action1.triggered.connect(lambda: self.key_menu_com("execute", 'ESC'))

            action2 = QAction("F8", self)
            action2.triggered.connect(lambda: self.key_menu_com("execute", 'F8'))

            action3 = QAction("F9", self)
            action3.triggered.connect(lambda: self.key_menu_com("execute", 'F9'))

            action4 = QAction("F10", self)
            action4.triggered.connect(lambda: self.key_menu_com("execute", 'F10'))

            action5 = QAction("END", self)
            action5.triggered.connect(lambda: self.key_menu_com("execute", 'END'))

            key_menu.addAction(action1)
            key_menu.addAction(action2)
            key_menu.addAction(action3)
            key_menu.addAction(action4)
            key_menu.addAction(action5)
            return key_menu

    def action_Clicked(self, key):
        if key == '自定义':
            custom = pyautogui.prompt()
            if custom.isdigit():
                self.uim.sort = f'自 {custom}'
                self.uim._3pushButton_4.setText(f"设置启停快捷键({self.uim.sort})")
            else:
                RESULT = pyautogui.confirm(
                    "格式错误 请输入正确的按键所对应的数字 详情请参考: https://fcyang.cn/others/key.html\n是否跳转到该页面?")
                if RESULT == "OK":
                    webbrowser.open("https://fcyang.cn/others/key.html")
        else:
            self.uim.sort = key
            self.uim._3pushButton_4.setText(f"设置启停快捷键({self.uim.sort})")

    def key_menu_com(self, types, key):
        if types == 'record':
            self.uim.end_key = key
            self.uim.end_key_button.setText(f"{key}")
        elif types == 'execute':
            self.uim.end_execute_key = key
            self.uim.end_execute_button.setText(f"{key}")

    def delete_file(self):
        if (self.uim.button_file.text() not in ('选择配置文件', '暂无配置文件 需要创建')):
            result = pyautogui.confirm("你确定要删除配置文件吗？")
            if result == "OK":
                os.remove('./scripts/' + self.uim.button_file.text())
                self.uim.populateMenu('scripts')
                # 列出文件夹中的所有文件和文件夹
                files_in_folder = os.listdir("scripts")
                # 检查文件夹中是否有文件
                if len(files_in_folder) == 0:
                    txt = "暂无配置文件 需要创建"
                else:
                    txt = '选择配置文件'
                self.uim.button_file.setText(txt)

    def create_file(self):
        files_in_folder = os.listdir("scripts")
        if len(files_in_folder) == 0:
            txt = "选择配置文件"
            self.uim.button_file.setText(txt)
        file_name = self.uim.file_lineEdit.text()
        directory = './scripts/'
        full_path = os.path.join(directory, file_name)
        with open(full_path, 'w') as file:
            pass
        self.update_filename()
        self.uim.populateMenu('scripts')

    def update_filename(self):
        current_name = self.uim.file_lineEdit.text()
        parts = current_name.split('-')
        if len(parts) == 4:
            number = int(parts[3].replace('.txt', ''))
            new_number = number + 1
            new_name = f"{parts[0]}-{parts[1]}-{parts[2]}-{new_number:02d}.txt"
            self.uim.file_lineEdit.setText(new_name)

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

    def update_checks(self):  # 判断哪个 RadioButton 被选中  序列发送类型选择
        if self.uim.order_radio_list.isChecked():
            self.uim.order_list_int_label.setEnabled(True)
            self.uim.order_list_int.setEnabled(True)
            self.uim.order_random_int_label.setEnabled(False)
            self.uim.order_random_int.setEnabled(False)
            self.uim.order_list_speed.setEnabled(True)
            self.uim._2doubleSpinBox_order_list.setEnabled(True)
            self.uim.order_random_speed.setEnabled(False)
            self.uim._2doubleSpinBox_order_random.setEnabled(False)
        elif self.uim.order_radio_random.isChecked():
            self.uim.order_list_int_label.setEnabled(False)
            self.uim.order_list_int.setEnabled(False)
            self.uim.order_random_int_label.setEnabled(True)
            self.uim.order_random_int.setEnabled(True)
            self.uim.order_list_speed.setEnabled(False)
            self.uim._2doubleSpinBox_order_list.setEnabled(False)
            self.uim.order_random_speed.setEnabled(True)
            self.uim._2doubleSpinBox_order_random.setEnabled(True)

    def mixPicture(self):  # 图片格式转换
        # 检查选择的格式
        if self.uim.JPG_radioButton.isChecked():
            output_image_format = "JPG"
        elif self.uim.PNG_radioButton.isChecked():
            output_image_format = "PNG"
        elif self.uim.GIF_radioButton.isChecked():
            output_image_format = "GIF"
        else:
            pyautogui.confirm("ERROR!")
            return 0

        input_image_path = self.uim._5lineEdit4.text()
        output_folder_path = self.uim._5lineEdit5.text()
        if input_image_path == '' or output_folder_path == '':
            pyautogui.confirm("请选则文件")
            return 0
        put = (input_image_path.split('.')[-1]).lower()
        out_put = output_image_format.lower()
        file_name = os.path.splitext(os.path.basename(input_image_path))[0]
        file_path = output_folder_path + '\\' + file_name + '.' + out_put
        if put == out_put:
            pyautogui.confirm("输入输出文件类型一致")
            return 0
        result = function.Convert_File(put, out_put, input_image_path, output_folder_path, file_name, self)
        if result == 0:
            pyautogui.confirm(f"文件转换成功\n{input_image_path}\n{file_path}")
        else:
            pyautogui.confirm(f"文件转换失败\n错误如下:{result}")

    def download(self):  # 下载网易云音乐
        try:
            download_url = 'https://music.163.com/song/media/outer/url?id={}'
            headers = {
                'Referer': 'https://music.163.com/search/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
            }

            url = self.uim._5lineEdit.text()
            music_id = url.split('=')[1]
            response = requests.get(download_url.format(music_id), headers=headers)
            file_name = self.uim._5lineEdit2.text()
            save_path = f'{self.uim._5lineEdit3.text()}\\{file_name}'
            with open(save_path, 'wb') as file:
                file.write(response.content)
            with open(save_path, 'rb') as f:
                first_line = f.readline().decode('utf-8', errors='ignore')
                if '<!DOCTYPE html>' in first_line:
                    self.show_message_box("提示", "下载失败 该歌曲可能是VIP专属 或其他原因 VIP歌曲暂不支持解析")
                else:
                    # 获取文件大小（以字节为单位）
                    file_size_bytes = os.path.getsize(save_path)
                    # 将字节转换为 KB 或 MB，并格式化输出
                    if file_size_bytes < 1_000_000:  # 小于 1 MB
                        file_size = f"{(file_size_bytes / 1_024):.2f} KB"  # 转换为 KB
                    else:
                        file_size = f"{(file_size_bytes / 1_024 / 1_024):.2f} MB"  # 转换为 MB

                    self.show_message_box("提示", f"下载成功! 文件大小:{file_size}")
        except Exception as e:
            self.show_message_box("提示", f"下载失败:{e}")

    def deal_pictures(self, file_name_V):
        # 输出图像保存路径
        output_folder = './trend'
        shutil.rmtree(output_folder)
        # 重新创建空文件夹
        os.mkdir(output_folder)
        # os.makedirs(output_folder, exist_ok=True)
        # 打开视频文件
        cap = cv2.VideoCapture(file_name_V)
        # 检查视频是否成功打开
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        # 函数：处理每个帧并保存
        def save_frame(frame_data):
            frame, frame_number = frame_data
            frame = cv2.resize(frame, (1000, 600))
            output_path = os.path.join(output_folder, f'frame_{frame_number}.jpg')
            cv2.imwrite(output_path, frame)

        frame_count = 0
        frame_list = []
        # 读取视频帧并存储在列表中
        while True:
            ret, frame = cap.read()
            # 如果未能读取帧，则终止循环
            if not ret:
                print("End of video or error occurred.")
                break
            frame_list.append((frame, frame_count + 1))
            frame_count += 1
        # 释放视频捕获对象
        cap.release()
        # 使用多线程保存帧
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(save_frame, frame_list)
        print(f"Frames saved successfully. Total frames: {frame_count}")

    def show_folder_dialog(self, number):  # 文件路径选择
        if number == 1:  # 网音乐音乐输出路径
            folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            folder_path = folder_path.replace("/", "\\")
            self.uim._5lineEdit3.setText(folder_path)
        elif number == 2:  # 图片输入
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                       "Image Files (*.jpg *.png *.bmp *.gif *.pdf *.docx)",
                                                       options=options)
            file_name = file_name.replace("/", "\\")
            if file_name:
                self.uim._5lineEdit4.setText(file_name)
                if self.uim._5lineEdit5.text() == '':
                    parent_folder = os.path.dirname(file_name)
                    self.uim._5lineEdit5.setText(parent_folder)
        elif number == 3:  # 图片输出路径
            folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            folder_path = folder_path.replace("/", "\\")
            self.uim._5lineEdit5.setText(folder_path)
        elif number == 4:  # QQ群信息保存
            folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            folder_path = folder_path.replace("/", "\\")
            self.uim.QQ_Group_Save.setText(folder_path)
        elif number == 5:  # QQ序列发送文件选择
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                       "Image Files (*.txt)",
                                                       options=options)
            file_name = file_name.replace("/", "\\")
            self.uim.order_lineEdit.setText(file_name)

    def quit_team_H(self):  #队员退出队伍
        self.uim.create_team_button.setVisible(True)  # 创建队伍按钮
        self.uim.button_copy_id.setVisible(False)  # 复制
        self.uim.random_id_Label.setText("队伍ID为:")
        self.uim.random_id_Label.setVisible(False)
        self.uim.add_team_label.setVisible(True)  # 加入队伍标签
        self.uim.button_copy_id.setVisible(False)  # 复制ID按钮
        self.uim.add_team_ID.setVisible(True)
        self.uim.add_team_lineEdit.setVisible(True)
        self.uim.add_team_button.setVisible(True)
        self.uim.create_team_label_prompt.setVisible(False)


        for button in self.uim.buttonGroup2.buttons():
            button.setVisible(False)
        for button in self.uim.buttonGroup3.buttons():
            button.setVisible(False)
        self.uim.run_execute.setVisible(False)

        icon = QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
        scaled_icon = icon.pixmap(QSize(140, 140)).scaled(
            QSize(140, 140),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        self.uim.user2_image.setIcon(QIcon(scaled_icon))
        self.uim.user2_image.update()
        self.uim.user2_name.setText("等待用户加入")
        self.uim.user2_id.setText("ID:")

        self.uim.talk_textBrowser.setVisible(False)
        self.uim.talk_lineEdit.setVisible(False)

    def quit_team_C(self):  # 队长退出队伍
        self.uim.create_team_label.setVisible(True)
        self.uim.random_id_Label.setText("队伍ID为:")
        self.uim.random_id_Label.setVisible(False)
        self.uim.create_team_button.setVisible(True)
        self.uim.add_team_label_prompt_right.setVisible(False)


        self.uim.add_team_label.setVisible(True)
        self.uim.add_team_label_prompt.setVisible(False)
        self.uim.add_team_ID.setVisible(True)
        self.uim.add_team_lineEdit.setText("")
        self.uim.add_team_lineEdit.setVisible(True)
        self.uim.add_team_button.setVisible(True)

        icon = QIcon("./image/other_user.png")  # 将此处的路径替换为实际的图像路径
        scaled_icon = icon.pixmap(QSize(140, 140)).scaled(QSize(140, 140), Qt.AspectRatioMode.IgnoreAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)
        self.uim.user2_image.setIcon(QIcon(scaled_icon))
        self.uim.user2_image.setIconSize(QSize(140, 140))
        self.uim.user2_name.setText("等待用户加入")
        self.uim.user2_id.setText("ID:")
        self.uim.talk_textBrowser.setVisible(False)
        self.uim.talk_lineEdit.setVisible(False)
        self.uim.talk_textBrowser.setGeometry(20, 480, 240, 80)
        self.uim.talk_lineEdit.setGeometry(20, 560, 240, 20)
        self.uim.wait_label.setVisible(False)

    def team(self):  # 创建队伍
        self.uim.create_team_button.setVisible(False)  # 创建队伍按钮
        self.uim.add_team_label.setVisible(False)  #加入队伍标签
        self.uim.button_copy_id.setVisible(True)  # 复制ID按钮
        characters = string.ascii_letters + string.digits
        global random_string
        random_string = ''.join(random.choices(characters, k=30))
        self.uim.random_id_Label.setText(f"队伍ID为:{random_string}")
        self.uim.random_id_Label.setVisible(True)

        self.uim.create_team_label_prompt.setVisible(True)  # 队伍已创建
        self.uim.add_team_ID.setVisible(False)  # ID label
        self.uim.add_team_lineEdit.setVisible(False)  # 输入栏
        self.uim.add_team_button.setVisible(False)  # 加入按钮

        send_encry(f'10004 {random_string}')

    def jointeam(self):
        id = self.uim.add_team_lineEdit.text()
        if len(id) != 30:
            self.show_message_box("提示", "队伍id不正确!")
        else:
            send_encry(f'20001 {id}')

    def team_c(self):
        captain, member = self.uim.checkRadio()
        if member == 'handle':
            send_encry('20011')
        elif member == 'qq':
            send_encry('20012')
        elif member == 'copy':
            send_encry('20013')
        elif member == 'renew':
            send_encry('20014')
        elif member == 'execute':
            send_encry('20015')
        else:
            send_encry('20016')
        if captain == 'handle':
            self.Handle_Send()
        elif captain == 'qq':
            self.Send_QQ()
        elif captain == 'copy':
            self.Send_Copy()
        elif captain == 'renew':
            self.QQ_image_update()
        elif captain == 'execute':
            self.Click_Record_execute()
        else:
            pyautogui.confirm("ERROR! UNKNOWN")

    def copy(self):
        global random_string
        clipboard = QApplication.clipboard()
        clipboard.setText(f'{random_string}')

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


class LoginWindow(QMainWindow):  # 实例化登录窗口
    global resign_window, reword_window
    def __init__(self):
        super().__init__()
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self)
        if remember == True:
            self.ui.checkBox.click()
        if Log == True:
            self.ui.checkBox2.click()
        self.ui.Account_lineEdit.setText('此版本为开源版本 点击登录即可使用')
        self.ui.Password_lineEdit.setText('此版本为开源版本 点击登录即可使用')
        self.setWindowTitle("Fuchen 登录")
        icon = QIcon("./image/window.ico")
        self.setWindowIcon(icon)
        self.ui.pushButton_signin.clicked.connect(self.reg)  # 注册按钮
        self.ui.Login_Button.clicked.connect(lambda: self.LOGIN("login"))  # 登录按钮

        self.ui.pushButton_tourist.clicked.connect(lambda: self.LOGIN("tourist_login"))  # 游客登录
        self.ui.pushButton_short.clicked.connect(self.showMinimized)  # 最小化按钮
        self.ui.pushButton_more.clicked.connect(self.open_file_background)

        self.ui.pushButton_quit.clicked.connect(self.close)  # 关闭窗口按钮

        self.open_memory_hotkey = QShortcut(QKeySequence("Ctrl+1"), self)
        self.open_memory_hotkey.activated.connect(lambda: self.key("memory"))
        self.open_autologin_hotkey = QShortcut(QKeySequence("Ctrl+2"), self)
        self.open_autologin_hotkey.activated.connect(lambda: self.key("autologin"))

        self.ui.Account_lineEdit.returnPressed.connect(self.ui.Password_lineEdit.setFocus)
        self.ui.Password_lineEdit.returnPressed.connect(lambda: self.LOGIN("login"))
        font = QFont("等线", 14)
        self.ui.Account_lineEdit.setFont(font)
        self.ui.Password_lineEdit.setFont(font)
        self.ui.Number_Label.setText(f'当前在线人数:{Number_People}')
        self.ui.Version_Label.setText(f'版本:{Version}')
        self.ui.pushButton_reword.clicked.connect(self.rew)

    def open_file_background(self):
        RESULE = pyautogui.confirm("登录界面背景图片可自定义\n若文件夹中存放多个图片将随机选择一张\n点击确认将打开图片文件夹")
        if RESULE == "OK":
            folder_path = './image/Background'  # 修改为你要打开的文件夹路径
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)


    def closeEvent(self, e):
        self.close()
        if reword_window == True:
            window_reword.close()
        if resign_window == True:
            window_signin.close()
        #os._exit(0)

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

    def LOGIN(self, mode):  # 登录函数
        global Log,city_name,Account
        try:
            if mode == 'login':
                self.ui.Login_Button.setEnabled(False)
                time.sleep(0.1)
                Account = self.ui.Account_lineEdit.text()
                Password = self.ui.Password_lineEdit.text()
                '''if (len(Account) != 6) and ('@' not in Account):  #非邮箱非数字
                    if Log == True:
                        window_login.show()
                    pyautogui.confirm("账号为6位数字或邮箱 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if not (7 < len(Password) < 16):
                    if Log == True:
                        window_login.show()
                    pyautogui.confirm("密码为8-15位 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if (len(Account)==6) and (not Account.isdigit()):  #数字类型错误
                    pyautogui.confirm("账号为6位数字或邮箱 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if '@' in Account:
                    # 通过 '@' 分割邮箱
                    local_part, domain_part = Account.split('@')
                    # 只将域名部分转换为小写
                    domain_part = domain_part.lower()
                    # 将用户名和处理后的域名拼接起来
                    Account = f"{local_part}@{domain_part}"
                    del local_part,domain_part'''
                '''send_encry('login')
                time.sleep(0.1)
                send_encry((Account + ' ' + Password + ' ' + city_name + ' ' + system + ' ' + computer_name))
                log_ST = s.recv(256)
                log_ST = send_decry(log_ST)  # 密码是否正确状态'''
                log_ST = 'True'
                if eval(log_ST) == True:
                    print("密码正确 正在加载中")
                elif log_ST == "Cooling":
                    pyautogui.confirm("账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
                else:
                    print("密码错误 请重试")
            elif mode == 'tourist_login':
                self.ui.Login_Button.setEnabled(False)
                Account = "游客"
                Password = "None"
                send_encry('tourist_login')
                time.sleep(0.1)
                send_encry(city_name)
                log_ST = s.recv(256)
                log_ST = send_decry(log_ST)  # 密码是否正确状态
            elif mode == 'offline_login':
                self.ui.Login_Button.setEnabled(False)
                Account = "离线"
                Password = "None"
                time.sleep(0.1)
                log_ST = 'True'
            else:
                log_ST = 'False'
            if log_ST == 'True':  # 密码正确
                self.ui.pushButton_signin.setEnabled(False)
                self.ui.Login_Button.setEnabled(False)
                self.ui.pushButton_short.setEnabled(False)
                self.ui.pushButton_quit.setEnabled(False)
                self.ui.Login_Button.setText("正在加载用户数据")
                self.ui.Login_Button.repaint()
                # 记录开始时间
                start_time = time.time()
                if connect_status != None:
                    pass
                    '''dat = s.recv(4096)  # 开始处理用户信息
                    try:
                        dat = send_decry(dat)
                    except:
                        RESULT = pyautogui.confirm("数据处理失败 请尝试重启客户端\n点击确认将自动重启")
                        if RESULT == 'OK':
                            try:
                                subprocess.Popen([Fuchen_fullname])
                            except:
                                pass'''
                else:
                    dat = "游客 None False 2000-1-1 100 000000"
                #dat = dat.split()
                dat = ['开源版本', '123456@example.com', '1000', '2025-1-27','123456']
                print(dat)
                global Name, Email, exp, HImage_date
                Name = dat[0]  # 名称
                Email = dat[1]  # 邮箱
                HeadImage_status = dat[2]  # 是否有头像
                exp = int(dat[4])  # 经验值
                if "@" in Account:
                    Account = dat[5]
                '''fixed_key = b'j7_d7DWdCj7AzRdDhY7FJ0djQUa1t6_fJ0itlCubwMM='  # 使用一个固定的密钥
                # 创建一个Fernet密码学对象
                cipher_suite = Fernet(fixed_key)
                # 解密
                # 先使用Base64解码
                ciphertext_decoded = base64.b64decode(exp)
                decrypted_bytes = cipher_suite.decrypt(ciphertext_decoded)
                # 将解密后的字节串转换回数字
                exp = int(decrypted_bytes.decode('utf-8'))  # 解密后的经验值
                global lv
                if 0 <= exp < 20:
                    lv = 1
                elif 20 <= exp <300:
                    lv = 2
                elif 300 <= exp < 600:
                    lv = 3
                elif 600 <= exp <1000:
                    lv = 4
                elif 1000 <=exp:
                    lv = 5
                # 将整数转换为字节数组（二进制数据）
                data_to_encrypt = str(lv).encode('utf-8')
                # 创建SHA-512哈希对象
                sha512_hash = hashlib.sha512()
                # 更新哈希对象以处理数据
                sha512_hash.update(data_to_encrypt)
                # 计算SHA-512哈希值
                new_lv = sha512_hash.hexdigest()  # 经过sha512再 次加密后的经验等级 1-2-3-4-5'''
                HImage_date = dat[3]  # 用户上一次更新头像的日期
                year, month, day = map(int, HImage_date.split('-'))
                HImage_date = date(year, month, day)  # 继续处理
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
                                chunk = s.recv(2048)
                                time.sleep(0.2)
                                if not chunk:
                                    break
                                file.write(chunk)
                                total_received += len(chunk)
                                progress_percentage = round(total_received / file_size * 100, 2)  # 将进度转换为百分比并保留两位小数
                                self.ui.Login_Button.setText(f"正在加载用户头像 {progress_percentage}%")
                                self.ui.Login_Button.repaint()
                        print('文件写入完成')
                        global HImage_load_status
                        HImage_load_status = True
                        self.ui.Login_Button.setText("头像加载成功")
                    except Exception as e:
                        print("文件接收类型错误", e)
                        self.ui.Login_Button.setText("头像加载失败")
                    self.ui.Login_Button.repaint()
                    time.sleep(0.2)

                if self.ui.checkBox.isChecked() and self.ui.checkBox2.isChecked():  #记住密码 自动登录
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
                elif self.ui.checkBox2.isChecked():  # 自动登录
                    # 读取 JSON 文件
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    # 添加新元素到数据结构
                    config["AutoLogin"] = True
                    Log = True
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                else:  #不记住密码/自动登录
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
                # 关闭登录窗口，显示主窗口
                global window_s, Ask, Theme, Sound, ClosePrompt, CloseExecute, Path_Custom_S, Path_Trend_S, transparent, FPS
                window_s = False
                # 读取JSON文件
                with open('config.json', 'r') as file:
                    config = json.load(file)
                Sound = config.get("Sound", True)
                ClosePrompt = config.get("ClosePrompt", True)
                CloseExecute = config.get("CloseExecute", "Close")
                Theme = config.get("Theme", "White")  # 主题
                if Theme == "Custom":
                    Path_Custom_S = config.get("Path")
                elif Theme == "Trend":
                    Path_Trend_S = config.get("Path")
                transparent = config.get("transparent", 30)
                FPS = config.get("FPS", 16)
                try:
                    windows = Ui_Form()
                    windows.show()
                    print("窗口成功打开")

                    process = psutil.Process()
                    memory_info = process.memory_info()
                    memory_info = memory_info.rss / (1024 * 1024)  # 输出内存占用
                    print(f"内存占用(MB): {memory_info:.2f} MB")
                    end_time = time.time()
                    execution_time = end_time - start_time
                    execution_time = round(execution_time, 2)
                    global current_time_string
                    sys_list.append('g' + '[' + time.strftime(
                        "%H:%M:%S") + ']' + f"窗口打开成功 本次登录耗时:{execution_time}秒")
                    windows.show()
                except Exception as e:
                    traceback.print_exc()
                    print(e)


            elif log_ST == "Cooling":
                pyautogui.confirm("账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
            else:
                self.ui.Login_Button.setEnabled(False)
                if Log == True:
                    window_login.show()
                time.sleep(0.5)
                pyautogui.confirm("密码错误")
                self.ui.Login_Button.setEnabled(True)
        except Exception as e:
            traceback.print_exc()
            pyautogui.confirm("未知错误", e)

    def reg(self):
        global resign_window
        if resign_window is False:
            resign_window = True
            window_signin.exec_()
    def rew(self):
        global reword_window
        if reword_window is False:
            reword_window = True
            window_reword.exec_()


class SigninWindow(QtWidgets.QDialog):  # 实例化注册窗口
    global Email
    Email = None
    def __init__(self):
        super().__init__()
        self.ui2 = Signin.MainWindow()
        self.ui2.setupUi(self)
        self.ui2.SigninButton.clicked.connect(self.Registration)
        self.ui2.QuitButton.clicked.connect(self.close)
        self.pushButton3 = QPushButton(self)
        self.pushButton3.setGeometry(QtCore.QRect(255, 290, 105, 31))
        self.pushButton3.setText("获取验证码")
        self.pushButton3.setObjectName("pushButton")
        # 创建圆角按钮样式
        style = "QPushButton#pushButton {border-radius: 5px; background-color: #55c3ff; color: white;}"
        self.pushButton3.setStyleSheet(style)
        self.pushButton3.clicked.connect(self.send)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 60
        self.border_width = 8
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    def send(self):
        global Email
        Email = self.ui2.EmailEdit.text()
        if validate_email(Email) == 0:
            send_encry("**--*Registration*--**")
            time.sleep(0.3)
            send_encry(f'Email {self.ui2.EmailEdit.text()}')
            self.pushButton3.setEnabled(False)
            style = "QPushButton#pushButton {border-radius: 5px; background-color: #e0e0e0; color: white;}"
            self.pushButton3.setStyleSheet(style)
            result = s.recv(256)
            result = send_decry(result)
            if result == 'Successfully_send':
                self.remaining_time = 60
                self.timer.start(1000)
                self.update_timer()
                pyautogui.confirm("验证码发送成功!")
            else:
                self.pushButton3.setEnabled(True)
                pyautogui.confirm("验证码发送失败")
        else:
            pyautogui.confirm("请输入正确的邮箱")

    def update_timer(self):  # 验证码更新
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.pushButton3.setText(f"剩余时间: {self.remaining_time}秒")
        else:
            self.timer.stop()
            self.pushButton3.setText("获取验证码")
            self.pushButton3.setEnabled(True)
            style = "QPushButton#pushButton {border-radius: 5px; background-color: #55c3ff; color: white;}"
            self.pushButton3.setStyleSheet(style)

    def Registration(self):
        global Email
        input_name = self.ui2.NameEdit.text()
        input_password = self.ui2.PasswordEdit.text()
        input_email = self.ui2.EmailEdit.text()
        input_check = self.ui2.CheckEdit.text()
        if not (0 < len(input_name) < 11):
            self.show_message_box('提示', '名称只能为1-10位')
            return 0
        if not (7 < len(input_password) < 16):
            self.show_message_box('提示', '密码只能为8-15位')
            return 0
        if len(input_email) == 0:
            self.show_message_box('提示', '请输入邮箱')
            return 0
        if len(input_check) != 6:
            self.show_message_box('提示','请输入六位验证码')
            return 0
        if validate_email(input_email) == 1:
            self.show_message_box('提示', '邮箱格式不正确')
            return 0
        if Check(input_name) == 1:
            self.show_message_box('提示', '名称只能包含中文 26个大小写字母以及  .  -  _  =  ')
            return 0
        if Check_Password(input_password) == 1:
            self.show_message_box('提示', '密码只能包含26个大小写字母以及  .  -  _  =  ')
            return 0
        if not Email:
            self.show_message_box('提示','未发送验证码 请发送后再尝试')
            return 0
        send_encry("**--*Registration*--**")
        time.sleep(0.3)
        try:
            res = requests.get('http://myip.ipip.net', timeout=5).text
            # 提取城市信息
            split_res = res.split('  ')
            city_info = split_res[-2]  # 倒数第二个元素是城市信息
            city_info = city_info.split(' ')
            city_info = city_info[-1]
            city_name = city_info
        except:
            city_name = 'Unknown'
        info = f"Rigistration {input_check} {input_name} {input_password} {Email} {city_name}"
        send_encry(str(info))
        Check_Email = s.recv(512)
        Check_Email = send_decry(Check_Email)
        if Check_Email == 'Right_Check':
            Reg_Staus = s.recv(1024)
            Reg_Staus = send_decry(Reg_Staus)
            Reg_Staus = Reg_Staus.split()
            if Reg_Staus[0] == 'Successfully':
                self.close()
                window_login.close()
                # 获取桌面路径
                def get_desktop_path():
                    return os.path.join(os.path.expanduser("~"), "Desktop")
                desktop_path = get_desktop_path()
                file_name = 'Fuchen账号.txt'
                file_path = os.path.join(desktop_path, file_name)
                # 写入文件
                with open(file_path, "w", encoding='utf-8') as file:
                    file.write(
                        f"您已注册成功 \n系统随机分配的账号ID为:{Reg_Staus[1]}  密码:{self.ui2.PasswordEdit.text()}\n")
                    file.write(f"请妥善保管账号和密码 请勿泄露给他人！\n感谢您的使用")
                pyautogui.alert(f"账号注册成功!您的ID为:{Reg_Staus[1]}"
                                f"账号ID由服务器自动分配 登录时需用ID登录而不是用户名\n\n"
                                f"为了避免您忘记账号 现已将您的账号ID文件创建到桌面 >>Fuchen账号.txt中\n"
                                f"请您尽快记住账号并妥当保管文件 以防丢失账号 泄露账号等情况\n\n"
                                f"在此非常感谢您使用我的软件\n"
                                f"请关闭此窗口 或点击确认按钮 登录线上模式使用吧!")
            else:
                pyautogui.confirm("注册失败")
                self.close()

        elif Check_Email == 'Error_Email':
            self.pushButton3.setEnabled(False)
            MyThread(play_warning_sound)
            pyautogui.confirm("邮箱已被注册! 请更换邮箱后注册")
            self.pushButton3.setEnabled(True)
        else:
            pyautogui.confirm("验证码不正确")


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
            ref = QRectF(10 - i, 10 - i, self.width() - (10 - i) * 2, self.height() - (10 - i) * 2)
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
        if e.y() <= 35:  # 35像素的标题栏高度
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

    def closeEvent(self, e):
        global resign_window
        if resign_window is True:
            self.close()
            resign_window = False


class RewordWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # 存储单例窗口实例的类属性
        self.ui_reword = ReWord.Ui_MainWindow()
        self.ui_reword.setupUi(self)
        self.setWindowIcon(QIcon('./image/Component/重置密码.png'))
        self.setWindowTitle("重置密码")
        self.ui_reword.pushButton_check.clicked.connect(self.Check_identity)
        self.ui_reword.pushButton_getcheck.clicked.connect(self.get_check)
        self.ui_reword.pushButton_a.clicked.connect(self.reword_password)
        self.layout = [self.ui_reword.label, self.ui_reword.label_2, self.ui_reword.lineEdit, self.ui_reword.lineEdit_2,
                       self.ui_reword.pushButton_getcheck, self.ui_reword.pushButton_check]

        self.layout_after = [self.ui_reword.label_a, self.ui_reword.label_a2, self.ui_reword.lineEdit_a,
                             self.ui_reword.lineEdit_a2, self.ui_reword.pushButton_a]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 60

    def update_timer(self):  # 验证码更新
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.ui_reword.pushButton_getcheck.setText(f"剩余时间: {self.remaining_time}秒")
        else:
            self.timer.stop()
            self.ui_reword.pushButton_getcheck.setText("获取验证码")
            self.ui_reword.pushButton_getcheck.setEnabled(True)
            style = "QPushButton#pushButton {border-radius: 5px; background-color: #55c3ff; color: white;}"
            self.ui_reword.pushButton_getcheck.setStyleSheet(style)

    def show_message_box(self, head, message):
        QMessageBox.question(self, head, message,
                             QMessageBox.Yes)

    def get_check(self):
        global Email
        Email = self.ui_reword.lineEdit.text()
        if validate_email(Email) == 0:
            send_encry("**--*Reword*--**")
            print("开始重置密码")
            time.sleep(0.3)
            send_encry(f'Email {Email}')
            self.ui_reword.pushButton_getcheck.setEnabled(False)
            style = "QPushButton#pushButton {border-radius: 5px; background-color: #e0e0e0; color: white;}"
            self.ui_reword.pushButton_getcheck.setStyleSheet(style)
            result = s.recv(256)
            result = send_decry(result)
            print(result)
            if result == 'Successfully_send':
                self.remaining_time = 60
                self.timer.start(1000)
                self.update_timer()
                pyautogui.confirm("验证码发送成功!")
            else:
                self.ui_reword.pushButton_getcheck.setEnabled(True)
                pyautogui.confirm("验证码发送失败")
        else:
            self.show_message_box("提示", "请输入正确的邮箱")

    def Check_identity(self):
        global Email
        Check_word = self.ui_reword.lineEdit_2.text()
        send_encry("**--*Reword*--**")
        time.sleep(0.3)
        send_encry(f"Check {Email} {Check_word}")
        result = s.recv(1024)
        result = send_decry(result)
        if result == "Error_Check":
            time.sleep(0.5)
            self.show_message_box("提示", "验证码错误！")
            return 0
        elif result == "Error_Email":
            time.sleep(0.5)
            self.show_message_box("提示", "账号不存在 无法重置密码")
            return 0
        for index in self.layout:
            if index is not None:
                start_pos = index.pos()
                end_pos = QRect(-500, start_pos.y(), index.width(), index.height())
                animation = QPropertyAnimation(index, b"geometry", self)
                animation.setDuration(300)
                animation.setStartValue(QRect(start_pos, index.size()))
                animation.setEndValue(end_pos)
                easing_curve = QEasingCurve(QEasingCurve.InQuad)
                animation.setEasingCurve(easing_curve)
                animation.start()
        QTimer.singleShot(100, self.showAfterAnimation)

    def showAfterAnimation(self):
        self.ui_reword.label.deleteLater()
        self.ui_reword.label_2.deleteLater()
        self.ui_reword.lineEdit.deleteLater()
        self.ui_reword.lineEdit_2.deleteLater()
        self.ui_reword.pushButton_getcheck.deleteLater()
        self.ui_reword.pushButton_check.deleteLater()
        position = [30, 30, 120, 120, 120]
        num = 0
        for index in self.layout_after:
            pox = position[num]
            num = num + 1
            if index is not None:
                start_pos = index.pos()
                end_pos = QRect(pox, index.y(), index.width(), index.height())
                animation = QPropertyAnimation(index, b"geometry", self)
                animation.setDuration(450)
                animation.setStartValue(QRect(start_pos, index.size()))
                animation.setEndValue(end_pos)
                easing_curve = QEasingCurve(QEasingCurve.InQuad)
                animation.setEasingCurve(easing_curve)
                animation.start()

    def reword_password(self):
        Password_First = self.ui_reword.lineEdit_a.text()
        RePassword = self.ui_reword.lineEdit_a2.text()
        if Check_Password(Password_First) == True:
            time.sleep(0.1)
            self.show_message_box("提示", "密码包含无法识别的字符 密码只能为26个大小写字母 以及数字 和- . ? ~ ")
            return 0
        if Password_First != RePassword:
            time.sleep(0.1)
            self.show_message_box("提示", "二次输入密码不相同 请确认后再次尝试")
            return 0
        if not (7 <= len(Password_First) < 16):
            time.sleep(0.1)
            self.show_message_box("提示", "密码只能设置为8-15位")
            return 0
        time.sleep(0.2)
        send_encry("**--*Reword*--**")
        time.sleep(0.3)
        send_encry(f"Reword {Password_First}")
        result = s.recv(1024)
        result = send_decry(result)
        if result == 'Successfully_Reword':
            self.show_message_box("提示", "密码已成功更改！\n请重启客户端后重新登录")
            self.close()
            os._exit(0)
        else:
            self.show_message_box("提示", "密码更改失败")

    def closeEvent(self, e):
        global reword_window
        reword_window = False


if __name__ == "__main__":
    try:
        # 适应高DPI设备
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # 适应Windows缩放
        QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except:
        pass
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('./mod/trans/qt_zh_CN.qm')
    app.installTranslator(translator)
    if initial == False:
        win = ui.Agreement.AgreementWindow()
        win.show()
        app.exec_()
        if ui.Agreement.User_Agree == False:
            sys.exit()
        else:
            with open('config.json', 'r') as file:
                config = json.load(file)
            config["Initial"] = True
            with open("config.json", "w") as json_file:
                json.dump(config, json_file, indent=4)
    window_login = LoginWindow()  #登录窗口
    window_signin = SigninWindow()  #注册窗口
    window_reword = RewordWindow()  #重置密码窗口
    if Log == True and connect_status != None:
        time.sleep(0.1)
        window_login.LOGIN("login")
    elif connect_status == None:  #离线模式
        window_login.LOGIN("offline_login")
    else:
        window_login.show()
    sys.exit(app.exec_())
os._exit(0)
#active_threads = threading.enumerate()
#print("进程结束 ", active_threads)
# 输出当前活动的线程