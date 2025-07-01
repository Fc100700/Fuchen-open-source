import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QVBoxLayout, QLabel, QMessageBox, QColorDialog
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal


class CustomColorPicker(QWidget):
    color_selected = pyqtSignal(QColor)     # 确认选择的颜色
    preview_color = pyqtSignal(QColor)      # 实时预览颜色
    move_signal = pyqtSignal(str)           # 方向移动信号

    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义颜色选择器")
        self.setFixedSize(300, 350)
        self.selected_color = None
        self.confirmed = False  # 用于标记是否确认

        self.basic_colors = [
            '#000000', '#800000', '#008000', '#808000', '#00FF00', '#80FF00',
            '#000080', '#800080', '#008080', '#808080', '#00FFFF', '#80FFFF',
            '#0000FF', '#8000FF', '#0080FF', '#8080FF', '#00CCFF', '#80CCFF',
            '#FF0000', '#FF8000', '#FFFF00', '#FF00FF', '#C0C0C0', '#FFFFFF',
            '#FF0080', '#FF80FF', '#FFC0CB', '#FFA07A', '#FFA500', '#F0E68C'
        ]

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        grid_layout = QGridLayout()
        for i, color in enumerate(self.basic_colors):
            btn = QPushButton()
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"background-color: {color}")
            btn.clicked.connect(lambda checked, c=color: self.set_selected_color(c))
            grid_layout.addWidget(btn, i // 6, i % 6)

        main_layout.addLayout(grid_layout)

        center_layout = QGridLayout()
        self.empty_label = QLabel(" ")
        self.empty_label.setFixedSize(100, 50)
        center_layout.addWidget(QPushButton("↑", clicked=lambda: self.move("up")), 0, 1)
        center_layout.addWidget(QPushButton("←", clicked=lambda: self.move("left")), 1, 0)
        center_layout.addWidget(self.empty_label, 1, 1)
        center_layout.addWidget(QPushButton("→", clicked=lambda: self.move("right")), 1, 2)
        center_layout.addWidget(QPushButton("↓", clicked=lambda: self.move("down")), 2, 1)

        main_layout.addLayout(center_layout)

        confirm_button = QPushButton("确认")
        confirm_button.clicked.connect(self.confirm_color)
        main_layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

    def set_selected_color(self, color):
        self.selected_color = QColor(color)
        self.preview_color.emit(self.selected_color)  # 实时预览
        self.empty_label.setStyleSheet(f"background-color: {color}")

    def move(self, direction):
        self.move_signal.emit(direction)

    def confirm_color(self):
        if self.selected_color:
            self.confirmed = True
            self.color_selected.emit(self.selected_color)
        self.close()

    def closeEvent(self, event):
        if not self.confirmed:
            # 如果用户关闭窗口但没确认，发出 None 信号
            self.color_selected.emit(QColor())  # 发送无效 QColor 而不是 None

        event.accept()


class NotificationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.current_color = QColor("black")  # 当前文字颜色
        self.old_color = QColor("black")  # 记录原颜色

        self.now_number = 0
        self.total_number = 1
        self.operation = '暂无操作'

        self.setFixedSize(200, 80)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(50, 50, 50, 200);
                border-radius: 10px;
            }
            QLabel {
                color: black;
                background-color: transparent;
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout()



        self.label = QLabel(f"当前操作: {self.operation}\n次数: {self.now_number}/{self.total_number}次", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        self.move(screen_rect.width() - self.width() - 20, screen_rect.height() - self.height() - 20)



    def update_now_number(self, now):
        self.now_number = now
        self.label.setText(f"当前操作: {self.operation}\n次数: {self.now_number}/{self.total_number}次")

    def update_total_number(self, total):
        self.total_number = total
        self.label.setText(f"当前操作: {self.operation}\n次数: {self.now_number}/{self.total_number}次")

    def update_operation(self, opera):
        self.operation = opera
        self.label.setText(f"当前操作: {self.operation}\n次数: {self.now_number}/{self.total_number}次")

    def update_color(self):
        # 记录当前颜色
        self.old_color = self.current_color

        self.color_picker = CustomColorPicker()
        self.color_picker.preview_color.connect(self.apply_preview_color)
        self.color_picker.color_selected.connect(self.handle_confirm_color)
        self.color_picker.move_signal.connect(self.handle_move)

        self.color_picker.setWindowModality(Qt.ApplicationModal)
        self.color_picker.show()

    def apply_preview_color(self, color: QColor):
        if color:
            self.current_color = color
            self.label.setStyleSheet(f"color: {color.name()};")

    def handle_confirm_color(self, color: QColor):
        if color.isValid():
            self.current_color = color
            self.label.setStyleSheet(f"color: {color.name()};")
        else:
            # 用户取消：恢复旧颜色
            self.current_color = self.old_color
            self.label.setStyleSheet(f"color: {self.old_color.name()};")

    def apply_color(self, color: QColor):
        self.label.setStyleSheet(f"color: {color.name()};")

    def handle_move(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy = -50
        elif direction == "down":
            dy = 50
        elif direction == "left":
            dx = -50
        elif direction == "right":
            dx = 50

        current_pos = self.pos()
        self.move(current_pos.x() + dx, current_pos.y() + dy)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotificationWindow()
    window.show()

    # 测试按钮：打开颜色选择器
    test_button = QPushButton("测试选择颜色")
    test_button.clicked.connect(window.update_color)
    test_button.show()

    sys.exit(app.exec_())
