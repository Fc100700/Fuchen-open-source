import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QColorDialog, QDialog, QRadioButton, QButtonGroup, QLabel, QComboBox
)
from PyQt5.QtGui import QPainter, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPointF, QTranslator


class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_color = QColor("#6ec7ff")
        self.end_color = QColor("#7cb9e8")
        self.gradient_direction = 'horizontal'  # 默认左右渐变
        self.setMinimumSize(200, 150)

    def set_colors(self, start, end):
        self.start_color = QColor(start)
        self.end_color = QColor(end)
        self.update()

    def set_single_color(self, color):
        self.start_color = QColor(color)
        self.end_color = QColor(color)
        self.update()

    def set_direction(self, direction):
        self.gradient_direction = direction
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.gradient_direction == 'horizontal':
            gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), 0))
        else:  # vertical
            gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.height()))
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
        self.selected_colors = {}
        self.initUI()


    def initUI(self):
        self.setWindowTitle('主界面自定义颜色')
        self.setGeometry(300, 300, 960, 600)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # === 左侧面板 ===
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        self.left_gradient_widget = GradientWidget()
        left_layout.addWidget(self.left_gradient_widget, stretch=3)

        # 渐变方向选择
        self.left_direction_combo = QComboBox()
        self.left_direction_combo.addItems(['左右渐变', '上下渐变'])
        left_layout.addWidget(QLabel("渐变方向"))
        left_layout.addWidget(self.left_direction_combo)

        self.left_radio_gradient = QRadioButton("渐变")
        self.left_radio_solid = QRadioButton("纯色")
        self.left_radio_gradient.setChecked(True)
        left_radio_layout = QHBoxLayout()
        left_radio_layout.addWidget(self.left_radio_gradient)
        left_radio_layout.addWidget(self.left_radio_solid)
        left_layout.addLayout(left_radio_layout)

        self.left_btn_start = QPushButton("起始颜色")
        self.left_btn_end = QPushButton("结束颜色")
        self.left_btn_solid = QPushButton("选择纯色")
        self.left_btn_start.setStyleSheet("background-color: #6ec7ff")
        self.left_btn_end.setStyleSheet("background-color: #7cb9e8")
        self.left_btn_solid.setStyleSheet("background-color: #6ec7ff")

        left_color_btn_layout = QHBoxLayout()
        left_color_btn_layout.addWidget(self.left_btn_start)
        left_color_btn_layout.addWidget(self.left_btn_end)
        left_layout.addLayout(left_color_btn_layout)
        left_layout.addWidget(self.left_btn_solid)
        self.left_btn_solid.hide()

        left_panel.setLayout(left_layout)
        main_layout.addWidget(left_panel, stretch=1)

        # === 右侧面板 ===
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        self.right_gradient_widget = GradientWidget()
        self.right_gradient_widget.set_colors("#FFFFFF", "#DDDDDD")
        right_layout.addWidget(self.right_gradient_widget, stretch=3)

        self.right_direction_combo = QComboBox()
        self.right_direction_combo.addItems(['左右渐变', '上下渐变'])
        right_layout.addWidget(QLabel("渐变方向"))
        right_layout.addWidget(self.right_direction_combo)

        self.right_radio_gradient = QRadioButton("渐变")
        self.right_radio_gradient.setChecked(False)
        self.right_radio_solid = QRadioButton("纯色")
        #self.right_radio_solid.setChecked(True)
        right_radio_layout = QHBoxLayout()
        right_radio_layout.addWidget(self.right_radio_gradient)
        right_radio_layout.addWidget(self.right_radio_solid)
        right_layout.addLayout(right_radio_layout)

        self.right_btn_start = QPushButton("起始颜色")
        self.right_btn_end = QPushButton("结束颜色")
        self.right_btn_solid = QPushButton("选择纯色")
        self.right_btn_start.setStyleSheet("background-color: #FFFFFF")
        self.right_btn_end.setStyleSheet("background-color: #DDDDDD")
        self.right_btn_solid.setStyleSheet("background-color: #FFFFFF")

        right_color_btn_layout = QHBoxLayout()
        right_color_btn_layout.addWidget(self.right_btn_start)
        right_color_btn_layout.addWidget(self.right_btn_end)
        right_layout.addLayout(right_color_btn_layout)
        right_layout.addWidget(self.right_btn_solid)

        self.right_btn_start.hide()
        self.right_btn_end.hide()

        # 确保在按钮创建后才调用更新模式
        self.right_radio_solid.setChecked(True)
        self.update_right_mode()  # 正确位置：在按钮初始化之后

        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, stretch=3)

        # === 确认按钮 ===
        self.btn_confirm = QPushButton("确认颜色")
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

        container = QVBoxLayout()
        container.addLayout(main_layout, stretch=9)
        container.addWidget(self.btn_confirm, stretch=1)
        self.setLayout(container)

        # === 信号连接 ===
        self.left_btn_start.clicked.connect(self.pick_left_start)
        self.left_btn_end.clicked.connect(self.pick_left_end)
        self.left_btn_solid.clicked.connect(self.pick_left_solid)

        self.right_btn_start.clicked.connect(self.pick_right_start)
        self.right_btn_end.clicked.connect(self.pick_right_end)
        self.right_btn_solid.clicked.connect(self.pick_right_solid)

        self.left_radio_gradient.toggled.connect(self.update_left_mode)
        self.right_radio_gradient.toggled.connect(self.update_right_mode)
        self.left_direction_combo.currentIndexChanged.connect(self.update_left_direction)
        self.right_direction_combo.currentIndexChanged.connect(self.update_right_direction)

        self.btn_confirm.clicked.connect(self.show_color_info)

    # === 模式切换 ===
    def update_left_mode(self):
        is_gradient = self.left_radio_gradient.isChecked()
        self.left_btn_start.setVisible(is_gradient)
        self.left_btn_end.setVisible(is_gradient)
        self.left_btn_solid.setVisible(not is_gradient)
        if not is_gradient:
            color = self.left_btn_solid.palette().button().color()
            self.left_gradient_widget.set_single_color(color)

    def update_right_mode(self):
        is_gradient = self.right_radio_gradient.isChecked()
        self.right_btn_start.setVisible(is_gradient)
        self.right_btn_end.setVisible(is_gradient)
        self.right_btn_solid.setVisible(not is_gradient)
        if not is_gradient:
            color = self.right_btn_solid.palette().button().color()
            self.right_gradient_widget.set_single_color(color)

    def update_left_direction(self):
        direction = 'horizontal' if self.left_direction_combo.currentIndex() == 0 else 'vertical'
        self.left_gradient_widget.set_direction(direction)

    def update_right_direction(self):
        direction = 'horizontal' if self.right_direction_combo.currentIndex() == 0 else 'vertical'
        self.right_gradient_widget.set_direction(direction)

    # === 颜色选择 ===
    def pick_left_start(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.left_gradient_widget.start_color = color
            self.left_btn_start.setStyleSheet(f'background-color: {color.name()}')
            self.left_gradient_widget.update()

    def pick_left_end(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.left_gradient_widget.end_color = color
            self.left_btn_end.setStyleSheet(f'background-color: {color.name()}')
            self.left_gradient_widget.update()

    def pick_left_solid(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.left_gradient_widget.set_single_color(color)
            self.left_btn_solid.setStyleSheet(f'background-color: {color.name()}')

    def pick_right_start(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.right_gradient_widget.start_color = color
            self.right_btn_start.setStyleSheet(f'background-color: {color.name()}')
            self.right_gradient_widget.update()

    def pick_right_end(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.right_gradient_widget.end_color = color
            self.right_btn_end.setStyleSheet(f'background-color: {color.name()}')
            self.right_gradient_widget.update()

    def pick_right_solid(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.right_gradient_widget.set_single_color(color)
            self.right_btn_solid.setStyleSheet(f'background-color: {color.name()}')

    # === 确认 ===
    def show_color_info(self):
        self.selected_colors = {
            "left_mode": "gradient" if self.left_radio_gradient.isChecked() else "solid",
            "right_mode": "gradient" if self.right_radio_gradient.isChecked() else "solid",
            "left_start": self.left_gradient_widget.start_color.name().upper(),
            "left_end": self.left_gradient_widget.end_color.name().upper(),
            "left_direction": self.left_gradient_widget.gradient_direction,
            "right_start": self.right_gradient_widget.start_color.name().upper(),
            "right_end": self.right_gradient_widget.end_color.name().upper(),
            "right_direction": self.right_gradient_widget.gradient_direction,
        }
        self.accept()

    def get_colors(self):
        return self.selected_colors


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('./image/qt_zh_CN.qm')
    app.installTranslator(translator)
    ex = ColorPicker()
    ex.show()
    sys.exit(app.exec_())
