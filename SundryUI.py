import re
import struct
import subprocess
import sys
from PyQt5.QtCore import Qt, QRectF, QRect, QPropertyAnimation, QTimer, QSize, QParallelAnimationGroup, pyqtSignal, \
    QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QBrush, QPainterPath, QFont, QCursor, QLinearGradient, QPen
from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication, QLabel, QLineEdit, QTextEdit, QToolButton, \
    QMessageBox, QPushButton, QSystemTrayIcon, QAction, QMenu, QDialog, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect, \
    QMenuBar, QInputDialog
from PyQt5 import QtGui, QtWidgets, QtCore
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import function
import ui.style
import ui.buttons
from datetime import date
import pyautogui
from PIL import Image
import time
import json
from ctypes import cdll
from ctypes.wintypes import HWND
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

def send_json(sock, data):
    """发送JSON数据（带长度前缀）"""
    try:
        json_data = json.dumps(data).encode('utf-8')
        # 使用4字节网络字节序作为长度前缀
        header = struct.pack('>I', len(json_data))
        sock.sendall(header + json_data)
    except (TypeError, json.JSONEncodeError) as e:
        print(f"JSON编码失败: {e}")
    except BrokenPipeError:
        print("客户端连接已中断")
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


class ExpandingWindow(QWidget):
    def __init__(self):
        super().__init__(None)

        desktop = QApplication.desktop()
        rect = desktop.screenGeometry(desktop.primaryScreen())
        taskbar_height = rect.height() - desktop.availableGeometry().height()

        # 设置初始位置
        screen_geometry = desktop.screenGeometry()
        initial_geometry = QRect(screen_geometry.width() - 320,
                                 screen_geometry.height() - taskbar_height, 300, 0)
        self.setGeometry(initial_geometry)

        self.setWindowTitle("Fuchen")
        self.setWindowIcon(QIcon("./image/window.ico"))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        try:
            hWnd = HWND(int(self.winId()))
            cdll.LoadLibrary('./mod/dll/aeroDll.dll').setBlur(hWnd)
        except Exception as e:
            print("导入失败:", e)


        # 动画
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(750)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setStartValue(initial_geometry)

        final_geometry = QRect(screen_geometry.width() - 320,
                               screen_geometry.height() - 180 - taskbar_height, 300, 180)
        self.animation.setEndValue(final_geometry)

        self.opacity_animation = QPropertyAnimation(self, b'windowOpacity')
        self.opacity_animation.setDuration(750)
        self.opacity_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)

        self.animation_group = QParallelAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.opacity_animation)

        # 标题
        self.title_label = QLabel("提示", self)
        self.title_label.setGeometry(25, 10, 150, 30)
        self.title_label.setFont(QFont("微软雅黑", 10, QFont.Bold))
        self.title_label.setStyleSheet("color: #333;")

        # 关闭按钮
        self.Button_Close = ui.buttons.CloseButton(self)
        self.Button_Close.setGeometry(260, 15, 22, 22)
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QSize(20, 20))
        self.Button_Close.setObjectName("Button_Close")
        self.Button_Close.clicked.connect(self.close)

        # 主消息
        self.message_label = QLabel("Fuchen 已执行完毕", self)
        self.message_label.setGeometry(10, 50, 260, 40)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.message_label.setStyleSheet("color: #222;")

        # 倒计时标签
        self.remaining_time_label = QLabel("窗口将在 5 秒后自动关闭", self)
        self.remaining_time_label.setGeometry(10, 100, 260, 30)
        self.remaining_time_label.setAlignment(Qt.AlignCenter)
        self.remaining_time_label.setFont(QFont("微软雅黑", 11))
        self.remaining_time_label.setStyleSheet("color: #666;")

        # 定时器
        self.remaining_seconds = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRemainingTime)
        self.timer.start(1000)

    def showEvent(self, event):
        self.animation_group.start()

    def updateRemainingTime(self):
        self.remaining_seconds -= 1
        if self.remaining_seconds == 0:
            self.timer.stop()
            self.close()
        else:
            self.remaining_time_label.setText(f"窗口将在 {self.remaining_seconds} 秒后自动关闭")

    def paintEvent(self, event):
        shadow_radius = 10
        corner_radius = 6
        self.border_width = corner_radius

        # 绘制阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(100, 100, 100, 70)

        for i in range(shadow_radius):
            i_path = QPainterPath()
            i_path.setFillRule(Qt.WindingFill)

            offset = shadow_radius - i
            rect = QRectF(offset, offset, self.width() - offset * 2, self.height() - offset * 2)
            i_path.addRoundedRect(rect, corner_radius, corner_radius)

            color.setAlpha(int(150 - i ** 0.5 * 50))
            painter.setPen(color)
            painter.drawPath(i_path)

        # 绘制白色背景 + 圆角主体
        pat2 = QPainter(self)
        pat2.setRenderHint(QPainter.Antialiasing)
        pat2.setBrush(QColor(255, 255, 255, 170))  # 白色 + 半透明，范围 0~255

        pat2.setPen(Qt.NoPen)

        rect = self.rect().adjusted(5, 5, -5, -5)
        pat2.drawRoundedRect(rect, corner_radius, corner_radius)

class View(QWidget):
    def __init__(self, lis):
        super().__init__()
        global windows, s
        windows = lis[0]
        s = lis[1]
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
        contact = self.lineEdit.text()
        if contact == '':
            QMessageBox.question(self, "提示", "联系方式不能为空")
        elif self.textEdit.toPlainText() == '':
            QMessageBox.question(self, "提示", "反馈内容不能为空")
        elif len(self.textEdit.toPlainText()) > 400:
            QMessageBox.question(self, "提示", "反馈内容过多!")
        else:
            view = self.textEdit.toPlainText()
            view = re.sub(' ', '~~space~~', view)
            view = re.sub('\n', '~~next~~', view)
            TypedJSONClient("view",{"contact": contact, 'information': view})
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
        action6.triggered.connect(windows.close)

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


class ClickSpeedTest(QWidget):
    def __init__(self):
        super().__init__()
        self.test_duration = 10  # 默认测试时间改为10秒
        self.initUI()
        self.remaining_time = self.test_duration
        self.click_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def initUI(self):
        self.setWindowTitle('点击速度测试')
        layout = QVBoxLayout()

        # 创建菜单栏并添加到布局
        menubar = QMenuBar(self)
        settings_menu = menubar.addMenu('设置')
        time_action = settings_menu.addAction('测试时间')
        time_action.triggered.connect(self.open_settings_dialog)

        # 添加菜单栏到布局
        layout.setMenuBar(menubar)  # 这是关键修改

        self.start_btn = QPushButton('开始测试', self)
        self.reset_btn = QPushButton('重置', self)
        self.time_label = QLabel(f'剩余时间：{self.test_duration}秒', self)
        self.count_label = QLabel('点击次数：0', self)
        self.result_label = QLabel('点击速度：0.00次/秒', self)

        self.reset_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_test)
        self.reset_btn.clicked.connect(self.reset_test)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.time_label)
        layout.addWidget(self.count_label)
        layout.addWidget(self.result_label)

        # 添加一些间距
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(layout)
        self.resize(300, 200)

    def open_settings_dialog(self):
        new_time, ok = QInputDialog.getInt(
            self,
            '设置测试时间',
            '输入测试时间（秒）:',
            self.test_duration,  # 默认值
            1,  # 最小值
            3600,  # 最大值
            1  # 步长
        )
        if ok:
            self.test_duration = new_time
            # 如果测试没有进行，更新显示
            if not self.timer.isActive():
                self.remaining_time = self.test_duration
                self.time_label.setText(f'剩余时间：{self.remaining_time}秒')

    def start_test(self):
        # 断开旧连接防止重复计数
        try:
            self.start_btn.clicked.disconnect()
        except TypeError:
            pass

        self.start_btn.clicked.connect(self.increment_count)
        self.remaining_time = self.test_duration
        self.click_count = 0
        self.start_btn.setText('点击这里')
        self.reset_btn.setEnabled(True)
        self.timer.start(1000)

        # 初始化显示
        self.time_label.setText(f'剩余时间：{self.remaining_time}秒')
        self.count_label.setText('点击次数：0')
        self.result_label.setText('点击速度：0.00次/秒')

    def update_timer(self):
        self.remaining_time -= 1
        self.time_label.setText(f'剩余时间：{self.remaining_time}秒')

        if self.remaining_time <= 0:
            self.timer.stop()
            self.start_btn.setEnabled(False)
            # 最终速度计算
            speed = self.click_count / self.test_duration
            self.result_label.setText(f'最终速度：{speed:.2f}次/秒')

    def increment_count(self):
        if self.remaining_time > 0:
            self.click_count += 1
            self.count_label.setText(f'点击次数：{self.click_count}')

            # 实时速度计算
            elapsed_time = self.test_duration - self.remaining_time
            if elapsed_time > 0:
                speed = self.click_count / elapsed_time
            else:
                speed = 0.0
            self.result_label.setText(f'实时速度：{speed:.2f}次/秒')

    def reset_test(self):
        self.timer.stop()
        self.remaining_time = self.test_duration
        self.click_count = 0

        # 恢复按钮初始状态
        self.start_btn.clicked.disconnect()
        self.start_btn.clicked.connect(self.start_test)
        self.start_btn.setText('开始测试')
        self.start_btn.setEnabled(True)
        self.reset_btn.setEnabled(False)

        # 重置显示
        self.time_label.setText(f'剩余时间：{self.test_duration}秒')
        self.count_label.setText('点击次数：0')
        self.result_label.setText('点击速度：0.00次/秒')

class KeyDetector(QDialog):
    keycode_selected = pyqtSignal(str, int)  # 修改信号为发送两个参数

    def __init__(self):
        super().__init__()
        self.setWindowTitle("键盘/鼠标自定义按键设置")
        self.setFixedSize(600, 250)
        self.current_keycode = None
        self.inverted_dict = {v: k for k, v in function.keycode_dict.items()}

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 提示标签
        self.instruction_label = QLabel("请设置按键 目前只支持同时检测一个按键")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
            }
        """)

        # 按键显示标签
        self.detected_label = QLabel("请按下任意键...")
        self.detected_label.setAlignment(Qt.AlignCenter)
        self.detected_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #FFFFFF;
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.detected_label.setMinimumHeight(100)

        # 确认按钮布局
        btn_layout = QHBoxLayout()
        self.btn_confirm = QPushButton("确认")
        self.btn_confirm.setFixedHeight(40)
        self.btn_confirm.clicked.connect(self.confirm)
        self.btn_confirm.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #27ae60;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)
        btn_layout.addWidget(self.btn_confirm)

        # 添加部件到主布局
        main_layout.addWidget(self.instruction_label)
        main_layout.addWidget(self.detected_label)
        main_layout.addLayout(btn_layout)

    def keyPressEvent(self, event):
        key = event.nativeVirtualKey()
        self.current_keycode = key
        self.update_display(key)

    def mousePressEvent(self, event):
        btn = event.button()
        self.current_keycode = btn
        self.update_display(btn)

    def update_display(self, keycode):
        if keycode != 1:
            name = self.inverted_dict.get(keycode, f"未知按键: {keycode}")
            self.detected_label.setText(f"{name}\n({keycode})")

    def confirm(self):
        if self.current_keycode is not None:
            # 获取按键名称
            name = self.inverted_dict.get(
                self.current_keycode,
                f"未知按键: {self.current_keycode}"
            )
            # 同时发送名称和键码
            self.keycode_selected.emit(name, self.current_keycode)
            self.accept()
        else:
            self.reject()


'''
if __name__ == "__main__":
    app = QApplication([])
    dialog = ExpandingWindow()
    dialog.show()
    app.exec_()'''