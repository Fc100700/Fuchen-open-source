
import json
import os
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
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setBackgroundBrush(Qt.white)
        self.image_item = None  # 新增图片项引用

    def wheelEvent(self, event):
        if self.image_item is not None:
            delta = event.angleDelta().y()
            if delta == 0:
                return
            factor = 1.1 if delta > 0 else 0.9

            # 当前缩放
            current_scale = self.image_item.scale()
            new_scale = current_scale * factor

            # 计算图像缩放后大小
            pixmap = self.image_item.pixmap()
            scaled_width = pixmap.width() * new_scale
            scaled_height = pixmap.height() * new_scale

            # 计算最小缩放：确保不小于视图尺寸
            min_scale_x = self.viewport().width() / pixmap.width()
            min_scale_y = self.viewport().height() / pixmap.height()
            min_scale = max(min_scale_x, min_scale_y)

            # 限制缩放不能小于最小比例
            if new_scale < min_scale:
                new_scale = min_scale

            # 重新计算缩放因子（因为可能修改了 new_scale）
            factor = new_scale / current_scale

            # 获取鼠标位置并转换坐标
            pos = event.pos()
            scene_pos = self.mapToScene(pos)
            item_pos = self.image_item.mapFromScene(scene_pos)

            # 应用缩放
            self.image_item.setScale(new_scale)

            # 调整位置以保持鼠标点不变
            new_item_pos = item_pos * factor
            new_scene_pos = self.image_item.mapToScene(new_item_pos)
            delta_pos = scene_pos - new_scene_pos

            self.image_item.setPos(self.image_item.pos() + delta_pos)
        else:
            super().wheelEvent(event)


class CustomPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap, canvas_width, canvas_height):
        super().__init__(pixmap)
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
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
            # 计算水平限制
            if self.scaled_width > self.canvas_width:
                min_x = self.canvas_width - self.scaled_width
                max_x = 0
            else:
                min_x = 0
                max_x = self.canvas_width - self.scaled_width
            # 计算垂直限制
            if self.scaled_height > self.canvas_height:
                min_y = self.canvas_height - self.scaled_height
                max_y = 0
            else:
                min_y = 0
                max_y = self.canvas_height - self.scaled_height

            clamped_x = max(min(new_pos.x(), max_x), min_x)
            clamped_y = max(min(new_pos.y(), max_y), min_y)

            return QPointF(clamped_x, clamped_y)
        return super().itemChange(change, value)


class FixPicture(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片裁切工具")
        self.setFixedSize(600, 400)  # 主窗口固定大小
        self.result_value = None

        # 动态视图参数（初始设为16:9）
        self.view_width = 400
        self.view_height = 225
        self.max_view_size = 500  # 视图最大尺寸

        # 创建场景和视图
        self.scene = QGraphicsScene(0, 0, self.view_width, self.view_height)
        self.scene.setBackgroundBrush(QBrush(Qt.white))

        self.view = CustomGraphicsView(self.scene)
        self.view.setFixedSize(self.view_width, self.view_height)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHint(QPainter.Antialiasing, True)  # 在视图初始化时添加

        # 初始化遮罩层和图片项
        self.mask_item = None
        self.image_item = None
        self.button_proxy = None
        self.resizable_button = None

        # 创建默认遮罩
        self.create_mask_layer(0, 0, self.view_width, self.view_height)

        # 控件创建
        open_btn = QPushButton("选择图片")
        save_btn = QPushButton("保存裁切")

        # 布局管理
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # 添加边距
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(save_btn)
        btn_layout.addStretch()

        # 视图容器保证居中
        view_container = QWidget()
        view_layout = QHBoxLayout(view_container)
        view_layout.addStretch()
        view_layout.addWidget(self.view)
        view_layout.addStretch()

        layout.addWidget(view_container)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # 信号连接
        open_btn.clicked.connect(self.open_image)
        save_btn.clicked.connect(self.save_image)

    def create_mask_layer(self, x, y, width, height):
        """创建自适应遮罩层"""
        if self.mask_item:
            self.scene.removeItem(self.mask_item)

        self.mask_item = QGraphicsPathItem()
        path = QPainterPath()
        path.addRect(x, y, width, height)
        self.mask_item.setPath(path)
        self.mask_item.setBrush(QBrush(QColor(128, 128, 128, 50)))
        self.mask_item.setZValue(1)
        self.scene.addItem(self.mask_item)

    def reset_view_size(self, img_ratio):
        """
        根据图片比例重置视图尺寸
        :param img_ratio: 图片宽高比（width/height）
        """
        # 计算最大可用尺寸
        max_width = min(self.max_view_size, self.width() - 40)  # 40是布局边距
        max_height = min(self.max_view_size, self.height() - 120)  # 120是按钮区域

        # 根据比例计算视图尺寸
        if img_ratio > 1:  # 宽图
            self.view_width = max_width
            self.view_height = self.view_width / img_ratio
            if self.view_height > max_height:
                self.view_height = max_height
                self.view_width = self.view_height * img_ratio
        else:  # 高图或方形
            self.view_height = max_height
            self.view_width = self.view_height * img_ratio
            if self.view_width > max_width:
                self.view_width = max_width
                self.view_height = self.view_width / img_ratio

        # 更新视图和场景
        self.view.setFixedSize(int(self.view_width), int(self.view_height))
        self.scene.setSceneRect(0, 0, self.view_width, self.view_height)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)")
        if not path:
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.reset_view_size(16 / 9)
            self.create_mask_layer(0, 0, self.view_width, self.view_height)
            return

        img_width = pixmap.width()
        img_height = pixmap.height()
        img_ratio = img_width / img_height

        self.reset_view_size(img_ratio)

        if self.image_item:
            self.scene.removeItem(self.image_item)
        if self.button_proxy:
            self.scene.removeItem(self.button_proxy)

        self.image_item = CustomPixmapItem(pixmap, self.view_width, self.view_height)
        self.view.image_item = self.image_item  # 新增引用赋值
        self.image_item.setTransformationMode(Qt.SmoothTransformation)
        self.scene.addItem(self.image_item)

        scale = max(
            self.view_width / img_width,
            self.view_height / img_height
        )
        self.image_item.setScale(scale)

        scaled_width = img_width * scale
        scaled_height = img_height * scale

        self.view.setFixedSize(int(scaled_width), int(scaled_height))
        self.scene.setSceneRect(0, 0, scaled_width, scaled_height)
        self.image_item.setPos(0, 0)

        self.create_mask_layer(0, 0, scaled_width, scaled_height)

        # 获取视图的当前尺寸
        view_width = self.view.width()
        view_height = self.view.height()

        # 确定初始裁切框的大小和max_size
        if view_width == view_height:
            initial_size = view_width
            max_size = view_width
        else:
            initial_size = min(view_width, view_height)
            max_size = initial_size

        # 创建可调整按钮并设置初始大小和max_size
        scene_rect = self.scene.sceneRect().toRect()
        self.resizable_button = ResizableButton(max_size=max_size, view_rect=scene_rect)
        self.resizable_button.resize(initial_size, initial_size)

        # 计算居中位置
        pos_x = (view_width - initial_size) // 2
        pos_y = (view_height - initial_size) // 2

        self.button_proxy = self.scene.addWidget(self.resizable_button)
        self.button_proxy.setFlag(QGraphicsItem.ItemIsMovable, True)  # 允许代理项移动
        self.button_proxy.setPos(pos_x, pos_y)
        self.button_proxy.setZValue(2)

    def save_image(self):
        if not self.image_item or not self.resizable_button:
            return

        # 获取按钮在场景中的位置和尺寸
        btn_size = self.resizable_button.width()
        btn_pos = self.button_proxy.pos()

        # 计算裁切区域（基于视图坐标系）
        crop_rect = QRectF(
            btn_pos.x(),
            btn_pos.y(),
            btn_size,
            btn_size
        )

        # 转换到原始图片坐标系
        img_scale = self.image_item.scale()
        original_rect = QRectF(
            (crop_rect.x() - self.image_item.x()) / img_scale,
            (crop_rect.y() - self.image_item.y()) / img_scale,
            crop_rect.width() / img_scale,
            crop_rect.height() / img_scale
        )

        # 执行裁切
        cropped = self.image_item.pixmap().copy(
            int(original_rect.x()),
            int(original_rect.y()),
            int(original_rect.width()),
            int(original_rect.height())
        )
        # 新增：缩放至256x256并保存为JPG
        cropped = cropped.scaled(256, 256, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        output_path = "./temp/avatar.png"
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))  # 确保目录存在[3](@ref)
        if not cropped.save(output_path, "JPEG", quality=80):
            QMessageBox.warning(self, "错误", "保存失败，请检查路径和权限")  # 错误处理[1](@ref)
            return
        self.result_value = '修改成功'
        self.accept()
class ResizableButton(QPushButton):
    def __init__(self, max_size, view_rect, parent=None):
        super().__init__(parent)
        self.max_size = max_size
        self.view_rect = view_rect  # 新增视图边界参数 QRect(0,0,width,height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid rgba(0, 166, 255, 200);
                background-color: rgba(0, 0, 0, 30);
            }
        """)
        self.resize(self.max_size, self.max_size)
        self.edge_margin = 8
        self.drag_mode = None
        self.mouse_press_offset = QPointF()
        self.setMouseTracking(True)

    def get_edge_zone(self, pos):
        """判断鼠标位置所在的区域"""
        rect = self.rect()
        edge = self.edge_margin

        in_left = pos.x() < edge
        in_right = pos.x() > rect.width() - edge
        in_top = pos.y() < edge
        in_bottom = pos.y() > rect.height() - edge

        if in_left or in_right or in_top or in_bottom:
            return "edge"
        return "center"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            zone = self.get_edge_zone(event.pos())
            self.drag_mode = "resize" if zone == "edge" else "move"
            self.mouse_press_offset = event.pos()
            self.original_geometry = self.geometry()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # 更新光标形状
        if self.drag_mode is None:
            zone = self.get_edge_zone(event.pos())
            self.setCursor(Qt.SizeAllCursor if zone == "center" else Qt.SizeFDiagCursor)
        else:
            # 执行拖动操作
            if self.drag_mode == "resize":
                delta = event.pos() - self.mouse_press_offset
                new_size = max(
                    self.original_geometry.width() + delta.x(),
                    self.original_geometry.height() + delta.y(),
                    20
                )
                new_size = min(new_size, self.max_size)
                self.resize(new_size, new_size)
                self.setCursor(Qt.SizeFDiagCursor)
                # 添加缩放时的平滑过渡
                animation = QVariantAnimation()
                animation.setDuration(100)
                animation.setStartValue(self.size())
                animation.setEndValue(QSize(new_size, new_size))
                animation.valueChanged.connect(lambda value: self.resize(value))
                animation.start()
            elif self.drag_mode == "move":
                delta = event.pos() - self.mouse_press_offset
                new_pos = self.mapToParent(event.pos() - self.mouse_press_offset)

                # 限制移动范围
                parent_rect = self.view_rect  # 使用 sceneRect 作为限制范围

                new_x = max(0, min(new_pos.x(), parent_rect.width() - self.width()))
                new_y = max(0, min(new_pos.y(), parent_rect.height() - self.height()))

                self.move(int(new_x), int(new_y))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_mode = None
        super().mouseReleaseEvent(event)
def get_rounded_pixmap(pixmap: QPixmap, size: int) -> QPixmap:
    rounded = QPixmap(size, size)
    rounded.fill(Qt.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, size, size, pixmap)
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