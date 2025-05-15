import ctypes
import json
import os
import sys
import webbrowser
from ctypes import wintypes
from datetime import datetime
import shutil
import threading
import psutil
import requests
from PyQt5 import QtCore, QtGui, sip
from PyQt5.QtCore import Qt, QPoint, QSize, QLine, QObject, pyqtSignal, QTimer, QRect, QUrl
from PyQt5.QtGui import QFont, QColor, QPixmap, QMouseEvent, QIcon, QPainterPath, QRegion, QKeySequence, QCursor, \
    QPainter, QRadialGradient, QDesktopServices
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from pynput import mouse
import win32gui
import win32con
import ast
import extend_install
import ui.buttons
import ui.style
import ui.console_window
import keyboard
import pyautogui
import subprocess
import random


style_font_Yahei = ui.style.style_font_Yahei
style_Radio_Small = ui.style.style_Radio_Small
style_lineEdit = ui.style.style_lineEdit
style_Radio = ui.style.style_Radio
style_Double = ui.style.style_Double
style_Spin = ui.style.style_Spin
style_CheckBox = ui.style.style_CheckBox
style_white_blue_button = ui.style.style_white_blue_button
style_white_blue_toolbutton = ui.style.style_white_blue_toolbutton
style_font_10 = ui.style.style_font_10
style_font_9 = ui.style.style_font_9
style_font_11 = ui.style.style_font_11
style_font_12 = ui.style.style_font_12
style_font_black_10 = ui.style.style_font_black_10
s = None
avatar_load_status = False
position_status = None
Name = None
Account = None
send_position = None
textedit_position = None
mode = 'login'
Version = 'V1.0.0'
information = '正在加载'

class MouseSignals(QObject):
    right_click = pyqtSignal()

class ScreenMask(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        # 初始化鼠标监听信号
        self.signals = MouseSignals()
        self.signals.right_click.connect(self.on_right_click)

        # 创建鼠标监听线程
        self.listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_thread = threading.Thread(target=self.listener.start)
        self.mouse_thread.daemon = True
        self.mouse_thread.start()

        font = QFont()
        font.setFamily("等线")
        font.setPointSize(11)

        self.label = QLabel(self)
        self.label.setStyleSheet("color: white; font-size: 16px; background: rgba(0,0,0,0.5);")
        self.label.resize(200, 40)
        self.label.setFont(font)
        self.label.hide()

        self.target_rect = None
        # 在类中新增缓存变量
        self.last_hwnd = None
        self.cached_title = ""

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_coordinates)
        self.timer.start(35)

    def on_mouse_click(self, x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            self.signals.right_click.emit()

    def on_right_click(self):
        self.close()
        #QApplication.instance().quit()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(100, 100, 100, 150))

        if self.target_rect:
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(self.target_rect, Qt.transparent)

    def update_coordinates(self):
        try:
            screen_pos = QCursor.pos()
            # 获取当前鼠标所在屏幕的几何信息
            current_screen = QApplication.screenAt(screen_pos)
            if current_screen:
                screen_rect = current_screen.geometry()
            else:
                screen_rect = QApplication.primaryScreen().geometry()

            hwnd = win32gui.WindowFromPoint((screen_pos.x(), screen_pos.y()))

            if hwnd:
                window_rect = win32gui.GetWindowRect(hwnd)
                rect = (window_rect[0], window_rect[1], window_rect[2], window_rect[3])

                # 新增：获取窗口标题
                try:
                    window_title = win32gui.GetWindowText(hwnd)
                except:
                    window_title = "未知标题"

                try:
                    point = win32gui.ScreenToClient(hwnd, (screen_pos.x(), screen_pos.y()))
                    rel_x, rel_y = point
                except:
                    rel_x = screen_pos.x() - rect[0]
                    rel_y = screen_pos.y() - rect[1]

                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                if width > 0 and height > 0:
                    self.target_rect = QRect(rect[0], rect[1], width, height)
                    # 修改标签文本显示标题
                    self.label.setText(
                        f"句柄: {hwnd}\n"
                        f"标题: {window_title}\n"  # 新增标题显示
                        f"坐标: ({rel_x}, {rel_y})")

                    # 调整标签尺寸以适应更多行
                    self.label.resize(200, 60)  # 增加高度

                    # 计算标签的理想位置
                    label_width = self.label.width()
                    label_height = self.label.height()
                    x = screen_pos.x() + 15
                    y = screen_pos.y() + 15

                    # 水平方向调整
                    if x + label_width > screen_rect.right():
                        x = screen_pos.x() - label_width - 15

                    # 垂直方向调整
                    if y + label_height > screen_rect.bottom():
                        y = screen_pos.y() - label_height - 15

                    self.label.move(x, y)
                    self.label.show()
                else:
                    self.target_rect = None
                    self.label.hide()
            else:
                self.target_rect = None
                self.label.hide()
        except Exception as e:
            print(f"坐标更新错误: {e}")
            self.target_rect = None
            self.label.hide()

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:  # 右键退出
            QApplication.instance().quit()

    def closeEvent(self, event):
        self.listener.stop()
        event.accept()

class CustomLineEdit(QLineEdit):  # 网易云链接解析输入框
    def __init__(self, ui_form_instance, parent=None):
        super().__init__(parent)
        self.ui_form_instance = ui_form_instance  # 保存传入的已初始化的 Ui_FormS 实例

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Paste):
            clipboard = QApplication.clipboard()
            url = clipboard.text()
            if '/#/' in url:
                url = url.replace('/#/', '/')
            if url.startswith('https://music.163.com/song?id'):
                try:
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
                    res = requests.get(url, headers=header)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    keywords_tag = soup.find('meta', {'name': 'keywords'})
                    keywords_content = keywords_tag['content'] if keywords_tag else None
                    if keywords_content:
                        first_content = keywords_content.split('，')[0]
                        # 使用已初始化的实例设置文本
                        self.ui_form_instance.music_filename.setText(first_content + ".mp3")
                except Exception as e:
                    print(e)
        super().keyPressEvent(event)

class OperationGroup(QGroupBox):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QGroupBox {
                background: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #C0C0C0;
                border-radius: 4px;
                padding: 4px;
                min-height: 28px;
                background: white;
            }
            QComboBox::drop-down {
                width: 24px;
                border-left: 1px solid #C0C0C0;
            }
            /* 关键修复部分 */
            QComboBox QAbstractItemView {
                background: white !important;    /* 强制背景白 */
                color: black !important;         /* 强制文字黑 */
                border: 1px solid #C0C0C0;
                outline: 0;                       /* 去除选中虚线框 */
                selection-background-color: #E0E0E0;
            }
            /* 修复下拉项高度和边距 */
            QComboBox QAbstractItemView::item {
                min-height: 28px;
                padding: 4px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 句柄输入
        self.edit_handle = QLineEdit()
        self.edit_handle.setPlaceholderText("窗口句柄")

        # 操作选择
        self.combo_action = QComboBox()
        self.combo_action.addItems(["点击", "右键", "粘贴", "按键", "回车", "等待"])


        # 参数输入
        self.edit_param = QLineEdit()
        self.edit_param.setPlaceholderText("参数（可选）")

        # 删除按钮
        self.btn_remove = QPushButton("❌")
        self.btn_remove.setStyleSheet("""
            QPushButton {
                background: #FF6666;
                border-radius: 4px;
                min-width: 24px;
                max-width: 24px;
                color: white;
            }
            QPushButton:hover { background: #FF4444; }
        """)

        # 布局组件
        layout.addWidget(QLabel("句柄:"))
        layout.addWidget(self.edit_handle)
        layout.addWidget(QLabel("操作:"))
        layout.addWidget(self.combo_action)
        layout.addWidget(QLabel("参数:"))
        layout.addWidget(self.edit_param)
        layout.addWidget(self.btn_remove)

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(35)
        self.mouse_pos = QPoint(0, 0)
        # 关键修复步骤 1：设置对象名称用于样式表定位
        self.setObjectName("CustomTitleBar")

        # 关键修复步骤 2：启用样式表背景绘制
        self.setAttribute(Qt.WA_StyledBackground, True)  # 必须启用！
        self.status = True
        '''self.setStyleSheet("""
            #CustomTitleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #b3e5fc,  /* 标题栏主色 */
            stop:0.8 #fafafa); /* 向右侧过渡 */
                border-radius: 0px;  /* 可选：圆角 */
                border-bottom: 1px solid #cdcdcd;  /* 替代分割线 */
            }
            /* 强制子组件透明 */
            QLabel, QPushButton {
                background-color: transparent;
            }
        """)'''
        self.setStyleSheet("""
                    #CustomTitleBar {
                        background: qlineargradient(
                            x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 rgba(210, 210, 210, 140),
                            stop: 1 rgba(255, 255, 255, 140)
                        );
                        border-radius: 0px;  /* 可选：圆角 */
                        border-bottom: 1px solid #cdcdcd;  /* 替代分割线 */
                    }
                    /* 强制子组件透明 */
                    QLabel, QPushButton {
                        background-color: transparent;
                    }
                """)

        self.setup_ui()
        self.create_context_menu()

    def setup_ui(self):
        # 主布局改为垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 0, 0, 0)  # 清除主布局的边距
        main_layout.setSpacing(0)  # 清除子组件间距
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)



        # 标题图标和文字
        self.icon = QLabel()
        self.icon.setPixmap(QPixmap(r"C:\Users\13224\Desktop\项目\image\fc 斜体.png").scaled(24, 24))  # 准备图标文件
        font= QFont()
        font.setPointSize(11)
        font.setItalic(True)
        font.setFamily('等线')
        self.title = QLabel(f" Fuchen - {Version}")
        self.title.setFont(font)
        self.title.setStyleSheet("color: #555555; font-size: 14px;font-family:等线;")
        # 或者给标题增加上方边距
        self.title.setContentsMargins(0, 3, 0, 0)



        self.Button_More = ui.buttons.ComponentButton()
        self.Button_More.setToolTip('更多')
        self.Button_More.setObjectName("Button_More")
        self.Button_More.setIcon(QIcon("./image/same/更多2.png"))
        self.Button_More.setIconSize(QtCore.QSize(21, 21))
        self.Button_More.setStyleSheet("""
                    QToolButton {
                        border: none;
                        padding: 1px;
                    }
                    QToolButton::menu-indicator {
                        width: 0px;
                        height: 0px;
                    }
                """)

        # 创建一个菜单
        self.menu = QMenu()

        '''self.action_option1 = self.menu.addAction(QIcon("./image/page_menu/setting.png"), "设置")
        self.action_option1.setFont(style_font_black_10)'''
        self.action_option2 = self.menu.addAction(QIcon("./image/page_menu/about.png"), "关于")
        self.action_option2.setFont(style_font_black_10)
        self.action_option3 = self.menu.addAction(QIcon("./image/page_menu/help.png"), "赞助")
        self.action_option3.setFont(style_font_black_10)
        self.action_option4 = self.menu.addAction(QIcon("./image/page_menu/log.png"), "日志")
        self.action_option4.setFont(style_font_black_10)
        self.action_option5 = self.menu.addAction(QIcon("./image/page_menu/web.png"), "官网")
        self.action_option5.setFont(style_font_black_10)
        self.action_option6 = self.menu.addAction("意见反馈")
        self.action_option6.setFont(style_font_black_10)
        self.action_option7 = self.menu.addAction("清空日志")
        self.action_option7.setFont(style_font_black_10)
        self.action_option8 = self.menu.addAction("清理缓存")
        self.action_option8.setFont(style_font_black_10)
        self.action_option9 = self.menu.addAction("重启软件")
        self.action_option9.setFont(style_font_black_10)
        self.action_option10 = self.menu.addAction("使用帮助")
        self.action_option10.setFont(style_font_black_10)

        self.separate_label = QLabel("|")
        font = QFont()
        font.setPointSize(13)
        font.setWeight(QFont.Thin)  # 或 QFont.Light
        self.separate_label.setFont(font)

        self.Button_More.setMenu(self.menu)
        self.Button_More.setPopupMode(QToolButton.InstantPopup)

        self.Button_SetTop = ui.buttons.ComponentButton()
        self.Button_SetTop.setToolTip('置顶')
        self.Button_SetTop.setObjectName("Button_SetTop")
        self.Button_SetTop.setIcon(QIcon("./image/Component/Top.png"))
        self.Button_SetTop.setIconSize(QtCore.QSize(21, 21))

        self.Button_Minisize = ui.buttons.ComponentButton()
        self.Button_Minisize.setIcon(QIcon("./image/short.png"))
        self.Button_Minisize.setIconSize(QtCore.QSize(19, 19))
        self.Button_Minisize.setObjectName("Button_Minisize")
        self.Button_Minisize.setToolTip('最小化')

        self.Button_Close = ui.buttons.CloseButton()
        self.Button_Close.setToolTip('关闭')
        self.Button_Close.setIcon(QIcon("./image/quit.png"))
        self.Button_Close.setIconSize(QtCore.QSize(24, 24))
        self.Button_Close.setFixedSize(24,24)
        self.Button_Close.setObjectName("Button_Close")

        # 添加到布局
        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addSpacing(5)
        #layout.addWidget(self.separate_label)
        layout.addSpacing(5)
        layout.addWidget(self.Button_More)
        layout.addSpacing(8)

        layout.addWidget(self.Button_SetTop)
        layout.addSpacing(8)
        layout.addWidget(self.Button_Minisize)
        layout.addSpacing(8)
        layout.addWidget(self.Button_Close)

        # 将水平布局添加到主布局
        main_layout.addLayout(layout)

        # 按钮信号连接
        self.Button_Minisize.clicked.connect(self.window().showMinimized)
        #self.Button_Close.clicked.connect(self.window().close)




    def create_context_menu(self):
        self.context_menu = QMenu(self)
        self.context_menu.setStyleSheet("""
        QMenu {
            background-color: #FFFFFF;
            border: 1px solid #CCCCCC;
            padding: 6px;
            border-radius: 4px;
        }
        QMenu::item {
            padding: 6px 24px;
            color: #333333;
            font-family: '等线';
            font-size: 13px;
        }
        QMenu::item:selected {
            background-color: #F0F0F0;
        }
        QMenu::separator {
            height: 1px;
            background: #EEEEEE;
            margin: 4px 8px;
        }
    """)

        # 添加菜单项
        minimize_action = QAction("最小化", self)
        minimize_action.triggered.connect(self.window().showMinimized)

        close_action = QAction("关闭", self)
        close_action.triggered.connect(self.window().close)

        other_action = QAction("其他", self)
        other_action.triggered.connect(self.show_other_options)

        self.context_menu.addAction(minimize_action)
        self.context_menu.addAction(close_action)
        self.context_menu.addSeparator()
        self.context_menu.addAction(other_action)

    def show_other_options(self):
        # 实现其他功能
        pass
    def toggle_maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        self.mouse_pos = event.globalPos()
        if event.button() == Qt.RightButton:
            self.context_menu.exec_(self.mapToGlobal(event.pos()))

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.window().isMaximized():
            return
        delta = QPoint(event.globalPos() - self.mouse_pos)
        self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
        self.mouse_pos = event.globalPos()

class UserWidget(QGroupBox):
    def __init__(self, name, user_id, avatar_path):
        super().__init__()
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #EEEEEE;
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
            }
        """)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # 头像区域（添加固定尺寸确保对齐）
        self.avatar_frame = QLabel()
        self.avatar_user_team = QPixmap(avatar_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.avatar_frame.setPixmap(self.avatar_user_team)
        self.avatar_frame.setFixedSize(100, 100)  # 固定头像框尺寸
        layout.addWidget(self.avatar_frame)

        # 用户信息（添加间距和垂直居中）
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(10, 0, 0, 0)  # 左侧留出间距
        info_layout.setAlignment(Qt.AlignVCenter)   # 垂直居中

        self.lbl_name = QLabel(name)
        self.lbl_name.setStyleSheet("font: bold 16px 'Microsoft YaHei'; color: #212121;")
        self.lbl_id = QLabel(f"ID: {user_id}")  # 添加ID前缀更清晰
        self.lbl_id.setStyleSheet("font: 12px 'Microsoft YaHei'; color: #757575;")

        info_layout.addWidget(self.lbl_name)
        info_layout.addWidget(self.lbl_id)
        layout.addLayout(info_layout)

        # 其他保持不变...
        # 选项区域
        self.combo_options = QComboBox()
        self.combo_options.addItems(["句柄式发送消息", "@指定用户", "复制消息发送", "QQ个人信息更新", "执行自动脚本"])
        self.combo_options.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #E0E0E0;
                border-radius: 6px;
                min-width: 120px;
                font: 14px 'Microsoft YaHei';
            }
            QComboBox::drop-down {
                width: 20px;
            }
        """)
        layout.addStretch()
        layout.addWidget(self.combo_options)

        self.setLayout(layout)
    def get_selection(self):
        return self.combo_options.currentText()

class FileNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("创建配置文件")
        self.setFixedSize(400, 160)

        icon = QIcon("./image/Component/新建.png")  # 设置窗口图标
        self.setWindowIcon(icon)

        self.default_name = self.generate_default_filename()
        self.init_ui()
        self.set_style()

    def set_style(self):
        """设置子窗口样式"""
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border-radius: 8px;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
                padding: 4px;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
                padding: 4px;
            }
            QPushButton {
                min-width: 80px;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton#confirm {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#confirm:hover {
                background-color: #45a049;
            }
            QPushButton#cancel {
                background-color: #f44336;
                color: white;
            }
            QPushButton#cancel:hover {
                background-color: #da190b;
            }
        """)

    def generate_default_filename(self):
        """生成默认文件名"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        directory = "./scripts/"

        # 确保目录存在
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 查找已有文件
        files = [f for f in os.listdir(directory)
                 if f.startswith(date_str) and f.endswith(".txt")]

        # 找出最大序号
        max_number = 0
        for file in files:
            parts = file.replace(".txt", "").split("-")
            if len(parts) == 4:  # 格式为年-月-日-编号
                try:
                    number = int(parts[3])
                    max_number = max(max_number, number)
                except ValueError:
                    continue

        return f"{date_str}-{max_number + 1:02d}.txt"

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 输入框
        self.label = QLabel("文件名:")
        style_font_Yahei = QtGui.QFont()
        style_font_Yahei.setFamily("微软雅黑")
        self.label.setFont(style_font_Yahei)
        self.input = QLineEdit()
        self.input.setText(self.default_name)
        self.input.setFont(style_font_Yahei)

        # 按钮布局
        btn_layout = QHBoxLayout()
        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.setObjectName("confirm")
        self.confirm_btn.setFont(style_font_Yahei)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.setFont(style_font_Yahei)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.confirm_btn)

        # 组合布局
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addLayout(btn_layout)

        # 信号连接
        self.confirm_btn.clicked.connect(self.create_file)
        self.cancel_btn.clicked.connect(self.reject)

        self.setLayout(layout)

    def create_file(self):
        """创建文件"""
        filename = self.input.text().strip()
        if not filename:
            QMessageBox.warning(self, "警告", "文件名不能为空！")
            return

        directory = "./scripts/"
        filepath = os.path.join(directory, filename)

        try:
            # 再次确保目录存在
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 创建文件
            with open(filepath, "w") as f:
                pass  # 创建空文件

            self.accept()  # 关闭对话框
            QMessageBox.information(self, "成功", f"文件 {filename} 已创建！")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建文件失败: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏原生标题栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        #self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000,640)


        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()

        # 计算窗口居中时的位置
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        # 设置窗口位置
        self.move(x, y)

        self.record_hotkey = None
        self.execute_hotkey = None
        self.sort = "F8"
        self.end_key = "ESC"
        self.end_execute_key = "ESC"
        self.pressed_keys = set()
        self.recorded_keys = set()
        self.record_key_status = False
        self.execute_key_status = False

        # 创建遮罩层
        self.mask = QWidget()
        self.mask.setStyleSheet("background-color: rgba(0,0,0,150);")
        self.mask.hide()

        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #F5F6FA;
                    }
                """)

        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(30)  # 阴影模糊程度
        shadow_effect.setOffset(0, 0)  # 阴影偏移，0表示四周都有
        shadow_effect.setColor(QColor(0, 0, 0, 150))  # 阴影颜色

        # 主 widget（原 main_widget）
        main_widget = QWidget()
        main_widget.setStyleSheet("""
                    background-color: #F5F6FA;
                    border-radius: 15px;
                """)
        #main_widget.setGraphicsEffect(shadow_effect)  # 应用阴影

        # 添加自定义标题栏
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)

        # 内容区域
        content_widget = QWidget()
        self.main_layout.addWidget(content_widget)
        self.content_layout = QHBoxLayout(content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(5)  # 子控件间

        # 初始化侧边栏和内容区
        self.init_sidebar()
        self.init_content_area()

        self.choose_music.clicked.connect(lambda: self.select_file_path('download_music'))
        self.QQ_Seq_file_button.clicked.connect(lambda: self.select_file_path('qq_send_seq'))

    def init_sidebar(self):
        # 侧边栏初始化（使用绝对布局）
        self.sidebar = QWidget()  # 改用QWidget更轻量
        self.sidebar.setFixedWidth(240)
        self.sidebar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #6ec7ff, stop:1 #7cb9e8);
            border-radius: 10px;
            margin: 10px 5px 10px 10px;
        """)


        # ===== 用户信息区域 =====
        # 头像
        self.avatar = QToolButton(self.sidebar)
        global avatar_load_status
        if avatar_load_status == True:  # 判断头像是否成功加载
            self.avatar.setIcon(QIcon("./temp/avatar.png"))
        else:
            self.avatar.setIcon(QIcon("./image/float/fc.png"))
        self.avatar.setGeometry(40, 45, 90, 90)
        # 设置图标大小与按钮大小一致
        self.avatar.setCursor(QCursor(Qt.PointingHandCursor))
        self.avatar.setIconSize(QSize(90, 90))  # 与按钮大小相同
        self.avatar.setStyleSheet("""
                        border-radius: 3px;
                        border: 2px solid rgba(255,255,255,0.9);
                        background: rgba(255,255,255,0.1);
                        padding: 0px;  /* 移除内边距 */
                        margin: 0px;   /* 移除外边距 */""")

        # 用户名（居中下方）
        self.username = QPushButton(str(Name), self.sidebar)
        self.username.setGeometry(25, 130, 200, 50)
        self.username.setCursor(QCursor(Qt.PointingHandCursor))
        self.username.setStyleSheet("""
            color: #FFFFFF;
            font: bold 24px 'Microsoft YaHei';
            letter-spacing: 1px;
            text-align: left;    /* 水平左对齐 */
            padding-left: 2px;  /* 左侧留出间距 */""")

        # 邮箱（更精致的样式）
        self.userid = QPushButton(f"id: {Account}", self.sidebar)
        self.userid.setGeometry(30, 170, 150, 30)
        self.userid.setCursor(QCursor(Qt.PointingHandCursor))
        self.userid.setStyleSheet("""
            color: rgba(255,255,255,0.85);
            background-color: transparent;
            font: 12px 'Microsoft YaHei';
            letter-spacing: 0.5px;
            text-align: left;    /* 水平左对齐 */
            padding-left: 2px;  /* 左侧留出间距 */
        """)

        # ===== 天气标签 =====
        self.weather_label = QLabel("正在获取天气...", self.sidebar)
        self.weather_label.setGeometry(10, 550, 220, 40)
        self.weather_label.setStyleSheet("""
            QLabel {
                background: rgba(255,255,255,0.15);
                color: white;
                font: 500 13px 'Microsoft YaHei'; 
                border-radius: 8px;
                qproperty-alignment: AlignCenter;
                border: 1px solid rgba(255,255,255,0.25);
            }
        """)
        # 添加微光效果
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(10)
        glow_effect.setOffset(0)
        glow_effect.setColor(QColor(255, 255, 255, 50))
        #self.weather_label.setGraphicsEffect(glow_effect)

        # ===== 导航按钮 =====
        nav_items = [
            ("🖱️  点击功能", 0),
            ("📨 消息发送", 1),
            ("👥 组队功能", 2),
            ("🛠️ 常用工具", 3),
            ("⚙️ 系统设置", 4)
        ]
        COMMON_STYLE = """
            QPushButton {
                color: rgba(255,255,255,0.9);
                font: 15px '等线';
                text-align: left;
                padding-left: 20px;
                border-radius: 8px;
                background: transparent;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.15);
            }
            QPushButton:checked {
                background: rgba(255,255,255,0.2);
                border-left: 3px solid #2196f3;
            }
        """


        self.button_group = QButtonGroup()

        # 创建第一个按钮（默认选中）
        self.button_1 = QPushButton(nav_items[0][0], self.sidebar)
        self.button_1.setGeometry(10, 220, 220, 50)
        self.button_1.setCheckable(True)
        self.button_1.setChecked(True)  # 设置默认选中
        self.button_1.clicked.connect(lambda: self.switch_page(0))
        self.button_group.addButton(self.button_1)

        # 创建第二个按钮
        self.button_2 = QPushButton("📨 消息发送", self.sidebar)
        self.button_2.setGeometry(10, 265, 220, 50)  # Y坐标递增45
        self.button_2.setCheckable(True)
        # 应用给所有按钮
        self.button_1.setStyleSheet(COMMON_STYLE)
        self.button_2.setStyleSheet(COMMON_STYLE)
        self.button_2.clicked.connect(lambda: self.switch_page(1))
        self.button_group.addButton(self.button_2)

        # 创建第三个按钮（后续按钮样式可复用）
        self.button_3 = QPushButton("👥 组队功能", self.sidebar)
        self.button_3.setGeometry(10, 310, 220, 50)
        self.button_3.setCheckable(True)
        self.button_3.setStyleSheet(self.button_2.styleSheet())
        self.button_3.clicked.connect(lambda: self.switch_page(2))
        self.button_group.addButton(self.button_3)

        # 创建第四个按钮
        self.button_4 = QPushButton("🛠️ 常用工具", self.sidebar)
        self.button_4.setGeometry(10, 355, 220, 50)
        self.button_4.setCheckable(True)
        self.button_4.setStyleSheet(self.button_2.styleSheet())
        self.button_4.clicked.connect(lambda: self.switch_page(3))
        self.button_group.addButton(self.button_4)

        # 创建第五个按钮
        self.button_5 = QPushButton("⚙️ 系统设置", self.sidebar)
        self.button_5.setGeometry(10, 400, 220, 50)
        self.button_5.setCheckable(True)
        self.button_5.setStyleSheet(self.button_2.styleSheet())
        self.button_5.clicked.connect(lambda: self.switch_page(4))
        self.button_group.addButton(self.button_5)

        self.slabel = QLabel(self.sidebar)
        self.slabel.setGeometry(self.button_1.pos().x(),self.button_1.pos().y(),220,50)
        self.slabel.setObjectName("slabel")
        self.slabel.setStyleSheet("background-color: rgba(255,255,255,0.2); border-radius: 8px;")
        self.slabel.lower()
        self.animation = QtCore.QPropertyAnimation(self.slabel, b"pos")
        # 添加装饰元素
        self.add_sidebar_decorations()


        # ===== 公告区域 =====
        self.notice_browser = QTextBrowser(self.sidebar)
        self.notice_browser.setGeometry(10, 460, 220, 80)  # 位于导航按钮下方，天气上方
        self.notice_browser.setStyleSheet("""
                    QTextBrowser {
                        background: rgba(255,255,255,0.1);
                        border: 1px solid rgba(255,255,255,0.2);
                        border-radius: 8px;
                        color: rgba(255,255,255,0.9);
                        font: 12px 'Microsoft YaHei';
                        padding: 6px 6px;
                        line-height: 1.3;
                    }
                """)


        # 示例公告内容（支持HTML格式）
        self.notice_browser.setHtml("""
                    <p style='color: rgba(255,255,255,0.95); margin:2px;'>
                        <b>📢 系统公告</b><br/>
                        · 服务器维护通知：1月1日 02:00-04:00<br/>
                        · 新增功能<br/>
                        · 修复问题<br/>
                        <span style='color: #ffdd55;'>[详情]</span>
                    </p>
                """)
        self.notice_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直滚动条
        # 启用链接交互功能
        self.notice_browser.setOpenExternalLinks(False)  # 禁用自动跳转，由我们自己处理
        # 修改信号连接方式（替换原来的连接方式）
        self.notice_browser.anchorClicked.connect(lambda link: self.open_notice_link(link))


        self.content_layout.addWidget(self.sidebar)

    def connect_handle(self):
        pass
    # 在类中添加处理方法
    def open_notice_link(self, link):
        current_html = self.notice_browser.toHtml()
        QDesktopServices.openUrl(QUrl(link.toString()))
        # 还原内容（防止被清空）
        self.notice_browser.setHtml(current_html)

    def add_sidebar_decorations(self):
        # 顶部装饰线
        top_line = QLabel(self.sidebar)
        top_line.setGeometry(20, 0, 200, 1)
        top_line.setStyleSheet("background: rgba(255,255,255,0.2);")

        # 底部渐变装饰
        bottom_deco = QLabel(self.sidebar)
        bottom_deco.setGeometry(0, 600, 240, 40)
        bottom_deco.setStyleSheet("""
            background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
                stop:0 rgba(110,199,255,0), 
                stop:1 rgba(110,199,255,0.3));
        """)

    # 侧边栏和内容区初始化代码与之前相同...
    def switch_page(self, index):

        self.stack.setCurrentIndex(index)
        # 移动标签到该按钮的右侧
        self.animation.setStartValue(self.slabel.pos())
        self.animation.setEndValue(QtCore.QPoint(self.button_group.buttons()[index].x(), self.button_group.buttons()[index].y()))
        self.animation.setDuration(135)
        self.animation.start()

    def init_content_area(self):
        self.stack = QStackedWidget()
        # 添加以下两行关键代码
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.setMinimumSize(0, 0)  # 允许缩小到零
        self.stack.setStyleSheet("border-radius: 15px;")
        self.stack.setStyleSheet("""
                    QStackedWidget {
                        background-color: #FFFFFF;
                        border-radius: 15px;
                        margin: 10px 10px 10px 0;
                        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                    }
                """)

        # 创建四个页面
        self.stack.addWidget(self.create_click_page())
        self.stack.addWidget(self.create_sendmessage_page())
        self.stack.addWidget(self.create_team_page())
        self.stack.addWidget(self.create_tools_page())
        self.stack.addWidget(self.create_setting_page())


        self.content_layout.addWidget(self.stack)

    def create_click_page(self):
        page = QWidget()

        # 主布局：上下分层（3:7比例）
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        # ===== 上部连点器区域（30%）=====
        clicker_panel = QFrame()
        clicker_panel.setObjectName("clickerPanel")  # 设置唯一对象名
        clicker_panel.setStyleSheet("""
            QFrame {
                background: #FAFCFF;
                border-radius: 12px;
                border: 1px solid #D0D5DD;
                padding: 12px;
            }
        """)
        clicker_layout = QHBoxLayout(clicker_panel)
        clicker_layout.setContentsMargins(10, 10, 10, 10)

        config_Widget = QWidget()
        config_Widget.setObjectName('config_Widget')
        config_Widget.setStyleSheet("""
            QWidget#config_Widget {
                background: #FAFCFF;
                border-radius: 12px;
                border: 1px solid #D0D5DD;
                padding: 2px;
            }
        """)
        config_layout = QVBoxLayout(config_Widget)
        title_label_click = QLabel("连点器")
        title_label_click.setStyleSheet('''QLabel {
                font: 20px '等线';
                color: #667085;
                border: None;
            }''')
        config_layout.addWidget(title_label_click)

        # 点击类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel("点击类型:")
        type_label.setStyleSheet("font: 13px '等线'; color: #475467;border: None;")
        self.LClick_Radio = QRadioButton("左键")
        self.MClick_Radio = QRadioButton("中键")
        self.RClick_Radio = QRadioButton("右键")
        for btn in [self.LClick_Radio, self.MClick_Radio, self.RClick_Radio]:
            btn.setStyleSheet("font: 13px '等线'; color: #344054;")
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.LClick_Radio)
        type_layout.addWidget(self.MClick_Radio)
        type_layout.addWidget(self.RClick_Radio)
        self.LClick_Radio.setChecked(True)


        # 间隔时间设置
        interval_layout = QHBoxLayout()
        interval_label = QLabel("间隔(秒):")
        interval_label.setStyleSheet("font: 13px '等线'; color: #475467;border: None;")
        self._3D = QDoubleSpinBox()
        self._3D.setRange(0.01, 1000)
        self._3D.setValue(0.1)
        self._3D.setFixedWidth(150)
        self._3D.setStyleSheet(ui.style.new_spinbox_style)
        interval_layout.addWidget(interval_label)
        interval_layout.addSpacing(10)
        interval_layout.addWidget(self._3D)
        interval_layout.addSpacing(150)


        speed_mode_layout = QHBoxLayout()
        speed_label = QLabel("速度模式:")
        speed_label.setStyleSheet("font: 13px '等线'; color: #475467;border: None;")
        self.high_speed_radio = QRadioButton("高速模式")
        self.low_speed_radio = QRadioButton("低速模式")
        for btn in [self.high_speed_radio, self.low_speed_radio]:
            btn.setStyleSheet("font: 13px '等线'; color: #344054;")
        speed_mode_layout.addWidget(speed_label)
        speed_mode_layout.addWidget(self.high_speed_radio)
        speed_mode_layout.addWidget(self.low_speed_radio)
        speed_mode_layout.addSpacing(100)
        self.high_speed_radio.setChecked(True)  # 默认选择高速模式

        config_layout.addLayout(interval_layout)
        #config_layout.addLayout(speed_mode_layout)
        config_layout.addLayout(type_layout)


        # 右侧控制区
        control_group = QFrame()
        control_layout = QVBoxLayout(control_group)
        control_layout.setContentsMargins(20, 0, 0, 0)

        self._3pushButton_4 = QPushButton(f"⚡ 快捷键设置: {self.sort}")
        self._3pushButton_6 = QPushButton("▶ 启动连点")
        self._3pushButton_7 = QPushButton("⏹ 停止")
        for btn in [self._3pushButton_4, self._3pushButton_6, self._3pushButton_7]:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2196F3, stop:1 #03A9F4);  /* 蓝色渐变 */
                    color: white;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font: 14px '等线';
                    min-width: 120px;
                    margin: 5px 0;
                }
                QPushButton:hover { background: #1976D2; }      /* 深蓝色悬停 */
                QPushButton:pressed { background: #0D47A1; }   /* 更深的蓝色按下 */
                QPushButton:disabled {
                    background: #E0E0E0;       /* 浅灰色背景 */
                    color: #9E9E9E;            /* 灰色文字 */
                    border: 1px solid #BDBDBD; /* 浅灰色边框 */
                }
            """)
        self._3pushButton_7.setVisible(False)
        control_layout.addWidget(self._3pushButton_4)
        control_layout.addWidget(self._3pushButton_6)
        control_layout.addWidget(self._3pushButton_7)

        # clicker_layout.addLayout(config_layout)
        clicker_layout.addWidget(config_Widget)
        clicker_layout.addWidget(control_group)

        # ===== 下部脚本区域（70%）=====
        script_panel = QFrame()
        script_panel.setObjectName('script_panel')
        script_panel.setStyleSheet("""
            QFrame {
                background: #F8FAFF;
                border-radius: 12px;
                padding: 15px;
                font-family: 等线;
            }
            QFrame#script_panel{
        border: 1px solid #D0D5DD;}
        """)

        script_layout = QVBoxLayout(script_panel)
        script_layout.setContentsMargins(15, 15, 15, 15)

        # 标题和操作栏
        header = QHBoxLayout()
        title = QLabel("自动脚本")
        title.setStyleSheet('''QLabel {
                font: 20px '等线';
                color: #667085;
                border: None;
            }''')
        tool_buttons = QHBoxLayout()
        self.button_file = QPushButton("📂 选择脚本")
        self.button_file.clicked.connect(self.show_file_menu)

        self.button_create = QPushButton("🆕 新建脚本")
        self.button_create.clicked.connect(self.show_child_dialog)
        for btn in [self.button_file, self.button_create]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #E0E7FF;
                    color: #4F46E5;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font: 13px '等线';
                    margin-left: 10px;
                }
                QPushButton:hover { background: #C7D2FE; }
            """)
        tool_buttons.addWidget(self.button_file)
        tool_buttons.addWidget(self.button_create)
        header.addWidget(title)
        header.addLayout(tool_buttons)
        script_layout.addLayout(header)

        # 配置表单
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)

        # 脚本设置
        self.file_lineEdit = ui.style.DraggableLineEdit()
        self.file_lineEdit.setPlaceholderText("输入脚本名称")
        self.file_lineEdit.setContentsMargins(0, 10, 0, 0)
        self.file_lineEdit.setStyleSheet(ui.style.new_style_lineEdit)
        self.file_lineEdit.setFixedHeight(40)

        self.param_lineEdit = QLineEdit()
        self.param_lineEdit.setPlaceholderText("输入参数")
        self.param_lineEdit.setContentsMargins(0, 10, 0, 0)
        self.param_lineEdit.setStyleSheet(ui.style.new_style_lineEdit)
        self.param_lineEdit.setFixedHeight(40)

        # 初始化菜单
        self.file_menu = QMenu(self)
        self.setup_menu()
        # 参数设置
        param_group = QHBoxLayout()

        self.wait_doubleSpinBox = QDoubleSpinBox()
        self.wait_doubleSpinBox.setStyleSheet(ui.style.new_spinbox_style)
        self._3spinBox_3 = QSpinBox()
        self._3spinBox_3.setMinimum(1)
        self._3spinBox_3.setValue(1)
        self.spinbox_play_speed = QSpinBox()
        self.spinbox_play_speed.setMinimum(0)
        self.spinbox_play_speed.setMaximum(1000)
        self.spinbox_play_speed.setValue(100)
        for widget in [self._3spinBox_3, self.spinbox_play_speed]:
            widget.setStyleSheet(ui.style.new_spinbox_style)
            widget.setMinimumWidth(60)

        param_group.addWidget(QLabel("启动延时:"))
        param_group.addWidget(self.wait_doubleSpinBox)
        param_group.addWidget(QLabel("执行次数:"))
        param_group.addWidget(self._3spinBox_3)
        param_group.addWidget(QLabel("执行速度%:"))
        param_group.addWidget(self.spinbox_play_speed)
        param_group.addWidget(QLabel("结束按键"))
        # 创建 QComboBox 并添加选项
        self.end_key_combo = QComboBox()
        # 设置下拉框和下拉菜单样式
        self.end_key_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right top;
                width: 20px;
                border-left: 1px solid #CCCCCC;
            }
            QComboBox QAbstractItemView {  /* 下拉菜单样式 */
                background-color: white;
                selection-background-color: #0078D4;
                selection-color: white;
                outline: none;  /* 去除选中虚线框 */
            }
        """)
        self.end_key_combo.addItems(["ESC", "F8", "F9", "F10", "END"])  # 设置选项
        param_group.addWidget(self.end_key_combo)
        # param_group.addStretch()

        form_layout.addRow("脚本名称:", self.file_lineEdit)
        form_layout.addRow(QLabel("参数设置:"), self.param_lineEdit)
        form_layout.addRow(param_group)
        script_layout.addLayout(form_layout)

        # 控制按钮
        action_btns = QHBoxLayout()


        self._3pushButton = QPushButton("开始录制: F9")
        self._3pushButton.clicked.connect(lambda: self.start_recording("record"))
        self._3pushButton_2 = QPushButton("开始执行: F10")
        self._3pushButton_2.clicked.connect(lambda: self.start_recording("execute"))
        for btn in [self._3pushButton, self._3pushButton_2]:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #10B981, stop:1 #34D399);
                    color: white;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font: bold 14px '等线';
                    min-width: 140px;
                    margin: 0 10px;
                }
                QPushButton:hover { 
                    background: #059669; 
                }
                QPushButton:pressed { 
                    background: #047857; 
                }
                QPushButton:disabled {
                    background: #E5E7EB;  /* 浅灰色背景 */
                    color: #6B7280;       /* 深灰色文字 */
                    /* 其他属性保持与默认状态一致 */
                }
            """)
        action_btns.addStretch()
        #action_btns.addWidget(self.record_hotkey_btn)
        action_btns.addWidget(self._3pushButton)
        action_btns.addWidget(self._3pushButton_2)
        action_btns.addStretch()
        script_layout.addLayout(action_btns)

        # 添加到主布局
        main_layout.addWidget(clicker_panel, stretch=4)
        main_layout.addWidget(script_panel, stretch=6)

        return page

    def start_recording(self, types):

        """开始记录按键"""
        if types == 'record':
            if self.record_hotkey != None:
                # 需要解绑时
                keyboard.remove_hotkey(self.record_hotkey)
            self._3pushButton.setText('开始录制: ')
            self._3pushButton.setEnabled(False)
            self.record_key_status = True
        else:
            if self.execute_hotkey != None:
                # 需要解绑时
                keyboard.remove_hotkey(self.execute_hotkey)
            self._3pushButton_2.setText('开始执行: ')
            self._3pushButton_2.setEnabled(False)
            self.execute_key_status = True
        self.pressed_keys.clear()
        self.recorded_keys.clear()
        self.setFocus()
    def keyPressEvent(self, event):
        """处理按键按下事件"""
        if self.record_key_status:
            key = event.key()
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
                if len(self.recorded_keys) < 2:
                    self.recorded_keys.add(key)
                    self.update_button_text('record')
        elif self.execute_key_status:
            key = event.key()
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
                if len(self.recorded_keys) < 2:
                    self.recorded_keys.add(key)
                    self.update_button_text('execute')
        event.accept()

    def keyReleaseEvent(self, event):
        """处理按键释放事件"""
        if self.record_key_status:
            key = event.key()
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
                if not self.pressed_keys:
                    self.record_key_status = False
                    self._3pushButton.setEnabled(True)
                    # 提取按键名称
                    hotkey = self._3pushButton.text().split(':')[-1].strip()
                    # 设置热键
                    self.record_hotkey = keyboard.add_hotkey(hotkey, self.Click_Record)
                    #self.record_hotkey = keyboard.add_hotkey(self.record_hotkey_btn.text(), self.Click_Record)
        elif self.execute_key_status:
            key = event.key()
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
                if not self.pressed_keys:
                    self.execute_key_status = False
                    self._3pushButton_2.setEnabled(True)
                    # 提取按键名称
                    hotkey = self._3pushButton_2.text().split(':')[-1].strip()
                    # 设置热键
                    self.execute_hotkey = keyboard.add_hotkey(hotkey, self.Click_Record_execute)
        event.accept()
    def update_button_text(self, types):
        """更新按钮显示的文本"""
        key_names = []
        for key in self.recorded_keys:
            # 转换特殊按键
            special_keys = {
                Qt.Key_Control: "Ctrl",
                Qt.Key_Shift: "Shift",
                Qt.Key_Alt: "Alt",
                Qt.Key_Meta: "Meta",
                Qt.Key_Space: "Space"
            }
            if key in special_keys:
                key_names.append(special_keys[key])
                continue

            # 处理功能键
            if Qt.Key_F1 <= key <= Qt.Key_F35:
                key_names.append(f"F{key - Qt.Key_F1 + 1}")
                continue

            # 获取可读名称
            seq = QKeySequence(key)
            name = seq.toString()
            if not name:
                key_name = Qt.Key(key).name[4:] if Qt.Key(key).name.startswith('Key_') else Qt.Key(key).name
                name = key_name.capitalize()
            key_names.append(name)
        if types == 'record':
            self._3pushButton.setText("开始录制: "+'+'.join(key_names))
        else:
            self._3pushButton_2.setText("开始录制: " + '+'.join(key_names))
    def resiZED(self, event):
        print(f"连点器高度: {self.clicker_group.height()}")
        print(f"脚本高度: {self.script_group.height()}")

    def create_sendmessage_page(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")

        # 主布局
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # ===== 标题和切换按钮 =====
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("消息发送功能")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font: bold 20px 'Microsoft YaHei';
                padding-left: 5px;
            }
        """)

        # 切换按钮容器
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)

        self.btn_handle = QPushButton("句柄式发送")
        self.btn_simulate = QPushButton("模拟点击发送")
        self.btn_custom = QPushButton("自定义操作")

        self.style_group = QButtonGroup()
        self.style_group.addButton(self.btn_handle)
        self.style_group.addButton(self.btn_simulate)
        self.style_group.addButton(self.btn_custom)

        for btn in [self.btn_handle, self.btn_simulate,self.btn_custom]:
            btn.setFixedSize(140, 26)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: #f8f9fa;
                    color: #7f8c8d;
                    border: 1px solid #dcdde1;
                    border-radius: 6px;
                    margin-right: 5px;
                }
                QPushButton:hover {
                    background: #e9ecef;
                    color: #2c3e50;
                }
                QPushButton:checked {
                    background: #3498db;
                    color: white;
                    border-color: #2980b9;
                }
            """)
            btn.setFont(ui.style.style_font_9)

        self.btn_handle.setChecked(True)
        btn_layout.addWidget(self.btn_handle)
        btn_layout.addWidget(self.btn_simulate)
        btn_layout.addWidget(self.btn_custom)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(btn_container)

        main_layout.addWidget(header)

        # ===== 页面堆栈 =====
        self.send_stack = QStackedWidget()
        self.send_stack.setStyleSheet("""
            QStackedWidget {
                background: white;
                border-radius: 12px;
                border: 1px solid #dfe4ea;
            }
        """)

        # 添加两个子页面
        self.send_stack.addWidget(self.create_handle_subpage())
        self.send_stack.addWidget(self.create_simulate_subpage())
        self.send_stack.addWidget(self.create_custom_subpage())

        main_layout.addWidget(self.send_stack)

        # 连接切换信号
        self.btn_handle.clicked.connect(lambda: self.send_stack.setCurrentIndex(0))
        self.btn_simulate.clicked.connect(lambda: self.send_stack.setCurrentIndex(1))
        self.btn_custom.clicked.connect(lambda: self.send_stack.setCurrentIndex(2))

        return page

    def create_handle_subpage(self):
        subpage = QWidget()
        layout = QVBoxLayout(subpage)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 版本选择
        version_group = QWidget()
        version_layout = QHBoxLayout(version_group)
        self.old_QQ = QRadioButton("旧版QQ (9.7.23±)")
        self.new_QQ = QRadioButton("新版QQ (9.9.15±)")
        self.old_QQ.setChecked(True)

        for rb in [self.old_QQ, self.new_QQ]:
            rb.setStyleSheet("""
                QRadioButton {
                    font: 12px 'Microsoft YaHei';
                    color: #34495e;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            version_layout.addWidget(rb)

        version_layout.addStretch()

        # 输入区域
        input_group = QGroupBox("句柄设置")
        input_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px 'Microsoft YaHei';
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        grid = QGridLayout(input_group)

        # 句柄输入行
        self._2lineEdit_3 = QLineEdit()
        self._2lineEdit_3.setPlaceholderText("输入句柄值或点击右侧按钮获取")
        self._2lineEdit_3.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #D0D5DD;
                        border-radius: 6px;
                        padding: 6px;
                        font: 13px '等线';
                    }
                """)
        self._2pushButton2 = QPushButton("点击此处后单击聊天窗口获取句柄")
        self._2pushButton2.setFont(ui.style.style_font_Yahei)
        self._2pushButton2.setStyleSheet("""
                                                QPushButton {
                                                    border: 1px solid #989898;    /* 设置为RGB颜色#3498db的边框 */
                                                    background-color: transparent;    /* 设置透明背景 */
                                                    border-radius: 3px;    /* 设置圆角 */
                                                    padding: 6px;
                                                }
                                                QPushButton:hover {
                                                    background-color: #CDCDCD;    /* 设置鼠标悬停时的背景颜色为RGB颜色#3498db */
                                                    border: 1px solid #989898;    /* 设置鼠标悬停时的边框颜色为RGB颜色#3498db */
                                                }
                                            """)
        Handle_Label = QLabel("句柄:")
        Handle_Label.setStyleSheet("""
                    QLabel {
                        font-family: '等线';    /* 字体名称 */
                        font-size: 12px;       /* 字号 */
                        color: #344054;        /* 文字颜色 */
                    }""")
        grid.addWidget(Handle_Label, 0, 0)
        grid.addWidget(self._2lineEdit_3, 0, 1)
        grid.addWidget(self._2pushButton2, 0, 2)

        # 参数设置
        '''param_group = QWidget()
        param_layout = QHBoxLayout(param_group)'''

        spin_group = QGroupBox('参数设置')
        spin_group.setStyleSheet("""
            QLabel {
                font-family: '等线';    /* 字体名称 */
                font-size: 12px;       /* 字号 */
                color: #344054;        /* 文字颜色 */
            }
            QGroupBox {
                font: bold 14px 'Microsoft YaHei';
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        spin_layout = QFormLayout(spin_group)
        self.handle_send_times = QSpinBox()
        self.handle_send_times.setStyleSheet("""
                                    QSpinBox {
                                        border: 1px solid #D0D5DD;
                                        border-radius: 6px;
                                        padding: 4px;
                                        font: 13px '等线';
                                    }
                                """)
        self.handle_send_times.setMinimum(1)
        self.handle_send_times.setValue(10)
        self.handle_send_times.setMaximum(9999)
        spin_layout.addRow("发送次数:", self.handle_send_times)

        self.handle_send_interval = QDoubleSpinBox()
        self.handle_send_interval.setStyleSheet("""
                                            QDoubleSpinBox {
                                                border: 1px solid #D0D5DD;
                                                border-radius: 6px;
                                                padding: 4px;
                                                font: 13px '等线';
                                            }
                                        """)
        self.handle_send_interval.setMinimum(0)
        self.handle_send_interval.setValue(1)
        self.handle_send_interval.setMaximum(999)

        spin_layout.addRow("间隔(秒):", self.handle_send_interval)


        # 内容输入
        content_group = QGroupBox("消息内容")
        content_group.setStyleSheet(input_group.styleSheet())
        content_layout = QVBoxLayout(content_group)
        self._2textEdit = QTextEdit()
        self._2textEdit.setPlaceholderText("输入要发送的消息内容...\n提示：不能以数字开头")
        self._2textEdit.setStyleSheet(ui.style.style_textEdit)
        self._2textEdit.setFont(ui.style.style_font_Yahei)
        content_layout.addWidget(self._2textEdit)

        # 开始按钮
        self.handle_send_btn = QPushButton("🚀 开始发送")
        self.handle_send_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border-radius: 6px;
                padding: 12px 24px;
                font: bold 14px 'Microsoft YaHei';
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)

        # 组合布局
        layout.addWidget(version_group)
        layout.addWidget(input_group)
        layout.addWidget(spin_group)
        layout.addWidget(content_group)
        layout.addWidget(self.handle_send_btn, 0, Qt.AlignRight)

        return subpage

    def create_simulate_subpage(self):
        subpage = QWidget()
        layout = QVBoxLayout(subpage)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 创建带阴影效果的模块容器
        def create_card(title, widget):
            card = QWidget()
            card.setObjectName("card_container")  # 设置唯一对象名限定样式作用域
            card.setStyleSheet("""
                    QWidget#card_container {
                        border-radius: 8px;
                        border: 1px solid #ecf0f1;
                    }
                    QLabel#card_title {
                        color: #34495e;
                        font: bold 14px 'Microsoft YaHei';
                        border-bottom: 1px solid #bdc3c7;
                        padding-bottom: 3px;
                    }
                """)
            layout = QVBoxLayout(card)
            layout.setContentsMargins(12, 12, 12, 12)  # 卡片内边距
            layout.setSpacing(8)

            title_label = QLabel(title)
            title_label.setObjectName("card_title")  # 设置标题专用样式
            title_label.setFixedHeight(35)
            title_label.setAlignment(Qt.AlignBottom)
            layout.addWidget(title_label)
            # 内容容器（确保内部控件无边框）
            content_container = QWidget()
            content_container.setStyleSheet("border: none;")  # 清除内部容器样式
            content_layout = QVBoxLayout(content_container)
            content_layout.setContentsMargins(0, 0, 0, 0)  # 内部控件无边距
            content_layout.addWidget(widget)
            layout.addWidget(content_container)
            return card

        # @QQ功能
        at_group = QWidget()
        at_group.setStyleSheet("""
                    QLabel {
                        font-family: "Microsoft YaHei";
                        font-size: 12px;
                        color: #333333;
                    }
                """)
        at_layout = QFormLayout(at_group)
        self.QQ_StartSend_At_target_lineedit = QLineEdit()
        self.QQ_StartSend_At_target_lineedit.setStyleSheet(ui.style.new_style_lineEdit)
        self.QQ_StartSend_At_pause_doublespb = QDoubleSpinBox()
        self.QQ_StartSend_At_pause_doublespb.setStyleSheet(ui.style.new_spinbox_style)
        self.QQ_StartSend_At_pause_doublespb.setValue(1)
        # 新增发送次数控件
        self.QQ_StartSend_At_times_spinbox = QSpinBox()
        self.QQ_StartSend_At_times_spinbox.setStyleSheet(ui.style.new_spinbox_style)
        # 原复选框
        self.QQ_StartSend_At_number_checkbox = QCheckBox()
        self.QQ_StartSend_At_number_checkbox.setStyleSheet(ui.style.new_checkbox_style)
        self.QQ_StartSend_At_number_checkbox.setText("添加数字后缀")
        # 创建次数和复选框的水平布局
        times_check_layout = QHBoxLayout()
        times_check_layout.addWidget(self.QQ_StartSend_At_times_spinbox)
        times_check_layout.addWidget(self.QQ_StartSend_At_number_checkbox)
        times_check_layout.addStretch(1)  # 添加弹性空间保持左对齐



        at_layout.addRow("目标QQ:", self.QQ_StartSend_At_target_lineedit)
        at_layout.addRow("发送间隔:", self.QQ_StartSend_At_pause_doublespb)
        at_layout.addRow("发送次数:", times_check_layout)
        # 创建水平布局并添加按钮
        button_layout = QHBoxLayout()
        self.QQ_StartSend_At_Button = QPushButton("开始发送")
        self.QQ_StartSend_At_Button.setStyleSheet("""
                QPushButton {
                    background-color: #4DA3FF;  /* 浅蓝色 */
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px 10px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #3D8FD3;  /* 稍深的水蓝色 */
                }
                QPushButton:pressed {
                    background-color: #2C7ABF;  /* 柔和的深蓝色 */
                }
            """)
        button_layout.addWidget(self.QQ_StartSend_At_Button, stretch=2)  # 按钮占2份拉伸
        button_layout.addStretch(1)  # 右侧拉伸
        at_layout.addRow(button_layout)
        at_card = create_card("@指定用户(此模拟点击发送页所有功能可按F10强制退出)", at_group)

        # 复制发送
        copy_group = QWidget()
        copy_group.setStyleSheet("""
                            QLabel {
                                font-family: "Microsoft YaHei";
                                font-size: 12px;
                                color: #333333;
                            }
                        """)
        copy_layout = QFormLayout(copy_group)
        self.QQ_Send_Copy_pause_doublespb = QDoubleSpinBox()
        self.QQ_Send_Copy_pause_doublespb.setStyleSheet(ui.style.new_spinbox_style)
        self.QQ_Send_Copy_pause_doublespb.setValue(1)

        self.QQ_Send_Copy_times_spinbox = QSpinBox()
        self.QQ_Send_Copy_times_spinbox.setStyleSheet(ui.style.new_spinbox_style)
        self.QQ_Send_Copy_times_spinbox.setValue(0)

        self.QQ_Send_Copy_startsend_button = QPushButton('开始发送')
        self.QQ_Send_Copy_startsend_button.setStyleSheet(ui.style.new_style_pushbutton)
        copy_layout.addRow("发送间隔:", self.QQ_Send_Copy_pause_doublespb)
        copy_layout.addRow("发送次数:", self.QQ_Send_Copy_times_spinbox)

        copy_layout.addRow(self.QQ_Send_Copy_startsend_button)
        copy_card = create_card("📋 复制内容发送", copy_group)

        # 序列发送
        seq_group = QWidget()
        # 在创建seq_group后添加样式表
        seq_group.setStyleSheet("""
            QLabel {
                font-family: "Microsoft YaHei";
                font-size: 12px;
                color: #333333;
            }
        """)
        seq_layout = QFormLayout(seq_group)
        self.QQ_Seq_lineEdit = QLineEdit()
        self.QQ_Seq_lineEdit.setStyleSheet(ui.style.new_style_lineEdit)
        # 创建文件选择按钮和水平布局
        file_select_layout = QHBoxLayout()
        self.QQ_Seq_file_button = QPushButton("选择文件")
        self.QQ_Seq_file_button.setStyleSheet(ui.style.new_style_pushbutton)  # 使用现有按钮样式
        #self.QQ_Seq_file_button.clicked.connect(self.open_seq_file_dialog)  # 连接点击信号
        file_select_layout.addWidget(self.QQ_Seq_lineEdit)
        file_select_layout.addWidget(self.QQ_Seq_file_button)

        self.QQ_Seq_combobox = QComboBox()
        self.QQ_Seq_combobox.addItems(["顺序发送", "随机发送"])  # 设置选项
        self.QQ_Seq_combobox.setStyleSheet(ui.style.new_style_comboBox)
        self.QQ_Seq_Times_spinBox = QSpinBox()
        self.QQ_Seq_Times_spinBox.setStyleSheet(ui.style.new_spinbox_style)
        self.QQ_Seq_doublebox = QDoubleSpinBox()
        self.QQ_Seq_doublebox.setStyleSheet(ui.style.new_spinbox_style)
        self.QQ_Seq_doublebox.setValue(1)
        self.QQ_Seq_Start_button = QPushButton()
        self.QQ_Seq_Start_button.setText("开始发送")
        self.QQ_Seq_Start_button.setStyleSheet(ui.style.new_style_pushbutton)
        # 修改文件选择行布局
        seq_layout.addRow("文件选择:", file_select_layout)  # 使用水平布局替换单个控件
        seq_layout.addRow("发送模式:", self.QQ_Seq_combobox)
        seq_layout.addRow("遍数/次数:", self.QQ_Seq_Times_spinBox)
        seq_layout.addRow("操作间隔:", self.QQ_Seq_doublebox)
        seq_layout.addRow(self.QQ_Seq_Start_button)
        seq_card = create_card("📁 序列内容发送", seq_group)

        # 位置设置
        pos_group = QWidget()
        pos_group.setObjectName("pos_group")

        pos_layout = QVBoxLayout(pos_group)
        self.label_position_status = QLabel()
        self.label_position_status.setFont(style_font_10)
        self.label_position_status.setObjectName("label_position_status")
        if position_status != True:
            self.label_position_status.setText(
                '<font color="black">位置设置：</font> <font color="red">未设置</font>')
        else:
            self.label_position_status.setText(
                '<font color="black">位置设置：</font> <font color="green">已设置</font>')

        self.label_position_text = QLabel()
        self.label_position_text.setFont(style_font_10)
        self.label_position_text.setObjectName("label_position_text")
        if position_status != True:
            self.label_position_text.setText(
                f'<font color="black">聊天框位置：</font> <font color="red">{textedit_position}</font>')
        else:
            self.label_position_text.setText(
                f'<font color="black">聊天框位置：</font> <font color="green">{textedit_position}</font>')

        self.label_position_send = QLabel()
        self.label_position_send.setFont(style_font_10)
        self.label_position_send.setObjectName("label_position_send")
        if position_status != True:
            self.label_position_send.setText(
                f'<font color="black">发送键位置：</font> <font color="red">{send_position}</font>')
        else:
            self.label_position_send.setText(
                f'<font color="black">发送键位置：</font> <font color="green">{send_position}</font>')

        pos_layout.addWidget(self.label_position_status)
        pos_layout.addWidget(self.label_position_text)
        pos_layout.addWidget(self.label_position_send)


        self.record_position_button = QPushButton("📍 记录位置")
        self.record_position_button.setStyleSheet("""
    QPushButton {
        background-color: #4DA3FF;  /* 浅蓝色 */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #3D8FD3;  /* 稍深的水蓝色 */
    }
    QPushButton:pressed {
        background-color: #2C7ABF;  /* 柔和的深蓝色 */
    }
""")
        pos_layout.addWidget(self.record_position_button)
        pos_card = create_card("位置设置", pos_group)

        # 网格布局
        grid = QGridLayout()
        grid.addWidget(at_card, 0, 0)
        grid.addWidget(copy_card, 0, 1)
        grid.addWidget(seq_card, 1, 0)
        grid.addWidget(pos_card, 1, 1)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        layout.addLayout(grid)

        return subpage

    def create_custom_subpage(self):
        subpage = QWidget()
        layout = QVBoxLayout(subpage)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 操作组容器
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #D1D1D6;
                border-radius: 8px;
                background: #F5F5F7;
            }
        """)

        content_widget = QWidget()
        self.scroll_layout = QVBoxLayout(content_widget)
        self.scroll_layout.setSpacing(10)

        # 初始操作组
        self.operation_groups = []
        self.add_operation_group()

        # 全局执行参数
        global_config = QWidget()
        global_config.setStyleSheet("""
            QWidget {
                background: #FFFFFF;
                border-radius: 8px;
            }
            QLabel {
                font: 14px 'Microsoft YaHei';
                color: #666666;
            }
        """)

        global_layout = QHBoxLayout(global_config)
        global_layout.setContentsMargins(10, 10, 10, 10)
        global_layout.setSpacing(15)

        # 执行次数
        lbl_executions = QLabel("整体执行次数:")
        self.spin_executions = QSpinBox()
        self.spin_executions.setRange(1, 9999)
        self.spin_executions.setValue(1)
        self.spin_executions.setStyleSheet(ui.style.new_spinbox_style)

        # 间隔时间
        lbl_interval = QLabel("每次间隔(秒):")
        self.spin_interval = QDoubleSpinBox()
        self.spin_interval.setRange(0, 3600)
        self.spin_interval.setValue(0)
        self.spin_interval.setSingleStep(0.5)
        self.spin_interval.setStyleSheet(ui.style.new_spinbox_style)

        # 参数布局
        global_layout.addWidget(lbl_executions)
        global_layout.addWidget(self.spin_executions)
        global_layout.addSpacing(20)
        global_layout.addWidget(lbl_interval)
        global_layout.addWidget(self.spin_interval)
        global_layout.addStretch()

        # 控制按钮
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # 按钮样式
        button_style = """
            QPushButton {
                border-radius: 6px;
                font: 13px 'Microsoft YaHei';
                color: black;
                min-width: 100px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """

        # 按钮创建
        self.btn_add = QPushButton("➕ 添加操作组")
        self.btn_clear = QPushButton("🗑️ 清空所有")
        self.btn_import = QPushButton("📥 导入配置")
        self.btn_export = QPushButton("📤 导出配置")
        self.btn_get_position = QPushButton("📍 获取位置")
        self.btn_custom_start = QPushButton("🚀 开始执行")

        # 设置样式
        buttons = [
            (self.btn_add, "#3498db"),
            (self.btn_clear, "#e74c3c"),
            (self.btn_import, "#9b59b6"),
            (self.btn_export, "#9b59b6"),
            (self.btn_get_position, "#2ecc71"),
            (self.btn_custom_start, "#2ecc71")
        ]

        for btn, color in buttons:
            btn.setStyleSheet(f"{button_style} background: {color};")

        # 布局按钮
        control_layout.addWidget(self.btn_add)
        control_layout.addWidget(self.btn_clear)
        control_layout.addWidget(self.btn_import)
        control_layout.addWidget(self.btn_export)
        control_layout.addWidget(self.btn_get_position)
        control_layout.addStretch()
        control_layout.addWidget(self.btn_custom_start)

        # 组装界面
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        layout.addWidget(global_config)  # 全局参数区域
        layout.addWidget(control_panel)

        # 信号连接
        self.btn_add.clicked.connect(self.add_operation_group)
        self.btn_clear.clicked.connect(self.clear_operation_groups)
        self.btn_import.clicked.connect(self.load_custom_profile)
        self.btn_export.clicked.connect(self.save_custom_profile)

        return subpage

    def add_operation_group(self):
        group = OperationGroup()
        group.btn_remove.clicked.connect(lambda: self.remove_operation_group(group))
        self.operation_groups.append(group)
        self.scroll_layout.addWidget(group)

    def remove_operation_group(self, group):
        group.deleteLater()
        self.operation_groups.remove(group)

    def clear_operation_groups(self):
        for group in self.operation_groups[:]:
            self.remove_operation_group(group)

    def load_custom_profile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                   "Text Files (*.txt)",
                                                   options=options)
        self.clear_operation_groups()
        with open(file_name, 'r') as file:
            num = 0
            for line in file:
                # 将字符串转换为字典
                line_dict = ast.literal_eval(line.strip())
                self.add_operation_group()
                self.operation_groups[num].edit_handle.setText(line_dict.get("handle"))
                self.operation_groups[num].combo_action.setCurrentIndex(line_dict.get("action"))
                self.operation_groups[num].edit_param.setText(line_dict.get("param"))
                num += 1  # 确保每次循环递增num
        #file_name = file_name.replace("/", "\\")

    def save_custom_profile(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "选择保存路径",
            "auto_profile.txt",  # 这里设置默认文件名
            "All Files (*)"
        )
        if file_path:  # 如果用户选择了路径
            with open(file_path, 'w') as file:
                for group in self.operation_groups:
                    config = {
                        "handle": group.edit_handle.text(),
                        "action": group.combo_action.currentIndex(),
                        "param": group.edit_param.text()
                    }
                    file.write(str(config)+'\n')

    def create_team_page(self):
        page = QWidget()
        self.team_layout = QVBoxLayout(page)
        self.team_layout.setSpacing(15)

        join_team_widget = QWidget()


        # 顶部按钮区域
        top_layout = QHBoxLayout(join_team_widget)
        top_layout.setContentsMargins(0, 0, 0, 10)

        self.create_team_button = ui.buttons.CustomButton( radius=2, start_color=QColor(207, 207, 207, 0),
                                                          hover_color=QColor(33, 150, 243, 255),
                                                          border_color=QColor(33, 120, 255), border_width=1,
                                                          font_color=QColor(0, 0, 0))
        self.create_team_button.setFixedSize(200, 35)
        font = QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.create_team_button.setFont(font)
        self.create_team_button.setObjectName("create_team_button")
        self.create_team_button.setText("点击创建队伍")

        self.add_team_lineEdit = QLineEdit()
        self.add_team_lineEdit.setFixedHeight(35)
        self.add_team_lineEdit.setObjectName("add_team_lineEdit")
        self.add_team_lineEdit.setPlaceholderText("输入队伍ID")
        self.add_team_lineEdit.setFont(style_font_10)
        self.add_team_lineEdit.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font: 14px 'Microsoft YaHei';
            }
        """)


        self.add_team_button = ui.buttons.CustomButton( radius=2, start_color=QColor(207, 207, 207, 0),
                                                       hover_color=QColor(33, 150, 243, 255),
                                                       border_color=QColor(33, 120, 255), border_width=1,
                                                       font_color=QColor(0, 0, 0))
        self.add_team_button.setFixedSize(150, 35)
        self.add_team_button.setObjectName("add_team_button")
        self.add_team_button.setText("加入")
        self.add_team_button.setFont(style_font_12)



        self.add_team_ID = QLabel()
        self.add_team_ID.setFont(style_font_11)
        self.add_team_ID.setObjectName("add_team_ID")
        self.add_team_ID.setVisible(False)
        self.add_team_ID.setText("队伍ID为:")

        self.button_copy_id = ui.buttons.CustomButton(radius=2, start_color=QColor(207, 207, 207, 0),
                                                      hover_color=QColor(33, 150, 243, 255),
                                                      border_color=QColor(33, 120, 255), border_width=1,
                                                      font_color=QColor(0, 0, 0))
        font = QFont()
        font.setFamily("等线")
        font.setPointSize(12)
        self.button_copy_id.setFont(font)
        self.button_copy_id.setObjectName("button_copy_id")
        self.button_copy_id.setText("点击复制ID")
        self.button_copy_id.setVisible(False)

        self.create_team_label_prompt = QLabel()
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.create_team_label_prompt.setFont(font)
        self.create_team_label_prompt.setObjectName("create_team_label_prompt")
        self.create_team_label_prompt.setText("队伍加入!")
        self.create_team_label_prompt.setVisible(False)



        top_layout.addWidget(self.create_team_button)
        top_layout.addWidget(self.add_team_lineEdit)
        top_layout.addWidget(self.add_team_button)
        top_layout.addWidget(self.add_team_ID,stretch=7)
        top_layout.addWidget(self.button_copy_id,stretch=3)
        top_layout.addWidget(self.create_team_label_prompt)
        '''self.team_layout.addLayout(top_layout,stretch=2)'''
        self.team_layout.addWidget(join_team_widget)

        # 用户选择区域
        if avatar_load_status == True:
            self.user1 = UserWidget(f"{Name}[我]", f"{Account}", "./temp/avatar.png")
        else:
            self.user1 = UserWidget(f"{Name}[我]", f"{Account}", "./image/float/fc.png")
        self.user2 = UserWidget("等待用户加入", "None", "./image/other_user.png")
        self.team_layout.addWidget(self.user1,stretch=4)
        self.team_layout.addWidget(self.user2,stretch=4)

        # 开始按钮
        self.team_btn_start = QPushButton("开始执行")
        self.team_btn_start.setFixedHeight(45)
        self.team_btn_start.setStyleSheet(ui.style.new_style_pushbutton)
        self.team_execute_prompt = QLabel("等待队长开始执行...")

        self.team_layout.addWidget(self.team_btn_start)

        return page

    def create_tools_page(self):
        # 创建主页面及其布局
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 导航栏：使用水平布局放置四个按钮
        nav_bar = QWidget()
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(20)

        btn_music = QPushButton("下载网易云音乐", nav_bar)
        btn_format = QPushButton("文件格式转换", nav_bar)
        btn_qq = QPushButton("QQ信息", nav_bar)
        btn_group = QPushButton("QQ群信息获取", nav_bar)

        # 统一按钮风格
        for btn in (btn_music, btn_format, btn_qq, btn_group):
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font: bold 14px 'Microsoft YaHei';
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
            """)
            nav_layout.addWidget(btn)

        main_layout.addWidget(nav_bar)

        # 创建工具页堆栈，包含四个子页面
        self.tools_stack = QStackedWidget()
        self.tools_stack.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")
        main_layout.addWidget(self.tools_stack, 1)

        # --- 页面1：网易云音乐下载 ---
        page_music = QWidget()
        layout_music = QVBoxLayout(page_music)
        layout_music.setContentsMargins(20, 20, 20, 20)
        layout_music.setSpacing(15)

        label_music_title = QLabel("下载网易云音乐")
        label_music_title.setFont(QtGui.QFont("Arial", 18))
        layout_music.addWidget(label_music_title)

        # 歌曲链接输入
        url_layout = QHBoxLayout()
        label_url = QLabel("歌曲链接")
        label_url.setFont(style_font_Yahei)
        self.music_url = CustomLineEdit(self)
        self.music_url.setPlaceholderText("点击输入音乐链接 (Ctrl+V 粘贴)")
        self.music_url.setStyleSheet(ui.style.new_style_lineEdit)
        self.music_url.setFont(style_font_Yahei)
        self.music_url.setFixedHeight(35)
        url_layout.addWidget(label_url)
        url_layout.addWidget(self.music_url)
        layout_music.addLayout(url_layout)

        # 保存文件名输入
        filename_layout = QHBoxLayout()
        label_filename = QLabel("歌曲名称")
        label_filename.setFont(style_font_Yahei)
        self.music_filename = QLineEdit()
        self.music_filename.setPlaceholderText("点击输入保存文件名 (包含扩展名)")
        self.music_filename.setStyleSheet(ui.style.new_style_lineEdit)
        self.music_filename.setFont(style_font_Yahei)
        self.music_filename.setFixedHeight(35)
        filename_layout.addWidget(label_filename)
        filename_layout.addWidget(self.music_filename)
        layout_music.addLayout(filename_layout)

        # 保存路径显示
        path_layout = QHBoxLayout()
        label_path = QLabel("保存路径")
        label_path.setFont(style_font_Yahei)
        self.music_savepath = QLineEdit(os.getcwd() + '\\mod\\music')
        self.music_savepath.setStyleSheet(ui.style.new_style_lineEdit)
        self.music_savepath.setFont(style_font_Yahei)
        self.music_savepath.setFixedHeight(35)
        path_layout.addWidget(label_path)
        path_layout.addWidget(self.music_savepath)
        layout_music.addLayout(path_layout)

        self.choose_music = QPushButton()
        self.choose_music.setObjectName("choose_music")
        self.choose_music.setText("选择")
        self.choose_music.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        border: 2px solid #1976D2;
                        border-radius: 5px;
                        color: white;
                        font-family: 'Microsoft YaHei';
                        font-size: 14px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #42A5F5;
                        border: 2px solid #2196F3;
                    }
                    QPushButton:pressed {
                        background-color: #1976D2;
                        border: 2px solid #1565C0;
                    }
                """)
        self.choose_music.setFont(style_font_9)

        self.view_music = QPushButton()
        self.view_music.setObjectName("view_music")
        self.view_music.setText("浏览")
        self.view_music.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        border: 2px solid #1976D2;
                        border-radius: 5px;
                        color: white;
                        font-family: 'Microsoft YaHei';
                        font-size: 14px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #42A5F5;
                        border: 2px solid #2196F3;
                    }
                    QPushButton:pressed {
                        background-color: #1976D2;
                        border: 2px solid #1565C0;
                    }
                """)
        self.view_music.setFont(style_font_9)

        music_file_layout = QHBoxLayout()
        music_file_layout.addStretch()
        music_file_layout.addWidget(self.choose_music)
        music_file_layout.addWidget(self.view_music)

        layout_music.addLayout(music_file_layout)

        # 下载按钮
        self.btn_download_music = QPushButton("下载")
        self.btn_download_music.setFixedHeight(35)
        self.btn_download_music.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #43A047;
            }
        """)
        layout_music.addWidget(self.btn_download_music)
        layout_music.addStretch()

        self.tools_stack.addWidget(page_music)

        # --- 页面2：文件格式转换 ---
        page_format = QWidget()
        layout_format = QVBoxLayout(page_format)
        layout_format.setContentsMargins(20, 20, 20, 20)
        layout_format.setSpacing(15)

        label_format_title = QLabel("文件格式转换")
        label_format_title.setFont(QtGui.QFont("Arial", 18))
        layout_format.addWidget(label_format_title)

        # 图片路径输入（添加选择按钮）
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)

        # 图片路径输入
        self.pic_input_lineEdit = ui.style.DraggableLineEdit('picture')
        self.pic_input_lineEdit.setPlaceholderText("选择或拖拽文件到此处")
        self.pic_input_lineEdit.setFixedHeight(35)
        self.pic_input_lineEdit.setStyleSheet(ui.style.new_style_lineEdit)
        #layout_format.addWidget(self.pic_input_lineEdit)

        # 添加文件选择按钮
        btn_input = QPushButton("选择文件")
        btn_input.setFixedSize(80, 35)
        btn_input.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font: bold 14px;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                """)
        btn_input.clicked.connect(lambda: self.select_file_path('pic_file_path'))

        input_layout.addWidget(self.pic_input_lineEdit)
        input_layout.addWidget(btn_input)
        layout_format.addWidget(input_widget)

        # 输出文件夹路径输入（添加选择按钮）
        output_widget = QWidget()
        output_layout = QHBoxLayout(output_widget)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(10)

        # 输出文件夹路径输入
        self.pic_output_lineEdit = QLineEdit()
        self.pic_output_lineEdit.setPlaceholderText("点击输入图片输出路径")
        self.pic_output_lineEdit.setStyleSheet(ui.style.new_style_lineEdit)
        self.pic_output_lineEdit.setFixedHeight(35)
        #layout_format.addWidget(self.pic_output_lineEdit)

        # 添加文件夹选择按钮
        btn_output = QPushButton("选择路径")
        btn_output.setFixedSize(80, 35)
        btn_output.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font: bold 14px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
        btn_output.clicked.connect(lambda: self.select_file_path('pic_folder_path'))

        output_layout.addWidget(self.pic_output_lineEdit)
        output_layout.addWidget(btn_output)
        layout_format.addWidget(output_widget)

        # 格式选择，使用单选按钮
        format_selection = QWidget()
        format_layout = QHBoxLayout(format_selection)
        format_layout.setSpacing(20)
        self.JPG_radioButton = QRadioButton()
        self.JPG_radioButton.setObjectName("JPG_radioButton")
        self.JPG_radioButton.setText("JPG")
        self.JPG_radioButton.setChecked(True)
        self.JPG_radioButton.setStyleSheet(style_Radio)
        self.PNG_radioButton = QRadioButton()
        self.PNG_radioButton.setObjectName("PNG_radioButton")
        self.PNG_radioButton.setText("PNG")
        self.PNG_radioButton.setStyleSheet(style_Radio)
        self.GIF_radioButton = QRadioButton()
        self.GIF_radioButton.setObjectName("GIF_radioButton")
        self.GIF_radioButton.setText("GIF")
        self.GIF_radioButton.setStyleSheet(style_Radio)
        self.PDF_radioButton = QRadioButton()
        self.PDF_radioButton.setObjectName("PDF_radioButton")
        self.PDF_radioButton.setText("PDF")
        self.PDF_radioButton.setStyleSheet(style_Radio)
        format_layout.addWidget(self.JPG_radioButton)
        format_layout.addWidget(self.PNG_radioButton)
        format_layout.addWidget(self.GIF_radioButton)
        format_layout.addWidget(self.PDF_radioButton)
        '''for fmt in ["JPG", "PNG", "GIF", "PDF"]:
            radio = QRadioButton(fmt)
            radio.setStyleSheet("font: 14px;")
            if fmt == "JPG":
                radio.setChecked(True)
            format_layout.addWidget(radio)'''
        layout_format.addWidget(format_selection)

        # 输出按钮
        self.pic_confirm_button = QPushButton("输出")
        self.pic_confirm_button.setFixedHeight(35)
        self.pic_confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        layout_format.addWidget(self.pic_confirm_button)
        layout_format.addStretch()

        self.tools_stack.addWidget(page_format)

        # --- 页面3：QQ信息 ---
        page_qq = QWidget()
        layout_qq = QVBoxLayout(page_qq)
        layout_qq.setContentsMargins(20, 20, 20, 20)
        layout_qq.setSpacing(15)

        # 标题行（包含主标题和等级标签）
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        label_qq_title = QLabel("QQ信息 - 随机下载QQ头像")
        label_qq_title.setFont(QtGui.QFont("Arial", 18))
        label_lv2 = QLabel("LV2")
        label_lv2.setFont(QtGui.QFont("Arial", 16))
        label_lv2.setStyleSheet("color: #4CAF50;")  # 修改为绿色
        title_layout.addWidget(label_qq_title)
        title_layout.addWidget(label_lv2)
        title_layout.addStretch()  # 保持标题左对齐
        layout_qq.addWidget(title_widget)

        # 下载次数设置行
        download_count_widget = QWidget()
        download_count_layout = QHBoxLayout(download_count_widget)
        download_count_layout.setContentsMargins(0, 0, 0, 0)
        download_count_layout.setSpacing(10)
        label_download_count = QLabel("下载次数：")
        self.qq_image_down_spinbox = QSpinBox()
        self.qq_image_down_spinbox.setMinimum(1)
        self.qq_image_down_spinbox.setMaximum(9999)
        self.qq_image_down_spinbox.setValue(10)
        self.qq_image_down_spinbox.setStyleSheet(ui.style.new_spinbox_style)
        download_count_layout.addWidget(label_download_count)
        download_count_layout.addWidget(self.qq_image_down_spinbox)
        download_count_layout.addStretch()
        layout_qq.addWidget(download_count_widget)

        # 开始下载按钮
        self.btn_download_qq = QPushButton("开始下载")
        self.btn_download_qq.setFixedSize(200,35)
        self.btn_download_qq.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)


        # 浏览文件夹和清空文件夹按钮
        qq_folder_widget = QWidget()
        qq_folder_layout = QHBoxLayout(qq_folder_widget)
        qq_folder_layout.setSpacing(10)
        btn_browse_qq = QPushButton("浏览图片文件夹")
        btn_browse_qq.setStyleSheet(ui.style.new_style_pushbutton)
        btn_browse_qq.clicked.connect(lambda: self.open_folder('picture'))
        btn_clear_qq = QPushButton("一键清空文件夹")
        btn_clear_qq.setStyleSheet(ui.style.new_style_pushbutton)
        btn_clear_qq.clicked.connect(self.delete_images)
        qq_folder_layout.addWidget(btn_browse_qq)
        qq_folder_layout.addWidget(btn_clear_qq)
        qq_folder_layout.addStretch()
        self.total_download_times = QLabel('总下载次数: 0 次')
        self.successfully_download_times  = QLabel('有效次数: 0 次')
        layout_qq.addWidget(self.total_download_times)
        layout_qq.addWidget(self.successfully_download_times)
        layout_qq.addWidget(qq_folder_widget)
        layout_qq.addWidget(self.btn_download_qq)

        # 信息修改区域
        label_info_edit = QLabel("信息修改")
        label_info_edit.setFont(QtGui.QFont("Arial", 16))
        layout_qq.addWidget(label_info_edit)

        # 操作间隔设置
        interval_widget = QWidget()
        interval_layout = QHBoxLayout(interval_widget)
        interval_layout.setContentsMargins(0, 0, 0, 0)
        interval_layout.setSpacing(10)
        label_interval = QLabel("操作间隔（秒）")
        self.qq_image_update_spinbox_interval = QDoubleSpinBox()
        self.qq_image_update_spinbox_interval.setStyleSheet(ui.style.new_spinbox_style)
        self.qq_image_update_spinbox_interval.setMinimum(0.1)
        self.qq_image_update_spinbox_interval.setMaximum(3600.0)
        self.qq_image_update_spinbox_interval.setValue(1.0)
        self.qq_image_update_spinbox_interval.setSingleStep(0.5)
        interval_layout.addWidget(label_interval)
        interval_layout.addWidget(self.qq_image_update_spinbox_interval)
        interval_layout.addStretch()
        layout_qq.addWidget(interval_widget)

        # 开始执行按钮
        self.qq_information_edit_button = QPushButton("开始执行")
        self.qq_information_edit_button.setFixedSize(200,35)
        self.qq_information_edit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout_qq.addWidget(self.qq_information_edit_button)

        # 底部弹性空间
        layout_qq.addStretch()

        self.tools_stack.addWidget(page_qq)

        # --- 页面4：QQ群信息获取 ---
        page_group = QWidget()
        layout_group = QVBoxLayout(page_group)
        layout_group.setContentsMargins(20, 20, 20, 20)
        layout_group.setSpacing(15)

        label_group_title = QLabel("QQ群信息获取")
        label_group_title.setFont(QtGui.QFont("Arial", 18))
        layout_group.addWidget(label_group_title)

        # 输出文件夹路径输入（例如xlsx文件夹）
        self.lineEdit_group_path = QLineEdit(os.getcwd() + '\\mod\\xlsx')
        self.lineEdit_group_path.setPlaceholderText("点击输入xlsx文件夹路径")
        self.lineEdit_group_path.setStyleSheet("padding: 5px; border: 1px solid #CCCCCC; border-radius: 5px;")
        layout_group.addWidget(self.lineEdit_group_path)

        # 浏览和选择按钮并排显示
        group_folder_widget = QWidget()
        group_folder_layout = QHBoxLayout(group_folder_widget)
        group_folder_layout.setSpacing(10)
        btn_select_group = QPushButton("选择")
        btn_select_group.setStyleSheet(ui.style.new_style_pushbutton)
        btn_select_group.clicked.connect(lambda: self.select_file_path('group_folder_path'))
        btn_browse_group = QPushButton("浏览")
        btn_browse_group.setStyleSheet(ui.style.new_style_pushbutton)
        btn_browse_group.clicked.connect(lambda: self.open_folder('xlsx'))
        group_folder_layout.addStretch()
        group_folder_layout.addWidget(btn_select_group)
        group_folder_layout.addWidget(btn_browse_group)
        layout_group.addWidget(group_folder_widget)

        # 浏览器选择（Edge, Chrome, IE）
        # ============ 浏览器选择 ============
        browser_widget = QWidget()
        browser_layout = QHBoxLayout(browser_widget)

        # Edge
        self.Edge_Radio = QRadioButton("Edge")
        self.Edge_Radio.setStyleSheet("font: 14px;")
        self.Edge_Radio.setChecked(True)
        browser_layout.addWidget(self.Edge_Radio)

        # Chrome
        self.Chrome_Radio = QRadioButton("Chrome")
        self.Chrome_Radio.setStyleSheet("font: 14px;")
        browser_layout.addWidget(self.Chrome_Radio)

        # IE（注意用户指定控件名为Ie_Radio）
        self.Ie_Radio = QRadioButton("IE")
        self.Ie_Radio.setStyleSheet("font: 14px;")
        browser_layout.addWidget(self.Ie_Radio)

        layout_group.addWidget(browser_widget)

        # ============ 内容选择 ============
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setSpacing(10)

        # 不可勾选的复选框
        self.checkBox_serial = QCheckBox("序号")
        self.checkBox_serial.setStyleSheet("font: 12px;")
        self.checkBox_serial.setChecked(True)
        self.checkBox_serial.setEnabled(False)
        checkbox_layout.addWidget(self.checkBox_serial)

        self.checkBox_name = QCheckBox("名称")
        self.checkBox_name.setStyleSheet("font: 12px;")
        self.checkBox_name.setChecked(True)
        self.checkBox_name.setEnabled(False)
        checkbox_layout.addWidget(self.checkBox_name)

        self.checkBox_nickname = QCheckBox("群昵称")
        self.checkBox_nickname.setStyleSheet("font: 12px;")
        self.checkBox_nickname.setChecked(True)
        self.checkBox_nickname.setEnabled(False)
        checkbox_layout.addWidget(self.checkBox_nickname)

        # 可勾选的复选框
        self.checkBox_qid = QCheckBox("QQ号")
        self.checkBox_qid.setStyleSheet("font: 12px;")
        self.checkBox_qid.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_qid)

        self.checkBox_sex = QCheckBox("性别")
        self.checkBox_sex.setStyleSheet("font: 12px;")
        self.checkBox_sex.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_sex)

        self.checkBox_qq_year = QCheckBox("QQ年龄")
        self.checkBox_qq_year.setStyleSheet("font: 12px;")
        self.checkBox_qq_year.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_qq_year)

        self.checkBox_join_date = QCheckBox("进群日期")
        self.checkBox_join_date.setStyleSheet("font: 12px;")
        self.checkBox_join_date.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_join_date)

        self.checkBox_send_date = QCheckBox("最后发言日期")
        self.checkBox_send_date.setStyleSheet("font: 12px;")
        self.checkBox_send_date.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_send_date)

        self.checkBox_group_lv = QCheckBox("群等级")
        self.checkBox_group_lv.setStyleSheet("font: 12px;")
        self.checkBox_group_lv.setChecked(True)
        checkbox_layout.addWidget(self.checkBox_group_lv)

        layout_group.addWidget(checkbox_widget)

        # 获取信息按钮
        self.btn_get_group = QPushButton("获取")
        self.btn_get_group.setFixedHeight(35)
        self.btn_get_group.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border: none;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
        """)
        layout_group.addWidget(self.btn_get_group)
        layout_group.addStretch()

        self.tools_stack.addWidget(page_group)

        # --- 按钮与子页面切换的信号 ---
        btn_music.clicked.connect(lambda: self.tools_stack.setCurrentIndex(0))
        btn_format.clicked.connect(lambda: self.tools_stack.setCurrentIndex(1))
        btn_qq.clicked.connect(lambda: self.tools_stack.setCurrentIndex(2))
        btn_group.clicked.connect(lambda: self.tools_stack.setCurrentIndex(3))

        return page

    def create_setting_page(self):
        page = QWidget()
        # 设置页面级样式表（新增代码）
        page.setStyleSheet("""
                * {
                    font-family: "Segoe UI", "等线";
                    font-size: 9pt;
                }

                /* 覆盖特殊控件的字号 */
                QGroupBox {
                    font-size: 14px;
                }
                QPushButton#save_button {
                    font-size: 14px;
                }
            """)

        # 主布局
        main_layout = QVBoxLayout(page)
        main_layout.setAlignment(Qt.AlignTop)

        # ===== 基础设置组 =====
        basic_group = QGroupBox("基本设置")
        basic_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px 'Microsoft YaHei';
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 3px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)

        # 自动登录
        self.auto_login_check = QCheckBox("启用自动登录")
        self.auto_login_check.setStyleSheet("QCheckBox { padding: 8px 0; }")

        # 点击提示音
        self.sound_check = QCheckBox("启用点击提示音")
        self.sound_check.setStyleSheet("QCheckBox { padding: 8px 0; }")

        # ===== 关闭操作组 =====
        self.close_group = QGroupBox("关闭时操作")
        close_layout = QVBoxLayout()

        # 主复选框
        self.close_check = QCheckBox("启用关闭提示")
        self.close_check.setChecked(True)
        self.close_check.stateChanged.connect(lambda: [
            btn.setEnabled(not self.close_check.isChecked())
            for btn in [self.close_radio, self.tray_radio]
        ])

        # 子选项
        self.close_radio = QRadioButton("直接关闭软件")
        self.tray_radio = QRadioButton("最小化到系统托盘")
        self.close_radio.setEnabled(False)
        self.tray_radio.setEnabled(False)

        close_layout.addWidget(self.close_check)
        close_layout.addWidget(self.close_radio)
        close_layout.addWidget(self.tray_radio)
        self.close_group.setLayout(close_layout)

        # ===== 系统设置组 =====
        system_group = QGroupBox("系统设置")

        # 开机自启
        self.boot_check = QCheckBox("开机自动启动")

        # 悬浮窗
        self.float_check = QCheckBox("启用悬浮窗功能")

        # ===== 背景设置组 =====
        bg_group = QGroupBox("背景设置")
        bg_layout = QVBoxLayout()

        # 背景类型
        self.bg_default = QRadioButton("默认背景")
        self.bg_custom = QRadioButton("自定义背景")
        self.bg_dynamic = QRadioButton("动态背景")
        self.bg_default.setChecked(True)

        # 自定义背景设置
        self.bg_custom_path = ui.style.DraggableLineEdit()
        self.bg_custom_path.setPlaceholderText("请将图片文件拖拽至此处")
        self.bg_custom_path.setVisible(False)
        self.bg_custom_path.setStyleSheet(ui.style.new_style_lineEdit)



        # 自定义透明度滑块
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(40, 90)
        self.opacity_slider.setValue(80)
        self.opacity_slider.setTickInterval(10)
        self.opacity_slider.setStyleSheet("""
            QSlider::handle:horizontal {
                background: #2196F3;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        self.opacity_slider.setVisible(False)

        # 动态背景设置
        dynamic_layout = QHBoxLayout()
        self.bg_dynamic_path = ui.style.DraggableLineEdit()
        self.bg_dynamic_path.setPlaceholderText("请将视频文件拖拽至此处")
        self.bg_dynamic_path.setStyleSheet(ui.style.new_style_lineEdit)
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(24)
        dynamic_layout.addWidget(self.bg_dynamic_path)
        dynamic_layout.addWidget(QLabel("FPS:"))
        dynamic_layout.addWidget(self.fps_spin)
        dynamic_widget = QWidget()
        dynamic_widget.setLayout(dynamic_layout)
        dynamic_widget.setVisible(False)

        # 背景选项切换逻辑（修复默认背景显示问题）
        def update_bg_controls():
            is_custom = self.bg_custom.isChecked()
            is_dynamic = self.bg_dynamic.isChecked()

            self.bg_custom_path.setVisible(is_custom)
            self.opacity_slider.setVisible(is_custom)
            dynamic_widget.setVisible(is_dynamic)

        self.bg_default.toggled.connect(update_bg_controls)
        self.bg_custom.toggled.connect(update_bg_controls)
        self.bg_dynamic.toggled.connect(update_bg_controls)

        bg_layout.addWidget(self.bg_default)
        bg_layout.addWidget(self.bg_custom)
        bg_layout.addWidget(self.bg_custom_path)
        bg_layout.addWidget(self.opacity_slider)
        dynamic_radio_layout = QHBoxLayout()
        dynamic_radio_layout.setSpacing(5)  # 设置按钮与文字间距

        # 添加单选按钮和图标按钮
        dynamic_radio_layout.addWidget(self.bg_dynamic)

        # 创建提示按钮（根据你的代码调整父级参数）
        self.trand_problem = QPushButton()  # 移除了父级参数，后续会自动加入布局
        self.trand_problem.setFixedSize(15, 15)
        #self.trand_problem.clicked.connect(self.problem)


        # 将按钮加入布局并添加到主布局
        dynamic_radio_layout.addWidget(self.trand_problem)
        dynamic_radio_layout.addStretch(1)  # 添加伸缩项保持左对齐

        # 替换原来的 addWidget(self.bg_dynamic)
        bg_layout.addLayout(dynamic_radio_layout)
        bg_layout.addWidget(dynamic_widget)
        bg_group.setLayout(bg_layout)

        # ===== 保存按钮 =====
        self.save_setting_btn = QPushButton("保存设置")
        self.save_setting_btn.setFixedSize(100, 36)
        self.save_setting_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                font: 14px 'Microsoft YaHei';
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        # ===== 新增系统状态信息组 =====
        status_group = QGroupBox("状态信息")
        status_group.setFixedHeight(80)
        status_group.setStyleSheet("""
                QGroupBox {
                    font: bold 14px 'Microsoft YaHei';
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                    margin-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px;
                }
            """)


        status_layout = QVBoxLayout()


        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel(f"当前版本: {Version}"))
        self.version_button = QPushButton("检查更新")
        self.version_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        version_layout.addWidget(self.version_button)



        # occupation
        occupation_layout = QHBoxLayout()
        self.storage_label = QLabel("当前应用占用率:")
        occupation_layout.addWidget(self.storage_label)
        self.storage_button = QPushButton("点击获取")
        # 设置按钮的尺寸策略为 "Fixed"，禁止水平扩展
        self.storage_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.storage_button.clicked.connect(self.get_process_usage)
        occupation_layout.addWidget(self.storage_button)

        # server
        server_layout = QHBoxLayout()
        color = QtGui.QColor(36, 152, 42)  # 使用RGB值设置颜色为绿色

        self.status_label = QLabel(f"与服务器状态: {'已连接'}")
        self.status_label.setStyleSheet(f"color: {color.name()};")  # 设置字体颜色
        server_layout.addWidget(self.status_label)

        self.update_status_button = QPushButton("更新")
        self.update_status_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        server_layout.addWidget(self.update_status_button)

        status_layout.addLayout(version_layout)
        status_layout.addLayout(occupation_layout)
        status_layout.addLayout(server_layout)


        # 数值右对齐
        for btn in [self.version_button, self.storage_button,self.update_status_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #666;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 10%);
                }
                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 20%);
                }
            """)

        status_group.setLayout(status_layout)

        # ===== 组装布局 =====
        basic_group_layout = QVBoxLayout()
        basic_group_layout.addWidget(self.auto_login_check)
        basic_group_layout.addWidget(self.sound_check)
        basic_group_layout.addWidget(self.close_group)
        basic_group.setLayout(basic_group_layout)

        system_group_layout = QVBoxLayout()
        system_group_layout.addWidget(self.boot_check)
        system_group_layout.addWidget(self.float_check)
        system_group.setLayout(system_group_layout)



        main_layout.addWidget(basic_group)
        main_layout.addWidget(system_group)
        main_layout.addWidget(bg_group)
        main_layout.addWidget(status_group)  # 新增状态信息组
        main_layout.addWidget(self.save_setting_btn, 0, Qt.AlignRight)

        return page

    def upwindow(self):  # 置顶窗口
        if self.is_topmost == False:  # 置顶
            self.windowHandle().setFlags(
                self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            self.is_topmost = True
            self.title_bar.Button_SetTop.setIcon(QIcon("./image/Component/Top2.png"))
        else:  #取消置顶
            self.windowHandle().setFlags(
                self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.is_topmost = False
            self.title_bar.Button_SetTop.setIcon(QIcon("./image/Component/Top.png"))

    def delete_file(self):
        if (self.uim.button_file.text() not in ('选择配置文件', '暂无配置文件 需要创建')):
            result = QMessageBox.question(self, '确认', "你确定要删除配置文件吗？", QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                os.remove('./scripts/' + self.uim.button_file.text())
                #self.uim.populateMenu('scripts')
                # 列出文件夹中的所有文件和文件夹
                files_in_folder = os.listdir("scripts")
                # 检查文件夹中是否有文件
                if len(files_in_folder) == 0:
                    txt = "暂无配置文件 需要创建"
                else:
                    txt = '选择配置文件'
                #self.uim.button_file.setText(txt)

    def LogRecord(self):  # 打开日志
        subprocess.Popen(["notepad.exe", "INFOR.log"])


    def empyt_log(self):  # 清空日志
        log_file_path = "INFOR.log"
        with open(log_file_path, "w") as log_file:
            pass  # 使用 pass 语句表示什么都不做，从而实现清空文件内容
        self.show_message_box("提示", "日志清空成功!")

    def about(self):
        pyautogui.confirm(
            f"版本:{Version}\nGui图形库:Pyqt5\n制作者:浮沉 QQ:3046447554 软件完全免费 纯净无广告\n软件免费 若发现收费购买 请联系我进行反馈\nUI设计本人没有灵感 略微草率还请谅解 如有建议请反馈",
            "Fuchen")

    def open_website(self):
        webbrowser.open("https://fcyang.cn/")

    def open_website_help(self):
        webbrowser.open("https://fcyang.cn/others/help.html")

    def get_process_usage(self):
        process = psutil.Process()

        # 初始化并等待0.1秒，确保首次测量准确
        process.cpu_percent(interval=0.1)

        # 实际测量期间，确保进程正在工作
        cpu_percent = process.cpu_percent(interval=0.1)

        # 获取USS内存（若可用）
        try:
            memory_info = process.memory_full_info()
            memory_mb = memory_info.uss / (1024 ** 2)
        except AttributeError:
            # 回退到RSS如果系统不支持USS
            memory_mb = process.memory_info().rss / (1024 ** 2)

        self.storage_label.setText(f"CPU: {cpu_percent}% Mem: {memory_mb:.2f}MB")
        return cpu_percent, memory_mb

    def show_child_dialog(self):
        # 创建并显示子窗口
        dialog = FileNameDialog(self)
        dialog.setWindowModality(Qt.ApplicationModal)
        result = dialog.exec_()

    def populateMenu(self, folder_path):
        # 清空现有菜单项并填充新的菜单项
        self.file_menu.clear()
        files = [f for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]

        # 如果有文件，则为每个文件创建一个菜单项
        for file in files:
            action = self.file_menu.addAction(file)
            action.triggered.connect(lambda checked, f=file: self.updateButtonText(f))
        import_action = self.file_menu.addAction("请新建或点此导入外部配置")
        import_action.triggered.connect(self.select_file)

    def select_file_path(self, name):
        if name == 'download_music':
            folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
            if folder_path != '':
                folder_path = folder_path.replace("/", "\\")
                self.music_savepath.setText(folder_path)
        elif name == 'qq_send_seq':
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",
                                                       "Text Files (*.txt)",
                                                       options=options)
            file_name = file_name.replace("/", "\\")
            self.QQ_Seq_lineEdit.setText(file_name)
        elif name == 'pic_file_path':
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择输入文件", "", "Images (*.png *.jpg *.jpeg *.gif);;PDF (*.pdf)")
            if file_path:
                self.pic_input_lineEdit.setText(file_path)
                if self.pic_output_lineEdit.text() == '':
                    parent_folder = os.path.dirname(file_path)
                    self.pic_output_lineEdit.setText(parent_folder)

        elif name == 'pic_folder_path':
            folder_path = QFileDialog.getExistingDirectory(
                self, "选择输出文件夹")
            if folder_path:
                self.pic_output_lineEdit.setText(folder_path)
        elif name == 'group_folder_path':
            folder_path = QFileDialog.getExistingDirectory(
                self, "选择输出文件夹")
            if folder_path:
                self.lineEdit_group_path.setText(folder_path)

    def delete_images(self):
        reply = QMessageBox.question(self, '确认删除', "你确定要删除文件夹内容吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            shutil.rmtree('./mod/picture')
            # 重新创建空文件夹
            os.mkdir('./mod/picture')
            QMessageBox.information(self, '提示',"图片清除成功!")

    def open_folder(self, page):  # 浏览QQ头像下载文件夹
        if page == 'picture':
            folder_path = './mod/picture'
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)
        elif page == 'xlsx':
            folder_path = self.lineEdit_group_path.text()
            url = QUrl.fromLocalFile(folder_path)
            QDesktopServices.openUrl(url)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "All Files (*);;Text Files (*.txt)")
        self.file_lineEdit.setText(file_path)
        print(file_path)
        return file_path

    def showMenu(self):
        self.file_menu.exec_(
            self.button_file.mapToGlobal(QtCore.QPoint(0, self.button_file.height())))

    def setup_menu(self):
        """动态构建文件菜单"""
        self.file_menu.clear()
        self.folder_path = './scripts'

        if os.path.exists(self.folder_path):
            # 获取文件列表并排序
            files = sorted(
                [f for f in os.listdir(self.folder_path)
                 if os.path.isfile(os.path.join(self.folder_path, f))],
                key=str.lower
            )

            # 添加文件操作项
            for file in files:
                action = QAction(file, self)
                action.triggered.connect(
                    lambda _, f=file: self.updateButtonText(os.path.join(os.path.abspath(self.folder_path), f)))
                self.file_menu.addAction(action)
            import_action = self.file_menu.addAction("请新建或点此导入外部配置")
            import_action.triggered.connect(self.select_file)

    def show_file_menu(self):
        """显示文件菜单"""
        self.setup_menu()  # 每次点击刷新菜单
        self.file_menu.exec_(
            self.button_file.mapToGlobal(
                self.button_file.rect().bottomLeft() +
                self.button_file.rect().topRight() * 0.5
            )
        )

    def file_selected(self, filename):
        """文件选中处理"""
        print(f"选中的文件: {filename}")
        full_path = os.path.join(self.folder_path, filename)

    def updateButtonText(self, file_name):
        # 更新按钮文本
        self.file_lineEdit.setText(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 设置全局样式
    app.setStyleSheet("""
        QWidget {
            font-family: 'Microsoft YaHei';
        }
        
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())