#此文件为配置文件编辑窗口
from PyQt5.QtWidgets import QMessageBox, QWidget, QMenu, QAction, QTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QIcon, QFont, QTextCursor, QTextCharFormat
import ui.style
import ast
from pyautogui import confirm



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
        self.setViewportMargins(new_width + 20, 0, 0, 0)

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

ps = [1920,1080]
class FileEdit(QWidget):
    def __init__(self, file, windows):
        super().__init__()
        winx = windows.x()
        winy = windows.y()
        x = winx + 500 - 350
        y = winy + 300 - 200
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
        self.edit_text.verticalScrollBar().setStyleSheet(ui.style.style_verticalScrollBar)
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
        self.reload.setStyleSheet(ui.style.style_white_blue_button)
        self.reload.clicked.connect(self.ReLoad)

        self.mouse_event = QtWidgets.QPushButton(self)
        self.mouse_event.setGeometry(QtCore.QRect(190, 370, 170, 25))
        self.mouse_event.setFont(font)
        self.mouse_event.setObjectName("mouse_event")
        self.mouse_event.setText("添加鼠标事件")
        self.mouse_event.setStyleSheet(ui.style.style_white_blue_button)
        self.mouse_event.setMenu(self.create_mouse_Menu())

        self.key_event = QtWidgets.QPushButton(self)
        self.key_event.setGeometry(QtCore.QRect(370, 370, 170, 25))
        self.key_event.setFont(font)
        self.key_event.setObjectName("key_event")
        self.key_event.setText("添加键盘事件")
        self.key_event.setStyleSheet(ui.style.style_white_blue_button)
        self.key_event.setMenu(self.create_key_Menu())

        self.save_event = QtWidgets.QPushButton(self)
        self.save_event.setGeometry(QtCore.QRect(550, 370, 140, 25))
        self.save_event.setFont(font)
        self.save_event.setObjectName("save_event")
        self.save_event.setText("保存修改")
        self.save_event.setStyleSheet(ui.style.style_white_blue_button)
        self.save_event.clicked.connect(self.save_file)

    def LoadFile(self):
        self.list = []
        input_path = './scripts/' + self.file
        with open(input_path, 'r') as file:
            for line in file:
                try:
                    lines = ast.literal_eval(line)
                except Exception as e:
                    confirm(f"错误! 请检查配置文件内容是否正确\n{e}")
                    break
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

    def addpress(self, key, code, types):
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
            confirm("保存成功！")
        except Exception as e:
            print(e)
            confirm(e)

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
        self.addpress(key, self.key_codes.get(key), 'key')

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

    def closeEvent(self, Event):
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