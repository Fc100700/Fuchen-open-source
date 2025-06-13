import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QIcon
import ui.style


class HotkeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hotkey = ""
        self.last_hotkey = ""
        self.modifier_keys = []


        self.normal_keys = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("设置热键")
        self.setMinimumSize(200, 100)
        self.setWindowIcon(QIcon('./image/same/提示.png'))

        layout = QVBoxLayout()
        self.label = QLabel("请输入按键")
        self.label.setFont(ui.style.style_font_11)
        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.setFont(ui.style.style_font_10)

        layout.addWidget(self.label)
        layout.addWidget(self.confirm_btn)
        self.setLayout(layout)

        self.confirm_btn.clicked.connect(self.accept)
        self.label.setFocus()

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        key = event.key()
        # 判断是否为小键盘按键：检查 KeypadModifier
        is_keypad = bool(event.modifiers() & Qt.KeypadModifier)

        # 如果是修饰键，记录键码
        if key in (Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta):
            if key not in self.modifier_keys:
                self.modifier_keys.append(key)
        else:
            # 避免重复记录（同一个键可能已经在列表中）
            if not any(k == key and kp == is_keypad for k, kp in self.normal_keys):
                self.normal_keys.append((key, is_keypad))
        # 保存最新组合（注意：此时组合还没清空）
        self.last_hotkey = self.get_current_hotkey()
        self.update_display()
        event.accept()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        key = event.key()
        # 释放修饰键时直接移除（注意：修饰键一般不会区分小键盘）
        if key in (Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta):
            if key in self.modifier_keys:
                self.modifier_keys.remove(key)
        else:
            # 移除普通键时，根据键码匹配（忽略 is_keypad 标记，因为释放时 modifiers 可能已改变）
            for item in self.normal_keys[:]:
                if item[0] == key:
                    self.normal_keys.remove(item)
                    break

        # 不管是否所有按键都已释放，保持 last_hotkey 为上次记录的组合
        self.update_display()
        event.accept()

    def get_current_hotkey(self):
        mods = [self.get_modifier_name(key) for key in self.modifier_keys]
        # 对普通键，根据是否来自小键盘调用不同的显示映射
        normals = [self.get_key_name(key, is_keypad) for key, is_keypad in self.normal_keys]
        # 如果当前有按键，则返回组合，否则返回上次记录的组合（可能为空）
        return " + ".join(mods + normals) if (mods or normals) else self.last_hotkey

    def get_modifier_name(self, key):
        return {
            Qt.Key_Control: "Ctrl",
            Qt.Key_Alt: "Alt",
            Qt.Key_Shift: "Shift",
            Qt.Key_Meta: "Meta"
        }.get(key, "")

    def get_key_name(self, key, is_keypad=False):
        if is_keypad:
            keypad_map = {
                # 小键盘运算符及数字
                Qt.Key_Slash: "num/",
                Qt.Key_Asterisk: "num*",
                Qt.Key_Minus: "num-",
                Qt.Key_Plus: "num+",
                Qt.Key_Enter: "numEnter",
                # 有时小键盘回车可能也返回 Qt.Key_Return
                Qt.Key_Return: "numEnter",
                Qt.Key_0: "num0",
                Qt.Key_1: "num1",
                Qt.Key_2: "num2",
                Qt.Key_3: "num3",
                Qt.Key_4: "num4",
                Qt.Key_5: "num5",
                Qt.Key_6: "num6",
                Qt.Key_7: "num7",
                Qt.Key_8: "num8",
                Qt.Key_9: "num9",
                Qt.Key_Period: "num."
            }
            if key in keypad_map:
                return keypad_map[key]
        # 对主键盘及其它按键
        special_keys = {
            Qt.Key_Up: "Up",
            Qt.Key_Down: "Down",
            Qt.Key_Left: "Left",
            Qt.Key_Right: "Right",
            # 将主键盘回车 (Qt.Key_Return) 记录为 "Enter"
            Qt.Key_Return: "Enter",
            # 如果意外收到 Qt.Key_Enter（通常为小键盘），这里也可以设置默认
            Qt.Key_Enter: "Enter",
            Qt.Key_Escape: "Esc",
            Qt.Key_Space: "Space",
            # 显式添加 PrtSc、ScrLk、Pause 键
            Qt.Key_Print: "PrtSc",
            Qt.Key_ScrollLock: "ScrLk",
            Qt.Key_Pause: "Pause",
        }
        if key in special_keys:
            return special_keys[key]
        # 其他情况使用 QKeySequence 转换（可能会有些平台差异）
        return QKeySequence(key).toString()

    def update_display(self):
        current_hotkey = self.get_current_hotkey()
        if current_hotkey:
            self.label.setText(current_hotkey)
            self.hotkey = current_hotkey
        else:
            display = self.last_hotkey if self.last_hotkey else "请输入按键"
            self.label.setText(display)
            self.hotkey = self.last_hotkey

    @staticmethod
    def get_hotkey(parent=None):
        dialog = HotkeyDialog(parent)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.hotkey
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hotkey = HotkeyDialog.get_hotkey()
    print("设置的热键:", hotkey)
    sys.exit()  # 直接退出程序，不再启动事件循环
