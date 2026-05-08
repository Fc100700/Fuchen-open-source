import os
import random
import struct
import traceback
from datetime import datetime

import requests
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import  QMainWindow, QTextBrowser, QDesktopWidget
from pyexpat import ErrorString
import SundryUI
import ui.color_change
import ui.style
import function
import turtle
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QIcon
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel, \
    QPushButton, QAction, QMenu, QDialog
from PyQt5 import QtGui, QtWidgets, QtCore
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import ui.style
import ui.buttons
import pyautogui
import time
import json
import tkinter as tk
from SocketThread import socket_information


def encrypt(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return ciphertext

def decrypt(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def send_encry(text, s, key, iv):  # 加密发送
    content = encrypt((text).encode('utf-8'), key, iv)
    s.sendall(content)

def send_decry(text, key, iv):  # 解密内容
    content = decrypt(text, key, iv).decode('utf-8')
    return content

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


class CustomLineEdit(QtWidgets.QLineEdit):
    up_arrow_pressed = QtCore.pyqtSignal()  # 自定义信号
    down_arrow_pressed = pyqtSignal()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.up_arrow_pressed.emit()  # 触发信号
            event.accept()  # 阻止事件继续传递
        elif event.key() == Qt.Key_Down:
            self.down_arrow_pressed.emit()
        else:
            super().keyPressEvent(event)  # 其他按键保持默认行为


class ConsoleWindow(QMainWindow):
    def __init__(self, lis):
        super().__init__()
        global windows, s, key, iv, sys_list

        self.stdout_stream = lis[0]
        self.stderr_stream = lis[1]
        windows = lis[2]
        s = lis[3]
        theme = lis[4]
        if theme == 'dark':
            self.dark_mode = True  # 默认深色模式
        else:
            self.dark_mode = False
        self.input_content_last = ''
        self.input_history = []  # 存储最多5条历史记录
        self.history_index = 0  # 当前显示的历史记录索引
        self.temporary_input = ''  # 临时存储未提交的修改
        self.list_function = {
                            "签到": "每日可签到一次",
                            "查询经验值": "查询当前的经验值",
                            "update weather": "手动更新天气",
                            "runtime": "查看当前软件运行时间",
                            "局域网传输工具": "运行局域网传输工具",
                            "更改颜色": "自定义修改主题配色",
                            "点击测试": "测试左键点击速度",
                            "handle x y": "手动设置句柄发送输入栏位置",
                            "random 选项1 选项2.... ": "可以随机做出一个选择",

                        }

        # 隐藏原生标题栏并设置透明背景
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        self.load_history()
        # 添加右键菜单支持
        self.title_bar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.title_bar.customContextMenuRequested.connect(self.show_titlebar_menu)

        self.stdout_stream.text_written.connect(self.append_stdout)
        self.stderr_stream.text_written.connect(self.append_stderr)
        # 居中窗口
        self.center()

    def center(self):
        """将窗口居中显示"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        self.setWindowTitle('控制台Console')
        self.setGeometry(100, 100, 800, 500)
        self.setFixedSize(800,500)

        # 新增主题样式数据
        self.theme_styles = {
            "dark": {
                "main_bg": "#2D2D2D",
                "text_color": "#E0E0E0",
                "title_bar": "#202020",
                "input_bg": "#3A3A3A",
                "scroll_handle": "#4A4A4A",
                "button_bg": "#4A4A4A",
                "error_color": "red",
                "min_btn_bg": "#4A4A4A",
                "min_btn_hover": "#5A5A5A",
                "min_btn_press": "#3A3A3A"
            },
            "light": {
                "main_bg": "#F0F0F0",
                "text_color": "#333333",
                "title_bar": "#E0E0E0",
                "input_bg": "#FFFFFF",
                "scroll_handle": "#C0C0C0",
                "button_bg": "#D0D0D0",
                "error_color": "#D00000",
                "min_btn_bg": "#D0D0D0",
                "min_btn_hover": "#C0C0C0",
                "min_btn_press": "#B0B0B0"
            }
        }

        self.browser = QTextBrowser(self)
        self.browser.setAcceptRichText(True)
        self.browser.setLineWrapMode(QTextBrowser.NoWrap)
        self.browser.setGeometry(0,30,800,455)

        # 自定义标题栏
        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, 800, 30)
        # 标题栏样式调整
        self.title_bar.setMouseTracking(True)

        # 标题文字
        self.title_label = QLabel("控制台 Console", self.title_bar)
        self.title_label.setGeometry(10, 5, 200, 20)
        self.title_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 关闭按钮
        self.close_button = QPushButton("×", self.title_bar)
        self.close_button.setGeometry(775, 5, 20, 20)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
                            QPushButton {
                                background-color: #FF5555;
                                color: #E0E0E0;
                                border-radius: 3px;
                                font-size: 16px;
                            }
                            QPushButton:hover { background-color: #FF6666; }
                            QPushButton:pressed { background-color: #FF4444; }
                        """)

        # 最小化按钮
        self.min_button = QPushButton("—", self.title_bar)
        self.min_button.setGeometry(750, 5, 20, 20)
        self.min_button.clicked.connect(self.showMinimized)

        # 初始化主题切换按钮
        self.theme_button = QPushButton(self.title_bar)
        self.theme_button.setGeometry(725, 5, 20, 20)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #666666;
                        font-size: 14px;
                        border: none;
                    }
                    QPushButton:hover { color: #444444; }
                """)
        self.min_button.raise_()

        self.lineEdit = CustomLineEdit(self)
        self.lineEdit.setGeometry(0, 475, 800, 25)
        self.lineEdit.setObjectName('lineEdit')
        self.lineEdit.returnPressed.connect(self.input_content)
        self.lineEdit.up_arrow_pressed.connect(self.handle_up_arrow)
        self.lineEdit.down_arrow_pressed.connect(self.handle_down_arrow)

        # 把确认往左挪出空间
        self.confirm_button = QPushButton(self)
        self.confirm_button.setGeometry(650,475,75,25)
        self.confirm_button.setText('确认')
        self.confirm_button.setFont(ui.style.style_font_9)
        self.confirm_button.setObjectName('confirm_button')
        self.confirm_button.clicked.connect(self.input_content)

        # 新增问号按钮（在确认后面，保存前面）
        self.help_button = QPushButton(self)
        self.help_button.setGeometry(725,475,25,25)
        self.help_button.setObjectName('help_button')
        self.help_button.setIcon(QIcon("./image/Component/提示3.png"))
        self.help_button.setIconSize(QSize(18, 18))
        self.help_button.clicked.connect(self.show_help)

        # 保存按钮右侧
        self.save_button = QPushButton(self)
        self.save_button.setGeometry(750,475,25,25)
        self.save_button.clicked.connect(self.save)
        self.save_button.setObjectName('save_button')
        self.save_button.setStyleSheet(ui.style.save_button_style)
        self.save_button.setIcon(QIcon("./image/Component/保存-1.png"))  # 替换为实际图标路径
        self.save_button.setIconSize(QSize(20, 20))  # 明确设置图标大小

        self.apply_theme()

    def apply_theme(self):
        theme = "dark" if self.dark_mode else "light"
        self.theme_button.setText("🌙" if self.dark_mode else "🌞")
        function.update_console_theme(theme)

        if theme == 'light':
            self.browser.setStyleSheet(ui.style.style_console_browser_light)
            self.title_bar.setStyleSheet(ui.style.style_console_title_bar_light)
            self.title_label.setStyleSheet(ui.style.style_console_title_label_light)
            self.lineEdit.setStyleSheet(ui.style.style_console_lineedit_light)
            self.confirm_button.setStyleSheet(ui.style.style_console_confirm_button_light)
            self.save_button.setIcon(QIcon("./image/Component/保存.png"))  # 替换为实际图标路径
        else:
            self.browser.setStyleSheet(ui.style.style_console_browser_dark)
            self.title_bar.setStyleSheet(ui.style.style_console_title_bar_dark)
            self.lineEdit.setStyleSheet(ui.style.style_console_lineedit_dark)
            self.title_label.setStyleSheet(ui.style.style_console_title_label_dark)
            self.confirm_button.setStyleSheet(ui.style.style_console_confirm_button_dark)
            self.save_button.setIcon(QIcon("./image/Component/保存-1.png"))  # 替换为实际图标路径

        # 最小化按钮跟随主题颜色
        style_cfg = self.theme_styles[theme]
        self.min_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {style_cfg["min_btn_bg"]};
                color: #E0E0E0;
                border-radius: 3px;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {style_cfg["min_btn_hover"]}; }}
            QPushButton:pressed {{ background-color: {style_cfg["min_btn_press"]}; }}
        """)

        # help按钮做个简单的圆角背景，随主题淡一点
        self.help_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {style_cfg["button_bg"]};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {style_cfg["scroll_handle"]};
            }}
        """)

        self.load_history()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        print('控制台样式:', "深色" if self.dark_mode else "浅色",'切换成功')
        self.apply_theme()

    def save(self):
        content = self.browser.toPlainText()
        now_time_path = datetime.now().strftime("%Y%m%d.txt")
        with open(f'./temp/{now_time_path}','w', encoding = 'utf-8') as file:
            file.write(content)
        pyautogui.confirm(f"保存成功!\n/temp/{now_time_path}")

    def load_history(self):
        self.browser.clear()
        """加载所有历史记录"""
        for text, _ in self.stdout_stream.history:
            self.browser.append(text)
        for text, _ in self.stderr_stream.history:
            self.browser.append(f'<span style="color: red;">{text}</span>')

    def show_titlebar_menu(self, pos):
        # 创建右键菜单
        menu = QMenu(self)

        # 添加菜单动作
        minimize_action = QAction("最小化", self)
        minimize_action.triggered.connect(self.showMinimized)

        close_action = QAction("关闭", self)
        close_action.triggered.connect(self.close)

        # 添加主题切换动作
        theme_action = QAction("切换主题", self)
        theme_action.triggered.connect(self.toggle_theme)

        # 添加菜单项
        menu.addAction(minimize_action)
        menu.addSeparator()
        menu.addAction(theme_action)
        menu.addSeparator()
        menu.addAction(close_action)

        # 在鼠标位置显示菜单
        menu.exec_(self.title_bar.mapToGlobal(pos))

    def append_stdout(self, text, stream_type):
        color = self.theme_styles["dark" if self.dark_mode else "light"]["text_color"]
        self.browser.append(f'<span style="color: {color};">{text}</span>')

    def append_stderr(self, text, stream_type):
        color = self.theme_styles["dark" if self.dark_mode else "light"]["error_color"]
        self.browser.append(f'<span style="color: {color};">{text}</span>')

    def showEvent(self, event):
        self.lineEdit.setFocus()
        # 设置水平滚动条到最前
        virtical_scrollbar = self.browser.verticalScrollBar()
        virtical_scrollbar.setValue(0)
        # 设置水平滚动条到最前
        horizontal_scrollbar = self.browser.horizontalScrollBar()
        horizontal_scrollbar.setValue(0)

    # 添加窗口拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_pos') and event.buttons() == Qt.LeftButton:
            if self.title_bar.geometry().contains(event.pos()):
                self.move(event.globalPos() - self.drag_pos)
                event.accept()

    def handle_up_arrow(self):
        """上箭头：显示更旧的历史记录"""
        if not self.input_history:
            return

        # 保存当前未提交的输入
        if self.history_index == len(self.input_history):
            self.temporary_input = self.lineEdit.text()

        # 移动索引并设置文本
        if self.history_index > 0:
            self.history_index -= 1
            self.lineEdit.setText(self.input_history[self.history_index])

    def handle_down_arrow(self):
        """下箭头：显示更新的历史记录"""
        if not self.input_history:
            return

        if self.history_index < len(self.input_history) - 1:
            self.history_index += 1
            self.lineEdit.setText(self.input_history[self.history_index])
        elif self.history_index == len(self.input_history) - 1:
            # 恢复临时输入
            self.history_index += 1
            self.lineEdit.setText(self.temporary_input)
            self.temporary_input = ''

    def show_help(self):
        self.input_history.append('help')
        """按钮和输入help公用的帮助输出"""
        for index, (key_dic, value) in enumerate(self.list_function.items(), start=1):
            print(f"{index}. {key_dic} {value}")
        print('请输入数字或对应的名称以执行')

    def input_content(self):
        global sys_list, current_time_string, exp_status, temp_content, COLOR
        content = self.lineEdit.text()
        if len(self.input_history) > 0:
            if self.input_history[-1] == ('help' or '帮助'):
                if content.isdigit():
                    if int(content)<= len(self.list_function):
                        for i, key_dic in enumerate(self.list_function.keys(), 1):
                            if int(content) == i:
                                content = key_dic
                                break
        print(">>>", content)
        current_time_string = '[' + time.strftime("%H:%M:%S") + ']'
        self.lineEdit.setText("")
        # 保存非空内容到历史记录
        if content.strip():
            self.input_history.append(content)
            # 保持最多5条记录
            if len(self.input_history) > 5:
                self.input_history.pop(0)

        # 重置索引和临时存储
        self.history_index = len(self.input_history)
        self.temporary_input = ''
        self.browser.verticalScrollBar().setValue(
            self.browser.verticalScrollBar().maximum()
        )
        if content == '帮助' or content == 'help':
            self.show_help()
        elif content == '签到':
            TypedJSONClient('sign_in', 'None')
            try:
                result = socket_information.get(timeout=3)
                print(result)
                if type(result) == str:
                    print(result)
                else:
                    windows.set_variables({"exp": result[1]})
                    print(result[0] + ' 客户端经验值可能未更新 请重启客户端后重试')
            except:
                traceback.print_exc()
                print("签到失败:信息获取超时")
        elif content == '查询经验值':
            TypedJSONClient('query_exp', 'None')
            try:
                result = socket_information.get(timeout=3)
                print(result)
            except:
                traceback.print_exc()
        elif content[0:6] == 'random':
            contents = content.split()
            result = random.choice(contents[1:])
            print(result)
        elif content == '局域网传输工具':
            # 直接调用
            function.down_run_tool()
            print(r"此工具保存在C:\\Fuchen\\LocalSend文件夹中 如需重复使用可打开该文件夹运行")

        elif content == 'update weather':
            try:
                windows.Update_weather()
            except:
                traceback.print_exc()
        elif content == '点击测试':
            self.window = SundryUI.ClickSpeedTest()
            self.window.show()
        elif content == '更改颜色':
            dialog = ui.color_change.ColorPicker()
            if dialog.exec_() == QDialog.Accepted:
                colors = dialog.get_colors()

                # 设置 sidebar（左边区域）
                if colors["left_mode"] == "gradient":
                    if colors["left_direction"] == "horizontal":
                        direction = "x1:0, y1:0, x2:1, y2:0"
                    else:
                        direction = "x1:0, y1:0, x2:0, y2:1"

                    sidebar_style = f"""
                            background: qlineargradient({direction},
                                stop:0 {colors['left_start']}, stop:1 {colors['left_end']});
                            border-radius: 10px;
                            margin: 10px 5px 10px 10px;
                        """
                else:  # solid
                    sidebar_style = f"""
                            background-color: {colors['left_start']};
                            border-radius: 10px;
                            margin: 10px 5px 10px 10px;
                        """

                windows.sidebar.setStyleSheet(sidebar_style)

                # 设置 stack（右边区域）
                if colors["right_mode"] == "gradient":
                    if colors["right_direction"] == "horizontal":
                        direction = "x1:0, y1:0, x2:1, y2:0"
                    else:
                        direction = "x1:0, y1:0, x2:0, y2:1"

                    stack_style = f"""
                            QStackedWidget {{
                                background: qlineargradient({direction},
                                    stop:0 {colors['right_start']}, stop:1 {colors['right_end']});
                                border-radius: 15px;
                                margin: 10px 10px 10px 0;
                                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                            }}
                        """
                else:  # solid
                    stack_style = f"""
                            QStackedWidget {{
                                background-color: {colors['right_start']};
                                border-radius: 15px;
                                margin: 10px 10px 10px 0;
                                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                            }}
                        """

                windows.stack.setStyleSheet(stack_style)
                CONFIG_PATH = "config.json"
                if os.path.exists(CONFIG_PATH):
                    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                else:
                    cfg = {}

                    # 左侧
                if colors["left_mode"] == "gradient":
                    left_arr = [
                        "horizontal" if colors["left_direction"] == "horizontal" else "vertical",
                        colors["left_start"],
                        colors["left_end"],
                    ]
                else:
                    left_arr = [
                        "solid",
                        colors["left_start"],
                    ]
                cfg["left_color"] = left_arr

                # 右侧
                if colors["right_mode"] == "gradient":
                    right_arr = [
                        "horizontal" if colors["right_direction"] == "horizontal" else "vertical",
                        colors["right_start"],
                        colors["right_end"],
                    ]
                else:
                    right_arr = [
                        "solid",
                        colors["right_start"],
                    ]
                cfg["right_color"] = right_arr

                with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=4)

        elif content == 'runtime':
            currentTime = QtCore.QTime.currentTime()
            elapsedTime = windows.startTime.secsTo(currentTime)
            hours = elapsedTime // 3600
            minutes = (elapsedTime % 3600) // 60
            seconds = elapsedTime % 60
            print((f"运行时间 {hours:02d}:{minutes:02d}:{seconds:02d}"))
        elif content[0:4] == 'load':
            con = content.split()
            num = int(con[1])
            print(num)
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Fuchen Files (*.fc)",
                                                       options=options)
            if file_name:
                time.sleep(1)

                controller = function.WindowController()
                pyautogui.FAILSAFE = True

                try:
                    config = controller.load_config(file_name)
                    for i in range(config["settings"]["times"]):
                        for scenario in config["scenarios"]:
                            controller.execute_scenario(scenario)
                        print(f"✅ 执行成功")

                    print("✅ 所有场景执行完成")
                except Exception as e:
                    print(f"❌ 致命错误: {str(e)}")

        elif 'handle' in content.lower():
            x = int(content.split(' ')[1])
            y = int(content.split(' ')[2])
            windows.update_handle_value(x, y)
            print(f"发送位置修改成功{x} {y}")
        elif content == '经验值减少':
            send_encry("30005 xfbsomdfls", s, key, iv)
            try:
                exp = socket_information.get(timeout=3)
                print(exp)
            except:
                traceback.print_exc()
                print("经验值修改失败")
        elif content == 'error':
            try:
                raise ErrorString
            except:
                traceback.print_exc()
        elif content == 'XFBSOMDFLS114514':
            send_encry("experience_bonus xfbsomdfls114514", s, key, iv)
            try:
                exp = socket_information.get(timeout=3)
                print(exp)
            except:
                traceback.print_exc()
                print("经验值添加失败")


        elif content == 'android':
            print('')

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


