
import json
import re
import struct
import sys
from datetime import date,datetime
from ctypes import cdll
from ctypes.wintypes import HWND
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QInputDialog, QMessageBox, QLineEdit, QStackedLayout, QSizePolicy, QDialog
)
from PyQt5.QtGui import QPixmap, QMouseEvent, QRegion, QPainter, QPainterPath, QBrush, QIcon, QColor, QCursor
from PyQt5.QtCore import Qt, QSize, QEvent, QRectF, QVariantAnimation
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
                             QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
                             QGraphicsPathItem, QGraphicsPixmapItem, QGraphicsItem)
from PyQt5.QtGui import (QPixmap, QPainter, QImage, QPen, QBrush, QPainterPath, QColor)
from PyQt5.QtCore import Qt, QRectF, QPointF



def Check(input_str):  # 检测名称
    # 定义允许的字符集合：中文、大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[\u4e00-\u9fa5a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))


def Check_Password(input_str):
    # 定义允许的字符集合：大小写英文字母、数字、- . ? ~ _
    allowed_characters = re.compile(r'^[a-zA-Z0-9\-.?~_]+$')
    return not bool(allowed_characters.match(input_str))
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


class CustomGraphicsView(QGraphicsView):
    def wheelEvent(self, event):
        # 阻止默认的滚轮事件处理
        event.ignore()


class CustomPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap,canvas_size):
        super().__init__(pixmap)
        self.canvas_size = canvas_size
        self.scaled_width = pixmap.width()
        self.scaled_height = pixmap.height()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def setScale(self, scale):
        super().setScale(scale)
        self.scaled_width = self.pixmap().width() * scale
        self.scaled_height = self.pixmap().height() * scale

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            new_pos = value

            # 限制移动范围在画布边界内（不让图片跑出正方形）
            min_x = self.canvas_size - self.scaled_width
            max_x = 0
            min_y = self.canvas_size - self.scaled_height
            max_y = 0

            clamped_x = max(min(new_pos.x(), max_x), min_x)
            clamped_y = max(min(new_pos.y(), max_y), min_y)

            return QPointF(clamped_x, clamped_y)
        return super().itemChange(change, value)


class FixPicture(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("头像裁切工具")
        self.setFixedSize(400, 400)

        # 场景尺寸参数
        self.canvas_size = 256
        self.circle_diameter = int(self.canvas_size * 0.9)
        self.margin = (self.canvas_size - self.circle_diameter) // 2
        self.result_value = None

        # 创建场景和视图
        self.scene = QGraphicsScene(0, 0, self.canvas_size, self.canvas_size)
        self.view = CustomGraphicsView(self.scene)  # 使用自定义视图
        self.view.setFixedSize(self.canvas_size, self.canvas_size)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 添加环形遮罩层（关键优化）
        self.create_mask_layer()

        # 添加圆形参考线
        self.circle = QGraphicsPathItem()
        circle_path = QPainterPath()
        circle_path.addEllipse(self.margin, self.margin,
                               self.circle_diameter, self.circle_diameter)
        self.circle.setPath(circle_path)
        self.circle.setPen(QPen(Qt.white, 2))
        self.circle.setBrush(QBrush(Qt.NoBrush))
        self.circle.setZValue(2)  # 最顶层
        self.scene.addItem(self.circle)

        # 创建按钮
        open_btn = QPushButton("选择图片")
        save_btn = QPushButton("保存头像")

        # 布局设置
        central_widget = QWidget()
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(save_btn)
        layout.addWidget(self.view)
        layout.addLayout(btn_layout)
        central_widget.setLayout(layout)
        self.setLayout(layout)  # 直接将布局设置给QDialog

        # 初始化变量
        self.image_item = None
        self.scene.setBackgroundBrush(Qt.gray)  # 底层背景

        # 连接信号
        open_btn.clicked.connect(self.open_image)
        save_btn.clicked.connect(self.save_image)

    def create_mask_layer(self):
        """创建环形遮罩层"""
        mask = QGraphicsPathItem()
        path = QPainterPath()

        # 添加整个画布矩形
        path.addRect(0, 0, self.canvas_size, self.canvas_size)

        # 减去中心圆形区域
        circle_path = QPainterPath()
        circle_path.addEllipse(self.margin, self.margin,
                               self.circle_diameter, self.circle_diameter)
        path = path.subtracted(circle_path)

        mask.setPath(path)
        mask.setBrush(QBrush(QColor(128, 128, 128, 100)))  # 半透明灰色
        mask.setZValue(1)  # 介于背景和图片之间
        self.scene.addItem(mask)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)")
        if not path:
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            return

        if self.image_item:
            self.scene.removeItem(self.image_item)

        # 使用自定义图形项
        self.image_item = CustomPixmapItem(
            pixmap,
            self.canvas_size
        )

        self.scene.addItem(self.image_item)
        self.image_item.setZValue(0)
        self.center_and_scale_image(pixmap)

    def center_and_scale_image(self, pixmap):
        img_width = pixmap.width()
        img_height = pixmap.height()

        # 计算覆盖整个画布的缩放比例
        target_size = self.canvas_size
        scale = max(target_size / img_width, target_size / img_height)
        self.image_item.setScale(scale)

        # 计算初始居中位置
        scaled_width = img_width * scale
        scaled_height = img_height * scale
        x = (self.canvas_size - scaled_width) / 2
        y = (self.canvas_size - scaled_height) / 2
        self.image_item.setPos(x, y)

    def save_image(self):
        if not self.image_item:
            return

        # 创建输出图像（完整正方形）
        image = QImage(self.canvas_size, self.canvas_size, QImage.Format_RGB32)
        image.fill(Qt.transparent)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 隐藏遮罩和参考线
        for item in self.scene.items():
            if isinstance(item, QGraphicsPathItem):
                item.hide()

        # 渲染场景内容
        self.scene.render(painter,
                          QRectF(0, 0, self.canvas_size, self.canvas_size),
                          QRectF(0, 0, self.canvas_size, self.canvas_size))

        # 恢复显示
        for item in self.scene.items():
            if isinstance(item, QGraphicsPathItem):
                item.show()

        painter.end()

        # 默认保存路径（当前目录下 avatar.png）
        default_path = "./temp/avatar.png"
        image.save(default_path, "JPEG")
        self.result_value = '修改成功'
        self.accept()

        # # 可选：弹出文件保存对话框
        # path, _ = QFileDialog.getSaveFileName(
        #     self, "保存头像", "", "PNG图片 (*.png)")
        # if path:
        #     image.save(path, "PNG")

    def wheelEvent(self, event):
        if self.image_item and (event.modifiers() & Qt.ControlModifier):
            delta = event.angleDelta().y()
            scale_factor = 1.001 **delta
            self.image_item.setScale(self.image_item.scale() * scale_factor)
            event.accept()
        else:
            # 阻止默认的滚轮事件传播
            event.ignore()

def get_rounded_pixmap(pixmap: QPixmap, size: int, border_width: int = 2) -> QPixmap:
    total_size = size + 2 * border_width
    rounded = QPixmap(total_size, total_size)
    rounded.fill(Qt.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)

    # 白色边框
    path = QPainterPath()
    path.addEllipse(0, 0, total_size, total_size)
    painter.setBrush(QBrush(Qt.white))
    painter.setPen(Qt.NoPen)
    painter.drawPath(path)

    clip_path = QPainterPath()
    clip_path.addEllipse(border_width, border_width, size, size)
    painter.setClipPath(clip_path)
    painter.drawPixmap(
        border_width, border_width,
        pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    )

    painter.end()
    return rounded


class InfoPopup(QWidget):
    def __init__(self, lis):
        super().__init__()
        global windows, Account, Name, avatar_date, exp, s, Lv, avatar_load_status, Max_exp
        windows = lis[0]
        Account = lis[1]
        Name = lis[2]
        avatar_date = lis[3]
        exp = lis[4]
        s = lis[5]
        avatar_load_status = lis[6]
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        #self.setFixedSize(240, 340)  # 稍微增大窗口尺寸
        window_position = windows.pos()
        x = window_position.x() + 245
        y = window_position.y() + 45
        icon = QIcon("./image/Component/提示.png")
        self.setWindowIcon(icon)
        self.setGeometry(x, y, 240, 340)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("Fuchen个人信息")

        try:
            hWnd = HWND(int(self.winId()))
            cdll.LoadLibrary('./mod/dll/aeroDll.dll').setBlur(hWnd)
        except Exception as e:
            print("导入失败:", e)

        self.old_pos = self.pos()

        self.border_color = QColor("#FFFFFF")
        self.border_anim = QVariantAnimation(
            self,
            startValue=QColor("#FFFFFF"),
            endValue=QColor("#5B9BD5"),
            duration=400
        )
        self.border_anim.valueChanged.connect(self.update_avatar_border)

        self.username = Name
        self.user_id = Account
        self.exp = exp
        self.calculate_level_info()
        
        self.border_width = 8

        self.init_ui()
    def init_ui(self):
        # 头像按钮
        self.avatar_btn = QPushButton()
        self.avatar_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.avatar_btn.setFixedSize(100, 100)
        self.avatar_btn.setStyleSheet("""
            QPushButton {
                border: 3px solid #FFFFFF;
                border-radius: 50px;
                background-color: #F0F0F0;
            }
            QPushButton:hover {
                border: 3px solid #5B9BD5;
                background-color: #EDF4FA;
            }
        """)
        self.avatar_btn.setIconSize(QSize(90, 90))
        if avatar_load_status == True:
            fp = f"./temp/avatar.png"
        else:
            fp = "./image/float/fc.png"
        self.avatar_btn.setIcon(QIcon(get_rounded_pixmap(QPixmap(fp), 90)))
        self.avatar_btn.installEventFilter(self)

        self.avatar_btn.clicked.connect(self.upload_avatar)

        self.id_label = QLabel(f"ID: {self.user_id}")
        self.id_label.setAlignment(Qt.AlignCenter)
        self.id_label.setStyleSheet("""
            font-size: 14px; 
            color: #666;
            font-family: 'Microsoft YaHei';
        """)

        # 关闭按钮
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(34, 34)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                font-size: 18px;
                color: #999999;
                font-family: 'Arial';
            }
            QPushButton:hover {
                color: #FF3333;
            }
        """)
        close_btn.clicked.connect(self.close)

        # 顶部栏布局
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(close_btn)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar)
        main_layout.addSpacing(0)

        # 头像区域
        avatar_layout = QVBoxLayout()
        avatar_layout.addWidget(self.avatar_btn, alignment=Qt.AlignCenter)
        avatar_layout.addSpacing(8)

        # 用户名区域
        name_widget = QWidget()
        name_layout = QHBoxLayout(name_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)

        self.name_label = QLabel(f"{self.username}")
        self.name_label.setStyleSheet("""
            font-size: 18px;
            color: #333333;
            font-weight: 500;
            font-family: 'Microsoft YaHei';
        """)

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QIcon("./image/Component/edit.png"))
        self.edit_btn.setIconSize(QSize(16, 16))
        self.edit_btn.setFixedSize(24, 24)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
        """)
        self.edit_btn.clicked.connect(self.change_name)

        name_layout.addStretch()
        name_layout.addWidget(self.name_label)

        name_layout.addWidget(self.edit_btn)
        name_layout.addStretch()
        avatar_layout.addSpacing(15)
        avatar_layout.addWidget(name_widget)
        avatar_layout.addWidget(self.id_label)
        avatar_layout.addSpacing(10)

        main_layout.addLayout(avatar_layout)

        # 经验条布局
        exp_layout = QVBoxLayout()
        exp_layout.setContentsMargins(30, 0, 30, 10)


        # 等级和数值
        level_layout = QHBoxLayout()
        self.level_label = QLabel(self.Lv)
        self.level_label.setStyleSheet(f"""
                    font-size: 14px;
                    color: {self.level_color};
                    font-weight: bold;
                """)

        # 修改经验显示
        self.exp_label = QLabel()
        self.exp_label.setText(f"{self.exp}/{self.Max_exp}")

        self.exp_label.setStyleSheet("""
                font-size: 12px;
                color: #999999;
            """)

        level_layout.addWidget(self.level_label)
        level_layout.addStretch()
        level_layout.addWidget(self.exp_label)

        # 进度条
        self.progress_bar = QWidget()
        self.progress_bar.setFixedHeight(6)  # 高度更小
        self.progress_bar.setStyleSheet("""
            background-color: #EEEEEE;
            border-radius: 3px;
        """)

        # 修改进度条设置
        self.progress = QWidget(self.progress_bar)
        progress_percent = min(self.exp / self.Max_exp, 1.0)
        progress_width = int(180 * progress_percent)
        self.progress.setGeometry(0, 0, progress_width, 6)
        self.progress.setStyleSheet(f"""
                    background-color: {self.level_color};
                    border-radius: 3px;
                """)

        exp_layout.addLayout(level_layout)
        exp_layout.addSpacing(0)
        exp_layout.addWidget(self.progress_bar)

        main_layout.addLayout(exp_layout)

        # 功能按钮
        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(30, 0, 30, 20)
        btn_layout.setSpacing(12)

        self.change_pwd_btn = QPushButton("修改密码")
        self.change_pwd_btn.setFixedHeight(36)
        self.change_pwd_btn.setStyleSheet("""
            QPushButton {
                background-color: #5B9BD5;
                color: white;
                border-radius: 18px;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #407ec9;
            }
        """)

        self.change_pwd_btn.clicked.connect(self.change_password)

        btn_layout.addWidget(self.change_pwd_btn)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def update_avatar_border(self, color: QColor):
        self.border_color = color
        self.avatar_btn.setStyleSheet(f"""
            QPushButton {{
                border: 3px solid {color.name()};
                border-radius: 50px;
                background-color: #F0F0F0;
            }}
        """)

    def calculate_level_info(self):
        if 0 <= self.exp < 20:
            self.Lv = "Lv1"
            self.Max_exp = 20
            self.level_color = "#7ED957"
        elif 20 <= self.exp < 300:
            self.Lv = "Lv2"
            self.Max_exp = 300
            self.level_color = "#4FC3F7"
        elif 300 <= self.exp < 600:
            self.Lv = "Lv3"
            self.Max_exp = 600
            self.level_color = "#FFD700"
        elif 600 <= self.exp < 1000:
            self.Lv = "Lv4"
            self.Max_exp = 1000
            self.level_color = "#FF9800"
        elif self.exp >= 1000:
            self.Lv = "Lv5"
            self.Max_exp = 9999
            self.level_color = "#8E24AA"

    def enterEvent(self, event: QEvent):
        if self.childAt(event.pos()) == self.avatar_btn:
            self.border_anim.setDirection(QVariantAnimation.Forward)
            self.border_anim.start()

    def leaveEvent(self, event: QEvent):
        if not self.avatar_btn.underMouse():
            self.border_anim.setDirection(QVariantAnimation.Backward)
            self.border_anim.start()


    def eventFilter(self, source, event):
        if source == self.avatar_btn:
            if event.type() == QEvent.Enter:
                self.border_anim.setDirection(QVariantAnimation.Forward)
                self.border_anim.start()
            elif event.type() == QEvent.Leave:
                self.border_anim.setDirection(QVariantAnimation.Backward)
                self.border_anim.start()
        return super().eventFilter(source, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())

        path = QPainterPath()
        path.addRoundedRect(rect, 12, 12)

        painter.fillPath(path, QBrush(QColor(230, 230, 230, 150)))

    def upload_avatar(self):
        global avatar_date
        try:
            # 解析字符串为日期对象（支持不带前导零的月份和日期）
            date_obj = datetime.strptime(avatar_date, '%Y-%m-%d').date()
            # 获取今天的日期并比较
            if date_obj == date.today():
                QMessageBox.information(self, '提示', "今日已上传过头像 下次更换需要等到明天")
                return
            else:
                window = FixPicture()
                window.exec_()
                if window.result_value == '修改成功':
                    TypedJSONClient('upload_avatar', avatar_date)
                    with open('./temp/avatar.png', "rb") as f:
                        while True:
                            chunk = f.read(2048)
                            if not chunk:
                                break
                            s.sendall(chunk)
                    # 发送结束标记
                    s.sendall(b"EOF")
                    pixmap = QPixmap('./temp/avatar.png').scaled(90, 90, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                    self.avatar_btn.setIcon(QIcon(get_rounded_pixmap(pixmap, 90)))
                    self.avatar_btn.setIconSize(QSize(90, 90))
                    windows.avatar.setIcon(QIcon("./temp/avatar.png"))
                    avatar_date = str(date.today())
                    windows.set_variables({"avatar_date": avatar_date})
                    QMessageBox.information(self, '提示', "头像上传成功!")
        except ValueError:
            # 如果解析失败，说明格式不对
            return False

    def change_name(self):
        new_name, ok = QInputDialog.getText(self, "更改名称", "请输入新名称：", text=self.username)
        if ok and new_name.strip():
            new_name = new_name.strip()
            if len(new_name) < 1 or len(new_name) > 10:
                QMessageBox.warning(self, "错误", "用户名长度应为 1-10 位")
                return
            if Check(new_name):
                QMessageBox.warning(self, "错误", "用户名包含非法字符")
                return
            self.username = new_name
            self.name_label.setText(self.username)
            windows.username.setText(self.username)
            windows.set_variables({"Name": self.username})
            TypedJSONClient('update_profile', {'types': 'name', 'Name': self.username})
            QMessageBox.information(self, "成功", "用户名已更改")

    def change_password(self):
        new_pwd, ok = QInputDialog.getText(self, "更改密码", "请输入新密码：", echo=QLineEdit.Password)
        if ok and new_pwd.strip():
            new_pwd = new_pwd.strip()
            if len(new_pwd) < 8 or len(new_pwd) > 15:
                QMessageBox.warning(self, "错误", "密码长度应为 8-15 位")
                return
            if Check_Password(new_pwd):
                QMessageBox.warning(self, "错误", "密码包含非法字符")
                return
            TypedJSONClient('update_profile', {'types': 'password', 'Password': new_pwd})
            QMessageBox.information(self, "成功", "密码已更改")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.old_pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InfoPopup(['self', '123456', "Name", "2000-1-1", 100, 's',  False])
    window.show()
    sys.exit(app.exec_())