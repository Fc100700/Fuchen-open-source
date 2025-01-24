from PyQt5.QtCore import QRect, QPropertyAnimation, QEasingCurve, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
import json
import time
import pyautogui
import keyboard as keys
import win32gui


class record_position(QtWidgets.QDialog):
    def __init__(self, main):
        super().__init__()
        global windows
        windows = main
        window_position = windows.pos()
        x = window_position.x() + 500 - 275
        y = window_position.y() + 300 - 100
        self.setGeometry(x, y, 350, 200)
        self.setFixedSize(350, 200)
        self.setWindowIcon(QIcon('./image/same/提示.png'))
        self.page = 0
        self.setWindowTitle("记录位置")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)

        self.prompt_label = QtWidgets.QLabel(self)
        self.prompt_label.setGeometry(QtCore.QRect(15, 0, 400, 140))
        self.prompt_label.setFont(font)
        self.prompt_label.setObjectName("prompt_label")
        self.prompt_label.setText(
            "即将开始进行控件位置初始化设定\n是否立即开始？\n\n点击确定继续 点击取消关闭")

        self.continue_button = QtWidgets.QPushButton(self)
        self.continue_button.setGeometry(QtCore.QRect(60, 150, 100, 30))
        self.continue_button.setObjectName("continue_button")
        self.continue_button.setText("确定")
        self.continue_button.clicked.connect(self.next_continue)
        font11 = QtGui.QFont()
        font11.setFamily("等线")
        font11.setPointSize(11)
        self.continue_button.setFont(font11)

        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setGeometry(QtCore.QRect(180, 150, 100, 30))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.setText("取消")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setFont(font11)

        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(14)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(450, 0, 400, 110))
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.label1.setText(f"正在设置第一处位置(聊天框)<br>请将鼠标放置在窗口的<b>聊天框</b>上<br>按下<b>CTRL+P</b>记录位置<br><b>点击按钮</b>或<b>CTRL+L</b>继续下一步")

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setGeometry(QtCore.QRect(450, 110, 400, 40))
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.label2.setText( f"位置 <b>[等待记录]</b>")

        self.next_button = QtWidgets.QPushButton(self)
        self.next_button.setGeometry(QtCore.QRect(460, 150, 90, 30))
        self.next_button.setObjectName("next_button")
        self.next_button.setText("下一步")
        self.next_button.clicked.connect(self.next_normal)
        self.next_button.setEnabled(False)
        self.next_button.setFont(font11)

        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setGeometry(QtCore.QRect(560, 150, 90, 30))
        self.close_button.setObjectName("close_button")
        self.close_button.setText("取消")
        self.close_button.clicked.connect(self.close)
        self.close_button.setFont(font11)

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setGeometry(QtCore.QRect(450, 0, 400, 110))
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.label3.setText(
            f"正在设置第二处位置(发送按钮)<br>请将鼠标放在窗口的<b>发送按钮</b>上<br>按下<b>CTRL+P</b>记录位置<br><b>点击按钮</b>或<b>CTRL+L</b>继续")

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setGeometry(QtCore.QRect(450, 100, 400, 40))
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.label4.setText(
            f"位置 <b>[等待记录]</b>")

        self.complete_button = QtWidgets.QPushButton(self)
        self.complete_button.setGeometry(QtCore.QRect(460, 150, 90, 30))
        self.complete_button.setObjectName("complete_button")
        self.complete_button.setText("完成")
        self.complete_button.clicked.connect(self.complete)
        self.complete_button.setEnabled(False)
        self.complete_button.setFont(font11)

        self.cancel_last = QtWidgets.QPushButton(self)
        self.cancel_last.setGeometry(QtCore.QRect(460, 150, 90, 30))
        self.cancel_last.setObjectName("cancel_last")
        self.cancel_last.setText("取消")
        self.cancel_last.clicked.connect(self.close)
        self.cancel_last.setFont(font11)

        self.position = [20, 20, 80, 180]
        global global_position
        global_position = [[None, None], [None, None]]
        self.before_list = [self.prompt_label, self.continue_button, self.cancel_button]
        self.after_list = [self.label1, self.label2, self.next_button, self.close_button]
        self.last_list = [self.label3, self.label4, self.complete_button, self.cancel_last]

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
        self.keyboard_thread = KeyboardThread()
        self.keyboard_thread.keyPressed.connect(self.handle_key_pressed)
        self.keyboard_thread.start()

    def closeEvent(self, event):
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
        global global_position, position_status, textedit_position, send_position
        with open("config.json", "r") as file:
            pdata = json.load(file)
        pdata["position"] = global_position
        with open("config.json", "w") as file:
            json.dump(pdata, file, indent=4)
        position_status = True
        textedit_position = global_position[0]
        send_position = global_position[1]
        windows.update_position(global_position)
        windows.uim.label_position_status.setText(
            '<font color="black">位置设置：</font> <font color="green">已设置</font>')
        windows.uim.label_position_send.setText(
            f'<font color="black">发送键位置：</font> <font color="green">{send_position}</font>')
        windows.uim.label_position_text.setText(
            f'<font color="black">聊天框位置：</font> <font color="green">{textedit_position}</font>')

        self.close()
        pyautogui.confirm("设置成功！")

    def handle_key_pressed(self, key):
        if key == 'Ctrl+P':
            global global_position
            a = pyautogui.position()
            if self.page == 1:
                global_position[0] = [a.x, a.y]
                self.label2.setText(
                    f"位置 <b>[{a.x},{a.y}]</b>")
                self.next_button.setEnabled(True)
            elif self.page == 2:
                global_position[1] = [a.x, a.y]
                self.label4.setText(
                    f"位置 <b>[{a.x},{a.y}]</b>")
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

    def handle_key_pressed(self, key):
        if not self.is_window_open("记录位置"):
            keys.unhook_all()
        else:
            self.keyPressed.emit(key)

    def is_window_open(self, window_title):
        toplist = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), toplist)

        for hwnd in toplist:
            if win32gui.GetWindowText(hwnd) == window_title:
                return True

        return False