import re
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QColorDialog, QMessageBox,QDialog)
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPointF,QTranslator


class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_colors = {}  # 存储选择结果
        self.start_color = QColor("#6ec7ff")
        self.end_color = QColor("#7cb9e8")
        self.setMinimumSize(200, 150)

    def set_colors(self, start, end):
        self.start_color = QColor(start)
        self.end_color = QColor(end)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), 0))
        gradient.setColorAt(0.0, self.start_color)
        gradient.setColorAt(1.0, self.end_color)
        painter.fillRect(self.rect(), gradient)


class SolidColorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor("#FFFFFF")
        self.setMinimumSize(200, 150)

    def set_color(self, color):
        self.color = QColor(color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.color)


class ColorPicker(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('主界面自定义颜色')
        self.setGeometry(300, 300, 960, 600)  # 16:10比例

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # 左侧区域 (1/4宽度)
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        # 渐变控件 (3/4高度)
        self.gradient_widget = GradientWidget()
        left_layout.addWidget(self.gradient_widget, stretch=3)

        # 颜色选择按钮 (1/4高度)
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton('起始颜色')
        self.btn_end = QPushButton('结束颜色')
        self.btn_start.setStyleSheet(f'background-color: #6ec7ff')
        self.btn_end.setStyleSheet(f'background-color: #7cb9e8')
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_end)
        left_layout.addLayout(btn_layout, stretch=1)

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, stretch=1)

        # 右侧区域 (3/4宽度)
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # 纯色控件 (3/4高度)
        self.solid_widget = SolidColorWidget()
        right_layout.addWidget(self.solid_widget, stretch=3)

        # 颜色选择按钮 (1/4高度)
        self.btn_solid = QPushButton('选择纯色')
        self.btn_solid.setStyleSheet('background-color: #FFFFFF')
        right_layout.addWidget(self.btn_solid, stretch=1)

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, stretch=3)

        # 底部确认按钮
        self.btn_confirm = QPushButton('确认颜色')
        self.btn_confirm.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
        ''')

        # 整体布局
        container = QVBoxLayout()
        container.addLayout(main_layout, stretch=9)
        container.addWidget(self.btn_confirm, stretch=1)
        self.setLayout(container)

        # 信号连接
        self.btn_start.clicked.connect(self.pick_start_color)
        self.btn_end.clicked.connect(self.pick_end_color)
        self.btn_solid.clicked.connect(self.pick_solid_color)
        self.btn_confirm.clicked.connect(self.show_color_info)

    def pick_start_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gradient_widget.start_color = color
            self.btn_start.setStyleSheet(f'background-color: {color.name()}')
            self.gradient_widget.update()

    def pick_end_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gradient_widget.end_color = color
            self.btn_end.setStyleSheet(f'background-color: {color.name()}')
            self.gradient_widget.update()

    def pick_solid_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.solid_widget.set_color(color)
            self.btn_solid.setStyleSheet(f'background-color: {color.name()}')

    # 在show_color_info方法中保存颜色值
    def show_color_info(self):
        # 保存颜色值到字典
        self.selected_colors = {
            "start": self.gradient_widget.start_color.name().upper(),
            "end": self.gradient_widget.end_color.name().upper(),
            "solid": self.solid_widget.color.name().upper()
        }
        self.accept()  # 关闭对话框并返回Accepted状态

    # 添加获取颜色值的方法
    def get_colors(self):
        return self.selected_colors

    def get_color_info(self, color):
        return (
            f"HEX: {color.name().upper()}\n"
            f"RGB: ({color.red()}, {color.green()}, {color.blue()})"
        )



if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('./image/qt_zh_CN.qm')
    app.installTranslator(translator)
    ex = ColorPicker()
    ex.show()
    sys.exit(app.exec_())