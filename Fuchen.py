import logging
import os, sys, json, re, time, random, string, shutil, psutil, platform, threading, traceback
import socket,ssl
import concurrent.futures
import struct
import webbrowser
import keyboard as keys
import pyautogui
import pyperclip
import requests
import win32com.client
import win32gui,win32api,win32con
import win32clipboard as w
import winsound
import ctypes
from ctypes import wintypes
import subprocess
import pygetwindow as gw
import ui.userinfo
import function
from ui.ResetWindow import Reset
from ui.RegisterWindow import Register
import ui.Agreement,ui.RecordPosition,ui.style,ui.console_window,ui.fileEdit,ui.hotkey_record
import Login, SundryUI,update_install,SocketThread,new_mainpage,extend_install
from SocketThread import socket_information
#from function import parse_version
try:
    import cv2
    cv2_available = True
    #raise ImportError
except ImportError:
    cv2_available = False
try:
    import op  #计数文件
except:
    pass
from playsound import playsound
from PIL import Image, ImageFilter
from pypinyin import pinyin, Style
from collections import deque
from datetime import datetime,date
from pynput import mouse,keyboard
from pynput.keyboard import Key, Controller as KeyboardController, KeyCode
from pynput.mouse import Button, Controller as MouseController
from PyQt5.QtCore import Qt, QTimer, QUrl, QTranslator, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QColor, QIcon, QPixmap, QKeySequence, QFont, \
    QDesktopServices, QPalette, QBrush, QImage
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel, QShortcut, \
    QMainWindow, QMenu, QAction, QSystemTrayIcon, QDialog, QGraphicsOpacityEffect, QInputDialog
from PyQt5 import QtCore, QtGui

logging.basicConfig(filename='INFOR.log', level=logging.ERROR)


def log_exception(*args):
    # 记录异常信息到日志文件中
    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(args))
    print("错误:",args)

sys.excepthook = log_exception  # 日志
with open("INFOR.log", 'a') as file:
    file.write(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime()) + "  软件运行" + '\n'))

class TimedStream(QObject):
    text_written = pyqtSignal(str, str)

    def __init__(self, original_stream, stream_type):
        super().__init__()
        self.original_stream = original_stream
        self.stream_type = stream_type
        self.buffer = ''
        self.history = []

    def write(self, text):
        self.buffer += text
        while '\n' in self.buffer:
            index = self.buffer.find('\n')
            line = self.buffer[:index]
            self.buffer = self.buffer[index + 1:]
            self._process_line(line)

    def _process_line(self, line):
        '''timestamp = datetime.now().strftime('[%H:%M:%S] ')
        full_line = f"{timestamp}{line}"

        self.history.append((full_line, self.stream_type))
        self.original_stream.write(f"{full_line}\n")  # 保持原始输出
        self.text_written.emit(full_line, self.stream_type)'''

        timestamp = datetime.now().strftime('[%H:%M:%S] ')
        if self.stream_type == 'stderr':
            full_line = f"{timestamp}[ERROR] {line}"  # 添加错误标签
        else:
            full_line = f"{timestamp}{line}"
        self.history.append((full_line, self.stream_type))
        if self.original_stream is not None:
            self.original_stream.write(f"{full_line}\n")

        self.text_written.emit(full_line, self.stream_type)

    def flush(self):
        if self.buffer:
            self._process_line(self.buffer)
            self.buffer = ''
        # 确保原始流存在
        if self.original_stream is not None:
            self.original_stream.flush()

    def __getattr__(self, name):
        return getattr(self.original_stream, name)
# 最早初始化流重定向
stdout_stream = TimedStream(sys.stdout, 'stdout')
stderr_stream = TimedStream(sys.stderr, 'stderr')
sys.stdout = stdout_stream
sys.stderr = stderr_stream

function.print_fuchen()


class MyThread(threading.Thread):  # 多线程封装（我也看不懂反正就是这么用的）
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.daemon=True
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)

def play_prompt_sound(file_path):
    global Sound
    try:
        if Sound:
            MyThread(playsound, file_path)
            #winsound.PlaySound(file_path, winsound.SND_FILENAME)
    except Exception as e:
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))

def play_warning_sound():
    # 设置警告音频文件路径
    try:
        sound_file = "C:\\Windows\\Media\\Windows Foreground.wav"
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)
    except Exception as e:
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 创建 SSL 上下文（客户端模式）
context = ssl.create_default_context()

# 如果你使用的是自签名证书，需要加载服务器证书用于验证（可选，建议）
context.load_verify_locations("certificate.pem")



s = context.wrap_socket(s, server_hostname='fcyang.cn')
# 如果你不验证服务器证书（开发阶段可以）：
#context.check_hostname = False
#context.verify_mode = ssl.CERT_NONE


def TypedJSONClient(msg_type,payload):
    data = {"type": msg_type, "data": payload}
    # 发送请求
    json_data = json.dumps(data).encode('utf-8')
    header = struct.pack('>I', len(json_data))
    s.sendall(header + json_data)


def recv_json(sock):
    """接收JSON数据（带长度前缀）"""
    try:
        # 读取4字节长度头
        header = sock.recv(4)
        if len(header) != 4:
            return None
        data_len = struct.unpack('>I', header)[0]

        # 分块读取数据
        chunks = []
        bytes_received = 0
        while bytes_received < data_len:
            chunk = sock.recv(min(data_len - bytes_received, 4096))
            if not chunk:
                break
            chunks.append(chunk)
            bytes_received += len(chunk)
        return json.loads(b''.join(chunks).decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"JSON解码失败: {e}")
        return {'error': 'Invalid JSON'}
    except struct.error:
        return None


function.initialization()

with open('config.json', 'r') as file:
    config = json.load(file)
AutoLogin = config.get("AutoLogin", False)
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
Version = 'V1.74'


try:
    # 获取数据文本
    url = 'https://fcyang.cn/data.txt'
    response = requests.get(url,proxies={
        "http": None,
        "https": None
    })
    data = response.text

    # 解析键值对
    config = {}
    for line in data.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            config[key.strip()] = value.strip()

    # 提取目标字段
    formal_version = config.get('formal_version')
    formal_link = config.get('formal_link')
except:
    traceback.print_exc()
    formal_version = 'V1.0.0'

Number_People = '加载中...'

IP = '47.116.75.93'  # IP地址192.168.2.75 47.116.75.93
Port = 30000  # 端口号
information = '正在加载公告...'
sys_list = []  # 控制台内容列表
exp_status = None
avatar_load_status = False  #头像加载
connect_status = None
Fuchen_name, Fuchen_type, Fuchen_fullname = function.get_exefile_name()
Name = None
mode = None
avatar_date = None
exp = None
print('配置加载成功')
try:  # 连接服务器
    s.settimeout(10)
    s.connect((IP, Port))
    connect_status = True
except Exception as e:
    traceback.print_exc()
    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
    pyautogui.confirm("服务器连接失败\n请留意服务器公告查询最新消息\n")

try:  # 处理信息\公告
    if connect_status == None:
        raise Exception()
    time.sleep(0.1)

    TypedJSONClient('Get Notice', 'None')
    request = recv_json(s)
    request_data = request.get('data')
    Server_Version = request_data.get('Version')
    Number_People = request_data.get('Number')
    link =  request_data.get('Link')
    information = request_data.get('Notice')
    try:
        status = request_data.get('status')
        if status == 'Fuchen Maintenance':
            pyautogui.confirm("服务器正在维护 请稍后")
            sys.exit()
    except:
        pass

    try:
        information = re.sub('~~space~~', ' ', information)
        information = re.sub('~~next~~', '\n', information)
        print(f""
              f"--------------------------------------------------------------------------\n"
              f"更新日志:\n"
              f"{information}\n"
              f"--------------------------------------------------------------------------")
    except Exception as e:
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
except Exception as e:
    traceback.print_exc()
    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
    if connect_status != None:  #服务器连接成功 但数据接收失败
        pyautogui.confirm("数据接收失败 请重新启动软件\n如多次重试失败 请尝试更新到最新版客户端")
        os._exit(0)
    else:  #服务器连接失败 以离线模式启动
        result = pyautogui.confirm("服务器连接失败 是否以离线模式启动?")
        if result == "OK":
            formal_version = Version
            information = "当前是离线模式 \n部分状态可能未正常显示\n部分功能可能无法正常使用"
        else:
            sys.exit()

if function.parse_version(Version) < function.parse_version(formal_version):
    try:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        update_window = update_install.show_update_dialog(['', Version, formal_version])
        if update_window == 'update_successful':
            # 创建快捷方式
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_name = f'Fuchen.lnk'
            shortcut_path = os.path.join(desktop_path, shortcut_name)
            back_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
            new_version_path = os.path.join(back_path, f'Fuchen_{formal_version}')

            new_exe_path = rf'{new_version_path}\{Fuchen_name}.exe'

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = new_exe_path
            shortcut.WorkingDirectory = os.path.dirname(new_exe_path)  # 设置快捷方式的起始位置为exe文件所在的文件夹
            shortcut.save()
            try:
                shutil.copytree('./scripts', rf'{new_version_path}\scripts')
                shutil.copytree('./mod/music', rf'{new_version_path}\mod\music')
                shutil.copytree('./mod/picture', rf'{new_version_path}\mod\picture')
                shutil.copytree('./mod/xlsx', rf'{new_version_path}\mod\xlsx')
                #迁移旧版数据
            except:
                pass

            with open(f"{new_version_path}\\Fuchen.tmp", "w") as f:
                f.write(f'{os.getcwd()}')
            OLD_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
            function.new_update(new_exe_path,OLD_DIR, shortcut_path)

            #time.sleep(3)
            #pyautogui.confirm("您已成功更新 请关闭此窗口 使用桌面的快捷方式启动")

            sys.exit()
        elif update_window == 'cancel_update':
            sys.exit()
        else:
            sys.exit()
        os._exit(0)
    except Exception as e:
        traceback.print_exc()
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
        print(f"{str(e)}")
        sys.exit()


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
    city_name = city_info[-1]
    #city_name = city_info[-2]+city_info[-1]+(split_res[-1].replace('\n',''))
    #city_name = city_info
    #del city_info
except Exception as e:
    city_name = 'Unknown'
    city_info = ['中国','Unknown','Unknown']
    logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))

system = platform.system()  # 系统类型
computer_name = platform.node()  # 计算机网络名称
APP_VERSION = 0x2023ABCD
# Windows API 常量
WM_SYSCOMMAND = 0x0112
SC_MINIMIZE = 0xF020
SC_RESTORE = 0xF120
# 在类定义前添加共享内存结构体定义
class SharedParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("version", ctypes.c_int),
        ("hotkey", ctypes.c_int),
        ("interval", ctypes.c_double),
        ("clickType", ctypes.c_int),
    ]



class Ui_Form(new_mainpage.MainWindow):  # 主窗口
    def __init__(self, stdout_stream, stderr_stream):
        super(Ui_Form, self).__init__()
        self.stdout_stream = stdout_stream
        self.stderr_stream = stderr_stream
        self.setStyleSheet('''QDialog {
                background-color: #ffffff;
                border-radius: 8px;
                font-size: 16px;
                color: #333333;
                padding: 4px;
            }''')

        self.open_status = False
        self.c_thread_object = None
        self.first_image = False
        self._is_maximized = False  # 跟踪最大化状态
        self.record_status = False
        self.execute_status = False
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
        #self.record_hotkey = keys.add_hotkey(self.record_hotkey_btn.text(), self.Click_Record)
        # 提取按键名称
        hotkey = self._3pushButton.text().split(':')[-1].strip()
        self.record_hotkey = keys.add_hotkey(hotkey, self.Click_Record)

        hotkey = self._3pushButton_2.text().split(':')[-1].strip()
        self.execute_hotkey = keys.add_hotkey(hotkey, self.Click_Record_execute)
        self.title_bar.Button_SetTop.clicked.connect(self.upwindow)
        self.title_bar.Button_Close.clicked.connect(self.clo)  # 退出按钮

        self.open_window_hotkey = QShortcut(QKeySequence("Ctrl+o"), self)
        self.open_window_hotkey.activated.connect(self.open_console_window)

        self.open_window_hotkey = QShortcut(QKeySequence("F12"), self)
        self.open_window_hotkey.activated.connect(self.open_console_window)

        #self.title_bar.action_option1.triggered.connect(self.open_set_window)  # 设置按钮
        self.title_bar.action_option2.triggered.connect(self.about)
        self.title_bar.action_option3.triggered.connect(self.open_help_window)
        self.title_bar.action_option4.triggered.connect(self.LogRecord)
        self.title_bar.action_option5.triggered.connect(self.open_website)
        self.title_bar.action_option6.triggered.connect(self.open_view_window)
        self.title_bar.action_option7.triggered.connect(self.empyt_log)
        self.title_bar.action_option8.triggered.connect(self.clear_temp)
        self.title_bar.action_option9.triggered.connect(self.restart_app)
        self.title_bar.action_option10.triggered.connect(self.open_website_help)

        self.avatar.clicked.connect(self.open_user_window)
        self.username.clicked.connect(self.open_user_window)
        self.userid.clicked.connect(self.open_user_window)

        self.RClick_Radio.clicked.connect(self.update_shared_params)
        self.MClick_Radio.clicked.connect(self.update_shared_params)
        self.LClick_Radio.clicked.connect(self.update_shared_params)
        self._3D.valueChanged.connect(self.update_shared_params)
        self._3pushButton_6.clicked.connect(lambda: MyThread(self.open_click))
        self._3pushButton_7.clicked.connect(lambda: MyThread(self.break_click))

        self._3pushButton_4.setMenu(self.createMenu())
        self.weather_label.setCursor(Qt.PointingHandCursor)  # 鼠标变手型
        self.weather_label.mousePressEvent = self.change_city_name  # 绑定点击事件

        #self._3pushButton.clicked.connect(self.Click_Record)  # 记录自动脚本
        #self._3pushButton_2.clicked.connect(self.Click_Record_execute)

        #----消息发送控件----#
        self.old_QQ.toggled.connect(lambda checked: self.QQ_change("old"))
        self.new_QQ.toggled.connect(lambda checked: self.QQ_change("new"))
        self._2pushButton2.clicked.connect(self.gain_handle)
        self.handle_send_btn.clicked.connect(self.Handle_Send)

        self.QQ_StartSend_At_Button.clicked.connect(self.Send_QQ)  # page2(QQ)页面 绑定
        self.QQ_Send_Copy_startsend_button.clicked.connect(self.Send_Copy)  # 复制内容
        self.QQ_Seq_Start_button.clicked.connect(self.order_send)
        self.record_position_button.clicked.connect(self.open_record_window)


        self.btn_custom_start.clicked.connect(self.handle_auto_execute)
        self.btn_get_position.clicked.connect(self.start_detection)
        #----team---#
        self.create_team_button.clicked.connect(self.team)  # 创建队伍

        self.button_copy_id.clicked.connect(self.copy_team_number)  # 复制id
        self.add_team_button.clicked.connect(self.join_team)

        self.team_btn_start.clicked.connect(self.team_c)  # 开始执行
        #----工具页面----#

        self.view_music.clicked.connect(lambda: self.open_folder('music'))
        self.btn_download_music.clicked.connect(self.download)

        self.pic_confirm_button.clicked.connect(self.mixPicture)

        self.btn_download_qq.clicked.connect(lambda: MyThread(self.download_image))
        self.qq_information_edit_button.clicked.connect(self.QQ_image_update)
        self.save_setting_btn.clicked.connect(self.save_setting_option)

        self.btn_get_group.clicked.connect(lambda: MyThread(self.QQ_Group_information))

        #----设置页面----#

        self.version_button.clicked.connect(self.check_update)
        self.update_status_button.clicked.connect(self.get_connect_status)

        '''
        self.uim.Start_Click_Radio.clicked.connect(lambda: self.record_change('click'))
        self.uim.Start_Hotkey_Radio.clicked.connect(lambda: self.record_change('hotkey'))
        self.uim.Hotkey_record_button.clicked.connect(self.record_hotkey_setting)

        self.uim.Execute_Click_Radio.clicked.connect(lambda: self.execute_change('click'))
        self.uim.Execute_Hotkey_Radio.clicked.connect(lambda: self.execute_change('hotkey'))
        self.uim.Hotkey_execute_button.clicked.connect(self.execute_hotkey_setting)

        self.uim._3pushButton_5.clicked.connect(self.mouseinfo)
        
        self.uim.impor_button.clicked.connect(self.open_fileedit_window)
        self.uim.reflash.clicked.connect(lambda: self.uim.populateMenu('scripts'))

        
        self.uim.talk_lineEdit.returnPressed.connect(self.send_talk)

        '''

        self.image_cache = deque(maxlen=30)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.is_topmost = False
        self.border_width = 8
        self.record_thread = None
        self.execute_thread = None

        self.hotkey_record_status = None
        self.hotkey_execute_status = None


        MainWindow.setWindowTitle("Fuchen 浮沉制作")

        self.Trend_Status = False
        self.Trend_Now = False


        icon = QIcon("image/window.ico")  # 设置窗口图标
        self.setWindowIcon(icon)

        MyThread(self.Update_weather)
        MyThread(self.tourist_prompt)
        MyThread(self.setting_page_check)

        self.weather_timer = QtCore.QTimer(self)
        self.weather_timer.timeout.connect(self.Update_weather)
        self.weather_timer.start(1200000)  # 更新时间的间隔，单位为毫秒

        self.run_timer = QtCore.QTimer(self)
        self.run_timer.timeout.connect(self.updateTime)
        self.startTime = QtCore.QTime.currentTime()
        self.run_timer.start(1000)  # 每秒更新一次

        self.global_timer = QtCore.QTimer(self)
        self.global_timer.timeout.connect(self.get_current_time_string)
        self.global_timer.start(1000)  # 更新时间的间隔，单位为毫秒

        # self.data_thread = DataThread()
        self.data_thread = SocketThread.DataThread([self, s])
        self.data_thread.show_message_signal.connect(self.handle_message)
        self.data_thread.team_send_response.connect(self.deal_team_send)
        self.data_thread.start()

        # 将文本分割成行
        global information
        lines = information.split('\n')

        # 生成HTML内容
        html_content = f"""
        <p style='color: rgba(255,255,255,0.95); margin:2px;'>
            <b>📢{lines[0]}</b><br/>
            {"".join([f"· {line}<br/>" for line in lines[1:]])}
            <a href='https://fcyang.cn/others/log.html' 
           style='color: #ffdd55; text-decoration: none;'>[详情]</a>
        </p>
        """
        self.notice_browser.setHtml(html_content)

    def setting_page_check(self):
        if Account == '游客':
            self.avatar.setEnabled(False)
            self.username.setEnabled(False)
            self.userid.setEnabled(False)
            self.button_3.setEnabled(False)
            self.avatar.setToolTip("游客暂不支持该功能")
            self.username.setToolTip("游客暂不支持该功能")
            self.userid.setToolTip("游客暂不支持该功能")
            self.button_3.setToolTip("游客暂不支持该功能")

        if AutoLogin == True:
            self.auto_login_check.setChecked(True)
        else:
            self.auto_login_check.setChecked(False)
        if Sound == True:
            self.sound_check.setChecked(True)
        else:
            self.sound_check.setChecked(False)
        if ClosePrompt == True:
            self.close_check.setChecked(True)
        else:
            self.close_check.setChecked(False)
        if CloseExecute == "Close":
            self.close_radio.setChecked(True)
        elif CloseExecute == "Hide":
            self.tray_radio.setChecked(True)
        else:
            self.close_radio.setChecked(False)
            self.tray_radio.setChecked(False)
        # 要检查的文件名
        file_name = 'Fuchen_Start_File.bat'
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows',
                                      'Start Menu', 'Programs', 'Startup')
        file_path = os.path.join(startup_folder, file_name)
        self.First = False
        if os.path.exists(file_path):
            self.boot_check.setChecked(True)
            self.First = True
        else:
            self.boot_check.setChecked(False)
        if window_s == True:
            self.float_check.setChecked(True)
        else:
            self.float_check.setChecked(False)
        if cv2_available:
            self.trand_problem.setStyleSheet("""
                        QPushButton {
                            border-image: url(./image/Component/提示.png);
                            background-color: rgba(245,245,245,0);
                        }
                    """)

            print('设置成功')
        else:
            self.trand_problem.setStyleSheet("""
                        QPushButton {
                            border-image: url(./image/Component/下载.png);
                            background-color: rgba(245,245,245,0);
                        }
                    """)
            self.bg_dynamic.setEnabled(False)
            self.bg_dynamic.setToolTip("需要安装扩展内容")
            self.bg_dynamic_path.setPlaceholderText("需要先安装CV2扩展包才可使用")
            self.bg_dynamic_path.setEnabled(False)
            self.fps_spin.setEnabled(False)
        self.trand_problem.clicked.connect(self.problems)
        if Theme == "White":
            self.bg_default.setChecked(True)
        elif Theme == 'Custom':
            try:
                self.bg_custom.setChecked(True)
                with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                    config = json.load(file)
                # 添加新元素到数据结构
                Path_Custom = config["Path"]
                self.bg_custom_path.setText(Path_Custom)
            except Exception as e:
                print(e)
        elif Theme == 'Trend':
            self.bg_dynamic.setChecked(True)
            with open('config.json', 'r') as file:  # 填充自定义图片壁纸的输入栏
                config = json.load(file)
            # 添加新元素到数据结构
            Path_Trend = config["Path"]
            self.bg_dynamic_path.setText(Path_Trend)
        else:
            self.bg_default.setChecked(True)
        self.fps_spin.setValue(FPS)
        self.opacity_slider.setValue(transparent)

    def problems(self):
        if not cv2_available:
            window = extend_install.DownloadDialog(self)
            window.exec_()
        else:
            QMessageBox.information(self, '提示',"此功能对电脑占用较高\n不推荐使用大于20秒的视频 否则可能会过多占用内存!!!")

    def save_setting_option(self):
        global AutoLogin, Sound, ClosePrompt, CloseExecute, window_s, Theme, transparent, FPS

        if self.auto_login_check.isChecked():
            AutoLogin = True
        else:
            AutoLogin = False
        if self.sound_check.isChecked():
            Sound = True
        else:
            Sound = False
        if self.close_check.isChecked():
            ClosePrompt = True
        else:
            ClosePrompt = False
        if self.close_radio.isChecked():
            CloseExecute = "Close"
        else:
            CloseExecute = "Hide"
        with open('config.json', 'r') as file:
            config = json.load(file)
        transparent = self.opacity_slider.value()
        config["AutoLogin"] = AutoLogin
        config["Sound"] = Sound
        config["ClosePrompt"] = ClosePrompt
        config["CloseExecute"] = CloseExecute
        config["transparent"] = transparent
        fps_value = self.fps_spin.value()
        if fps_value != FPS:
            config["FPS"] = fps_value
            FPS = fps_value
        # 将更新后的数据写入 JSON 文件
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)
        n = True
        if (self.boot_check.isChecked()) and (self.First == False):
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
        elif (self.boot_check.isChecked() == False) and (self.First == True):
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
        if self.float_check.isChecked() and window_s == False:
            self.open_floating_window()
            window_s = True
        elif self.float_check.isChecked() == False and window_s == True:
            self.close_floating_window()
            window_s = False
        self.repaint()
        if self.bg_default.isChecked():
            if Theme == "Trend":
                self.stop_dynamic_background()
            self.should_draw = "White"  # 清空背景图片
            self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
            self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1))
            # 重置调色板为默认（例如白色主题）
            default_palette = QApplication.palette()
            self.setPalette(default_palette)
            # 读取 JSON 文件
            with open('config.json', 'r') as file:
                config = json.load(file)
            config["Theme"] = "White"
            # 将更新后的数据写入 JSON 文件
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)
            Theme = "White"

        if self.bg_custom.isChecked():
            try:
                if Theme == "Trend":
                    self.stop_dynamic_background()
                file_name = self.bg_custom_path.text()
                with open('config.json', 'r') as file:
                    config = json.load(file)
                if config["Theme"] != "Custom" or config["Path"] != file_name:  # 这个判断是为了防止目前的背景和选择的背景相同而设置 因此当选择的文件和现有设置的文件相同时 将不会执行
                    if file_name != '':
                        self.should_draw = "Custom"
                        # 读取 JSON 文件
                        with open('config.json', 'r') as file:
                            config = json.load(file)
                        config["Theme"] = "Custom"
                        config["Path"] = file_name
                        # 将更新后的数据写入 JSON 文件
                        with open('config.json', 'w') as file:
                            json.dump(config, file, indent=4)
                        im = Image.open(file_name)
                        reim = im.resize((1000, 600))  # 宽*高
                        reim.save('./temp/background_custom.png',
                                  dpi=(400, 400))  ##200.0,200.0分别为想要设定的dpi值
                        # 打开图片
                        image = Image.open('./temp/background_custom.png')
                        # 应用高斯模糊，radius参数控制模糊程度（半径越大越模糊）
                        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
                        # 保存处理后的图片
                        blurred_image.save('./temp/background_custom.png')

                        palette = QPalette()
                        palette.setBrush(QPalette.Background,
                                         QBrush(QPixmap('./temp/background_custom.png')))
                        self.setPalette(palette)
                        self.repaint()
                        self.update()  # 新增此行

                        Theme = "Custom"

                    else:
                        n = False
                        pyautogui.confirm("请选择文件!")
                trp = transparent / 100
                # 设置整体透明度（会影响所有子元素）
                self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp))
                self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp - 0.1))
            except Exception as e:
                print(e)

        if self.bg_dynamic.isChecked():
            file_name_V = self.bg_dynamic_path.text()
            with open('config.json', 'r') as file:
                config = json.load(file)
            if config["Theme"] != "Trend" or config["Path"] != file_name_V:
                if config["Theme"] != "Trend":
                    if file_name_V != '':
                        self.should_draw = "Trend"
                        # 读取 JSON 文件
                        with open('config.json', 'r') as file:
                            config = json.load(file)
                        config["Theme"] = f"Trend"
                        config["Path"] = file_name_V
                        # 将更新后的数据写入 JSON 文件
                        with open('config.json', 'w') as file:
                            json.dump(config, file, indent=4)
                        self.save_setting_btn.setText("正在加载 请等待")
                        self.save_setting_btn.repaint()
                        self.deal_pictures(file_name_V)
                        self.execute_trend()
                        self.save_setting_btn.setText("设置")
                        Theme = "Trend"
                elif config["Path"] != file_name_V:
                    with open('config.json', 'r') as file:
                        config = json.load(file)
                    config["Theme"] = f"Trend"
                    config["Path"] = file_name_V
                    # 将更新后的数据写入 JSON 文件
                    with open('config.json', 'w') as file:
                        json.dump(config, file, indent=4)
                    self.save_setting_btn.setText("正在加载 请等待")
                    self.save_setting_btn.repaint()
                    self.deal_pictures(file_name_V)
                    self.execute_trend_again()
                    self.save_setting_btn.setText("设置")

        if n == True:
            pyautogui.confirm("设置成功!")

    def tourist_prompt(self):
        if Account == "游客":
            try:
                # 读取 JSON 文件
                with open('config.json', 'r') as f:
                    config = json.load(f)

                # 修改数值（确保原值是整数）
                config['tourist_number'] += 1

                # 重新写入文件（覆盖原文件）
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)  # indent 保持美观格式

                with open('config.json') as f:
                    config = json.load(f)

                tourist_status = config['tourist_status']
                tourist_number = config['tourist_number']

                print(tourist_status, type(tourist_status))  # 输出示例: True <class 'bool'>
                print(tourist_number, type(tourist_number))  # 输出示例: 5 <class 'int'>

                if tourist_status == False:
                    if tourist_number == (5 or 20 or 100):
                        time_wait = random.randint(5, 15)
                        time.sleep(time_wait)
                        result = pyautogui.confirm(f"您已启动Fuchen {tourist_number} 次\n注册账号可以使用更全面的功能 推荐您注册账号使用完整功能")

            except:
                pass
            pass
        else:
            try:
                # 读取 JSON 文件
                with open('config.json', 'r') as f:
                    config = json.load(f)

                # 修改数值（确保原值是整数）
                config['tourist_status'] = True

                # 重新写入文件（覆盖原文件）
                with open('config.json', 'w') as f:
                    json.dump(config, f, indent=4)  # indent 保持美观格式
            except:
                pass

    def get_current_time_string(self):
        global current_time_string
        current_time = time.localtime()  # 获取当前时间的时间结构
        current_time_string = "[" + time.strftime("%H:%M:%S",
                                                  current_time) + "]"  # 格式化时间为字符串

    def restart_app(self):
        subprocess.Popen([Fuchen_fullname])
        self.close()
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
        trp = transparent / 100
        self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp))
        self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp - 0.1))
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

    def updateTime(self):
        currentTime = QtCore.QTime.currentTime()
        elapsedTime = self.startTime.secsTo(currentTime)



    def QQ_change(self, checked):  # 句柄发送位置切换
        global handle_position
        if checked == 'old':
            handle_position = [30, -60]
        else:
            handle_position = [-30, -60]

    def get_connect_status(self):
        TypedJSONClient('get_connect_status', 'N')
        try:
            color = QColor(36, 152, 42)
            self.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
            self.status_label.setText("与服务器状态: 已连接")
            result = socket_information.get(timeout=3)
            print(result)
        except:
            traceback.print_exc()
            print('与服务器断开连接')
            color = QColor(164, 38, 15)  # 使用RGB值设置颜色为红色
            self.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
            self.status_label.setText("与服务器状态: 断开连接")

    def response_value(self, value):
        # 通过全局变量字典获取
        param = globals()[value]
        return param

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

    def setValue(self, Set):
        global AutoLogin, Sound, ClosePrompt, CloseExecute,window_s, Theme, transparent, FPS
        AutoLogin = Set[0]
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
        global exp

        lis = [self, Account, Name, avatar_date, exp, s,  avatar_load_status]
        self.user_window = ui.userinfo.InfoPopup(lis)
        self.user_window.show()

    def open_help_window(self):
        self.help_window = SundryUI.Help()
        self.help_window.show()

    def open_view_window(self):
        lis = [self, s]
        self.view_window = SundryUI.View(lis)
        self.view_window.show()

    def open_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.show()

    def close_floating_window(self):
        self.floating_window = SundryUI.floating_window(self)
        self.floating_window.close()

    def open_point_window(self):
        self.point_window = SundryUI.ExpandingWindow()
        self.point_window.show()

    def open_record_window(self):
        self.record__position_window = ui.RecordPosition.record_position(self)
        self.record__position_window.exec_()

    def open_console_window(self):
        with open("config.json", "r") as file:
            config = json.load(file)
        if config['console_theme'] == 'light':
            console_theme = 'light'
        else:
            console_theme = 'dark'
        self.console_window = ui.console_window.ConsoleWindow(
            [self.stdout_stream, self.stderr_stream, self, s,console_theme])
        self.console_window.show()

    def open_fileedit_window(self):
        if (self.uim.button_file.text() in ('选择配置文件', '暂无配置文件 需要创建')):
            pyautogui.confirm("需要先选择或创建配置文件")
            return 0
        pyautogui.confirm("此功能还处于开发中 功能不全面可能有BUG")
        self.fileedit_window = ui.fileEdit.FileEdit(self.button_file.text(), self)
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


    '''def send_talk(self):
        text = self.uim.talk_lineEdit.text()
        text = re.sub(' ', '~~space~~', text)
        send_encry("20030 "+text)
        self.uim.talk_lineEdit.clear()'''


    def closeEvent(self, e):
        try:
            if self.open_status == True:
                self.c_thread_object.kill()
            try:
                if hasattr(self, 'shm_ptr'):
                    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                    UnmapViewOfFile = kernel32.UnmapViewOfFile
                    CloseHandle = kernel32.CloseHandle

                    UnmapViewOfFile(self.shm_ptr)
                    CloseHandle(self.shm_handle)

                    del self.shm_ptr
                    del self.shm_handle
            except:
                pass
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

    # 新增城市修改方法
    def change_city_name(self, event):
        global city_name

        # 创建输入对话框
        dialog = QInputDialog(self)
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle('修改城市')
        dialog.setLabelText('请输入城市名称:')
        dialog.setTextValue(str(city_name))

        # 设置对话框整体样式
        dialog.setStyleSheet("""
            QDialog {
                background: rgba(121, 188, 237, 0.9);
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.25);
            }
            QLabel {
                color: white;
                font: 500 13px 'Microsoft YaHei';
                background: transparent;
            }
            QLineEdit {
                background: rgba(255,255,255,0.15);
                color: white;
                font: 500 13px 'Microsoft YaHei';
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.25);
                padding: 5px;
            }
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: white;
                font: 500 12px 'Microsoft YaHei';
                border-radius: 6px;
                padding: 6px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
            }
        """)

        # 调整对话框尺寸
        dialog.resize(300, 150)

        if dialog.exec_() == QDialog.Accepted:
            new_city = dialog.textValue().strip()
            if new_city:
                city_name = new_city
                self.Update_weather()
    def Update_weather(self):  # 获取天气
        def get_response():
            try:
                print("开始更新天气 请稍后")
                api_key = "dce92b382ffb9409ca31ae4c1b240d4f"
                # 发送请求获取IP地址信息
                '''res = requests.get('http://myip.ipip.net', timeout=5).text
                # 提取城市信息
                split_res = res.split('  ')
                city_info = split_res[-2]  # 倒数第二个元素是位置信息
                city_info = city_info.split(' ')
                country = city_info[-3]
                city_info = city_info[-1]'''
                #global city_name, weather_status, temperature, humidity, weather_info
                self.weather_label.setText("正在获取天气...")
                global city_name, city_info
                country = city_info[-3]
                if country[-2:] == '中国':
                    #city_name = city_info
                    pinyin_list = pinyin(city_name, style=Style.NORMAL)
                    # 从拼音列表中提取拼音并连接成字符串
                    pinyin_str = ''.join([item[0] for item in pinyin_list])
                    # 设置API请求的URL
                    base_url = "http://api.openweathermap.org/data/2.5/weather"
                    url = f"{base_url}?q={pinyin_str}&appid={api_key}"
                    # 发送API请求并获取响应
                    response = requests.get(url, timeout=15)
                    data = response.json()
                    # 提取天气信息
                    if data["cod"] == 200:
                        temperature = data["main"]["temp"] - 273.15  # 摄氏度
                        temp = round(temperature)
                        humidity = data["main"]["humidity"]  # 湿度
                        weather_main = data["weather"][0]["main"]
                        weather_id = data["weather"][0]["id"]

                        # 根据天气类型设置emoji和描述
                        emoji, weather_desc = '🌡️', '未知天气'
                        if weather_main == 'Clear':
                            emoji, weather_desc = '☀️', '晴天'
                        elif weather_main == 'Clouds':
                            if 801 <= weather_id <= 802:
                                emoji, weather_desc = '⛅', '晴间多云'
                            elif 803 <= weather_id <= 804:
                                emoji, weather_desc = '☁️', '多云'
                        elif weather_main == 'Rain':
                            emoji, weather_desc = '🌧️', '下雨'
                        elif weather_main == 'Drizzle':
                            emoji, weather_desc = '🌧️', '小雨'
                        elif weather_main == 'Thunderstorm':
                            emoji, weather_desc = '⛈️', '雷雨'
                        elif weather_main == 'Snow':
                            emoji, weather_desc = '🌨️', '下雪'
                        elif weather_main in ('Mist', 'Fog'):
                            emoji, weather_desc = '🌫️', '雾'
                        elif weather_main == 'Haze':
                            emoji, weather_desc = '🌫️', '霾'
                        elif weather_main == 'Squall':
                            emoji, weather_desc = '💨', '大风'
                        elif weather_main == 'Tornado':
                            emoji, weather_desc = '🌪️', '龙卷风'

                        # 更新天气标签
                        # 生成完整显示文本
                        full_text = f"{emoji} {temp}°C {weather_desc} | {city_name}"

                        # 获取字体度量
                        font_metrics = self.weather_label.fontMetrics()
                        available_width = self.weather_label.width() - 10  # 保留边距

                        # 自动缩短文本算法
                        def shorten_text(text, max_width):
                            if font_metrics.horizontalAdvance(text) <= max_width:
                                return text
                            # 逐步移除城市名的最后一个字符
                            parts = text.split(" | ")
                            base = parts[0] + " | "
                            city = parts[1]
                            for i in range(len(city) - 1, 0, -1):
                                shortened = base + city[:i] + "…"
                                if font_metrics.horizontalAdvance(shortened) <= max_width:
                                    return shortened
                            return text[:3] + "…"  # 保底方案

                        # 应用自适应缩短
                        display_text = shorten_text(full_text, available_width)

                        # 设置显示文本和悬浮提示
                        self.weather_label.setText(display_text)
                        self.weather_label.setToolTip(full_text)  # 悬浮显示完整信息
                        weather_status = True
                        print(f"天气获取成功 城市:{city_name} 温度:{temp}°C 湿度:{humidity}%")
                    else:
                        self.weather_label.setText("天气获取失败")
                        weather_status = False
                        print('天气获取失败')
                else:
                    self.weather_label.setText("当前位置暂不支持天气解析")
                    print("当前位置暂不支持天气解析")
            except requests.exceptions.Timeout:
                self.weather_label.setText("获取天请求超时")
                print(f'获取天气请求超时')
            except Exception as e:
                traceback.print_exc()
                self.weather_label.setText("天气获取失败")
                print(f'天气获取失败: {str(e)}')
        MyThread(get_response)

    def open_folder(self, page):  # 浏览QQ头像下载文件夹
        if page == 'picture':
            folder_path = './mod/picture'
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == 'music':
            folder_path = self.music_savepath.text()
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

        elif page == 'xlsx':
            folder_path = '.mod/xlsx'
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

    def init_shared_memory(self):
        # 确保kernel32的API正确定义
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        # 定义CloseHandle（需要补充这部分声明）
        CloseHandle = kernel32.CloseHandle
        CloseHandle.argtypes = [wintypes.HANDLE]
        CloseHandle.restype = wintypes.BOOL

        # 定义UnmapViewOfFile（虽然当前函数未使用，但后续需要）
        UnmapViewOfFile = kernel32.UnmapViewOfFile
        UnmapViewOfFile.argtypes = [wintypes.LPCVOID]
        UnmapViewOfFile.restype = wintypes.BOOL

        # 定义CreateFileMappingW（已有定义需要保留）
        CreateFileMappingW = kernel32.CreateFileMappingW
        CreateFileMappingW.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPCWSTR
        ]
        CreateFileMappingW.restype = wintypes.HANDLE

        # 定义MapViewOfFile（已有定义需要保留）
        MapViewOfFile = kernel32.MapViewOfFile
        MapViewOfFile.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_size_t
        ]
        MapViewOfFile.restype = wintypes.LPVOID

        # 共享内存参数
        SHM_NAME = "Local\\ClickParamsSharedMemory"
        SHM_SIZE = ctypes.sizeof(SharedParams)

        # 创建共享内存
        h_map = CreateFileMappingW(
            wintypes.HANDLE(-1),
            None,
            0x04,  # PAGE_READWRITE
            0,
            SHM_SIZE,
            SHM_NAME
        )
        if h_map == 0:
            error = ctypes.GetLastError()
            # 重要修改：这里必须先声明CloseHandle才能调用
            CloseHandle(h_map)  # 清理无效句柄
            raise ctypes.WinError(error)

        # 映射内存
        ptr = MapViewOfFile(
            h_map,
            0xF001F,  # FILE_MAP_ALL_ACCESS
            0,
            0,
            SHM_SIZE
        )
        if not ptr:
            error = ctypes.GetLastError()
            CloseHandle(h_map)  # 映射失败时关闭句柄
            raise ctypes.WinError(error)

        return h_map, ptr

    def write_shared_memory(self, ptr, hotkey, interval, click_type):
        params = SharedParams()
        params.version = APP_VERSION
        params.hotkey = int(hotkey)
        params.interval = interval
        params.clickType = click_type
        ctypes.memmove(ptr, ctypes.byref(params), ctypes.sizeof(params))

    def update_shared_params(self):
        """更新共享内存参数"""
        if hasattr(self, 'shm_ptr'):
            # 转换当前参数
            hotkey = self._convert_hotkey_to_code()
            if hotkey == 8888:
                self.show_message_box('提示', '按键错误 请重新输入')
                return 0
            interval = float(self._3D.value())
            print(interval)
            click_type = self._get_current_click_type()  # 新增获取点击类型方法
            if interval != 0:
                # 写入共享内存
                self.write_shared_memory(self.shm_ptr, hotkey, interval, click_type)

    def _get_current_click_type(self):
        """获取当前点击类型的数字表示"""
        if self.LClick_Radio.isChecked():
            return 0
        elif self.MClick_Radio.isChecked():
            return 1
        else:
            return 2

    def open_click(self):  # 开启连点器部分
        if (self.RClick_Radio.isChecked()) and (self.sort == '鼠标右键'):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        elif (self.MClick_Radio.isChecked()) and (self.sort == '鼠标中键'):
            pyautogui.confirm("点击按键和监听热键不可相同!")
            return 0
        try:
            print("开启中")
            self._3pushButton_6.setText("正在开启...")
            self._3pushButton_6.setEnabled(False)
            try:
                # 转换点击类型为数字
                click_type = self._get_current_click_type()
                # 转换热键为数字
                hotkey = self._convert_hotkey_to_code()  # 需要实现这个转换方法
                interval = float(self._3D.value())

                if self.high_speed_radio.isChecked():
                    # 创建共享内存
                    h_map, ptr = self.init_shared_memory()
                    self.write_shared_memory(ptr, hotkey, interval, click_type)

                    # 启动click.exe
                    self.c_thread_object = subprocess.Popen(
                        ["./mod/more/click.exe", str(APP_VERSION)],  # 添加版本参数
                        creationflags=subprocess.CREATE_NO_WINDOW  # 隐藏控制台
                    )

                    # 保存句柄和指针用于后续清理
                    self.shm_handle = h_map
                    self.shm_ptr = ptr
                self.open_status = True
                self._3pushButton_6.setText("连点器已开启")
                self._3pushButton_7.setVisible(True)
                self.high_speed_radio.setEnabled(False)
                self.low_speed_radio.setEnabled(False)
            except KeyboardInterrupt:
                # 处理 Ctrl+C 中断
                self.c_thread_object.terminate()
                sys.exit()
            except Exception as e:
                traceback.print_exc()
                print(e)
                self._3pushButton_6.setText("开启失败")
                self._3pushButton_7.setVisible(True)
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
                self.c_thread_object.terminate()
                # 清理共享内存
                '''if hasattr(self, 'shm_ptr'):
                    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                    UnmapViewOfFile = kernel32.UnmapViewOfFile
                    CloseHandle = kernel32.CloseHandle

                    UnmapViewOfFile(self.shm_ptr)
                    CloseHandle(self.shm_handle)

                    del self.shm_ptr
                    del self.shm_handle'''
                del self.c_thread_object
                self.c_thread_object = None
                self.open_status = False
                self._3pushButton_6.setText("开启连点器")
                self._3pushButton_6.setEnabled(True)
                self._3D.setEnabled(True)
                self._3pushButton_7.setVisible(False)
                self.high_speed_radio.setEnabled(False)
                self.low_speed_radio.setEnabled(False)
        except Exception as e:
            traceback.print_exc()
            print(e)
            pyautogui.confirm(e)

    def _convert_hotkey_to_code(self):
        # 返回对应的键值或默认值
        return function.keycode_dict.get(self.sort.lower(), 8888)

    def gain_handle(self):  # 获取句柄
        self.showMinimized()

        def on_click(x, y, button, pressed):
            if pressed:
                if button == mouse.Button.left:  # 如果是左键点击
                    hwnd = win32gui.WindowFromPoint((x, y))  # 获取句柄
                    self._2lineEdit_3.setText(str(hwnd))  # 设置句柄到lineEdit
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

    def handle_auto_execute(self):
        # 获取所有配置数据示例
        configurations = []
        for group in self.operation_groups:
            config = {
                "handle": group.edit_handle.text(),
                "action": group.combo_action.currentText(),
                "param": group.edit_param.text()
            }
            configurations.append(config)

        if configurations != []:
            print(configurations)
            for i in range(self.spin_executions.value()):


                for x in configurations:
                    action = x['action']
                    if action == '点击':
                        try:
                            hwnd = int(x['handle'])
                            win32gui.SetForegroundWindow(hwnd)
                            time.sleep(0.5)  # 等待窗口聚焦
                            parts = x['param'].split(',')
                            click_x = int(parts[0])
                            click_y = int(parts[1])
                            long_position = win32api.MAKELONG(click_x, click_y)  # 模拟鼠标指针 传送到指定坐标
                            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON,
                                                 long_position)  # 模拟鼠标按下
                            win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON,
                                                 long_position)  # 模拟鼠标弹起
                        except Exception as e:
                            traceback.print_exc()
                    elif action == '右键':
                        try:
                            hwnd = int(x['handle'])
                            print(hwnd, type(hwnd))
                            win32gui.SetForegroundWindow(hwnd)
                            time.sleep(0.5)  # 等待窗口聚焦
                            parts = x['param'].split(',')
                            click_x = int(parts[0])
                            click_y = int(parts[1])
                            long_position = win32api.MAKELONG(click_x, click_y)  # 模拟鼠标指针 传送到指定坐标
                            print(long_position, type(long_position))
                            win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON,
                                                 long_position)  # 模拟鼠标按下
                            win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON,
                                                 long_position)  # 模拟鼠标弹起
                        except Exception as e:
                            traceback.print_exc()
                    elif action == '粘贴':
                        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                        # 按下 Ctrl 键
                        win32api.keybd_event(ord('V'), 0, 0, 0)
                        # 按下 V 键
                        win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
                        # 放开 V 键
                        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                        # 放开 Ctrl 键
                    elif action == '按键':
                        # 向指定窗口发送 Enter 键
                        win32api.keybd_event(x, 0, 0, 0)  # 按下 Enter 键
                        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开 Enter 键
                    elif action == '回车':
                        # 向指定窗口发送 Enter 键
                        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)  # 按下 Enter 键
                        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)  # 放开 Enter 键
                    elif action == '等待':
                        time.sleep(int(x['param']))

                time.sleep(self.spin_interval.value())
            print('执行完毕')

    def start_detection(self):
        #self.mask = page.ScreenMask(self)
        self.mask = new_mainpage.ScreenMask(self)
        self.mask.showFullScreen()

    def mouseinfo(self):  # 鼠标信息
        pyautogui.mouseInfo()

    def QQ_Group_information(self):  # QQ群信息获取
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        if self.Edge_Radio.isChecked():
            mode = 'Edge'
        elif self.Chrome_Radio.isChecked():
            mode = 'Chrome'
        elif self.Ie_Radio.isChecked():
            mode = 'Ie'
        else:
            pyautogui.confirm("文件选择类型错误 请重试!")
            return 0
        Qid = self.checkBox_qid.isChecked()
        sex = self.checkBox_sex.isChecked()
        QQ_year = self.checkBox_qq_year.isChecked()
        join_date = self.checkBox_join_date.isChecked()
        send_date = self.checkBox_send_date.isChecked()
        group_lv = self.checkBox_group_lv.isChecked()
        folder = self.lineEdit_group_path.text()
        result = function.QQ_Group_Obtain(mode, folder, Qid, sex, QQ_year, join_date, send_date, group_lv)
        if str(type(result)) == '<class \'selenium.common.exceptions.NoSuchWindowException\'>':
            pyautogui.confirm("操作取消")
        elif result == 'Cancel':
            pyautogui.confirm("操作取消")
        elif str(result[0:6]) == '文件保存成功':
            pyautogui.confirm(result)
        else:
            pyautogui.confirm(result, "错误:")

    def check_update(self):
        local_ver = Version
        url = "https://fcyang.cn/data.txt"

        try:
            response = requests.get(url)
            response.raise_for_status()

            config = {}
            for line in response.text.splitlines():
                line = line.strip()
                if line and ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()

            server_ver = config.get("last_version")
            last_link = config.get("last_link")

            print(f"Last Version: {server_ver}")
            print(f"Last Link: {last_link}")

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return

        def parse_version(version):
            cleaned = re.sub(r'^[^\d.]*', '', version, flags=re.IGNORECASE)
            parts = cleaned.split('.')
            nums = []
            for part in parts:
                try:
                    nums.append(int(part))
                except ValueError:
                    nums.append(0)
            return nums

        local_parts = parse_version(local_ver)
        server_parts = parse_version(server_ver)

        max_length = max(len(local_parts), len(server_parts))
        update_needed = False

        # 比较所有对应的版本号部分
        for i in range(max_length):
            local_num = local_parts[i] if i < len(local_parts) else 0
            server_num = server_parts[i] if i < len(server_parts) else 0

            if server_num > local_num:
                update_needed = True
                break
            elif server_num < local_num:
                QMessageBox.information(self, '提示:', '当前已是最新版本 无需更新')
                return

        # 如果前面部分完全相同，检查服务器是否有额外非零子版本
        if not update_needed and len(server_parts) > len(local_parts):
            for i in range(len(local_parts), len(server_parts)):
                if server_parts[i] > 0:
                    update_needed = True
                    break

        if update_needed:
            result = pyautogui.confirm(f"发现新版本: {server_ver}，是否更新？")
            if result == "OK":
                webbrowser.open(last_link)
        else:
            QMessageBox.information(self, '提示:', '当前已是最新版本 无需更新')

    def download_image(self):  # 下载QQ头像
        if exp < 20:
            pyautogui.confirm("该功能需要Lv2才能使用!\n按ctrl+o 或按f12 打开控制台 输入签到 签到一天即可使用!")
            return 0
        self.btn_download_qq.setEnabled(False)

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
        for i in range(self.qq_image_down_spinbox.value()):
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
                    self.successfully_download_times.setText(f"有效次数: {success} 次")
            self.total_download_times.setText(f"总下载次数: {total} 次")
        if success == 0:
            pass
            self.successfully_download_times.setText("有效次数: 0 次")
        self.btn_download_qq.setEnabled(True)
        MyThread(play_warning_sound)
        pyautogui.confirm(f"图片下载成功!\n本次已成功下载{success}张图片(已删除默认头像)")

    def QQ_image_update(self):  # QQ个人信息资料一键更新
        result = pyautogui.confirm(
            "此功能只适用于旧版QQ! 请确认QQ版本后再使用\n请确保QQ主窗口已经打开 若打开则点击确认按钮 修改资料时 请勿移动鼠标\n若出现修改失败的情况 可能是间隔时间过小 略微调大即可")
        if result != "OK":
            return 0
        try:
            rest = self.qq_image_update_spinbox_interval.value()
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
            times = self.handle_send_times.value()
            wait_time = self.handle_send_interval.value()
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)  # 等待窗口聚焦

            for i in range(int(times)):
                doClick(handle_position[0], handle_position[1], hwnd)  # 点击 (30, height-60)
                time.sleep(wait_time)  # 等待操作完成

        hwnd = self._2lineEdit_3.text()
        massage = self._2textEdit.toPlainText()
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

    def Send_QQ(self):  # @QQ
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            target_number = self.QQ_StartSend_At_target_lineedit.text()
            pause_time = self.QQ_StartSend_At_pause_doublespb.value()
            times = self.QQ_StartSend_At_times_spinbox.value()
            number_send = False
            if target_number == "":
                pyautogui.confirm('请输入QQ号')
            elif pause_time == 0.0:
                pyautogui.confirm("请输入间隔")
            elif len(target_number) > 11 or len(
                    target_number) <= 5 or not target_number.isdigit():
                pyautogui.confirm('请输入正确的QQ号')
            else:
                time.sleep(3)
                number = 0
                pyautogui.PAUSE = pause_time
                if self.QQ_StartSend_At_number_checkbox.isChecked():
                    number_send = True
                self.showMinimized()
                while True:
                    if keys.is_pressed("F10"):  # 按下F10退出
                        self.showNormal()
                        self.open_point_window()
                        break
                    number = number + 1# 新增次数检测逻辑
                    if times != 0 and number >= times:
                        self.showNormal()
                        self.open_point_window()
                        break
                    pyautogui.click(textedit_position)
                    pyautogui.write(f'@{target_number}')
                    time.sleep(0.02)
                    pyautogui.press('enter')
                    pyautogui.hotkey('ctrl', 'v')
                    if number_send == True:
                        pyautogui.write(str(number))
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

    def Send_Copy(self):  # 发送复制消息
        # 要检查的进程名称
        target_process_name = "QQ.exe"
        if check_process_exists(target_process_name):
            if position_status == False:
                pyautogui.confirm("需要先设置位置才能开始发送")
                return 0
            play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
            time.sleep(3)
            pause_time = self.QQ_Send_Copy_pause_doublespb.value()
            times = self.QQ_Send_Copy_times_spinbox.value()
            pyautogui.PAUSE = pause_time
            number = 0
            start_time = time.time()
            self.showMinimized()
            while True:
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.showNormal()
                    self.open_point_window()
                    end_time = time.time()
                    # 计算执行时间
                    execution_time = end_time - start_time
                    # 打印执行时间
                    print(f"执行时间: {execution_time} 秒")
                    break
                number = number + 1
                if times != 0 and number >= times:
                    self.showNormal()
                    self.open_point_window()
                    break
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
            print(f"本次Fuchen累计发送{number}条消息")
        else:
            pyautogui.confirm("QQ未启动!")

    def order_send(self):
        if self.QQ_Seq_lineEdit == '':
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
        wait_time = self.QQ_Seq_doublebox.value()
        if self.QQ_Seq_combobox.currentText() == '顺序发送':

            pyautogui.PAUSE = wait_time
            for i in range(self.QQ_Seq_Times_spinBox.value()):
                with open(self.QQ_Seq_lineEdit.text(), 'r', encoding='utf-8') as file:
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
            pyautogui.PAUSE = wait_time
            # 读取文件内容到列表中
            with open(self.QQ_Seq_lineEdit.text(), 'r', encoding='utf-8') as file:
                lines = file.readlines()
            # 随机选择一行
            for i in range(self.QQ_Seq_Times_spinBox.value()):
                random_line = random.choice(lines).strip()
                if keys.is_pressed("F10"):  # 按下F10退出
                    self.showNormal()
                    self.open_point_window()
                    break
                # 复制该行内容到剪切板
                pyperclip.copy(random_line)
                pyautogui.click(textedit_position)
                #time.sleep(wait_time)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.02)
                pyautogui.click(send_position)

    def handle_minimize(self):  #通过主进程最小化
        self.showMinimized()

    def handle_restore(self):  # 通过主进程恢复
        self.showNormal()
        self.repaint()  # 或者调用 update() 来刷新界面

    def record_change(self, type):  #记录脚本模式选择
        if type == 'hotkey':
            self.uim._3pushButton.setVisible(False)
            self.uim.Hotkey_record_button.setVisible(True)
            if self.uim.record_hotkey != '未设置':
                self.hotkey_record_status = keys.add_hotkey(self.uim.record_hotkey, self.start_recording)
        else:
            self.uim._3pushButton.setVisible(True)
            self.uim.Hotkey_record_button.setVisible(False)
            if self.hotkey_record_status != None:
                self.hotkey_record_status()
                self.hotkey_record_status = None

    def execute_change(self, type):  #执行脚本模式选择
        if type == 'hotkey':
            self.uim._3pushButton_2.setVisible(False)
            self.uim.Hotkey_execute_button.setVisible(True)
            if self.uim.execute_hotkey != '未设置':
                self.hotkey_execute_status = keys.add_hotkey(self.uim.execute_hotkey, self.start_executing)
        else:
            self.uim._3pushButton_2.setVisible(True)
            self.uim.Hotkey_execute_button.setVisible(False)
            if self.hotkey_execute_status != None:
                self.hotkey_execute_status()
                self.hotkey_execute_status = None

    def record_hotkey_setting(self):
        if self.hotkey_execute_status != None:
            self.hotkey_execute_status()
        # 创建并显示热键对话框（模态对话框）
        dialog = ui.hotkey_record.HotkeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # 等待对话框关闭
            hotkey = dialog.hotkey
            if hotkey == '':
                return
            if hotkey == self.uim.execute_hotkey:
                pyautogui.confirm('记录按键不可与执行按键相同')
                return
            self.uim.record_hotkey = hotkey
            if self.hotkey_record_status == None:
                self.hotkey_record_status = keys.add_hotkey(hotkey, self.start_recording)
            else:
                self.hotkey_record_status()
                self.hotkey_record_status = keys.add_hotkey(hotkey, self.start_recording)
            self.uim.Hotkey_record_button.setText(f"当前热键：{hotkey}")
            print("获取到的热键：", hotkey)
        if self.uim.execute_hotkey != '未设置':
            self.hotkey_execute_status = keys.add_hotkey(self.uim.execute_hotkey, self.start_executing)

    def on_record_finished(self):
        self.handle_restore()
        print("录制结束")
        self.record_thread = None

    def execute_hotkey_setting(self):
        if self.hotkey_record_status != None:
            self.hotkey_record_status()
        # 创建并显示热键对话框（模态对话框）
        dialog = ui.hotkey_record.HotkeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:  # 等待对话框关闭
            hotkey = dialog.hotkey
            if hotkey == '':
                return
            if hotkey == self.uim.record_hotkey:
                pyautogui.confirm('执行按键不可与记录按键相同')
                return
            self.uim.execute_hotkey = hotkey
            if self.hotkey_execute_status == None:
                self.hotkey_execute_status = keys.add_hotkey(hotkey, self.start_executing)
            else:
                self.hotkey_execute_status()
                self.hotkey_execute_status = keys.add_hotkey(hotkey, self.start_executing)
            self.uim.Hotkey_execute_button.setText(f"当前热键：{hotkey}")
            print("获取到的热键：", hotkey)
        if self.uim.record_hotkey != '未设置':
            self.hotkey_record_status = keys.add_hotkey(self.uim.record_hotkey, self.start_recording)

    def on_execute_finished(self):
        self.handle_restore()
        print("执行结束")
        self.execute_thread = None

    def Click_Record(self):  # 记录自动脚本

        # 确保在主线程执行
        if QThread.currentThread() != self.thread():
            QTimer.singleShot(0, self.Click_Record)
            return
        if self.record_status == False:  #防止重复执行
            self.record_status = True
        else:
            return
        if self.file_lineEdit.text() == '':
            QMessageBox.information(self, "提示", f"配置文件为空 请先选则文件")
            self.record_status = False
            return 0
        self.handle_minimize()
        #self.showMinimized()

        wait_time = self.wait_doubleSpinBox.value()
        time.sleep(wait_time)
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        current_position = pyautogui.position()
        print("开始记录自动脚本")
        global last_time, records, last_key, last_event_type

        records = []
        last_time = time.time()
        if self.end_key_combo.currentText() == "ESC":
            ed_bu = Key.esc
        elif self.end_key_combo.currentText() == "F8":
            ed_bu = Key.f8
        elif self.end_key_combo.currentText() == "F9":
            ed_bu = Key.f9
        elif self.end_key_combo.currentText() == "F10":
            ed_bu = Key.f10
        elif self.end_key_combo.currentText() == "END":
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

        def on_scroll(x, y, dx, dy):
            global last_time
            current_time = time.time()
            interval = int((current_time - last_time) * 1000)
            action = 'mouse scroll'
            records.append([interval, 'M', action, [0, dy]])
            last_time = current_time

        # 设置防抖时间间隔（毫秒）
        debounce_interval = 200
        last_key = None
        last_event_type = None

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


        # 打开文件进行写入
        '''with open(self.file_lineEdit.text(), 'w') as f:
            for record in records:
                if record[0] != 0:
                    if isinstance(record[3][1], str) and len(record[3][1]) == 1 and record[3][
                        1].isupper():
                        record[3] = (record[3][0], record[3][1].lower())
                    f.write(str(record) + '\n')'''
        json_records = []
        for record in records:
            interval, event_type, action, data = record
            json_record = {
                "interval": interval,
                "type": "keyboard" if event_type == 'K' else "mouse",
                "action": None,
                "details": {}
            }

            if event_type == 'K':
                json_record["action"] = action.split()[-1]
                json_record["details"] = {
                    "code": data[0],
                    "name": data[1].upper() if data[1].isalpha() else data[1]
                }
            else:
                if 'move' in action:
                    json_record["action"] = "move"
                    json_record["details"] = {"x": data[0], "y": data[1]}
                elif 'scroll' in action:
                    json_record["action"] = "scroll"
                    json_record["details"] = {"dx": data[0], "dy": data[1]}
                else:
                    button = action.split()[1]
                    json_record["action"] = action.split()[-1]
                    json_record["details"] = {
                        "button": button,
                        "x": data[0],
                        "y": data[1]
                    }
            json_records.append(json_record)

        # 最后写入整个 JSON 数组
        with open(self.file_lineEdit.text(), 'w') as f:
            json.dump(json_records, f, indent=2)

        '''with open(self.file_lineEdit.text(), 'w') as f:
            for record in records:
                interval, event_type, action, data = record
                json_record = {
                    "interval": interval,
                    "type": "keyboard" if event_type == 'K' else "mouse",
                    "action": None,
                    "details": {}
                }

                if event_type == 'K':
                    # 键盘事件
                    json_record["action"] = action.split()[-1]  # 'up' 或 'down'
                    json_record["details"] = {
                        "code": data[0],
                        "name": data[1].upper() if data[1].isalpha() else data[1]
                    }
                else:
                    # 鼠标事件
                    if 'move' in action:
                        json_record["action"] = "move"
                        json_record["details"] = {"x": data[0], "y": data[1]}
                    elif 'scroll' in action:
                        json_record["action"] = "scroll"
                        json_record["details"] = {"dx": data[0], "dy": data[1]}
                    else:
                        # 点击事件
                        button = action.split()[1]  # left/right/middle
                        json_record["action"] = action.split()[-1]  # down/up
                        json_record["details"] = {
                            "button": button,
                            "x": data[0],
                            "y": data[1]
                        }

                f.write(json.dumps(json_record) + '\n')'''


        mouse_listener.stop()
        keyboard_listener.stop()

        self.handle_restore()
        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")

        pyautogui.moveTo(current_position.x, current_position.y)
        print("记录完毕")
        self.record_status = False

    def Click_Record_execute(self):  # 执行自动脚本
        # 确保在主线程执行
        if QThread.currentThread() != self.thread():
            QTimer.singleShot(0, self.Click_Record_execute)
            return
        if self.execute_status == False:  #防止重复执行
            self.execute_status = True
        else:
            return
        if self.file_lineEdit.text() == '':
            QMessageBox.information(self, "提示", f"配置文件为空 请先选则文件")
            self.execute_status = False
            return 0
        stop_script = False  # 局部变量，用于控制脚本停止
        listener = None  # 全局引用监听器
        param = self.param_lineEdit.text()
        def key_listener():
            """监听键盘按键，检测终止按键"""
            nonlocal stop_script  # 使用非局部变量
            nonlocal listener

            def on_press(key):
                try:
                    # 检测到按键时停止脚本
                    if self.end_key_combo.currentText() == "ESC":
                        ed_bu = Key.esc
                    elif self.end_key_combo.currentText() == "F8":
                        ed_bu = Key.f8
                    elif self.end_key_combo.currentText() == "F9":
                        ed_bu = Key.f9
                    elif self.end_key_combo.currentText() == "F10":
                        ed_bu = Key.f10
                    elif self.end_key_combo.currentText() == "END":
                        ed_bu = Key.end
                    else:
                        ed_bu = Key.esc
                    if key == ed_bu:
                        nonlocal stop_script
                        stop_script = True
                        print(f"检测到 {self.end_key_combo.currentText()}，脚本终止中...")
                except Exception as e:
                    print(f"按键监听异常: {e}")

            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            listener.join()

        # 启动键盘监听器线程
        listener_thread = threading.Thread(target=key_listener, daemon=True)
        listener_thread.start()

        self.showMinimized()


        play_prompt_sound("C:\\Windows\\Media\\Windows Notify Messaging.wav")
        wait_time = self.wait_doubleSpinBox.value()
        current_position = pyautogui.position()
        count = self._3spinBox_3.value()
        time.sleep(wait_time)


        #self.handle_minimize()

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
        pyautogui.PAUSE = 0
        speed = self.spinbox_play_speed.value()/100
        # 获取主屏幕
        screen = app.primaryScreen()
        # 获取屏幕分辨率
        screen_width = screen.size().width()
        screen_height = screen.size().height()
        '''with open(self.file_lineEdit.text(), 'r') as f:
            for line in f:
                if line[0] != '#':
                    record = eval(line.strip())
                    record_time += record[0]
                    records.append(record)'''
        '''records = []
        with open(self.file_lineEdit.text(), 'r') as f:
            for line in f:
                json_record = json.loads(line.strip())

                # 转换回原始格式兼容旧执行逻辑
                if json_record["type"] == "keyboard":
                    record = [
                        json_record["interval"],
                        'K',
                        f'key {json_record["action"]}',
                        [json_record["details"]["code"], json_record["details"]["name"].lower()]
                    ]
                else:
                    if json_record["action"] == "move":
                        record = [
                            json_record["interval"],
                            'M',
                            'mouse move',
                            [json_record["details"]["x"], json_record["details"]["y"]]
                        ]
                    elif json_record["action"] == "scroll":
                        record = [
                            json_record["interval"],
                            'M',
                            'mouse scroll',
                            [json_record["details"]["dx"], json_record["details"]["dy"]]
                        ]
                    else:
                        record = [
                            json_record["interval"],
                            'M',
                            f'mouse {json_record["details"]["button"]} {json_record["action"]}',
                            [json_record["details"]["x"], json_record["details"]["y"]]
                        ]

                records.append(record)'''
        with open(self.file_lineEdit.text(), 'r') as f:
            json_records = json.load(f)

        records = []
        for json_record in json_records:
            if json_record["type"] == "keyboard":
                record = [
                    json_record["interval"],
                    'K',
                    f'key {json_record["action"]}',
                    [json_record["details"]["code"], json_record["details"]["name"].lower()]
                ]
            else:
                if json_record["action"] == "move":
                    record = [
                        json_record["interval"],
                        'M',
                        'mouse move',
                        [json_record["details"]["x"], json_record["details"]["y"]]
                    ]
                elif json_record["action"] == "scroll":
                    record = [
                        json_record["interval"],
                        'M',
                        'mouse scroll',
                        [json_record["details"]["dx"], json_record["details"]["dy"]]
                    ]
                else:
                    record = [
                        json_record["interval"],
                        'M',
                        f'mouse {json_record["details"]["button"]} {json_record["action"]}',
                        [json_record["details"]["x"], json_record["details"]["y"]]
                    ]
            records.append(record)

        print(f"记录执行时间:{record_time / 1000}秒")
        deal_time = 0
        for x in records:
            x[0] = int(x[0]/speed)
            deal_time += x[0]
        star = time.time()
        for i in range(count):  # 开始执行自动脚本
            for record in records:
                if stop_script:  # 检测是否需要终止
                    print("脚本执行已终止。")
                    listener.stop()  # 停止按键监听器
                    break
                #time.sleep((record[0] - 1) / 1000)  # 等待时间````
                #precise_sleep(record[0]-1)
                precise_sleep(record[0])
                if record[1] == 'M':  # 鼠标事件
                    x, y = record[3] if record[2] != 'mouse scroll' else (None, None)
                    if 'mouse move' in record[2]:
                        #pyautogui.moveTo(x, y)
                        mouse_controller.position = (x, y)
                        '''absolute_x = (x * 65535) // screen_width
                        absolute_y = (y * 65535) // screen_height
                        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, absolute_x, absolute_y, 0, 0)'''
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
                    elif 'mouse scroll' in record[2]:
                        dx, dy = record[3]
                        mouse_controller.scroll(dx, dy)
                        #win32api.SetCursorPos((x, y))


                elif record[1] == 'K':  # 键盘事件
                    key_code, key_char = record[3]
                    key = get_key(key_code, key_char)
                    if 'down' in record[2]:
                        keyboard_controller.press(key)
                    elif 'up' in record[2]:
                        keyboard_controller.release(key)
                """
                        elif 'mouse left down' in record[2]:
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    elif 'mouse left up' in record[2]:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif 'mouse right down' in record[2]:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        
            elif 'mouse right up' in record[2]:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        
        elif 'mouse middle down' in record[2]:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
        elif 'mouse middle up' in record[2]:
        win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)"""
        # 停止监听器
        if listener is not None:
            listener.stop()
        end_ti = time.time()
        print(f"实际执行时间:{(end_ti - star):.2f}秒")
        #self.showNormal()
        self.execute_status = False
        self.handle_restore()
        pyautogui.moveTo(current_position.x, current_position.y)


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


    def action_Clicked(self, key):
        if key == '自定义':
            detector = SundryUI.KeyDetector()
            if detector.exec_() == QDialog.Accepted:
                name = detector.inverted_dict.get(
                    detector.current_keycode,
                    f"未知按键: {detector.current_keycode}"
                )
                if detector.current_keycode != 1:
                    self.sort = name
                    self._3pushButton_4.setText(f"设置启停快捷键({self.sort})")
                    self.update_shared_params()
                    print(name,detector.current_keycode)
        else:
            self.sort = key
            self._3pushButton_4.setText(f"设置启停快捷键({self.sort})")
            self.update_shared_params()

    def key_menu_com(self, types, key):
        if types == 'record':
            self.end_key = key
            self.end_key_button.setText(f"{key}")
        elif types == 'execute':
            self.end_execute_key = key
            self.end_execute_button.setText(f"{key}")

    def mixPicture(self):  # 图片格式转换
        # 检查选择的格式
        if self.JPG_radioButton.isChecked():
            output_image_format = "JPG"
        elif self.PNG_radioButton.isChecked():
            output_image_format = "PNG"
        elif self.GIF_radioButton.isChecked():
            output_image_format = "GIF"
        elif self.PDF_radioButton.isChecked():
            output_image_format = "PDF"
        else:
            pyautogui.confirm("ERROR!")
            return 0

        input_image_path = self.pic_input_lineEdit.text()
        output_folder_path = self.pic_output_lineEdit.text()
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

            url = self.music_url.text()
            music_id = url.split('=')[1]
            response = requests.get(download_url.format(music_id), headers=headers)
            file_name = self.music_filename.text()
            save_path = f'{self.music_savepath.text()}\\{file_name}'
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

                    self.show_message_box("提示", f"下载成功! {file_name} 文件大小:{file_size}")
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

    def quit_team_H(self):  #队员退出队伍

        self.create_team_button.setVisible(True)  # 创建队伍按钮
        self.add_team_lineEdit.setVisible(True)  # 加入队伍标签
        self.add_team_button.setVisible(True)
        self.button_copy_id.setVisible(False)  # 复制ID按钮

        self.add_team_ID.setText(f"队伍ID为:")
        self.add_team_ID.setVisible(False)

        self.user2.lbl_name.setText("等待用户加入")
        self.user2.lbl_id.setText("id: ")
        self.user2.avatar_user_team = QPixmap('.image/other_user.png').scaled(100, 100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.user2.avatar_frame.setPixmap(self.user2.avatar_user_team)

    def set_variables(self, vars_dict, namespace=None):
        """
        通过变量名字符串动态修改指定命名空间中的变量值
        :param vars_dict: 字典格式 {变量名: 新值}
        :param namespace: 命名空间字典，默认使用全局作用域
        """
        namespace = namespace or globals()
        assignments = "; ".join(
            [f"{k} = {repr(v)}" for k, v in vars_dict.items()]
        )
        exec(assignments, namespace)

    def quit_team_C(self):  # 队长退出队伍
        self.create_team_button.setVisible(True)  # 创建队伍按钮
        self.add_team_lineEdit.setVisible(True)  # 加入队伍标签
        self.add_team_button.setVisible(True)
        self.create_team_label_prompt.setVisible(False)  # 复制ID按钮
        self.user1.combo_options.setVisible(True)
        self.user2.combo_options.setVisible(True)
        self.team_execute_prompt.setText("等待队长开始执行...")
        self.team_layout.removeWidget(self.team_execute_prompt)  # 解绑控件与布局
        self.team_execute_prompt.setParent(None)  # 解除父级关联
        self.team_execute_prompt.hide()  # 隐藏控件
        self.team_btn_start.setVisible(True)

        self.user1.lbl_name.setText(f"{self.username.text()}[我]")
        self.user1.lbl_id.setText(f"{self.username.text()}")
        self.user1.avatar_user_team = QPixmap('./temp/avatar.png').scaled(100, 100,
                                                                             Qt.KeepAspectRatio,
                                                                             Qt.SmoothTransformation)
        self.user1.avatar_frame.setPixmap(self.user1.avatar_user_team)

        self.user2.lbl_name.setText("等待用户加入")
        self.user2.lbl_id.setText("id: ")
        self.user2.avatar_user_team = QPixmap('.image/other_user.png').scaled(100, 100,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.user2.avatar_frame.setPixmap(self.user2.avatar_user_team)

    def team(self):  # 创建队伍
        self.create_team_button.setVisible(False)  # 创建队伍按钮
        self.add_team_lineEdit.setVisible(False)  #加入队伍标签
        self.add_team_button.setVisible(False)
        self.button_copy_id.setVisible(True)  # 复制ID按钮
        characters = string.ascii_letters + string.digits
        global random_string
        random_string = ''.join(random.choices(characters, k=30))
        self.add_team_ID.setText(f"队伍ID为:{random_string}")
        self.add_team_ID.setVisible(True)


        TypedJSONClient('create_team', {'number': random_string})

    def join_team(self):
        id = self.add_team_lineEdit.text()
        if len(id) != 30:
            self.show_message_box("提示", "队伍id不正确!")
        else:
            TypedJSONClient('join_team', {'number': id})

    def team_c(self):
        captain = self.user1.combo_options.currentIndex()
        member = self.user2.combo_options.currentIndex()
        types = None
        if member == 0:
            types = 'handle_send'
        elif member == 1:
            types = 'user_send'
        elif member == 2:
            types = 'copy_send'
        elif member == 3:
            types = 'information_update'
        elif member == 4:
            types = 'record_execute'
        else:
            types = 'unknown'
        if types == 'unknown':
            self.show_message_box('提示', '未知类型')
            return
        TypedJSONClient('team_execute', {'types': types})
        if captain == 0:
            self.Handle_Send()
        elif captain == 1:
            self.Send_QQ()
        elif captain == 2:
            self.Send_Copy()
        elif captain == 3:
            self.QQ_image_update()
        elif captain == 4:
            self.Click_Record_execute()
        else:
            self.show_message_box('提示', '未知类型')

    def deal_team_send(self, types):
        if types == 'handle_send':
            self.team_execute_prompt.setText(f"即将发送QQ句柄消息")
            self.Handle_Send()
        elif types == 'user_send':
            self.team_execute_prompt.setText(f"即将发送@QQ消息")
            self.Handle_Send()
        elif types == 'copy_send':
            self.team_execute_prompt.setText(f"即将发送QQ复制消息")
            self.Handle_Send()
        elif types == 'information_update':
            self.team_execute_prompt.setText(f"即将进行QQ信息更新")
            self.Handle_Send()
        elif types == 'record_execute':
            self.team_execute_prompt.setText(f"即将开始执行自动脚本")
            self.Handle_Send()
        else:
            self.team_execute_prompt.setText(f"未知类型 错误!")
            self.show_message_box('提示', '未知类型')

    def copy_team_number(self):
        global random_string
        clipboard = QApplication.clipboard()
        clipboard.setText(f'{random_string}')

    def showEvent(self, e):
        if self.first_image == False:
            if Theme == "Custom":  # 自定义图片背景设置
                with open('config.json', 'r') as file:
                    config = json.load(file)
                Path_Custom_S = config.get("Path")
                print(Path_Custom_S)
                self.should_draw = "Custom"
                im = Image.open(Path_Custom_S)
                reim = im.resize((self.width(), self.height()))  # 宽*高
                reim.save('./temp/background_custom.png',
                          dpi=(400, 400))  ##200.0,200.0分别为想要设定的dpi值
                # 打开图片
                image = Image.open('./temp/background_custom.png')
                # 应用高斯模糊，radius参数控制模糊程度（半径越大越模糊）
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
                # 保存处理后的图片
                blurred_image.save('./temp/background_custom.png')

                palette = QPalette()
                palette.setBrush(QPalette.Background,
                                 QBrush(QPixmap('./temp/background_custom.png')))

                self.setPalette(palette)
                trp = transparent / 100
                # 设置整体透明度（会影响所有子元素）
                self.sidebar.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp))
                self.stack.setGraphicsEffect(QGraphicsOpacityEffect(opacity=trp - 0.1))
                print('成功设置背景')

                del Path_Custom_S
                self.first_image = True
            elif Theme == 'Trend':
                self.execute_trend()
                self.first_image = True

    def show_message_box(self, head, message):
        QMessageBox.question(self, head, message,
                             QMessageBox.Yes)

    def handle_message(self, title, content):
        reply = QMessageBox.information(self, title, content, QMessageBox.Yes)

class LoginWindow(QMainWindow):  # 实例化登录窗口
    def __init__(self):
        super().__init__()
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.reset_window_status = False
        self.register_window_status = False
        self.reset_window = None
        self.register_window = None
        if remember == True:
            self.ui.checkBox.click()
        if AutoLogin == True:
            self.ui.checkBox2.click()
        self.ui.Account_lineEdit.setText(str(Account))
        self.ui.Password_lineEdit.setText(str(Password))
        self.setWindowTitle("Fuchen 登录")
        icon = QIcon(".image/window.ico")
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
            folder_path = 'C:\\Fuchen\\image'  # 修改为你要打开的文件夹路径
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)


    def closeEvent(self, e):
        self.close()
        if self.reset_window_status == True:
            self.reset_window.close()
        if self.register_window_status == True:
            self.register_window.close()
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
        global AutoLogin,city_name,Account
        try:
            if mode == 'login':
                self.ui.Login_Button.setEnabled(False)
                time.sleep(0.1)
                Account = self.ui.Account_lineEdit.text()
                Password = self.ui.Password_lineEdit.text()
                if (len(Account) != 6) and ('@' not in Account):  #非邮箱非数字
                    if AutoLogin == True:
                        window_login.show()
                    pyautogui.confirm("账号为6位数字或邮箱 请重新输入!")
                    self.ui.Login_Button.setEnabled(True)
                    return 0
                if not (7 < len(Password) < 16):
                    if AutoLogin == True:
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
                    del local_part,domain_part
                TypedJSONClient('login', {'user_input': Account, 'password': Password, 'position':city_name, 'system': system, 'computer_name': computer_name})
                time.sleep(0.1)
                request = recv_json(s)
                print(request)
                if request.get('type') == 'login_status':
                    log_ST = request.get('data')
                    print(log_ST)
                    log_ST = log_ST.get("status")
                    #if log_ST ==
                if log_ST == "pass":
                    print("密码正确 正在加载中")
                elif log_ST == "Cooling":
                    pyautogui.confirm("账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
                else:
                    print("密码错误 请重试")
            elif mode == 'tourist_login':
                TypedJSONClient('login_tourist',
                                {'position': city_name})
                self.ui.Login_Button.setEnabled(False)

                Account = "游客"
                Password = "None"
                #send_encry('tourist_login')
                time.sleep(0.1)
                request = recv_json(s)
                if request.get('type') == 'login_status':
                    log_ST = request.get('data')
                    print(log_ST)
                    log_ST = log_ST.get("status")
            elif mode == 'offline_login':
                self.ui.Login_Button.setEnabled(False)
                Account = "离线"
                Password = "None"
                time.sleep(0.1)
                log_ST = 'pass'
            else:
                log_ST = 'fail'
            if log_ST == 'pass':  # 密码正确


                self.ui.pushButton_signin.setEnabled(False)
                self.ui.Login_Button.setEnabled(False)
                self.ui.pushButton_short.setEnabled(False)
                self.ui.pushButton_quit.setEnabled(False)
                self.ui.Login_Button.setText("正在加载用户数据")
                self.ui.Login_Button.repaint()
                # 记录开始时间
                start_time = time.time()
                if connect_status != None:
                    request = recv_json(s)
                    request_type = request.get('type')
                    request_data = request.get('data')
                    if request_type == 'login_successfully':
                        if "@" in Account:
                            Account = request_data.get("account")
                        global Name, Email, exp, avatar_date, avatar_status
                        Name = request_data.get("name")
                        Email = request_data.get("email")
                        avatar_status = request_data.get("avatar_status")
                        avatar_date = request_data.get("avatar_date")
                        exp = request_data.get("exp")
                else:
                    #dat = "游客 None False 2000-1-1 100 000000"

                    Name = '游客'
                    Email = None
                    avatar_status = False
                    avatar_date = '2000-1-1'
                    exp = 100
                time.sleep(0.1)
                if avatar_status == True:
                    try:
                        self.ui.Login_Button.setText("正在加载用户头像")
                        self.ui.Login_Button.repaint()
                        print(f'正在加载用户头像 {Account}.jpg')
                        # 接收图片文件大小
                        file_size = int(s.recv(1024).decode().rstrip('\n'))
                        with open('./temp/avatar.png', 'wb') as file:
                            total_received = 0
                            while total_received < file_size:
                                chunk = s.recv(2048)
                                time.sleep(0.05)
                                if chunk == '\n':  # 检测到结束标记
                                    break
                                if not chunk:
                                    break
                                file.write(chunk)
                                total_received += len(chunk)
                                progress_percentage = round(total_received / file_size * 100, 2)  # 将进度转换为百分比并保留两位小数
                                self.ui.Login_Button.setText(f"正在加载用户头像 {progress_percentage}%")
                                self.ui.Login_Button.repaint()
                        print('文件写入完成')
                        global avatar_load_status
                        avatar_load_status = True
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
                    AutoLogin = True
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
                    AutoLogin = True
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
                    new_mainpage.Name = Name
                    new_mainpage.Account = Account
                    new_mainpage.Version = Version
                    new_mainpage.information = information
                    new_mainpage.avatar_load_status = avatar_load_status
                    new_mainpage.position_status = position_status
                    new_mainpage.textedit_position = textedit_position
                    new_mainpage.send_position = send_position
                    new_mainpage.mode = Account
                    new_mainpage.s = s
                    windows = Ui_Form(stdout_stream, stderr_stream)
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
                    print(f"窗口打开成功 本次登录耗时:{execution_time}秒")
                    windows.show()
                except Exception as e:
                    traceback.print_exc()
                    print(e)


            elif log_ST == "cooling":
                pyautogui.confirm("账号密码输入次数过多 账号已被锁定!请于一小时后重新登录")
            else:
                self.ui.Login_Button.setEnabled(False)
                if AutoLogin == True:
                    window_login.show()
                time.sleep(0.5)
                pyautogui.confirm("密码错误")
                self.ui.Login_Button.setEnabled(True)
        except Exception as e:
            traceback.print_exc()
            pyautogui.confirm("未知错误", e)

    def reg(self):
        if self.register_window_status is False:
            self.register_window_status = True
            self.register_window = Register(s)
            self.register_window.exec_()
            if self.register_window.result_value!= None:
                if self.register_window.result_value[0] == '注册成功':
                    self.ui.Account_lineEdit.setText(self.register_window.result_value[1])
                    self.ui.Password_lineEdit.setText(self.register_window.result_value[2])
                    self.ui.checkBox.setChecked(True)
            self.register_window_status = False

    def rew(self):
        if self.reset_window_status == False:
            self.reset_window_status = True
            self.reset_window = Reset(s)
            self.reset_window.exec_()
            self.reset_window_status = False



if __name__ == "__main__":
    try:
        # 适应高DPI设备
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        # 适应Windows缩放
        QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except Exception as e:
        logging.exception(str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())) + "错误:" + str(e))
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
    #window_signin = RegisterWindow.Register(s)  #注册窗口

    #window_reword = ResetWindow.Reset(s)  #重置密码窗口
    if AutoLogin == True and connect_status != None:
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